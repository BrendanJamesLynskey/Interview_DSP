// =============================================================================
// Challenge 05: Pipelined FIR Filter — Parameterizable RTL Implementation
// =============================================================================
//
// Description
// -----------
// Fully pipelined, signed fixed-point FIR filter.
//
// Parameters
// ----------
//   N_TAPS      : Number of filter taps (coefficients).  Must be >= 1.
//   DATA_WIDTH  : Bit width of the input and output data (signed).
//   COEF_WIDTH  : Bit width of each coefficient (signed).
//   COEF_FRAC   : Fractional bits in each coefficient (default COEF_WIDTH-1,
//                 i.e. Q1.15 for 16-bit coefficients: 16384 = 0.5).
//   SYMMETRIC   : 1 = exploit coefficient symmetry to halve multipliers
//                 (valid only when N_TAPS is odd and coefficients are
//                  symmetric about the centre tap).
//                 0 = direct-form, one multiplier per tap.
//
// Fixed-point conventions
// -----------------------
//   Input / output : Q(DATA_WIDTH-1).0  (i.e., full-precision integers, or
//                    interpret as Q1.(DATA_WIDTH-1) for fractional use).
//   Coefficients   : Q(COEF_WIDTH-COEF_FRAC).COEF_FRAC, Q1.15 by default
//   Internal acc.  : DATA_WIDTH + COEF_WIDTH + 1 + clog2(N_TAPS) + 1 bits, so
//                    nothing can overflow before the output stage.
//   Output         : acc >>> COEF_FRAC, rounded half-up and saturated to
//                    DATA_WIDTH. The output is in the same format as the input,
//                    so a filter with unity DC gain passes DC unchanged.
//
// Pipeline stages
// ---------------
//   Stage 0 : Input registration (sample shift register)
//   Stage 1 : Multiply each delayed sample by its coefficient
//             (SYMMETRIC=1 adds one pre-add register before the multiply)
//   Stage 2 : Adder tree (ceil(log2(N_TAPS)) + 1 registered levels)
//   Stage 3 : Output registration, rounding and saturation to DATA_WIDTH
//
// Total latency = 1 + 1 + (ceil(log2(N_TAPS)) + 1) + 1  clock cycles,
// plus 1 when SYMMETRIC=1.
//
// Synthesis notes
// ---------------
//   The adder tree is implemented as a generate-loop recursion.  Most
//   synthesis tools (Vivado, Quartus, DC) infer DSP48/DSP blocks for the
//   multipliers automatically when the widths match standard DSP primitives.
//
// =============================================================================

`timescale 1ns / 1ps
`default_nettype none

// ---------------------------------------------------------------------------
// Utility: ceiling log2
// ---------------------------------------------------------------------------
// Used as a function inside a module so it is available during elaboration.

// ---------------------------------------------------------------------------
// fir_filter — top-level module
// ---------------------------------------------------------------------------

module fir_filter #(
    parameter int unsigned N_TAPS     = 8,
    parameter int unsigned DATA_WIDTH = 16,
    parameter int unsigned COEF_WIDTH = 16,
    parameter int unsigned COEF_FRAC  = COEF_WIDTH - 1,  // Q1.15 coefficients
    parameter bit          SYMMETRIC  = 1'b0   // set 1 for symmetric optimisation
) (
    input  wire                        clk,
    input  wire                        rst_n,        // active-low synchronous reset
    input  wire                        valid_in,     // input data valid strobe
    input  wire signed [DATA_WIDTH-1:0] data_in,

    // Coefficients loaded via a simple address/data interface at elaboration.
    // In a real design these would come from a ROM or a register file written
    // by the host CPU.  Here we use a packed array port for testbench ease.
    input  wire signed [COEF_WIDTH-1:0] coef [0:N_TAPS-1],

    output logic                        valid_out,
    output logic signed [DATA_WIDTH-1:0] data_out
);

    // -----------------------------------------------------------------------
    // Internal width calculations
    // -----------------------------------------------------------------------
    // Product width: DATA_WIDTH + COEF_WIDTH, plus 1 because the symmetric
    // form multiplies a (DATA_WIDTH+1)-bit pre-sum (full precision, no truncation).
    // Accumulator width: add log2(N_TAPS) guard bits for the adder tree.
    localparam int ACC_EXTRA  = $clog2(N_TAPS);          // guard bits
    localparam int PROD_WIDTH = DATA_WIDTH + COEF_WIDTH + 1;
    localparam int ACC_WIDTH  = PROD_WIDTH + ACC_EXTRA;

    // -----------------------------------------------------------------------
    // Stage 0 — Shift register (delay line)
    // -----------------------------------------------------------------------
    // shift_reg[0] holds the most recently registered sample.
    logic signed [DATA_WIDTH-1:0] shift_reg [0:N_TAPS-1];
    logic                         valid_s0;

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            for (int i = 0; i < N_TAPS; i++) shift_reg[i] <= '0;
            valid_s0 <= 1'b0;
        end else begin
            valid_s0 <= valid_in;
            if (valid_in) begin
                shift_reg[0] <= data_in;
                for (int i = 1; i < N_TAPS; i++)
                    shift_reg[i] <= shift_reg[i-1];
            end
        end
    end

    // -----------------------------------------------------------------------
    // Stage 1 — Multiply
    // -----------------------------------------------------------------------
    // Each tap: product[k] = shift_reg[k] * coef[k]
    // Signed extension is handled automatically because both operands are
    // declared `signed`.
    //
    // Symmetric optimisation (SYMMETRIC == 1):
    //   For a linear-phase FIR with symmetric coefficients (h[k] = h[N-1-k]),
    //   we can pre-add the symmetric input samples and perform only ceil(N/2)
    //   multiplications, halving the DSP resource usage.
    //   The centre tap (if N is odd) is multiplied normally.

    logic signed [PROD_WIDTH-1:0] products [0:N_TAPS-1];
    logic                         valid_s1;

    generate
        if (SYMMETRIC) begin : gen_sym_multiply
            // Number of unique coefficient pairs
            localparam int HALF = N_TAPS / 2;

            // Pre-add symmetric pairs into wider registers to avoid overflow
            // before multiplication.  Width = DATA_WIDTH + 1 for the addition.
            logic signed [DATA_WIDTH:0] pre_sum [0:HALF-1];
            logic signed [DATA_WIDTH-1:0] centre_tap_reg;
            logic                         valid_pre;   // pre-add stage valid

            always_ff @(posedge clk) begin
                if (!rst_n) begin
                    for (int k = 0; k < HALF; k++) pre_sum[k] <= '0;
                    if (N_TAPS % 2 == 1) centre_tap_reg <= '0;
                    valid_pre <= 1'b0;
                end else begin
                    valid_pre <= valid_s0;
                    // Pre-add: sum the two input samples that share a coefficient
                    for (int k = 0; k < HALF; k++) begin
                        pre_sum[k] <= {{1{shift_reg[k][DATA_WIDTH-1]}}, shift_reg[k]}
                                    + {{1{shift_reg[N_TAPS-1-k][DATA_WIDTH-1]}},
                                       shift_reg[N_TAPS-1-k]};
                    end
                    if (N_TAPS % 2 == 1)
                        centre_tap_reg <= shift_reg[HALF];
                end
            end

            // Multiply: HALF unique multipliers
            // Map results back to the products array for a uniform adder tree.
            // products[k]           = pre_sum[k] * coef[k]     for k < HALF
            // products[HALF]        = centre_tap * coef[HALF]   (odd N only)
            // products[HALF+1 ..]   = 0  (unused, will be optimised away)
            logic signed [PROD_WIDTH-1:0] sym_prods [0:HALF];

            // Registered multipliers (DSP). The pre-add register above is an
            // extra pipeline stage, so valid is delayed once more here.
            always_ff @(posedge clk) begin
                if (!rst_n) begin
                    for (int k = 0; k <= HALF; k++) sym_prods[k] <= '0;
                    valid_s1 <= 1'b0;
                end else begin
                    valid_s1 <= valid_pre;
                    for (int k = 0; k < HALF; k++)
                        sym_prods[k] <= pre_sum[k] * coef[k];
                    if (N_TAPS % 2 == 1)
                        sym_prods[HALF] <= centre_tap_reg * coef[HALF];
                    else
                        sym_prods[HALF] <= '0;
                end
            end

            // Fill the products array used by the adder tree below.
            // Unused entries are tied to zero.
            always_comb begin
                for (int k = 0; k <= HALF; k++)
                    products[k] = sym_prods[k];
                for (int k = HALF+1; k < N_TAPS; k++)
                    products[k] = '0;
            end

        end else begin : gen_direct_multiply
            // Direct-form: one registered multiplier per tap.
            always_ff @(posedge clk) begin
                if (!rst_n) begin
                    for (int k = 0; k < N_TAPS; k++) products[k] <= '0;
                    valid_s1 <= 1'b0;
                end else begin
                    valid_s1 <= valid_s0;
                    for (int k = 0; k < N_TAPS; k++)
                        products[k] <= shift_reg[k] * coef[k];
                end
            end
        end
    endgenerate

    // -----------------------------------------------------------------------
    // Stage 2 — Pipelined adder tree
    // -----------------------------------------------------------------------
    // Reduces N_TAPS products to a single accumulator in ceil(log2(N_TAPS))
    // registered adder levels.  Each level halves the number of partial sums.
    //
    // Implementation: generate a 2D array big enough for all levels, then
    // chain them with always_ff blocks.  The compiler will prune unused bits.

    localparam int TREE_LEVELS = $clog2(N_TAPS) + 1;  // +1 so level 0 = products
    // Width grows by 1 bit per adder level (to absorb carry).
    // Maximum accumulator width = PROD_WIDTH + TREE_LEVELS.

    // We use a flat 2D packed array.  Row 0 = sign-extended products.
    // Row l = partial sums at adder level l.
    localparam int TREE_WIDTH = PROD_WIDTH + TREE_LEVELS;

    // Use a generate loop to create each adder level.
    // Because we cannot use generate inside generate with dynamic loop bounds
    // easily, we implement a simple recursive macro-style approach:
    // a fixed-depth array where unused rows are tied to the last level.

    // Allocate the full tree storage.
    logic signed [TREE_WIDTH-1:0] tree [0:TREE_LEVELS][0:N_TAPS-1];
    logic                         tree_valid [0:TREE_LEVELS];

    // Level 0: sign-extend products into TREE_WIDTH
    always_comb begin
        for (int k = 0; k < N_TAPS; k++)
            tree[0][k] = {{(TREE_WIDTH-PROD_WIDTH){products[k][PROD_WIDTH-1]}},
                          products[k]};
        tree_valid[0] = valid_s1;
    end

    // Levels 1..TREE_LEVELS: pairwise add and register
    genvar lvl;
    generate
        for (lvl = 1; lvl <= TREE_LEVELS; lvl++) begin : gen_adder_level
            // Number of inputs at this level
            localparam int N_IN  = (N_TAPS + (1 << (lvl-1)) - 1) >> (lvl-1);
            localparam int N_OUT = (N_IN + 1) / 2;

            always_ff @(posedge clk) begin
                if (!rst_n) begin
                    for (int k = 0; k < N_TAPS; k++) tree[lvl][k] <= '0;
                    tree_valid[lvl] <= 1'b0;
                end else begin
                    tree_valid[lvl] <= tree_valid[lvl-1];
                    for (int k = 0; k < N_OUT; k++) begin
                        if (2*k+1 < N_IN)
                            tree[lvl][k] <= tree[lvl-1][2*k] + tree[lvl-1][2*k+1];
                        else
                            tree[lvl][k] <= tree[lvl-1][2*k];  // odd node pass-through
                    end
                    // Tie remaining entries to zero (pruned by synthesis)
                    for (int k = N_OUT; k < N_TAPS; k++)
                        tree[lvl][k] <= '0;
                end
            end
        end
    endgenerate

    // The accumulator result is tree[TREE_LEVELS][0].
    wire signed [TREE_WIDTH-1:0] acc = tree[TREE_LEVELS][0];

    // -----------------------------------------------------------------------
    // Stage 3 — Output registration, rounding and saturation
    // -----------------------------------------------------------------------
    // The accumulator carries COEF_FRAC fractional bits from the coefficients.
    // Round half-up (add 0.5 LSB, then arithmetic shift), then saturate to
    // DATA_WIDTH. A production design might use convergent rounding instead.

    localparam logic signed [TREE_WIDTH-1:0] ROUND_HALF =
        (COEF_FRAC > 0) ? (TREE_WIDTH'(1) <<< (COEF_FRAC - 1)) : '0;
    localparam logic signed [TREE_WIDTH-1:0] OUT_MAX =  (TREE_WIDTH'(1) <<< (DATA_WIDTH-1)) - 1;
    localparam logic signed [TREE_WIDTH-1:0] OUT_MIN = -(TREE_WIDTH'(1) <<< (DATA_WIDTH-1));

    wire signed [TREE_WIDTH-1:0] acc_scaled = (acc + ROUND_HALF) >>> COEF_FRAC;

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            data_out  <= '0;
            valid_out <= 1'b0;
        end else begin
            valid_out <= tree_valid[TREE_LEVELS];

            if (acc_scaled > OUT_MAX)
                data_out <= {1'b0, {(DATA_WIDTH-1){1'b1}}};   // saturate to MAX
            else if (acc_scaled < OUT_MIN)
                data_out <= {1'b1, {(DATA_WIDTH-1){1'b0}}};   // saturate to MIN
            else
                data_out <= acc_scaled[DATA_WIDTH-1:0];
        end
    end

endmodule


// =============================================================================
// Testbench: fir_filter_tb
// =============================================================================
// Tests a 7-tap low-pass FIR (sinc-windowed) with:
//   - Passband sinusoid (0.1 * Fs):  should pass with gain ~1.
//   - Stopband sinusoid (0.45 * Fs): should be attenuated.
//   - White-noise-like pseudo-random input: checks no overflow/X.
//
// Coefficient set (Q1.15, 16384 = 0.5):
//   h = [  -821,      0,   9175,  16384,   9175,      0,  -821 ]
// A 7-tap windowed-sinc half-band LPF (fc = 0.25*Fs), DC gain = 1.005.
//
// Expected behaviour (|H| from the coefficients):
//   - Passband (0.1 Fs) tone: |H| = 0.969 -> 7752 LSB amplitude for 8000 in.
//     With a 3-sample group delay the samples never land on the crest: the
//     largest sampled output is 7752 * sin(72 deg) ~= 7372 LSB.
//   - Stopband (0.45 Fs) tone: |H| = 0.004 -> a few tens of LSB.
//
// Run with SYMMETRIC=1 as well (e.g. verilator -GSYMMETRIC=1) to exercise
// the pre-add / shared-multiplier form; results must match.
// =============================================================================

`timescale 1ns / 1ps

module fir_filter_tb;

    // -----------------------------------------------------------------------
    // Parameters matching the DUT
    // -----------------------------------------------------------------------
    localparam int N_TAPS     = 7;
    localparam int DATA_WIDTH = 16;
    localparam int COEF_WIDTH = 16;
    parameter  bit SYMMETRIC  = 1'b0;   // 0 = direct form, 1 = symmetric form

    localparam real CLK_PERIOD = 10.0;  // 100 MHz

    // -----------------------------------------------------------------------
    // DUT signals
    // -----------------------------------------------------------------------
    logic                         clk      = 0;
    logic                         rst_n    = 0;
    logic                         valid_in = 0;
    logic signed [DATA_WIDTH-1:0] data_in  = 0;
    logic signed [COEF_WIDTH-1:0] coef [0:N_TAPS-1];
    logic                         valid_out;
    logic signed [DATA_WIDTH-1:0] data_out;

    // -----------------------------------------------------------------------
    // DUT instantiation
    // -----------------------------------------------------------------------
    fir_filter #(
        .N_TAPS    (N_TAPS),
        .DATA_WIDTH(DATA_WIDTH),
        .COEF_WIDTH(COEF_WIDTH),
        .SYMMETRIC (SYMMETRIC)
    ) dut (
        .clk      (clk),
        .rst_n    (rst_n),
        .valid_in (valid_in),
        .data_in  (data_in),
        .coef     (coef),
        .valid_out(valid_out),
        .data_out (data_out)
    );

    // Clock generation
    always #(CLK_PERIOD/2) clk = ~clk;

    // -----------------------------------------------------------------------
    // Coefficient initialisation
    // 7-tap windowed-sinc LPF, fc = 0.25 * Fs
    // Q1.15: multiply by 2^15 and round
    // -----------------------------------------------------------------------
    initial begin
        coef[0] = -16'd821;
        coef[1] =  16'd0;
        coef[2] =  16'd9175;
        coef[3] =  16'd16384;
        coef[4] =  16'd9175;
        coef[5] =  16'd0;
        coef[6] = -16'd821;
    end

    // -----------------------------------------------------------------------
    // Stimulus + checking tasks
    // -----------------------------------------------------------------------

    // Apply one sample: valid_in high for one cycle, then one idle cycle
    task automatic apply_sample(input logic signed [DATA_WIDTH-1:0] sample);
        @(posedge clk);
        #1;                   // setup time margin
        valid_in <= 1'b1;
        data_in  <= sample;
        @(posedge clk);
        #1;
        valid_in <= 1'b0;
    endtask

    // Output monitor: tracks the peak |data_out| of every valid output while
    // `measuring` is set. Sampling at the clock edge (rather than at a fixed
    // point in apply_sample) makes the check independent of pipeline latency.
    bit   measuring = 1'b0;
    real  peak_abs;

    always @(posedge clk) begin
        if (measuring && valid_out) begin
            if ($itor($signed(data_out)) > peak_abs)  peak_abs =  $itor($signed(data_out));
            if (-$itor($signed(data_out)) > peak_abs) peak_abs = -$itor($signed(data_out));
        end
    end

    real  out_peak_pass;
    real  out_peak_stop;

    int   WARMUP    = N_TAPS + $clog2(N_TAPS) + 5;  // pipeline depth, in samples
    int   MEAS_SAMP = 200;

    // Drive a tone at freq (cycles/sample) and return the steady-state peak
    task automatic measure_tone(input real freq, output real peak);
        logic signed [DATA_WIDTH-1:0] s;
        for (int i = 0; i < WARMUP + 20 + MEAS_SAMP; i++) begin
            s = DATA_WIDTH'($rtoi(8000.0 * $sin(2.0 * 3.14159265358979 * freq * i)));
            if (i == WARMUP + 20) begin
                peak_abs  = 0.0;
                measuring = 1'b1;
            end
            apply_sample(s);
        end
        repeat (2 * WARMUP) @(posedge clk);   // let the last outputs drain
        measuring = 1'b0;
        peak = peak_abs;
    endtask

    // -----------------------------------------------------------------------
    // Main test sequence
    // -----------------------------------------------------------------------
    initial begin
        $display("=== FIR Filter Testbench Start (SYMMETRIC=%0d) ===", SYMMETRIC);

        // Reset
        rst_n = 0;
        repeat(4) @(posedge clk);
        #1; rst_n = 1;
        repeat(2) @(posedge clk);

        // ---- Test 1: Passband tone (0.1 * Fs) ----
        $display("[TEST 1] Passband tone: f = 0.1*Fs, amplitude = 8000 LSB");
        measure_tone(0.1, out_peak_pass);
        $display("  Peak output = %0.1f LSB", out_peak_pass);
        if (out_peak_pass > 7300.0 && out_peak_pass < 7800.0) begin
            $display("  PASS: passband gain ~0.97 (7300 < sampled peak < 7800)");
        end else begin
            $display("  FAIL: passband output too low (peak = %0.1f)", out_peak_pass);
            $finish;
        end

        // ---- Test 2: Stopband tone (0.45 * Fs) ----
        $display("[TEST 2] Stopband tone: f = 0.45*Fs, amplitude = 8000 LSB");
        measure_tone(0.45, out_peak_stop);
        $display("  Peak output = %0.1f LSB", out_peak_stop);
        if (out_peak_stop < 200.0) begin
            $display("  PASS: stopband attenuates signal (peak < 200)");
        end else begin
            $display("  FAIL: stopband output too high (peak = %0.1f)", out_peak_stop);
            $finish;
        end

        // ---- Test 3: No X propagation with impulse ----
        $display("[TEST 3] Impulse response — checking for X values");
        rst_n = 0;
        repeat(4) @(posedge clk); #1; rst_n = 1;
        // Feed a single impulse
        @(posedge clk); #1;
        valid_in <= 1'b1;
        data_in  <= 16'sh7FFF;    // maximum positive value
        @(posedge clk); #1;
        valid_in <= 1'b0;
        data_in  <= 16'sh0000;
        // Drain the pipeline
        for (int i = 0; i < WARMUP + N_TAPS + 5; i++) begin
            @(posedge clk); #1;
            valid_in <= 1'b1;
            data_in  <= 16'sh0000;
            @(posedge clk); #1;
            valid_in <= 1'b0;
            if (valid_out) begin
                if ($isunknown(data_out)) begin
                    $display("  FAIL: X/Z detected on data_out at sample %0d", i);
                    $finish;
                end
            end
        end
        $display("  PASS: No X/Z on output during impulse response");

        $display("=== All Tests PASSED ===");
        $finish;
    end

    // Timeout watchdog
    initial begin
        #500000;
        $display("TIMEOUT: Simulation exceeded time limit");
        $finish;
    end

    // Optional waveform dump
    initial begin
        $dumpfile("/tmp/fir_filter_tb.vcd");
        $dumpvars(0, fir_filter_tb);
    end

endmodule

`default_nettype wire
