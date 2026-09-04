# R0.76J primary mathematical audit

## Verdict

- Mathematical verdict: **PASS**
- Mathematical blockers: **0**
- Source-range blockers: **0**
- Claim-boundary blockers: **0**
- Scope: the local edge reconstruction J.1--J.45 and its hash-bound
  insertion into the already-audited R0.76I downstream chain.

The audit initially found one formal division-by-zero omission for
`F=0` and a nonoptimal interior constant.  The frozen candidate now
handles `F=0` before division, pads distinct zero-coefficient slots before
the basis expansion, and uses the two-sided interior argument.  Both
repairs have been reread below.

## Bound objects

| object | SHA-256 | role |
|---|---|---|
| R0.76J main theorem | `a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f` | Audited local proof and exact-shear insertion. |
| R0.76J source report | `371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7` | Source roles, collision boundary, and search stop. |
| R0.76I main theorem | `6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce` | Frozen downstream derivative, terminal, energy, and physical chain. |
| R0.76I primary audit | `65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe` | Independent sign, power, range, and normalization audit of that chain. |

The R0.76I core commit is
`0b73f68e072e573d9aaaa824e137e29a49d3cd67`.  Any mismatch in these
dependency hashes is fail-closed and requires a new downstream audit.

## 1. Hardy/Laplace conventions and the finite basis

The inner product in J.14 is linear in the first variable.  With

\[
 k_w(s)=\frac1{s+\overline w}
       =\mathcal L(e^{-\overline wt})(s),
\]

Plancherel gives

\[
 \langle G,k_w\rangle
 =\int_0^\infty h(t)e^{-wt}dt=G(w),
 \qquad \|k_w\|^2=\frac1{2\Re w}.
\]

For `zeta_j=alpha/2-i lambda_j`, direct calculation gives

\[
 |s+\zeta_j|^2-|s-\overline{\zeta_j}|^2
 =2\alpha\Re s,
\]

so `B_j` is contractive in the right half-plane and unimodular on its
boundary.  The kernel in J.16 is
`sqrt(alpha) k_(overline(zeta_m))`.  For `m<n`, after cancelling the
common boundary-unimodular product,

\[
 \langle B_m\Psi,\sqrt\alpha k_{\overline{\zeta_m}}\rangle
 =\sqrt\alpha(B_m\Psi)(\overline{\zeta_m})=0.
\]

The denominator at the zero is
`overline(zeta_m)+zeta_m=alpha`, so no zero-over-zero occurs.  The residue

\[
 c_{mm}=\sqrt\alpha\prod_{\ell<m}
 \frac{-\alpha+i(\lambda_m-\lambda_\ell)}
      {i(\lambda_m-\lambda_\ell)}
\]

is nonzero for distinct frequencies.  Orthogonality, unit norms,
triangularity, and spanning in J.12--J.20: **PASS**.

## 2. Volterra signs and both Laguerre majorants

The Laplace symbol of J.21 is

\[
 1-\frac\alpha{s+\zeta}
 =\frac{s-\overline\zeta}{s+\zeta},
\]

because `zeta-alpha=-overline(zeta)`.  Thus the product in J.23 has the
correct order and symbol.

At `-x`, reversing the straight segment changes the integral sign, giving
the plus sign in J.25.  If the old bound is
`sqrt(alpha) exp(alpha y/2)P_(r-1)(y)`, its product with the kernel modulus
is exactly `sqrt(alpha) exp(alpha x/2)P_(r-1)(y)`.  On the positive
half-line the exact recurrence retains a minus sign, but its modulus has
the same scalar recursion with `exp(-alpha t/2)`.  Therefore both sides
use

\[
 P_r(x)=P_{r-1}(x)+\alpha\int_0^xP_{r-1}(y)dy
       =L_r(-\alpha x).
\]

Equations J.21--J.31, including every sign and exponential: **PASS**.

## 3. The local weighted-tail inequality

The all-zero function is separated before division.  Otherwise repeated
frequencies are merged and unused distinct zero-coefficient slots pad the
representation to dimension `N`; hence the basis expansion has exactly
the indexed range in J.32 and `I_alpha(F)>0`.

Parseval for the finite orthonormal expansion and Cauchy--Schwarz give

\[
 |F(t)|^2e^{-\alpha t}
 \le I_\alpha(F)\alpha e^{-\alpha t}
 \sum_{m<N}L_m(-\alpha t)^2.
\]

The elementary series bound is

\[
 0\le L_m(-y)\le e^{2\sqrt{my}},
\]

so after `y=alpha t` the factors `alpha` and `dt=dy/alpha` cancel and

\[
 \frac{\text{tail}}{I_\alpha(F)}
 \le N\int_{25N}^\infty e^{-y+4\sqrt{Ny}}dy.
\]

For `y>=25N`, `4sqrt(Ny)<=4y/5`, hence this is at most
`5N exp(-5N)`.  The function `N exp(-5N)` decreases for real `N>=1`,
and `5 exp(-5)<1/20` follows from `exp(5)>100`.  Thus the tail is less
than `I_alpha(F)/20`, yielding the factor `20/19` in J.11.  Equations
J.32--J.34: **PASS**.

## 4. Half-line comparison and edge constants

The entire representatives justify evaluation of the finite basis
expansion at negative time.  The factors `exp(alpha x)` in J.35 and J.36
cancel exactly, leaving J.37 with no exponential prefactor outside the
Laguerre sum.

For `alpha=25N/2`, the tail cutoff is exactly `2`, and

\[
 \frac{20}{19}\alpha N=\frac{250}{19}N^2,
 \qquad
 4\sqrt{N\alpha d}=10\sqrt2N\sqrt d.
\]

Taking square roots produces

\[
 \sqrt{250/19}\,N e^{5\sqrt2N\sqrt d}.
\]

Reflection preserves both the term count and the `L2[-1,1]` norm.
Equations J.35--J.41 and the bilateral theorem J.2: **PASS** for every
`d>=0`, including `d=0` and `N=1`.

## 5. Interior, exterior, and branch-count insertion

At fixed time the real `q`-cosine fibre has at most `N=2q` complex
branches at arbitrary real frequencies `+-kappa_j`.  Frequency collisions
only lower the effective count; no separation denominator enters.

After `z=e_a x`, the exterior squared prefactor is

\[
 \frac1{e_a}\frac{250}{19}(2q)^2
 =\frac{1000}{19e_a}q^2,
\]

and the squared exponential is

\[
 10\sqrt2(2q)\sqrt{\Delta_a}
 =20\sqrt2q\sqrt{\Delta_a}=\Phi_a^{\rm loc}.
\]

For an interior point, affine endpoint scaling on a one-sided interval of
length `ell` gives

\[
 \ell |G(z)|^2\le\frac{500}{19}N^2
 \int_{J_\ell}|G|^2.
\]

Adding the left and right estimates uses total length `2e_a`, so the
factor returns to `250/(19e_a)` before `N<=2q`.  Endpoints follow from
the full interval.  Hence the interior and exterior have the same
`1000/(19e_a)` coefficient.  Finally,

\[
 \int_{E_a}|G|^2\le(2e_a)^{1/3}h(s)^{2/3},
 \qquad e_a\ge\frac12,
\]

gives the explicit observation constant `2000/19` in J.45.  Equations
J.42--J.45: **PASS**.

## 6. Frozen downstream chain and asymptotic rate

R0.76J changes only the observation exponent and constant.  The bound

\[
 \|G\|_\infty^2
 \le Cq^2e^{\Phi_a^{\rm loc}}h^{2/3}
\]

has exactly the same polynomial `q^2` structure as R0.76I.  Therefore the
audited Erdelyi Markov row remains `q^7+q^3alpha^2`, the Kós reverse-time
row remains polynomial, the four-row complete-real identity has unchanged
signs, and the exact physical conversion retains
`a^(2/3)R^(-1/3)q^7`.

Since `Delta_a=O(L^(-1))`,

\[
 \frac{\Phi_a^{\rm loc}}{L^2}
 =O\!\left(\frac{q}{L^{5/2}}\right)=o(1)
\]

under `q=o(L^(5/2))`.  Polynomial factors contribute `o(L^2)` to the
logarithm, while the frozen `omega^(1/3)` contribution is exactly
`-2/11907`.  Equations J.6--J.9 and J.46: **PASS**.

## 7. Source and claim boundary

- Zhang v1 is attribution for the architecture and a sharper constant,
  not a theorem imported by R0.76J.
- Erdelyi's finite-range and interior Nikol'skii inequalities are not used
  in the new observation proof.
- The only specialized literature inputs are in the frozen downstream
  chain: Erdelyi's journal Markov estimate and the Kós endpoint inequality
  recorded there.
- The proof applies to complex coefficients and arbitrary real
  frequencies, but its Navier--Stokes insertion is only the exact real
  one-band constant shear.
- No novelty, priority, arbitrary-field, suitable-weak, regularity,
  singularity, or Clay claim is made.

Source and claim boundary: **PASS**.  **NOT CLAY.**

## Certificate boundary

Finite certificates may bind all source and dependency hashes, check the
equation inventory, verify exact rational constants and branch-count
arithmetic, compare direct Laguerre values with the majorant at finite
fixtures, and confirm the normalized-rate arithmetic.  They cannot prove
boundary Plancherel, a continuum Volterra induction, the downstream
literature inequalities, or the full continuum implication.  This audit
is a mathematical reread, not a peer review or a priority determination.
