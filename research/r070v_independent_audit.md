# R0.70V independent mathematical audit

**Verdict:** **PASS** for the snapshot identified below. No blocker or major
issue remains. R0.70V proves an exact complete-frame response-distance
decomposition, a mode-count-independent narrow-radial-band estimate, a
full-tensor residual obstruction, a strain-projected viscosity ledger, and a
pairwise triad-area reduction. It does not prove the missing shell summation,
time integrability, an enstrophy closure, a continuation criterion, or any
Navier--Stokes Millennium-problem conclusion.

## 1. Audited snapshot

I audited branch `codex/r070v-response-distance-defect` at base commit

\[
 \mathtt{992be8f696e9ab925f9949ba68a92814c5168dc6}.
\]

The audited payload has the following SHA-256 digests:

- `research/r070v_report-source.md`:
  `868800ca8a3b4aa0067cede6494771102270d1d066fa6093114f7f9b4b46151c`;
- `research/r070v_exact_audit.py`:
  `03d8de2a2aee5b45eb5dfb8be1797beefb3ce0a386b4822da205fe53576e9b40`;
- `tests/r070v-response-distance-strain-gate.test.mjs`:
  `b139819e10bb313c59e142dfeb762a82abd70e6e4239cb8f094053f9eef4a0f5`;
- `research/certificates/r070v/README.md`:
  `5e38e13633855cd980ca6099669fff369cff897961f9c6651d41c4a26b4965af`;
- `research/certificates/r070v/command.txt`:
  `eedc9d825b5b2d2b3a4ec14e663b3cc033fe8cd2076a1f7f067932715299add2`;
- `research/certificates/r070v/environment.txt`:
  `89c4c8fdaf927a93206b6c839c44c444ca20e170a658283821264025ef4fb01f`;
- `research/certificates/r070v/result.json`:
  `c2e57fcaf16089d1b863215413e6e49178da6c6d6b111b5597df6890e548c6fe`;
- `research/certificates/r070v/SHA256SUMS`:
  `5e7763ca2286f8db0918bb67b1a5484d4a736f7e511e2e7d9611f376667d7f49`.

The certificate manifest locks exactly five payload paths: the README,
command, environment, result, and producer. The report and focused test are
not part of that five-path manifest and are recorded separately above.

## 2. Current validation record

The final validation records are:

| Check | Current result | Scope |
|---|---:|---|
| Focused R0.70V Node gate | **9/9 PASS** | Raw producer-byte equality, endpoint branches, finite exact groups, claim tokens, and SHA path set |
| Certificate SHA manifest | **5/5 PASS** | Every archived digest and the exact five-path set match |
| Full repository Node suite | **664/664 PASS** | Final repository-wide regression record |
| Direct i18n build | **PASS** | 105 pages, 9855 translations, 41 stale translations |
| Direct vinext build | **5/5 PASS** | All five build stages completed |

The focused command required the bundled Node runtime because `node` is not
on the interactive shell PATH. This is an execution-environment detail, not
a theorem dependency. The exact producer reports Python 3.12.13 and SymPy
1.14.0 and regenerates output equal to the archived JSON byte for byte.

I independently reran the focused gate and certificate manifest. The main
agent supplied the final full-suite, i18n, and vinext records shown above
after the report fixes. The stale-translation count is a dictionary-
maintenance statistic, not a missing R0.70V page; this remains an internal
candidate and does not authorize publication.

## 3. Frame conventions and zero-mode ledger

The report consistently works on normalized

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad \int_{\mathbb T^3}1\,dx=1,
\]

with Fourier convention

\[
 \widehat f(n)=\int f(x)e^{-in\cdot x}\,dx,
 \qquad f(x)=\sum_n\widehat f(n)e^{in\cdot x}.
\]

The complete scalar frame includes the constant projector

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad \sum_\alpha T_\alpha^2=I.
\]

For nonzero modes the response is the unit vector

\[
 V(n)=\bigl(0,(\varphi(2^{-j}n))_{j\in\mathbb Z}\bigr)
 \in\ell^2.
\]

The report correctly retains the star block when the frame acts on
\(\omega\otimes\omega\). Although \(\Pi_0\omega=0\), deleting
\(T_\star^2(\omega\otimes\omega)\) from the product reconstruction would
destroy the zero Fourier coefficient. In the narrow-band proof the reference
response is explicitly extended by \(c_\star=0\), and mean zero gives
\(e_\star=0\).

## 4. Carré-du-champ and response-distance kernel

Writing

\[
 Q=\sum_\alpha T_\alpha\omega\otimes T_\alpha\omega,
 \qquad
 \mathcal D_\times=\omega\otimes\omega-Q,
\]

the two field identities

\[
 \mathcal D_\times
 =\sum_\alpha\left[
 T_\alpha^2(\omega\otimes\omega)
 -(T_\alpha\omega)\otimes(T_\alpha\omega)
 \right]
\]

and

\[
 \mathcal D_\times
 =\frac12\sum_\alpha\left[
 (T_\alpha^2\omega)\otimes\omega
 +\omega\otimes(T_\alpha^2\omega)
 -2(T_\alpha\omega)\otimes(T_\alpha\omega)
 \right]
\]

follow directly from complete-frame reconstruction. For \(L^2\) data, the
first two terms in the second display are interpreted through \(L^2\)
reconstruction, while

\[
 \sum_\alpha
 \|(T_\alpha\omega)\otimes(T_\alpha\omega)\|_{L^1(F)}
 =\|\omega\|_2^2.
\]

Thus the robust estimate

\[
 \|\mathcal D_\times\|_{L^1(F)}\le2\|\omega\|_2^2
\]

is correct and does not require a finite-mode assumption.

The Fourier kernel is

\[
 \widehat{\mathcal D_\times}(n)
 =\sum_{p+q=n}K(p,q)
   \widehat\omega(p)\otimes\widehat\omega(q),
\]

\[
 K(p,q)=1-\langle V(p),V(q)\rangle
 =\frac12\|V(p)-V(q)\|_{\ell^2}^2.
\]

The sign and factor \(1/2\) are correct. Real-evenness gives
\(V(-p)=V(p)\), hence \(K(p,-p)=0\) and

\[
 \widehat{\mathcal D_\times}(0)=0.
\]

Kernel nonnegativity is only scalar Fourier-pair positivity; the report
correctly does not infer that \(\mathcal D_\times(x)\) is pointwise positive
semidefinite.

## 5. Radial cancellation and the narrow-band theorem

For the radial response curve \(v(r)\), the derivative constant

\[
 M_\varphi
 =\sup_{r>0}\|\partial_{\log r}v(r)\|_{\ell^2}
\]

is finite because only uniformly finitely many annular indices are active.
The Hilbert-space fundamental theorem of calculus gives

\[
 K(p,q)
 \le\min\left\{2,
 \frac{M_\varphi^2}{2}
 \left|\log\frac{|p|}{|q|}\right|^2\right\}.
\]

Consequently, equal radii annihilate exactly, and a field supported on one
Laplacian sphere has \(\mathcal D_\times\equiv0\). The Taylor coefficient

\[
 K(re^h,r)
 =\frac{h^2}{2}\|\partial_{\log r}v(r)\|_{\ell^2}^2
 +O_\varphi(|h|^3)
\]

has the correct sign and factor. The shift identity
\(v(2r)_j=v(r)_{j-1}\) rules out an identically vanishing derivative.

For support in

\[
 \left|\log\frac{|n|}{\rho}\right|\le\delta,
\]

put \(c=v(\rho)\),
\(e_\alpha=(T_\alpha-c_\alpha I)\omega\), and
\(g=\sum_\alpha c_\alpha e_\alpha\). If

\[
 \beta=\sup_{n\in\operatorname{supp}\widehat\omega}
 \|V(n)-c\|_{\ell^2}\le M_\varphi\delta,
\]

then Plancherel and the unit-sphere identity give

\[
 \sum_\alpha\|e_\alpha\|_2^2
 \le\beta^2\|\omega\|_2^2,
 \qquad
 \|g\|_2\le\frac{\beta^2}{2}\|\omega\|_2.
\]

The exact expansion

\[
 \mathcal D_\times
 =-\omega\otimes g-g\otimes\omega
  -\sum_\alpha e_\alpha\otimes e_\alpha
\]

therefore yields

\[
 \|\mathcal D_\times\|_{L^1(F)}
 \le2M_\varphi^2\delta^2\|\omega\|_2^2.
\]

Combining this with the unconditional constant two gives exactly the stated

\[
 \min\{2,2M_\varphi^2\delta^2\}\|\omega\|_2^2.
\]

The proof is mode-count independent. It does not claim that Navier--Stokes
evolution preserves the radial band.

## 6. Exact-rank full-tensor obstruction

For

\[
 \omega=e_3[A\cos(Nx_1)+B\cos(4Nx_1)],
\]

the strict annular support makes the two response index sets disjoint. Thus

\[
 Q=e_3\otimes e_3
 \left[A^2\cos^2(Nx_1)+B^2\cos^2(4Nx_1)\right].
\]

If \(\cos(Nx_1)=0\), then \(\cos(4Nx_1)=1\), so the top eigenvalue is
strictly positive everywhere and the covariance has a global simple rank-one
top eigenspace. Hence \(r=\operatorname{tr}(PQP)=0\), while

\[
 \mathcal D_\times
 =AB[\cos(3Nx_1)+\cos(5Nx_1)]e_3\otimes e_3
\]

and normalized Fourier Parseval gives

\[
 \|\mathcal D_\times\|_{\dot H^{-1}_\#,F}^2
 =\frac{17A^2B^2}{225N^2}>0.
\]

This is an actual fixed-frame vorticity construction, not an abstract
covariance matrix. It rules out any full-tensor estimate by a positive power
of \(r\) whose prefactor is finite on this field and whose left side is a
definite tensor norm.

The Biot--Savart velocity is an \(e_2\)-directed shear. Its strain has only
\(12/21\) entries, whereas the defect has only a \(33\) entry. Therefore

\[
 S:\mathcal D_\times=0,
 \qquad \mathfrak X_\times=0.
\]

The example is consequently not a counterexample to a strain-projected or
signed square-root estimate.

## 7. Fourier strain adjoint and exact constants

With row-gradient convention \(B_{ij}=\partial_i u_j\), Biot--Savart gives

\[
 \widehat u(n)=\frac{i\,n\times\widehat\omega(n)}{|n|^2}
\]

and therefore

\[
 \widehat S(n)
 =-\frac12\left[
 \nu_n\otimes(\nu_n\times\widehat\omega(n))
 +(\nu_n\times\widehat\omega(n))\otimes\nu_n
 \right],
 \qquad \nu_n=\frac n{|n|}.
\]

For a real symmetric mean-zero tensor \(D\), full-lattice Parseval must use
the complex conjugate. The report does so:

\[
 \int S:D\,dx
 =\sum_{n\ne0}\widehat\omega(n)\cdot
  \overline{\nu_n\times\widehat D(n)\nu_n}.
\]

Thus strain sees only the transverse part of
\(\widehat D(n)\nu_n\). Weighted Hermitian Cauchy--Schwarz gives

\[
 \left|\int S:D\,dx\right|
 \le\|\nabla\omega\|_2\mathfrak X[D]^{1/2},
\]

where

\[
 \mathfrak X[D]
 =\sum_{n\ne0}|n|^{-2}
  |\nu_n\times\widehat D(n)\nu_n|^2.
\]

For symmetric \(D\), rotating \(\nu_n\) to \(e_1\) gives

\[
 |e_1\times De_1|^2=|D_{12}|^2+|D_{13}|^2
 \le\frac12|D|_F^2.
\]

The factor \(1/2\) relies on the full Frobenius norm, which counts each
off-diagonal entry twice. Hence

\[
 \mathfrak X[D]
 \le\frac12\|D\|_{\dot H^{-1}_\#,F}^2.
\]

The report correctly defines the homogeneous mean-zero norm. The same
constant would not be valid with an inhomogeneous Bessel weight under the
same notation.

Young's inequality is inserted with the correct constants:

\[
 |\mathfrak E_S|
 \le\frac\nu2\|\nabla\omega\|_2^2
  +\frac1{2\nu}\mathfrak X_\times
 \le\frac\nu2\|\nabla\omega\|_2^2
  +\frac1{4\nu}
   \|\mathcal D_\times\|_{\dot H^{-1}_\#,F}^2.
\]

The equality anchor proves sharpness on the ambient class of compatible
vorticity modes paired with arbitrary symmetric tensor modes. The report
explicitly does not claim sharpness inside the constrained subclass
\(D=\mathcal D_\times(\omega)\).

## 8. R0.70U saturation and response-area endpoints

On the inherited fixed R0.70U family,

\[
 \mathcal D_{\times,\varepsilon}
 =\varepsilon(1-\gamma)
  (w\otimes h+h\otimes w).
\]

The \(\pm k\) outputs alone give

\[
 X_0\ge
 \frac{\delta^2m^2}{2(m^2+1)^4}>0,
\]

so for fixed \(m\ge2\), \(A>\delta>0\), and \(|\gamma|\le3/4\),

\[
 \mathfrak X_{\times,\varepsilon}=\Theta(\varepsilon^2).
\]

The residual and signed-work orders are inherited from the locked R0.70U
theorem rather than recomputed by the R0.70V producer. The report now uses
\(\asymp\), not asymptotic-equivalence notation with an unintended unit
ratio.

For two unit response vectors,

\[
 d=1-\gamma,
 \qquad \kappa=1-\gamma^2=d(1+\gamma).
\]

The quotient identity

\[
 \frac d{\sqrt\kappa}
 =\sqrt{\frac{1-\gamma}{1+\gamma}}
\]

is correctly restricted to \(-1<\gamma<1\). Both endpoint branches are
separately recorded:

- at \(\gamma=1\), \(d=\kappa=0\), the pair defect vanishes, and the ratio
  is the undefined expression \(0/0\);
- at \(\gamma=-1\), \(d=2\) and \(\kappa=0\), so covariance area cannot
  control the response chord.

The anti-correlation condition \(1+\gamma\ge\sigma>0\) is therefore a real
hypothesis, not a consequence of real-evenness. A nonnegative cutoff is a
sufficient special case.

## 9. Triad-area identity and uniform response compensation

Let

\[
 n+k+l=0,
 \qquad n\cdot c=k\cdot a=l\cdot b=0,
\]

and put \(z=\nu_n\times c\). Direct contraction and the Lagrange identity
give the exact formula

\[
 S_c:(a\otimes b+b\otimes a)
 =\frac{[(l-k)\times z]\cdot(a\times b)}{|n|}.
\]

There is no missing factor two. Consequently,

\[
 |S_c:(a\otimes b+b\otimes a)|
 \le\frac{|k|+|l|}{|n|}|c|\,|a\times b|.
\]

For \(r=|k|\), \(s=|l|\), \(t=|k+l|\), and
\(h=|\log(r/s)|\), reverse triangle and elementary hyperbolic estimates give

\[
 t\ge|r-s|,
 \qquad \frac{r+s}{t}\le\coth(h/2)\le1+\frac2h.
\]

Together with

\[
 K(k,l)\le\min\{2,M_\varphi^2h^2/2\},
\]

this yields, for every nonzero triad,

\[
 K(k,l)\frac{|k|+|l|}{|k+l|}
 \le2+2M_\varphi.
\]

The equal-radius branch is exact because \(K=0\). Thus the pairwise-area
estimate has a uniform constant and is not merely a high-high asymptotic.

If \(1+\Gamma(k,l)\ge\sigma>0\), the \(\Gamma=1\) branch is trivial. On
the remaining branch,

\[
 \frac{K}{\sqrt\kappa}
 =\sqrt{\frac{K}{1+\Gamma}},
\]

and one may take

\[
 C_{\varphi,\sigma}
 =\frac{\sqrt2(1+M_\varphi)}{\sqrt\sigma}.
\]

This is a pair-by-pair estimate. It does not by itself sum Fourier modes,
shells, or physical-space covariance areas.

## 10. Scaling obstruction to the raw area comparator

The scale-free whole-space analogue of the initially tempting comparison

\[
 \mathfrak X_\times
 \lesssim\int(\lambda_1r+\lambda_2\lambda_3)\,dx
\]

is correctly rejected as scaling incompatible. For the homogeneous
whole-space analogue and a dyadic dilation \(\mu=2^J\), frame responses only
shift index. Since \(\omega\) has amplitude degree two and
\(\mathcal D_\times\) degree four,

\[
 \mathfrak X_\times[\omega_\mu]
 =\mu^3\mathfrak X_\times[\omega],
\]

while

\[
 \int_{\mathbb R^3}
 (\lambda_1r+\lambda_2\lambda_3)[\omega_\mu]\,dx
 =\mu^5\int_{\mathbb R^3}
 (\lambda_1r+\lambda_2\lambda_3)[\omega]\,dx.
\]

On the fixed torus, dyadic integer dilation gives degrees six and eight.
The two-degree mismatch is the same. Restriction to dyadic dilation is
essential for an exact pinned-frame scaling identity and is sufficient to
rule out a scale-free constant.

Accordingly, the next candidate must preserve two inverse-frequency degrees
or an exactly equivalent scale compensation. On the fixed torus, this
calculation is a scaling warning rather than a standalone impossibility
theorem because the lowest frequency supplies a scale. R0.70V now states
this distinction explicitly.

## 11. Machine certificate versus analytic proof

The finite SymPy producer directly checks:

1. the finite response-vector chord and wedge identities, including the two
   endpoint values \(\gamma=\pm1\);
2. the two-shell product-to-sum coefficients, homogeneous
   \(\dot H^{-1}\) value, null strain projection, and shear contraction;
3. the ambient symmetric-matrix Frobenius slack and simultaneous equality
   anchor;
4. the R0.70U defect factorization and strictly positive \(\pm k\) projected
   subtotal;
5. the divergence-free triad identity and the scaling-degree arithmetic;
6. the finite-channel narrow-band expansion and unit-sphere quadratic
   identity.

The focused test also requires raw stdout equality with `result.json`, locks
the exact endpoint payloads and inherited-order label, and verifies the
five-path SHA manifest.

The following remain analytic dependencies and are not falsely presented as
finite machine theorems:

- complete infinite-frame reconstruction and the \(L^2\)-to-\(L^1\)
  passage;
- the arbitrary-cutoff logarithmic Lipschitz estimate and Taylor expansion;
- the mode-count-independent narrow-band operator estimate;
- strict-annulus response separation and the global simple top gap in the
  two-shell field;
- the uncomputed nonnegative outputs in the R0.70U projected subtotal;
- extension of the finite Gram identity to the actual \(\ell^2\) response;
- the scalar proof of the uniform triad constants;
- dyadic covariance of the pinned frame under the scaling calculation;
- every vector-valued shell summation and every time-dependent PDE claim.

The certificate's hard-coded prose readings are treated as scope labels, not
as independent symbolic proofs. In particular, the R0.70U residual and
signed-work orders are explicitly marked as inherited.

## 12. Issues found and closed during audit

The review exposed and the final audited snapshot closes the following
points:

1. the chord-to-area quotient is no longer asserted at \(\gamma=\pm1\), and
   both singular endpoint branches are locked separately;
2. the malformed form-feed before `frac12` in the certificate README is
   removed;
3. \(c_\star=0\), \(e_\star=0\), and the definitions of \(L\), \(P\), and
   \(r\) are explicit;
4. critical-order comparison uses \(\asymp\), while exact \(\Theta\) orders
   are stated separately;
5. the inherited R0.70U premise \(m\ge2\), amplitude conditions, and source
   of the residual and signed-work orders are explicit;
6. the scale-free whole-space analogue of the raw covariance-area comparator
   is identified as two frequency degrees too strong;
7. exact frame scaling is restricted to dyadic dilations rather than an
   arbitrary continuous or non-dyadic integer dilation;
8. the test locks the new endpoint, inherited-scope, and scaling ledgers;
9. the radial variables in Section 9 no longer collide with the covariance
   residual \(r\), the filtered multiplier in the Yu comparison is defined,
   and the scaling no-go is explicitly restricted to the scale-free
   whole-space analogue.

No correction in this list is left open in the hashes recorded in Section 1.

## 13. Findings by severity

### Blocker

None.

### Major

None.

### Minor

None remaining in the audited snapshot. The report now says “dyadic integer
dilation,” uses distinct radial variables, defines the comparison filter
multiplier, and confines the scaling obstruction to its valid whole-space
scope.

## 14. Final boundary

R0.70V establishes a rigorous local harmonic-analysis advance:

- the complete-frame defect is exactly a response-distance quadratic form;
- same-radius interactions vanish and narrow radial bands have quadratic
  \(L^1\) smallness;
- covariance rank cannot control the full defect tensor;
- strain sees the smaller projected quantity \(\mathfrak X_\times\), with
  the correct critical viscosity ledger;
- response distance and divergence-free polarization area cancel the
  apparent low-output singularity one triad at a time;
- the scale-free whole-space analogue of the raw unweighted covariance-area
  comparator is ruled out by a two-degree scaling mismatch, while the torus
  statement is kept only as a scaling warning.

The remaining gate is an analytic, scale-correct vector-valued summation
with two inverse-frequency degrees retained. Until that gate is proved,
there is no bound of \(\mathfrak X_\times\) from energy-level data, no time
integrability, no enstrophy closure, and no Navier--Stokes regularity result.
