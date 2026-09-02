# R0.74S problem freeze — signed stopping times and weighted internal faces

## 0. Purpose

R0.74R isolates recent positive clock variation as one of the three ways a
large terminal completed clock can avoid a persistent kinetic window.
R0.74S tests the first proposed repair: stop each active shell at its last
upcrossing, sum the resulting signed work, and use adjacent-shell
cancellation before taking absolute values.

The first gate is deliberately more favorable than the frozen padded-shell
geometry.  It assumes an exact adjacent-boundary representation

\[
 f_k(t)=b_{k+1}(t)-b_k(t),\qquad 1\le k\le M,
\tag{S.F1}
\]

and asks whether discrete Abel summation by itself makes the stopped
coefficients small.  If there is no gain even in this ideal model, the actual
R0.74P flux can only close through additional Navier--Stokes sign,
backscatter, leakage, or observability information.

This gate does not replace the R0.74R conditional theorem and does not alter
the frozen clocks.  It is an auxiliary falsification test.  **NOT CLAY.**

## 1. Frozen weights and stopping data

Retain

\[
 \gamma_k=\exp\!\left(-\frac{4^{k-1}}{32}\right),\qquad k\ge1.
\tag{S.F2}
\]

Fix a terminal time \(\tau\), a finite shell range \(1\le k\le M\), and
stopping times \(\sigma_k<\tau\).  At time \(t\), the active set and stopped
coefficient are

\[
 A(t)=\{k:\sigma_k<t<\tau\},\qquad
 c_k(t)=\gamma_k1_{A(t)}(k).
\tag{S.F3}
\]

The spatial coefficient variation is

\[
 V_\gamma(A)
 :=|c_1|+\sum_{k=2}^{M}|c_k-c_{k-1}|+|c_M|,
\tag{S.F4}
\]

equivalently after extending \(c_0=c_{M+1}=0\).

## 2. Exact questions

The Step-1 gate asks:

1. What is the exact stopped Abel identity for
   \(\sum_k\gamma_k\int_{\sigma_k}^{\tau}f_k\)?
2. If \(A\) is a union of connected shell blocks, how does
   \(V_\gamma(A)\) compare with \(\sum_{k\in A}\gamma_k\)?
3. Does the super-Gaussian weight create a vanishing internal-face
   coefficient, an \(M^{-1/2}\) gain, or any other compression factor?
4. Is an absolute-value estimate after Abel summation algebraically sharp?

## 3. Decision rule

- If \(V_\gamma(A)=o(\sum_{k\in A}\gamma_k)\) for broad active sets, retain
  coefficient cancellation as a possible packing mechanism.
- If the two quantities are uniformly comparable and the absolute Abel
  bound is saturable, reject coefficient cancellation as a standalone
  mechanism.  Continue only with a named PDE sign or boundary-work input.

No conclusion about the actual Navier--Stokes boundary flux follows from an
abstract witness.  The eventual PDE binding must separately account for the
frozen padded cutoffs, quadratic source terms, pressure, moving-frame drift,
terminal energy, dissipation, leakage, and negative work.

## 4. Claim boundary

| Statement | Status at freeze |
|---|---|
| R0.74R terminal-window first-shell stability | **INHERITED / PROVED** |
| R0.74R arbitrary-clock two-factor implication | **INHERITED / PROVED IMPLICATION; INPUT OPEN** |
| Ideal adjacent-boundary identity (S.F1) for the actual frozen flux | **NOT ASSUMED / REQUIRES BINDING** |
| Weighted stopped-Abel coefficient gain | **TO BE DECIDED IN R0.74S STEP 1** |
| Signed PDE cancellation or backscatter control | **OPEN** |
| Fixed-scale inequality (Q.1), contraction, regularity, or Clay conclusion | **OPEN / NOT CLAIMED** |
