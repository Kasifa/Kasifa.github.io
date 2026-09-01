# R0.73X minimal finite Fourier harness: exact falsification and tent-slice diagnostic

**Status:** reproducible single-package diagnostic; exact algebra plus converged
absolute-value quadrature; not a two-producer sealed certificate

**Command:**

```bash
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/r073x_finite_fourier_harness.py --check-only
```

- **DGX used:** false
- **Network used:** false
- **Navier--Stokes simulation:** false
- **Clay conclusion:** OPEN

## 1. Quantifier boundary

The exact counterexample below concerns the deliberately strong statement
with a **fixed nonnegative harmonic probe**
\(\eta=1+\tfrac12\Phi_\ell(x)\), where \(\Phi_\ell\) is the declared
sine or cosine phase and the carrier heat factor is
\(Q=e^{-N^2s}=1/2\),
and a constant independent of the amplitude \(A\).  To keep the frozen
radius restriction, the harness verifies the exact NSE rescaling
\(u_{A,N}(x)=ANW(Nx)\) with \(N=4\), \(R=1/4<\pi/8\),
\(s=(\log2)/16=(\log2)R^2\), and \(\nu=1\).  The displayed exact rows
below have the common \(N^4\) factor divided out.  This
probe is periodic and satisfies \(\eta\ge1/2\), but it is not compactly
supported.  Therefore the calculation does not yet refute the compact local
cutoff versions (5.1)--(5.2) in the problem freeze.  That transfer needs a
separate certified bump or fixed-sign-neighborhood argument.

The tent rows integrate **heat scale only at one frozen time**.  They are not
parabolic time-integrated tent or Carleson norms and cannot establish an
epsilon-regularity or continuation theorem.

## 2. Exact two-pair improvement

One conjugate pair gives \(\Pi_s=\nabla\!\cdot K_s={\mathscr S}_s=0\)
exactly.  Already the two-pair field

\[
u=(-2\sin(x+y),\,-2\cos x+2\sin(x+y),\,-\cos x-\sin(x+y))
\]

with the rescaled probe \(\eta_4=1+\tfrac12\sin(4x)\) has, after division
by the common \(N^4\) factor and at the carrier heat factor \(1/2\),

\[
\langle\eta\Pi_s\rangle=\frac{225}{1024},\qquad
-\langle\nabla\eta\cdot K_s\rangle=\frac{27}{512},\qquad
\langle\eta{\mathscr S}_s\rangle=\frac{171}{1024}.
\]

Thus \(225/1024=27/512+171/1024\), with all three entries nonzero.
The direct Gaussian-moment construction of \({\mathscr S}_s\) agrees
coefficientwise with \(\Pi_s-\nabla\cdot K_s\); it is not obtained by
reusing that subtraction.

For the complete displayed quadratic denominator
\(\nu D+R^{-2}k\), with the same common \(N^4\) factor divided out,

\[
N^{-4}\langle\eta(\nu D_{ii,s}+R^{-2}k_s)\rangle
=\frac{855}{64}A^2.
\]

Consequently the exact ratios are

\[
\frac{|\langle\eta\Pi_s\rangle|}
{\langle\eta(\nu D_{ii,s}+R^{-2}k_s)\rangle}
=\frac{5|A|}{304},\qquad
\frac{|\langle\eta{\mathscr S}_s\rangle|}
{\langle\eta(\nu D_{ii,s}+R^{-2}k_s)\rangle}
=\frac{|A|}{80}.
\]

Hence no amplitude-independent constant controls these two numerators in
this exact harmonic-probe class.  The result also shows that two conjugate
pairs suffice for a fully nonzero localized split; it is not an exhaustive
minimal-wavevector theorem.

## 3. Three-pair anchor reproduction

For the R0.73W three-pair field and the rescaled probe
\(1+\tfrac12\cos(4x+4y)\), the harness recovers, after the same
\(N^4\) normalization,

\[
-\frac3{32}=\frac9{128}-\frac{21}{128}.
\]

The complete quadratic denominator is \(1035A^2/64\), so the exact
production and remainder ratios are \(2|A|/345\) and \(7|A|/690\),
respectively.  This independently reproduces the design anchor while
keeping its harmonic-cutoff scope explicit.

## 4. Signed versus spatially absolute heat-scale slices

For each field the harness evaluates in the carrier variable
\(r=N^2s\in(0,1)\), equivalently over the physical heat interval
\(0<s<R^2\),

\[
\left|\int_0^1\!\langle\eta f_r\rangle\,dr\right|
\quad\hbox{and}\quad
\int_0^1\!\langle\eta|f_r|\rangle\,dr,
\qquad f\in\{\Pi,{\mathscr S}\}.
\]

The signed value is a 70-digit evaluation of an exact finite exponential
sum.  The absolute value is a deterministic 1024-by-1024 Fourier-grid,
64-node Gauss--Legendre result, accompanied by 128/256/512/1024 convergence.
It is numerical, not interval-certified.

| field | channel | signed/absolute cancellation ratio | last absolute convergence delta |
|---|---:|---:|---:|
| two-pair | \(\Pi\) | 0.26072055157691815 | 3.0273101087052723e-07 |
| two-pair | \({\mathscr S}\) | 0.16833788146320283 | 1.5932787131855974e-06 |
| three-pair | \(\Pi\) | 0.10680817068352023 | 1.3984889102314213e-07 |
| three-pair | \({\mathscr S}\) | 0.21746474493348442 | 3.0287638153048135e-07 |

A small ratio records cancellation only.  It gives no upper bound for the
absolute tent quantity.  A bounded ratio along these two finite fields gives
no evidence for a universal Carleson estimate.

## 5. Licensed conclusions and open rows

- **Exact:** the one-pair cubic channels vanish; the displayed two- and
  three-pair cutoff rows and amplitude ratios are exact.
- **Exact falsification:** the fixed-harmonic-probe, amplitude-independent
  quadratic absorption candidates are false.
- **Finite numerical diagnostic:** signed and absolute static scale slices
  differ substantially and the stored quadrature ladder is converged at the
  reported resolution.
- **Still open:** compact-cutoff (5.1)--(5.2), the ledger-complete cubic
  candidate (5.3), any time-integrated tent/Carleson control, suitable-weak
  defect passage, epsilon regularity, and three-dimensional global
  regularity.

NOT CLAY.
