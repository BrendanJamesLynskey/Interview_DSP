// =============================================================================
// Challenge 06: Radix-2 FFT Butterfly Unit — Fixed-Point RTL
// =============================================================================
//
// Description
// -----------
// Implements a single radix-2 Cooley-Tukey DIT (Decimation-In-Time) butterfly:
//
//   Given complex inputs A and B, and twiddle factor W = e^{-j2pi*k/N}:
//
//       P = A + W * B       (butterfly "top" output)
//       Q = A - W * B       (butterfly "bottom" output)
//
// This is the fundamental compute kernel of any power-of-2 FFT.
// Many butterfly units are instantiated and interconnected to form a complete
// FFT datapath.
//
// Fixed-point format
// ------------------
//   Q1.DATA_FRAC format with DATA_WIDTH total bits (1 sign + DATA_FRAC fraction).
//   Default: DATA_WIDTH=16, DATA_FRAC=14  => Q1.14  (range [-2, +2)).
//
//   Twiddle factors use TWIDDLE_WIDTH bits in Q1.(TWIDDLE_WIDTH-2) format.
//   Default: TWIDDLE_WIDTH=16 => Q1.14.
//
// Complex multiply (B * W)
// ------------------------
//   Re(B*W) = Re(B)*Re(W) - Im(B)*Im(W)
//   Im(B*W) = Re(B)*Im(W) + Im(B)*Re(W)
//
//   Each real multiplication produces (DATA_WIDTH + TWIDDLE_WIDTH) bits.
//   We round the product back to DATA_WIDTH before the add/subtract to keep
//   the datapath width bounded.  The rounding mode is round-half-up.
//
// Pipeline stages
// ---------------
//   Stage 0 : Complex multiply (registered)
//   Stage 1 : Add and subtract (registered)
//
//   Total latency = 2 clock cycles.
//   valid_out is registered with the same 2-cycle delay.
//
// Overflow handling
// -----------------
//   The butterfly can overflow if A and B are at full scale simultaneously.
//   A standard technique is to right-shift inputs by 1 bit at each butterfly
//   stage (i.e., scale the FFT by 1/N across all stages).  An alternative is
//   block floating-point.  This module exposes a SCALE_SHIFT parameter to
//   right-shift inputs before processing.
//
// Parameters
// ----------
//   DATA_WIDTH    : Bit width of each real/imaginary component.
//   TWIDDLE_WIDTH : Bit width of twiddle factor real/imaginary components.
//   DATA_FRAC     : Number of fractional bits in data (default DATA_WIDTH-2).
//   SCALE_SHIFT   : Right-shift applied to A and B before the butterfly
//                   (0 = no scaling, 1 = halve, etc.).
//
// =============================================================================

`timescale 1ns / 1ps
`default_nettype none

// ---------------------------------------------------------------------------
// fft_butterfly — radix-2 DIT butterfly unit
// ---------------------------------------------------------------------------

module fft_butterfly #(
    parameter int unsigned DATA_WIDTH    = 16,
    parameter int unsigned TWIDDLE_WIDTH = 16,
    parameter int unsigned DATA_FRAC     = 14,    // fractional bits in data
    parameter int unsigned SCALE_SHIFT   = 1      // 1 = divide by 2 per stage
) (
    input  wire clk,
    input  wire rst_n,       // synchronous active-low reset
    input  wire valid_in,

    // Complex input A
    input  wire signed [DATA_WIDTH-1:0] a_re,
    input  wire signed [DATA_WIDTH-1:0] a_im,

    // Complex input B
    input  wire signed [DATA_WIDTH-1:0] b_re,
    input  wire signed [DATA_WIDTH-1:0] b_im,

    // Twiddle factor W = cos(theta) - j*sin(theta), Q1.(TWIDDLE_WIDTH-2)
    input  wire signed [TWIDDLE_WIDTH-1:0] w_re,
    input  wire signed [TWIDDLE_WIDTH-1:0] w_im,

    // Outputs (same width as inputs, 2-cycle latency)
    output logic                         valid_out,
    output logic signed [DATA_WIDTH-1:0] p_re,   // P = A + W*B
    output logic signed [DATA_WIDTH-1:0] p_im,
    output logic signed [DATA_WIDTH-1:0] q_re,   // Q = A - W*B
    output logic signed [DATA_WIDTH-1:0] q_im
);

    // -----------------------------------------------------------------------
    // Full-precision multiply width
    // -----------------------------------------------------------------------
    localparam int PROD_WIDTH = DATA_WIDTH + TWIDDLE_WIDTH;
    // After rounding back to DATA_WIDTH the adder needs one guard bit.
    localparam int ADD_WIDTH  = DATA_WIDTH + 1;

    // -----------------------------------------------------------------------
    // Stage 0 — Scale inputs and compute W*B (registered complex multiply)
    // -----------------------------------------------------------------------

    // Scale (arithmetic right-shift to prevent butterfly overflow)
    wire signed [DATA_WIDTH-1:0] a_re_s = $signed(a_re) >>> SCALE_SHIFT;
    wire signed [DATA_WIDTH-1:0] a_im_s = $signed(a_im) >>> SCALE_SHIFT;
    wire signed [DATA_WIDTH-1:0] b_re_s = $signed(b_re) >>> SCALE_SHIFT;
    wire signed [DATA_WIDTH-1:0] b_im_s = $signed(b_im) >>> SCALE_SHIFT;

    // Registered scaled A and W*B
    logic signed [DATA_WIDTH-1:0] a_re_r, a_im_r;   // A (scaled, registered)
    logic signed [DATA_WIDTH-1:0] wb_re,  wb_im;    // W*B (rounded, registered)
    logic                         valid_s0;

    // Combinational products (full precision before rounding)
    wire signed [PROD_WIDTH-1:0] prod_rr = b_re_s * w_re;   // Re(B)*Re(W)
    wire signed [PROD_WIDTH-1:0] prod_ii = b_im_s * w_im;   // Im(B)*Im(W)
    wire signed [PROD_WIDTH-1:0] prod_ri = b_re_s * w_im;   // Re(B)*Im(W)
    wire signed [PROD_WIDTH-1:0] prod_ir = b_im_s * w_re;   // Im(B)*Re(W)

    // Full-precision W*B (extra bit to handle the subtraction safely)
    wire signed [PROD_WIDTH:0] wb_re_full = {prod_rr[PROD_WIDTH-1], prod_rr}
                                          - {prod_ii[PROD_WIDTH-1], prod_ii};
    wire signed [PROD_WIDTH:0] wb_im_full = {prod_ri[PROD_WIDTH-1], prod_ri}
                                          + {prod_ir[PROD_WIDTH-1], prod_ir};

    // Round back to DATA_WIDTH.
    // The twiddle factor is in Q1.(TWIDDLE_WIDTH-2), so multiplying two
    // Q1.(DATA_FRAC) x Q1.(TWIDDLE_WIDTH-2) values gives
    // Q2.(DATA_FRAC + TWIDDLE_WIDTH - 2) full precision.
    // We need to drop (TWIDDLE_WIDTH - 2) bits and keep DATA_WIDTH bits,
    // applying round-half-up (add 0.5 LSB before truncation).
    localparam int ROUND_BITS = TWIDDLE_WIDTH - 2;   // bits to discard
    localparam int ROUND_HALF = 1 << (ROUND_BITS - 1);

    wire signed [PROD_WIDTH:0] wb_re_rounded = wb_re_full + ROUND_HALF;
    wire signed [PROD_WIDTH:0] wb_im_rounded = wb_im_full + ROUND_HALF;

    // Extract DATA_WIDTH bits after rounding and saturate
    function automatic logic signed [DATA_WIDTH-1:0] saturate_round;
        input logic signed [PROD_WIDTH:0] x;
        input int                          shift;
        logic signed [DATA_WIDTH:0] shifted;
        begin
            shifted = x >>> shift;
            // Saturate if the upper bits are not all the same sign
            if (shifted > $signed({1'b0, {(DATA_WIDTH-1){1'b1}}}))
                saturate_round = {1'b0, {(DATA_WIDTH-1){1'b1}}};   // +MAX
            else if (shifted < $signed({1'b1, {(DATA_WIDTH-1){1'b0}}}))
                saturate_round = {1'b1, {(DATA_WIDTH-1){1'b0}}};   // -MIN
            else
                saturate_round = shifted[DATA_WIDTH-1:0];
        end
    endfunction

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            a_re_r   <= '0;
            a_im_r   <= '0;
            wb_re    <= '0;
            wb_im    <= '0;
            valid_s0 <= 1'b0;
        end else begin
            valid_s0 <= valid_in;
            a_re_r   <= a_re_s;
            a_im_r   <= a_im_s;
            wb_re    <= saturate_round(wb_re_rounded, ROUND_BITS);
            wb_im    <= saturate_round(wb_im_rounded, ROUND_BITS);
        end
    end

    // -----------------------------------------------------------------------
    // Stage 1 — Add and subtract (registered)
    // -----------------------------------------------------------------------
    // P = A + W*B,  Q = A - W*B
    // Use ADD_WIDTH internally, then truncate/saturate back to DATA_WIDTH.

    wire signed [ADD_WIDTH-1:0] p_re_full = {{1{a_re_r[DATA_WIDTH-1]}}, a_re_r}
                                          + {{1{wb_re[DATA_WIDTH-1]}},   wb_re};
    wire signed [ADD_WIDTH-1:0] p_im_full = {{1{a_im_r[DATA_WIDTH-1]}}, a_im_r}
                                          + {{1{wb_im[DATA_WIDTH-1]}},   wb_im};
    wire signed [ADD_WIDTH-1:0] q_re_full = {{1{a_re_r[DATA_WIDTH-1]}}, a_re_r}
                                          - {{1{wb_re[DATA_WIDTH-1]}},   wb_re};
    wire signed [ADD_WIDTH-1:0] q_im_full = {{1{a_im_r[DATA_WIDTH-1]}}, a_im_r}
                                          - {{1{wb_im[DATA_WIDTH-1]}},   wb_im};

    // Saturate the (DATA_WIDTH+1)-bit adder output to DATA_WIDTH
    function automatic logic signed [DATA_WIDTH-1:0] sat_add;
        input logic signed [ADD_WIDTH-1:0] x;
        begin
            if (x > $signed({{1{1'b0}}, {(DATA_WIDTH-1){1'b1}}}))
                sat_add = {1'b0, {(DATA_WIDTH-1){1'b1}}};
            else if (x < $signed({{1{1'b1}}, {(DATA_WIDTH-1){1'b0}}}))
                sat_add = {1'b1, {(DATA_WIDTH-1){1'b0}}};
            else
                sat_add = x[DATA_WIDTH-1:0];
        end
    endfunction

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            p_re      <= '0;
            p_im      <= '0;
            q_re      <= '0;
            q_im      <= '0;
            valid_out <= 1'b0;
        end else begin
            valid_out <= valid_s0;
            p_re      <= sat_add(p_re_full);
            p_im      <= sat_add(p_im_full);
            q_re      <= sat_add(q_re_full);
            q_im      <= sat_add(q_im_full);
        end
    end

endmodule


// =============================================================================
// Testbench: fft_butterfly_tb
// =============================================================================
//
// Test vectors are chosen so the exact outputs are easy to predict:
//
// Test 1: W = 1 + j0  (twiddle = identity, k=0 for any N)
//   P = A + B,   Q = A - B    (simple add/subtract)
//
// Test 2: W = 0 - j1  (twiddle = -j, quarter-turn)
//   W*B = j*Im(B) - Re(B)*j^2...  more precisely:
//   Re(W*B) = Re(B)*0   - Im(B)*(-1) =  Im(B)
//   Im(W*B) = Re(B)*(-1) + Im(B)*0   = -Re(B)
//   P = A + W*B,  Q = A - W*B
//
// Test 3: W = -1 + j0  (half-turn, k = N/2)
//   W*B = -B
//   P = A - B,  Q = A + B   (roles of P and Q swap relative to Test 1)
//
// All values are scaled to fit in Q1.14 (DATA_WIDTH=16, DATA_FRAC=14).
// SCALE_SHIFT=0 for these tests so we can track exact arithmetic.
//
// =============================================================================

`timescale 1ns / 1ps

module fft_butterfly_tb;

    localparam int DW  = 16;   // DATA_WIDTH
    localparam int TW  = 16;   // TWIDDLE_WIDTH
    localparam int DF  = 14;   // DATA_FRAC
    localparam int SS  = 0;    // SCALE_SHIFT — disabled for exact arithmetic

    // Q1.14 scale factor: 1.0 = 2^14 = 16384
    localparam real SCALE = 16384.0;
    // Tolerance: allow 2 LSB rounding error in each component
    localparam int  TOL   = 2;

    localparam real CLK_PERIOD = 10.0;

    // -----------------------------------------------------------------------
    // DUT signals
    // -----------------------------------------------------------------------
    logic        clk = 0;
    logic        rst_n = 0;
    logic        valid_in = 0;

    logic signed [DW-1:0] a_re, a_im;
    logic signed [DW-1:0] b_re, b_im;
    logic signed [TW-1:0] w_re, w_im;

    logic                  valid_out;
    logic signed [DW-1:0]  p_re, p_im;
    logic signed [DW-1:0]  q_re, q_im;

    // -----------------------------------------------------------------------
    // DUT instantiation
    // -----------------------------------------------------------------------
    fft_butterfly #(
        .DATA_WIDTH   (DW),
        .TWIDDLE_WIDTH(TW),
        .DATA_FRAC    (DF),
        .SCALE_SHIFT  (SS)
    ) dut (
        .clk      (clk),
        .rst_n    (rst_n),
        .valid_in (valid_in),
        .a_re     (a_re),
        .a_im     (a_im),
        .b_re     (b_re),
        .b_im     (b_im),
        .w_re     (w_re),
        .w_im     (w_im),
        .valid_out(valid_out),
        .p_re     (p_re),
        .p_im     (p_im),
        .q_re     (q_re),
        .q_im     (q_im)
    );

    always #(CLK_PERIOD/2) clk = ~clk;

    // -----------------------------------------------------------------------
    // Tracking
    // -----------------------------------------------------------------------
    int pass_count = 0;
    int fail_count = 0;

    // -----------------------------------------------------------------------
    // Helper tasks
    // -----------------------------------------------------------------------

    // Convert real to Q1.14 integer (clamp to representable range)
    function automatic logic signed [DW-1:0] to_q14;
        input real v;
        real clamped;
        begin
            clamped = (v > 1.9999) ? 1.9999 : (v < -2.0) ? -2.0 : v;
            to_q14  = $signed(DW'(int'($rtoi(clamped * SCALE))));
        end
    endfunction

    // Apply one butterfly and wait for the result (2-cycle pipeline)
    task automatic apply_butterfly(
        input real ar, ai, br, bi, wr, wi,     // floating-point inputs
        input real exp_pr, exp_pi,              // expected P (float)
        input real exp_qr, exp_qi,             // expected Q (float)
        input string test_name
    );
        // Convert to fixed-point
        a_re = to_q14(ar); a_im = to_q14(ai);
        b_re = to_q14(br); b_im = to_q14(bi);
        w_re = to_q14(wr); w_im = to_q14(wi);

        // Assert valid for one cycle
        @(posedge clk); #1;
        valid_in = 1'b1;
        @(posedge clk); #1;
        valid_in = 1'b0;

        // Wait 2 pipeline stages
        @(posedge clk); #1;
        @(posedge clk); #1;

        // Check valid
        if (!valid_out) begin
            $display("[FAIL] %s: valid_out not asserted", test_name);
            fail_count++;
            return;
        end

        // Convert expected to Q1.14
        logic signed [DW-1:0] exp_pr_q, exp_pi_q, exp_qr_q, exp_qi_q;
        exp_pr_q = to_q14(exp_pr);
        exp_pi_q = to_q14(exp_pi);
        exp_qr_q = to_q14(exp_qr);
        exp_qi_q = to_q14(exp_qi);

        // Check with tolerance
        if ($signed(p_re - exp_pr_q) > TOL || $signed(p_re - exp_pr_q) < -TOL ||
            $signed(p_im - exp_pi_q) > TOL || $signed(p_im - exp_pi_q) < -TOL ||
            $signed(q_re - exp_qr_q) > TOL || $signed(q_re - exp_qr_q) < -TOL ||
            $signed(q_im - exp_qi_q) > TOL || $signed(q_im - exp_qi_q) < -TOL)
        begin
            $display("[FAIL] %s", test_name);
            $display("  P = (%0d, %0d)  expected (%0d, %0d)",
                      $signed(p_re), $signed(p_im),
                      $signed(exp_pr_q), $signed(exp_pi_q));
            $display("  Q = (%0d, %0d)  expected (%0d, %0d)",
                      $signed(q_re), $signed(q_im),
                      $signed(exp_qr_q), $signed(exp_qi_q));
            fail_count++;
        end else begin
            $display("[PASS] %s  P=(%0d,%0d) Q=(%0d,%0d)",
                      test_name,
                      $signed(p_re), $signed(p_im),
                      $signed(q_re), $signed(q_im));
            pass_count++;
        end
    endtask

    // -----------------------------------------------------------------------
    // Main test sequence
    // -----------------------------------------------------------------------
    initial begin
        $display("=== FFT Butterfly Testbench Start ===");

        // Reset
        rst_n = 0; repeat(4) @(posedge clk);
        #1; rst_n = 1; repeat(2) @(posedge clk);

        // ---- Test 1: W = 1 (identity twiddle, k=0) ----
        // A = 0.5 + j0.25,  B = 0.125 + j0.0625,  W = 1 + j0
        // W*B = B = 0.125 + j0.0625
        // P = A + B = 0.625 + j0.3125
        // Q = A - B = 0.375 + j0.1875
        apply_butterfly(
            .ar( 0.5 ), .ai( 0.25 ),
            .br( 0.125), .bi( 0.0625),
            .wr( 1.0 ), .wi( 0.0  ),
            .exp_pr( 0.625), .exp_pi( 0.3125),
            .exp_qr( 0.375), .exp_qi( 0.1875),
            .test_name("W=1: identity twiddle")
        );

        repeat(3) @(posedge clk);

        // ---- Test 2: W = -j  (quarter turn clockwise, k = N/4) ----
        // A = 0.5 + j0.25,  B = 0.5 + j0.25,  W = 0 - j1
        // W*B: Re = Re(B)*Re(W) - Im(B)*Im(W) = 0.5*0  - 0.25*(-1) =  0.25
        //      Im = Re(B)*Im(W) + Im(B)*Re(W) = 0.5*(-1)+ 0.25*0   = -0.5
        // P = (0.5+0.25, 0.25-0.5) = (0.75, -0.25)
        // Q = (0.5-0.25, 0.25+0.5) = (0.25,  0.75)
        apply_butterfly(
            .ar( 0.5 ), .ai( 0.25),
            .br( 0.5 ), .bi( 0.25),
            .wr( 0.0 ), .wi(-1.0 ),
            .exp_pr( 0.75), .exp_pi(-0.25),
            .exp_qr( 0.25), .exp_qi( 0.75),
            .test_name("W=-j: quarter-turn twiddle")
        );

        repeat(3) @(posedge clk);

        // ---- Test 3: W = -1  (half turn, k = N/2) ----
        // A = 0.5 + j0.25,  B = 0.25 + j0.125,  W = -1 + j0
        // W*B = -B = -0.25 - j0.125
        // P = A - B = (0.25, 0.125)
        // Q = A + B = (0.75, 0.375)
        apply_butterfly(
            .ar( 0.5 ), .ai( 0.25 ),
            .br( 0.25), .bi( 0.125),
            .wr(-1.0 ), .wi( 0.0  ),
            .exp_pr( 0.25), .exp_pi( 0.125),
            .exp_qr( 0.75), .exp_qi( 0.375),
            .test_name("W=-1: half-turn twiddle")
        );

        repeat(3) @(posedge clk);

        // ---- Test 4: W = (1/sqrt2) - j(1/sqrt2)  (N=8, k=1) ----
        // A = 0.5 + j0,  B = 0 + j0.5,  W = 0.7071 - j0.7071
        // W*B: Re = 0*0.7071  - 0.5*(-0.7071) =  0.3536
        //      Im = 0*(-0.7071)+ 0.5*(0.7071)  =  0.3536
        // P = (0.5+0.3536, 0+0.3536)   = (0.8536, 0.3536)
        // Q = (0.5-0.3536, 0-0.3536)   = (0.1464, -0.3536)
        apply_butterfly(
            .ar( 0.5    ), .ai( 0.0    ),
            .br( 0.0    ), .bi( 0.5    ),
            .wr( 0.7071 ), .wi(-0.7071 ),
            .exp_pr( 0.8536), .exp_pi( 0.3536),
            .exp_qr( 0.1464), .exp_qi(-0.3536),
            .test_name("W=exp(-jpi/4): N=8 k=1 twiddle")
        );

        repeat(3) @(posedge clk);

        // ---- Test 5: Zero inputs — output must be zero ----
        apply_butterfly(
            .ar(0.0), .ai(0.0),
            .br(0.0), .bi(0.0),
            .wr(0.7071), .wi(-0.7071),
            .exp_pr(0.0), .exp_pi(0.0),
            .exp_qr(0.0), .exp_qi(0.0),
            .test_name("Zero inputs")
        );

        repeat(3) @(posedge clk);

        // ---- Test 6: Near-overflow inputs (saturation check) ----
        // With SS=0, A = B = ~1.0, W=1  =>  P ~= 2.0  (may saturate to max)
        // Just check no X values propagate (structural check)
        a_re = 16'sh7FFF; a_im = 16'sh0000;
        b_re = 16'sh7FFF; b_im = 16'sh0000;
        w_re = 16'sh4000; w_im = 16'sh0000;   // W = 1.0 in Q1.14
        @(posedge clk); #1;
        valid_in = 1'b1;
        @(posedge clk); #1;
        valid_in = 1'b0;
        @(posedge clk); #1;
        @(posedge clk); #1;
        if ($isunknown(p_re) || $isunknown(p_im) ||
            $isunknown(q_re) || $isunknown(q_im)) begin
            $display("[FAIL] Near-overflow inputs: X/Z on output");
            fail_count++;
        end else begin
            $display("[PASS] Near-overflow inputs: no X/Z  P=(%0d,%0d) Q=(%0d,%0d)",
                      $signed(p_re), $signed(p_im),
                      $signed(q_re), $signed(q_im));
            pass_count++;
        end

        // -----------------------------------------------------------------------
        // Summary
        // -----------------------------------------------------------------------
        repeat(5) @(posedge clk);
        $display("");
        $display("=== Testbench Complete: %0d PASSED, %0d FAILED ===",
                  pass_count, fail_count);
        if (fail_count == 0)
            $display("ALL TESTS PASSED");
        else
            $display("FAILURES DETECTED -- review above");
        $finish;
    end

    // Timeout watchdog
    initial begin
        #200000;
        $display("TIMEOUT");
        $finish;
    end

    // Waveform dump
    initial begin
        $dumpfile("/tmp/fft_butterfly_tb.vcd");
        $dumpvars(0, fft_butterfly_tb);
    end

endmodule

`default_nettype wire
