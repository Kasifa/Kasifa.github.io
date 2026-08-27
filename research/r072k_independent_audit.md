# R0.72K independent audit protocol — complex complete-root ledger

**Date:** 2026-08-27  
**State:** source prepared; deliberately not executed in this change  
**Route:** independent finite corroboration, downstream only of the archived
R0.72J independent result

## 1. Question under audit

Let $B$ be a real or complex Banach space and let
$X\in W^{2,1}([a,b];B)$.  If

\[
 a\le t_1<t_2<\cdots<t_m\le b,
 \qquad X(t_j)=0,
\]

then the directional root-gap estimate is

\[
 \sum_{j=2}^{m}\|X'(t_j)\|^2
 \le
 2\int_{t_1}^{t_m}\|X'(x)\|\,\|X''(x)\|\,dx.
\tag{1.1}
\]

This is not a vector-valued assertion that $X'(c)=0$.  If the right endpoint
derivative is nonzero, choose on every gap $[t_{j-1},t_j]$ a norm-one
complex-linear norming functional $\ell_j$ for $X'(t_j)$, and put

\[
 \phi_j(x)=\operatorname{Re}\ell_j(X'(x)).
\]

The root condition gives

\[
 \int_{t_{j-1}}^{t_j}\phi_j(x)\,dx
 =\operatorname{Re}\ell_j(X(t_j)-X(t_{j-1}))=0.
\]

Continuity supplies a scalar zero $c_j$ of $\phi_j$.  Absolute
continuity then yields

\[
 \begin{aligned}
 \|X'(t_j)\|^2
 &=\phi_j(t_j)^2-\phi_j(c_j)^2\\
 &=2\int_{c_j}^{t_j}\phi_j\phi_j'\\
 &\le2\int_{t_{j-1}}^{t_j}\|X'\|\,\|X''\|.
 \end{aligned}
\]

If $X'(t_j)=0$, the corresponding bound is immediate.  Summing the disjoint
gaps proves (1.1).  For an arbitrary, possibly infinite, root set, apply
(1.1) to every finite subset and pay the first selected root by the uniform
bound $\sup_{X(t)=0}\|X'(t)\|^2$, which is finite on the compact interval.
If the root set has a least element, adjoining it to every finite subset
replaces that supremum by the derivative payment at the least root.  Taking
the supremum over finite collections defines the nonnegative root sum without
assuming isolated roots.  Thus complex targets require no common phase, no
vector-valued Rolle theorem, and no enumeration of zeros of the individual
real and imaginary parts.

## 2. Exact R0.72K ledger consequence

For the triangular target row

\[
 F_0'+\lambda_0F_0=\delta h,
 \qquad
 h'+\lambda_0h=QF+\delta b,
\tag{2.1}
\]

assume $\delta\ne0$ and set $g(x)=e^{\lambda_0x}F_0(x)$.  Then

\[
 g'=\delta e^{\lambda_0x}h,
 \qquad
 g''=\delta e^{\lambda_0x}(QF+\delta b).
\]

Apply (1.1) on each root gap ending at $t_j$, and divide that gap's
inequality by $\delta^2e^{2\lambda_0t_j}$.  Since $x\le t_j$ and
$\lambda_0\ge0$,

\[
 e^{-2\lambda_0(t_j-x)}\le1.
\]

Consequently,

\[
 \sum_{j=2}^{m}|h(t_j)|^2
 \le
 2\int |h|\,|QF+\delta b|
 \le 2\mathcal E_Q+2\mathcal C_\times.
\tag{2.2}
\]

The first root remains bounded by $E\rho^2$.  The complete measured
ledger audited here is therefore

\[
 G_{\mathrm{all}}^{\mathrm{ex}}
 \le E\rho^2+2\,\texttt{mixedRow}+2\,\texttt{cubic}.
\tag{2.3}
\]

There is no global exponential loss and no $2\lambda_0^2Q_*$ diagonal
term.  The archived analytic upper rows give the separate proxy

\[
 E\rho^2+\texttt{rawMixedMoment}+\texttt{rawTrueCubic}.
\tag{2.4}
\]

The audit explicitly checks that (2.4) equals the old archived BV proxy
after subtracting `rawBvProxyTargetDiagonal`.

## 3. Independence boundary and SHA lineage

The script reads exactly these two archived lineage files:

- `research/certificates/r072j/independent-result.json`;
- `research/certificates/r072j/SHA256SUMS`.

At runtime it requires the archived result's actual SHA-256 to equal the
entry in `SHA256SUMS`, requires status `passed`, and records the source audit,
generation time, Git commit, archived implementation hash, expected artifact
hash, and actual artifact hash.  It neither
imports nor reads any R0.72K producer implementation or producer artifact.
It performs no new PDE evolution.

## 4. Independent finite checks

### 4.1 Sharpness family

For $n\ge4$, put $\varepsilon=1/n$.  On $[0,1]$, let $X'(t)$ be
$-\varepsilon$ up to

\[
 a=1-\frac{2\varepsilon}{1+\varepsilon},
\]

then increase linearly from $-\varepsilon$ to $1$.  Its integral is zero,
so $X(0)=X(1)=0$, while

\[
 \int_0^1|X'||X''|=\frac{1+\varepsilon^2}{2},
 \qquad
 \frac{|X'(1)|^2}{2\int|X'||X''|}
 =\frac{1}{1+\varepsilon^2}\uparrow1.
\tag{4.1}
\]

Thus the factor $2$ in (1.1) cannot be reduced.  The implementation uses
the different integer parameter $n$, splits quadrature at the ramp and
velocity zeros, and compares the numerical and exact values.

### 4.2 Complex scalar projection

For several integers $k$, the audit takes

\[
 X_k(t)=e^{2\pi ikt}-1,
 \qquad 0\le t\le1/k.
\]

Both endpoints are roots, but $X_k'(t)$ never vanishes.  A norming
functional for the right endpoint derivative is constructed explicitly;
the audit numerically verifies its unit norm and zero mean projection,
reconstructs a directional zero by bracketing and bisection, and checks
(1.1).

### 4.3 Complex two-component Hilbert projection

For several $\alpha>0$, the vector test is

\[
 X_\alpha(t)=
 \bigl(e^{2\pi it}-1,
 \alpha(e^{4\pi it}-1)\bigr)\in\mathbb C^2,
 \qquad 0\le t\le1.
\]

The first derivative component never vanishes, so the vector derivative
cannot vanish.  The code independently builds the Hilbert norming
functional

\[
 \ell(z)=\frac{\sum_q\overline{X_q'(1)}z_q}{\|X'(1)\|},
\]

recovers a zero of $\operatorname{Re}\ell(X')$, and checks the weighted
variation bound.  This is the relevant counterexample to any attempted
vector-valued Rolle step and a positive check of the directional repair.

## 5. Derived finite ledgers and physical normalization

For every SHA-verified R0.72J independent row the script independently
computes

\[
 \begin{aligned}
 L_{\rm meas}
 &=E\rho^2+2\,\texttt{mixedRow}
   +2\,\texttt{deltaIntegralAbsHB},\\
 L_{\rm an}
 &=E\rho^2+\texttt{rawBvProxyMixedMoment}
   +\texttt{rawBvProxyTrueCubic},\\
 L_{\rm root}&=|h(\tau)|^2.
 \end{aligned}
\]

It checks $L_{\rm root}\le L_{\rm meas}\le L_{\rm an}$, records the raw
$R^{-2}$ scaling, and applies the inherited physical conversion

\[
 L^{\rm phys}=\Theta L,
 \qquad
 L^{\rm norm}=\frac{\Theta L}{\texttt{referencePayment}}.
\]

The output also records $L^{\rm phys}/R$,
$R^{2/3}L^{\rm norm}$, and all-size and last-three-size log-log slopes.
These finite slopes are diagnostics, not asymptotic proofs.

## 6. Artifacts and invocation

The default invocation, to be run only after review, is

```bash
python3 research/r072k_independent_audit.py \
  --output-dir research/certificates/r072k
```

The selected output directory receives:

- `independent-config.json`;
- `independent-progress.ndjson`;
- `independent-resource.ndjson`;
- `independent-result.json`;
- `independent-data.csv`;
- `independent-environment.txt`.

The CSV is a lossless union of sharpness, complex-scalar, complex-vector,
and ledger records.  The result preserves every declared check, lineage
field, scale diagnostic, and limitation.

## 7. Limitations retained by design

1. Binary64 quadrature and bisection are not interval certificates.
2. Finite examples corroborate but do not prove the analytic lemma; the
   proof is the argument in Section 1.
3. The sampled directional zero is not a complete enumeration of complex
   roots.
4. The ledger inherits the archived R0.72J model, $\Theta$, and reference
   payment; no new PDE trajectory is evolved.
5. Finite slopes do not establish the $R\to\infty$ laws.
6. The audit makes no statement about general three-dimensional
   Navier--Stokes regularity and does not resolve the Clay problem.
