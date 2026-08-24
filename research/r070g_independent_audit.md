# R0.70G independent internal audit

> **Audit date:** 2026-08-24
>
> **Final status:** PASS after correction
>
> **Scope:** source definitions, critical-scale algebra, fixed-grid and
> active-only pressure tests, dissipation and small-data boundaries,
> primary-source attribution, certificate reproduction, and figure QA. This
> is an internal adversarial audit, not external peer review.

## 1. Audit disposition

The audit initially found two material scope errors and several precision
issues. All are retained in this record because each changes how the result
may be used.

| audit area | initial issue | correction | final status |
|---|---|---|---|
| source and harmonic-analysis boundary | physical annular differences were described too close to martingale/variation hypotheses | separated fixed-source, changing-filter, and moving-center operators; added cancellation, Fourier-decay, and regularity requirements | PASS |
| energy and square estimate | the deterministic coefficient estimate was called an energy-level square function | restricted the pointwise statement to an \(L^2\) source and the NSE conclusion to a Leray dissipation-level spacetime weighted coefficient estimate | PASS |
| small-data transfer | amplitude scaling and heat suppression were phrased too broadly at positive time | restricted exact \(\varepsilon\) and \(\varepsilon^3\) scaling to the initial face and attributed short-time sign continuity to standard classical local theory | PASS |
| critical transport and recurrence | possible coefficient or boundary-index errors | checked degree \(0,1,2\) factors, finite recurrences, and finite Abel identities with exact arithmetic | PASS |
| pressure-test geometry | possible confusion between a fixed signed source row and the changing diagonal, and an unstated carrier-transition plateau | defined target-normalized sequences with \(k(j)=j+M\), imposed fixed generator/carrier transition plateaus, and retained the fixed-\(k\) telescope boundary | PASS |
| figure and archive | possible numerical-evidence overstatement or untracked output | archived closed-form data, source, manifest, validation, vector outputs, and a 600 dpi PNG with an explicit non-simulation boundary | PASS |

The final PASS applies only to the corrected report and the payload hashes in
the R0.70G certificate.

## 2. Source-definition audit

For one fixed source/filter index,

\[
 E_{J,k}-E_{J-1,k}=K*(\psi_J\Omega_k)
\]

is an exact consequence of linearity. Replacing either occurrence of
\(\Omega_k\) by a different filtered source adds a filter/target difference
and is not a single-annulus identity.

The multiplication operators associated with smooth physical cutoffs are not
conditional expectations relative to nested sigma-algebras. Their products
\(\psi_j\Omega\) are also not Fourier-annular projections. Bounded physical
overlap still gives

\[
 \sum_j\|\psi_j\Omega\|_2^2\lesssim\|\Omega\|_2^2,
\]

but this is elementary quasi-orthogonality of supports, not martingale
conditional-zero-mean or frequency Littlewood--Paley cancellation.

The moving-center convolution operator belongs to a different theorem class.
Classical jump and variation results require cancellation and kernel
regularity/decay conditions and average over moving evaluation centers. They
do not produce one fixed exterior-source field harmonic on an entire core
ball.

## 3. Critical transport and recurrence audit

For a degree-\(n\) strain jet, critical normalization has length weight
\(r_j^{n+2}\). Therefore

\[
 h_j^{(n)}
 =c_j^{(n)}-\left(\frac{r_j}{r_{j-1}}\right)^{n+2}
                  c_{j-1}^{(n)}.
\]

On the dyadic grid, the transport factors are exactly

\[
 \frac14,\qquad\frac18,\qquad\frac1{16}
\]

for constant, linear, and quadratic jets. Ordinary coefficient-one
differencing omits the dilation defect.

For \(h_m=1\), \(c_0=0\), and \(0<\lambda<1\), exact solution of
\(c_m-\lambda c_{m-1}=1\) gives

\[
 c_m=\frac{1-\lambda^m}{1-\lambda},
 \qquad c_m-c_{m-1}=\lambda^{m-1}.
\]

Thus the raw \(\ell^1\) norm and square mass equal \(N\), while the ordinary
difference sums remain bounded. The report uses this only as a discrete
transport diagnosis; it does not identify ordinary differences with the
positive Navier--Stokes work.

For zero-extended finite sequences, the shift estimate

\[
 (1-\lambda)\|c\|_{\ell^p}
 \le\|(I-\lambda S)c\|_{\ell^p}
 \le(1+\lambda)\|c\|_{\ell^p}
\]

is valid for \(1\le p\le\infty\). The statement is a fixed-grid norm
equivalence and does not suppress a recurrent mean mode.

## 4. Signed telescope and dual-gap audit

Finite componentwise summation by parts gives

\[
 \sum_{j=a}^b(P_j-P_{j-1}):M_j
 =P_b:M_b-P_{a-1}:M_a
  +\sum_{j=a}^{b-1}P_j:(M_j-M_{j+1}).
\]

The index signs and endpoints were checked directly for eight finite
lengths. A fixed-\(k\) row with one signed core moment telescopes. Changing
the core scale, filter, cutoff, time interval, or moment leaves the final
variation term. Taking a positive part also prevents the signed identity from
being passed through term by term.

For bounded-overlap physical annuli, the kernel estimate

\[
 |D^nK|\lesssim r_j^{-3-n}
\]

gives

\[
 \sum_j r_j^{2n+3}|J_j^{(n)}(x_0)|^2
 \lesssim\|\Omega\|_2^2.
\]

This is a deterministic weighted coefficient estimate for an \(L^2\) source.
For a Leray solution it becomes a spacetime estimate through

\[
 \int_0^T\|\omega(t)\|_2^2\,dt\lesssim E_0/\nu.
\]

It is not a pointwise-in-time consequence of
\(\sup_t\|u(t)\|_2\). Estimating filtered vorticity only from that velocity
norm costs the additional factor \(\ell^{-1}\).

Cauchy--Schwarz would close the affine source/core pairing under

\[
 \sum_j\left(r_j^{-3}|M_j^{(0)}|^2+
             r_j^{-5}|M_j^{(1)}|^2\right)<\infty.
\]

R0.70G neither proves this condition nor claims it is necessary. It records
the exact dual scale weights and identifies the estimate missing from the
tested proof route.

## 5. Complete-grid and active-only pressure tests

The complete-grid test is a changing diagonal, not a fixed signed row. With
\(k(j)=j+M\), its observables use the target weights
\(r_{k(j)}^2\) and \(r_{k(j)}^3\), rather than the source-radius weights in
Section 4. The selected components are isolated spikes. Each spike has one
entry and one exit, giving

\[
 2N\Lambda^{-2},\quad 2N\Lambda^{-4},
 \qquad
 12N\Lambda^{-3},\quad 72N\Lambda^{-6}
\]

for the constant/linear adjacent \(\ell^1\) and square masses. The factors
were checked on eight finite chains. This test does not contradict fixed-\(k\)
signed telescoping.

For active-only reindexing, the constant tensors

\[
 A_0=\operatorname{diag}(1,-1/2,-1/2),\qquad
 A_1=\operatorname{diag}(1,-1/4,-3/4)
\]

have the same \(e_1\)-pairing, different spectra, and
\(\|A_1-A_0\|_F^2=1/8\). The harmonic cubics

\[
 \Phi_0=x_1^3-3x_1x_2^2,\qquad
 \Phi_1=x_1^3-\frac32x_1(x_2^2+x_3^2)
\]

have the same positive \(e_1\)-lobe pairing, coefficient-tensor norms
\(144\) and \(90\), and difference norm squared \(54\). The unequal
invariants rule out removal by orthogonal frame alignment.

Projecting either family to the paired scalar makes every adjacent difference
zero. The exact positive work still contains \(b_n^2\ge1\), so its sum grows
linearly while its adjacent variation is bounded. This proves a dichotomy for
the two specified observables. It is not a no-go theorem for every adaptive
algorithm; a hybrid method could add a separate mean-mode estimate.

## 6. Radial correction and compact-family boundary

One fixed partition is required to equal one on every filter-expanded
generator return transition and every filter-expanded nonconstant carrier
transition. Large scale separation makes those plateaus compatible and
independent of \(N\). For a carrier \(V_{r_m}\), this gives

\[
 (1-\psi_{k_m})\Omega_{\ell_{k_m+M}}[V_{r_m}]
 =a(|x|)e_1,
\]

with \(a\) constant in the inner core. If a radial scalar source equals
\(a_0\) in a center ball and
\(-\Delta F=a\), the regular radial solution there is

\[
 F=-a_0|x|^2/6+C.
\]

The induced velocity \(\nabla F\times e_1\) is a solid rotation and has zero
strain. Since the full carrier also has zero core strain, the selected
carrier-transition piece has zero strain. This handles the complement even
when the selected annular cutoff does not capture the full vorticity support.
The corrected argument retains every source.

Alternating among finitely many compact profiles preserves the uniform
\(L^2\cap BMO^{-1}\) estimates from R0.70F. A common small amplitude therefore
enters the Koch--Tataru small global \(X\) class. Exact tensor and cubic-work
amplitude scaling is asserted only on the initial face. No
\(N\)-independent positive persistence time or common interior terminal point
is supplied.

## 7. Primary-source and claim audit

The primary-source matrix was checked against Yu, Frazier--Jawerth,
Coifman--Meyer--Stein, Fefferman--Stein, Jones--Seeger--Wright, Dorronsoro,
Koch--Tataru, Eyink--Aluie, and Hamlington--Schumacher--Dahm.

The final attribution boundary is:

- Yu explicitly leaves the fixed-source harmonic route conditional and does
  not identify it with the moving-shell positive estimate.
- Frequency and variation theorems use convolution, cancellation, frequency
  localization, or moving-center structures absent from a generic physical
  cutoff product.
- The BMO--Carleson theorem supplies a framework; global \(L^2\) mass does not
  supply the required uniformly normalized local Carleson supremum.
- Koch--Tataru supplies uniqueness in the small \(X\) class, not an
  unrestricted weak-solution uniqueness theorem.

The literature conclusion is a bounded search result: no theorem matching all
features of the target was found in the audited primary sources. It is not a
proof that no such theorem exists.

## 8. Reproduction and figure QA

The exact producer reproduces the archived JSON with all Boolean checks true.
It verifies finite algebra, polynomial identities, tensor invariants,
square-function exponents, and recurrence factors. It does not computer-prove
smooth partition gluing, \(BMO^{-1}\) heat estimates, the literature search,
the missing core Carleson bound, or positive-time NSE persistence.

The figure package contains plotting source, three closed-form CSV data files,
manifest, validation, caption, figure contract, PDF, SVG, and 600 dpi PNG.
The PDF is one page at 178 by 86 mm. The PNG is 4204 by 2031 pixels with
embedded 600 dpi metadata. All eleven validation checks pass. Original-size
and grayscale inspection found no clipped labels or color-only distinctions.

The figure is an analytic comparator, not DNS, a trajectory, a numerical PDE
proof, a physical core-moment model, or evidence for a common-terminal-time
cascade.

## 9. Final claim boundary

R0.70G establishes an exact critical transport law, a deterministic
source-side weighted coefficient estimate, and finite initial-face pressure
tests. It eliminates automatic closure by ordinary adjacent differencing
alone.

It does not establish the dual core-moment estimate, positive double-scale
packing at one common terminal point, large-data regularity, singularity
formation, or a Millennium solution.
