# R0.70X independent mathematical audit

**Verdict:** **PASS** for the snapshot identified below. The final review has
zero blocker, zero major issue, and zero minor issue. R0.70X proves an exact
Laplacian-weighted cyclic triad identity, a sharp orbitwise
high--high--low \(t/R\) factor, and a complete-frame rank-at-most-one
counterexample to signed covariance-area control. It does not prove a
global critical cyclic multiplier estimate, an enstrophy closure, a
continuation theorem, global regularity, or any Millennium-problem
conclusion.

## 1. Audited snapshot

The audited branch is
`codex/r070x-signed-trilinear-gate`, based on commit

\[
 \mathtt{43e95f38d04e9bb6550479866d74c122d71a21c3}.
\]

The final uncommitted payload has the following SHA-256 digests:

- `research/r070x_report-source.md`:
  `86a34601de5a7095ce7ec1bd24eb7ef9c64491068770168d7dc00bf6e8fadcd3`;
- `research/r070x_exact_audit.py`:
  `6221305beacd79d0e85f091df234bc7e9cc6ec4418774a945be4fc2e399d62d1`;
- `research/r070x_literature_audit.md`:
  `17b4797968b1ba927062e74fefcfe037ca5a13626b2c08a67c01360217e1bbdd`;
- `tests/r070x-signed-triad-cyclic-gate.test.mjs`:
  `94740f078925bede6db09af738ec6f50944c4c1570b73e0b70c6b06ad5f3cf70`;
- `research/certificates/r070x/README.md`:
  `94963f8bbcec1566095947506b85b87668b905681039ca0dea5039c2197ea3d6`;
- `research/certificates/r070x/command.txt`:
  `37d3e4e2d95eef369a9a77982b5f66272e87c8940d6f5bb6d15c2780738f2d70`;
- `research/certificates/r070x/environment.txt`:
  `b12f7e0348bd2bf3ac010615540ddad8ee6fd06d6d318db200f69de87906adb7`;
- `research/certificates/r070x/result.json`:
  `dd975d69f352654fdee98a11c92337b354ffbe963d4559f52c7e1f768fd4422a`;
- `research/certificates/r070x/SHA256SUMS`:
  `d48980fd9f1dd115593a8639e2affb68a46e781429b9adfe8da70f7cd1d21114`.

The five-entry certificate manifest locks the README, command,
environment, archived result, and exact producer. The report, literature
audit, focused test, and this independent audit are recorded separately and
are not silently included in that five-path manifest.

## 2. Validation record

| Check | Result | Scope |
|---|---:|---|
| Focused R0.70X Node gate | **8/8 PASS** | Producer-byte equality, cyclic and counterexample ledgers, claim boundary, prose boundary, and certificate paths |
| Certificate SHA manifest | **5/5 PASS** | Every archived payload digest and relative path match |
| Full repository Node suite | **681/681 PASS** | Final repository-wide regression with the R0.70X gate |
| Direct i18n build | **PASS** | Translation extraction/build completed without an R0.70X regression |
| Direct vinext build | **5/5 PASS** | All five build stages completed |
| Independent mathematical reviews | **PASS / PASS / PASS** | Generic triad audit, independent exact Fourier audit, and multiplier/claim-boundary audit |

The producer reports Python 3.12.13 and SymPy 1.14.0. It regenerates the
archived JSON byte for byte. The calculation is finite exact algebra and
does not require a numerical simulation, a formal figure, or DGX compute.

The system shell has no `node` command. The pinned bundled Node runtime is
therefore used directly for the focused and full suites. This is an
execution-environment detail and not a mathematical dependency.

The first repository-wide invocation still allowed historical tests to find
the system `python3`; that interpreter was too old for `int.bit_count` and
lacked SymPy, NumPy, and GMPY2. Those failures were environment failures in
unchanged historical producers. Repeating the identical Node suite with the
repository's pinned Python 3.12 environment first in `PATH` gave the final
681/681 result above.

## 3. Ordered triad formula

For

\[
 n+p+q=0,
 \qquad
 n\cdot c=p\cdot a=q\cdot b=0,
\]

the strain symbol is

\[
 S_c(n)
 =-\frac1{2|n|^2}
 [n\otimes(n\times c)+(n\times c)\otimes n].
\]

The two Fourier factors of \(i\) cancel. With

\[
 A_n
 =\frac{[(q-p)\times(n\times c)]\cdot(a\times b)}{|n|^2},
\]

the exact ordered sum is

\[
 \mathfrak E_S
 =\frac12\sum_{n+p+q=0}K(p,q)A_n.
\]

The factor \(1/2\) is correct. It comes from contracting a symmetric strain
with the symmetric part of \(a\otimes b\). The negative triad is the complex
conjugate of the positive triad, so the complete sum is real without another
factor or an added real-part operation.

## 4. Cyclic square-weight null identity

The report proves

\[
 |n|^2A_n+|p|^2A_p+|q|^2A_q=0.
\]

The physical-space proof is correct. For divergence-free \(v\),

\[
 -\Delta S(v)=\operatorname{sym}\nabla(\nabla\times v),
\]

and integration by parts gives

\[
 \int(-\Delta S(v)):v\otimes v=0.
\]

The gradient part of \((v\cdot\nabla)v\) vanishes against
\(\nabla\times v\), and its cross-product part is pointwise orthogonal.
Polarization gives the three-leg identity. The producer independently
parameterizes a generic divergence-free Fourier triad and obtains zero
symbolic residual.

Writing \(B_n=|n|^2A_n\) and
\(\beta_n=K(p,q)/|n|^2\), the cyclic block is exactly

\[
 \beta_nB_n+\beta_pB_p+\beta_qB_q
 =(\beta_n-\beta_q)B_n+(\beta_p-\beta_q)B_p.
\]

Thus a common response slope cancels. This is the available null form; it
acts across all three strain placements.

## 5. High--high--low factor and sharpness

Let \(t=|n|<\min(|p|,|q|)/4\) and
\(R=\max(|p|,|q|)\). Strict annular support makes the two low--high
response factors equal to one. If \(Q=|q|=R\) and \(P=|p|\), cyclic
elimination gives

\[
 \mathcal G
 =\left[K(p,q)-\frac{t^2}{Q^2}\right]A_n
 +\left[1-\frac{P^2}{Q^2}\right]A_p.
\]

The response chord is quadratic in
\(|\log(P/Q)|\lesssim t/R\). The first coefficient is therefore
\(O_\varphi((t/R)^2)\), while \(A_n\) can have size \(R/t\). The second
coefficient is \(O(t/R)\), and \(A_p\) is order one. Hence

\[
 |\mathcal G|
 \le C_\varphi\frac tR
 (|c|\,|a\times b|+|a|\,|b\times c|).
\]

The sharp family has exact block

\[
 -\frac{1+M\kappa_M}{\sqrt{2M^2+2M+1}}.
\]

Its polarizations are unit size and its wedge amplitudes stay bounded away
from zero. Since \(\kappa_M\ge0\), the block is at least a constant times
\(M^{-1}\) in absolute value. This proves sharpness of one \(t/R\) power for
the orbitwise estimate. The report correctly does not call this a completed
global scale-locality theorem.

## 6. Complete-frame covariance geometry

For

\[
 k=(1,-1,1),
 \quad
 \psi=\cos(p\cdot x)+\cos(q\cdot x)+\cos((p+q)\cdot x),
 \quad
 w=k\times\nabla\psi,
\]

the exact checks give

\[
 \nabla\cdot w=0,
 \quad k\cdot w=0,
 \quad -\Delta w=2w,
 \quad \langle\psi^3\rangle=\frac32.
\]

Multiplication by the axial harmonics \(1,6,7\) produces the three squared
radii

\[
 5,
 \qquad110,
 \qquad149.
\]

The strict factor-four slacks are \(30\) and \(69\), so the low response is
orthogonal to both high responses. Every actual complete-frame block is a
scalar multiple of the same vector \(w(x)\). Consequently,

\[
 \operatorname{rank}Q\le1,
 \qquad
 \Omega_\alpha\times\Omega_\beta=0,
 \qquad
 G_Q=0.
\]

The wording `rank-at-most-one` is essential. The field has zeros and no
uniformly positive top covariance eigenvalue. The final report preserves
this limitation.

## 7. Frame defect and signed work

Let

\[
 \kappa=1-\Gamma(\sqrt{110},\sqrt{149})\ge0.
\]

The complete response Gram expansion gives

\[
 \mathcal D_\times
 =2(f_1f_6+f_1f_7+\kappa f_6f_7)w\otimes w.
\]

The strain contraction has the exact form

\[
 S(f_jw):w\otimes w=\frac{f_j'}{L_j}A(x),
 \qquad
 \langle A\rangle=\frac{81}{2}.
\]

The axial resonance \(1+6=7\) then gives

\[
 \boxed{
 \mathfrak E_S
 =-\frac{81(62+1639\kappa)}{32780}<0.}
\]

The independent Fourier route expands all thirty-six vorticity modes,
constructs the Biot--Savart strain and all ordered defect pairs, and evaluates

\[
 \sum_n\widehat S(n):\widehat{\mathcal D_\times}(-n).
\]

It returns the same symbolic rational expression with zero residual. The
ordered Fourier enumeration and the factor two in the physical unordered
shell-pair formula agree exactly.

## 8. Failure of the covariance-area candidate

The old candidate has zero right side on this field and nonzero left side.
The producer explicitly records the nonnegative-frame branch: choosing an
admissible nonnegative cutoff gives

\[
 \Gamma_{67}\ge0,
 \qquad0\le\kappa\le1,
 \qquad1+\Gamma\ge1.
\]

Thus response anti-correlation is not responsible for the failure. The
counterexample rules out any estimate that first forms the physical wedges
and then applies a definite norm or operator to them.

The example does not satisfy a uniform positive top-gap hypothesis. It does
not rule out a theorem whose domain is restricted by such a hypothesis and
which uses that hypothesis essentially.

## 9. Ambient bound and open multiplier gate

The report's all-mode estimate

\[
 |\mathfrak E_S|
 \le C_{\varphi,p_1,p_2,p_3}
 \prod_{j=1}^3\|\omega\|_{p_j}
\]

is valid independently of the unproved cyclic summation. If

\[
 A_\Omega=(\sum_\alpha|\Omega_\alpha|^2)^{1/2},
\]

then

\[
 |\mathfrak E_S|
 \le\int|S|(|\omega|^2+A_\Omega^2).
\]

Hölder, Riesz-transform boundedness, and the vector-valued
Littlewood--Paley inequality prove the claimed range. This returns only a
separate-input cubic estimate.

The revised report does not attempt to factor the nonzero work through the
zero physical fields \(\Omega_\alpha\times\Omega_\beta\). It instead records
a pre-convolution pair-frequency chord object and leaves its critical
three-leg summation open. This is consistent with the counterexample.

## 10. Prior art and claim boundary

The literature audit correctly distinguishes the present observable from
classical helical-triad conservation, counterbalanced nonlocal transfer,
conditional kinetic-energy scale locality, and standard paraproduct theory.
The report does not claim the first cyclic conservation law or the first
\(t/R\) locality factor. It does not infer a global multiplier theorem from
the single-orbit estimate.

During review, four issues were identified and repaired before the final
snapshot:

1. the missing displayed plus sign in the exact far-triad identity;
2. an impossible schematic factorization through physical wedges that
   vanish in the counterexample;
3. ambiguity between rank one everywhere and rank at most one; and
4. explicit scoping of nonzero triad frequencies and the nonnegative-frame
   response guard.

The repaired snapshot has no remaining mathematical or claim-boundary
issue.

No publication, public-page update, DNS claim, or regularity claim follows
from this audit.
