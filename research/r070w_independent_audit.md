# R0.70W independent mathematical audit

**Verdict:** **PASS** for the snapshot identified below. The final review has
zero blocker, zero major issue, and zero minor issue. R0.70W proves an exact
far-shell obstruction to controlling the projected frame defect by norms of
the already-formed physical covariance-area fields. It also proves an exact
response-area current identity and a scale-correct universal Fourier
majorant. It does not prove the surviving direct signed trilinear estimate,
an enstrophy closure, a continuation theorem, global regularity, or any
Millennium-problem conclusion.

## 1. Audited snapshot

The audited branch is
`codex/r070w-nonlocal-summation-obstruction`, based on commit

\[
 \mathtt{b59b398fac3222b41acc6b218c20999454df68ec}.
\]

The final uncommitted payload has the following SHA-256 digests:

- `research/r070w_report-source.md`:
  `280839c95f03adaa99f018a06c651209f7345435e3831e1b66d7ceecb29b556e`;
- `research/r070w_exact_audit.py`:
  `66127e61ea2339f5bcf76178fe573df39e4047f0dd20ad29da8f82f392a5241f`;
- `tests/r070w-projected-area-summation-gate.test.mjs`:
  `3f0765011f40dc0d01c9b3fccf2b0754379c479e2e2a118052c732f4a133b332`;
- `research/certificates/r070w/README.md`:
  `a269f4edf8d047b551a71e7aad3c1fee39083aa569f53da672baeeb371d4c54f`;
- `research/certificates/r070w/command.txt`:
  `20436f8fd2ac03ef8e007826ef6bf29260f40d61ad3efa58eebf4037c38be3af`;
- `research/certificates/r070w/environment.txt`:
  `4c7ffe8c248a1211ea502cd20551a6e0fa605c6f233e4964599e17791dc67551`;
- `research/certificates/r070w/result.json`:
  `f7b1761c551a73ed7fac2969d34dc8cc160dd33bafe85d5336b43a940453bc23`;
- `research/certificates/r070w/SHA256SUMS`:
  `fbb9656ea561a61ec61c2ded9f1bdf3244c2dc3415d84d8d84e95c4158f02c88`.

The five-entry certificate manifest locks the README, command,
environment, archived result, and exact producer. The report, focused test,
and this audit are recorded separately and are not silently included in
that five-path manifest.

## 2. Validation record

| Check | Result | Scope |
|---|---:|---|
| Focused R0.70W Node gate | **9/9 PASS** | Producer-byte equality, exact ledgers, claim boundary, and certificate paths |
| Certificate SHA manifest | **5/5 PASS** | Every archived payload digest and relative path match |
| Full repository Node suite | **673/673 PASS** | Final repository-wide regression after the complete 18-mode repair |
| Direct i18n build | **PASS** | 105 pages, 9855 translations, 41 stale translations |
| Direct vinext build | **5/5 PASS** | All five build stages completed |
| Independent mathematical reviews | **PASS / PASS** | One theorem-and-summation audit and one independent exact-rank/signed audit |

The producer reports Python 3.12.13 and SymPy 1.14.0. It regenerates the
archived JSON byte for byte. The calculation is finite exact algebra and
does not require a numerical simulation, a formal figure, or DGX compute.

The package-manager wrapper attempted an unnecessary registry/store check
in this environment. The pinned Node runtime was therefore used directly
for the i18n script, vinext build, focused gate, and full suite. This is an
execution-environment detail and not a mathematical dependency.

## 3. Projected-wedge identity

For

\[
 n=p+q\ne0,
 \qquad p\cdot a=q\cdot b=0,
\]

the report proves

\[
 \nu_n\times[(a\otimes b+b\otimes a)\nu_n]
 =-\frac1{|n|}\nu_n\times[(q-p)\times(a\times b)].
\]

The sign and factor are correct. Inserting the symmetric response kernel
and retaining the ordered Fourier sum gives

\[
 F(n)
 =-\frac1{2|n|}\sum_{p+q=n}K(p,q)
 \nu_n\times[(q-p)\times
 (\widehat\omega(p)\times\widehat\omega(q))].
\]

The factor (1/2) is required because the displayed sum is ordered while
the tensor identity is polarized. The exact producer verifies the generic
divergence constraints, the vector identity, and the zero symbolic
residual.

## 4. Far-shell rank-one obstruction

For

\[
 w=e_1\cos x_2-e_2\cos x_1,
 \qquad h=\cos(4x_3)w,
 \qquad \omega_\varepsilon=w+\varepsilon h,
\]

the two radii are (1) and (sqrt{17}>4). Strict annular support makes
their response vectors orthogonal. Each frame block is a scalar multiple
of (w), hence

\[
 Q=(1+\varepsilon^2\cos^2(4x_3))w\otimes w,
 \qquad
 \Omega_\alpha\times\Omega_\beta=0,
 \qquad G_Q=r=0.
\]

The frame defect is nevertheless

\[
 \mathcal D_\times
 =2\varepsilon\cos(4x_3)w\otimes w.
\]

The producer constructs all eighteen nonzero defect modes. Ten diagonal
modes have zero strain projection. At the eight mixed modes
(n=(\pm1,\pm1,\pm4)), each contribution to
(mathfrak X_\times) is (arepsilon^2/2916). Therefore

\[
 \mathfrak X_\times=\frac{2\varepsilon^2}{729}>0.
\]

This proves the stated no-go: any definite norm or seminorm of the
physical cross-product fields is zero while the projected defect is
positive. Applying a linear derivative, inverse derivative, or shell
weight after those fields have already been formed cannot recover the
cancelled pair information.

The caveat is correctly retained. The sample has rank one where (w\ne0)
and rank zero at its common zeros; it does not have a uniform positive
lower bound on the top covariance eigenvalue. It therefore does not refute
a theorem that explicitly assumes such a global top gap.

## 5. General separated scale and physical cancellation

At (n=(1,1,4)), the two contributing polarization wedges are

\[
 -e_3/8,
 \qquad +e_3/8,
\]

so the physical area cancels. The corresponding symmetric tensors add to

\[
 -\frac{\varepsilon}{4}
 (e_1\otimes e_2+e_2\otimes e_1).
\]

Thus multiplicity two is already enough to invalidate the post-convolution
area comparison; no large mode count or logarithmic accumulation is
needed.

For every integer (M\ge4), the final producer constructs the complete
eighteen-mode defect from the low Fourier dictionary and the two shifts
(\pm M e_3), projects each mode, verifies that exactly eight projections
are nonzero, and sums them to

\[
 \mathfrak X_{\times,\varepsilon,M}
 =\frac{\varepsilon^2M^2}{(M^2+2)^3}.
\]

This closes the only machine-coverage issue raised during review; the
general-(M) formula is not inferred from one representative mode.

## 6. Signed-work boundary and negative control

Biot--Savart strain preserves Fourier support. The twelve vorticity modes
and eighteen defect modes of the exact-rank sample are disjoint, so

\[
 \mathfrak E_S
 =\int S(\omega_\varepsilon):\mathcal D_\times\,dx=0.
\]

The counterexample therefore disproves the route through the ambient
projected Hilbert majorant, not the direct signed trilinear route.

For the resonant perturbation

\[
 z_{\eta,M}=\eta(1,-1,0)
 \cos(x_1+x_2+Mx_3),
\]

the exact calculation gives

\[
 \mathfrak E_S
 =-\frac{\varepsilon\eta M}
 {2(M^2+1)(M^2+2)}.
\]

The spatial factors

\[
 A_{13}=\frac{M^2+3}{2(M^2+1)(M^2+5)},
\]

\[
 A_{23}
 =\frac{(2M^2+3)(12M^2+5)}
 {20(4M^2+1)(4M^2+5)}
\]

and the complete response-area expression

\[
 \mathcal A_{-1}
 =\eta^2[A_{13}
 +\varepsilon^2(1-\gamma_{23}^2)A_{23}]
\]

were independently recomputed. The final certificate obtains the response
wedge norms and mixed term from the Gram-determinant identity, computes the
physical mixed (dot H^{-1}) inner product, and locks the complete formula
with zero residual. For (eta\ne0), the ratio is
(O_\varphi(|\varepsilon|M^{-2})). This family is a negative control and
does not disprove the direct signed-area candidate.

## 7. Exact response-area current

For the row-matrix current

\[
 \mathcal C_m
 =2\left[\omega\times\partial_m\omega
 -\sum_\alpha\Omega_\alpha\times\partial_m\Omega_\alpha\right],
\]

ordered-pair symmetrization gives

\[
 \widehat{\mathcal C}(n)
 =i\sum_{p+q=n}K(p,q)(q-p)\otimes
 (\widehat\omega(p)\times\widehat\omega(q)).
\]

The row orientation, sign, and factor are correct. The final producer
compares the two ordered contributions from the definition with the
symmetrized symbol and records a zero residual. Antisymmetrization gives

\[
 F(n)=\frac{i}{2|n|}
 [\widehat{\mathcal C}(n)-
  \widehat{\mathcal C}(n)^{\mathsf T}]\nu_n.
\]

Consequently,

\[
 \|F\|_2^2\le\|\mathcal C\|_{\dot H^{-1}}^2,
 \qquad
 \mathfrak X_\times\le\|\mathcal C\|_{\dot H^{-2}}^2,
\]

and

\[
 |\mathfrak E_S|
 \le\|\omega\|_2\|\mathcal C\|_{\dot H^{-1}}.
\]

These are exact-order bounds but not a closure: the current retains a
derivative before pair summation and is not determined by the pointwise
covariance eigenvalues.

## 8. Universal exact-order majorant

Let (R=\max\{|p|,|q|\}). The two scalar regions give

\[
 K(p,q)\frac{|p|+|q|}{|p+q|^2}
 \le\frac{12}{R}
\]

when the smaller input is at most (R/2), and

\[
 K(p,q)\frac{|p|+|q|}{|p+q|^2}
 \le\frac{3M_\varphi^2}{R}
\]

otherwise. Both constants were checked independently. With
(C_0=\max\{12,3M_\varphi^2\}), this proves

\[
 \mathfrak X_\times\le C_0^2\mathcal U_{-2}(\omega).
\]

Defining (widehat b(0)=0) and
(widehat b(k)=|k|^{-1/2}|\widehat\omega(k)|) for (k\ne0), convolution,
Parseval, and
(dot H^{3/4}(\mathbb T^3)\hookrightarrow L^4(\mathbb T^3)) give

\[
 \mathfrak X_\times
 \le\frac{C_0^2C_{S,4}^4}{4}
 \|\omega\|_{\dot H^{1/4}}^4.
\]

Interpolation and Young's inequality then return only

\[
 |\mathfrak E_S|
 \le\frac\nu2\|\nabla\omega\|_2^2
 +C_\varphi\nu^{-3}\|\omega\|_2^6.
\]

This is the classical cubic-enstrophy scale. It is a valid all-mode bound,
but it gives no large-data a priori closure.

## 9. Claim boundary and next gate

The report correctly leaves open

\[
 |\mathfrak E_S|
 \stackrel{?}{\le}
 C_{\varphi,\sigma}
 \|\nabla\omega\|_2\|G_Q\|_{L^{6/5}}.
\]

The exact-rank obstruction passes the necessary null test because both
sides vanish. Neither finite consistency nor correct scaling proves the
estimate. The next valid gate is the resonance-aware signed trilinear form,
or a compensated estimate for the antisymmetric response-area current.

No publication, public-page update, DNS claim, or regularity claim follows
from this audit.
