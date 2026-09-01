# R0.74K independent inward-tail analytic audit

## Verdict and binding

**Overall verdict:** PASS AFTER TWO LOCAL STATEMENT REPAIRS
**Central analytic verdict:** SINGLE-INWARD-COLLAR REDUCTION VALID
**Open-gate verdict:** TRUE-PACKET BRIDGE/SHEAR-LAG ESTIMATE REMAINS OPEN
**Clay status:** NOT CLAY

Bound source:

- research/r074k_single_collar_shear_lag_reduction.md
- SHA-256
  20f5c41db46ecb8994a095778106eca0c6a5b2620fb8df85022eba53fd93f72f

Inherited analytic sources used here are R0.74E (4.12b)--(4.12d), R0.74F
(1.8)--(1.9), (3.16), (3.20), and (4.1), R0.74G (4.7)--(4.16), and
R0.74H (2.1)--(2.7), (7.1a)--(7.2).  Both finite scripts independently
return PASS 41/41; that finite result is not used as a substitute for the
analytic checks below.

The four principal results have the correct scale and implication.  Two local
repairs are required: Proposition 2.1 must restrict the physical shell index
to \(2\le m\le j-1\), and Proposition 2.2 must thicken its displayed slice
before calling the obstruction positive-volume.  Lemma 3.2 is valid, but its
phrase “uniformly in the upper time endpoint” should display the corresponding
truncated interval.

## 1. Proposition 2.1

**Verdict:** PASS WITH SHELL-INDEX REPAIR.

For

\[
 d_m=c_h-\frac{2^{1-m}}{\lambda},
 \qquad G_m=c_\gamma(1-4^{-m}),
\]

\(d_m\) is increasing and \(G_m<c_\gamma\).  Hence, for every \(m\ge2\),

\[
 \frac{d_m^2}{132}-G_m
 >\frac1{132}\left(\frac{689}{1008}\right)^2-\frac8{3969}
 =\frac{204385}{134120448}>0.
\]

Thus source (2.2)--(2.4) is correct.  The actual \(m=2\) margin is

\[
 \frac{d_2^2}{132}-G_2
 =\frac{221281}{134120448}>0.
\]

The coarse comparisons are also correct:

\[
 \frac{d_2^2}{262}-G_2
 =-\frac{28319}{266208768}<0,
 \qquad
 \frac{d_3^2}{262}-G_3
 =\frac{139297}{266208768}>0.
\]

When the statement refers to actual annuli \(A_{j-m}(R_j)\), the frozen
ledger starts at shell index \(1\).  Its physical quantifier should therefore
be

\[
 \boxed{\text{all sufficiently large }j,\qquad 2\le m\le j-1.}
\]

The unrestricted \(m\ge2\) assertion remains a true numerical inequality,
but annuli with \(j-m\le0\) are not members of the frozen endpoint ledger.
This repair changes no exponent or conclusion.

## 2. Proposition 2.2

**Exact-arithmetic verdict:** PASS.
**Positive-volume proof as written:** INCOMPLETE BUT LOCALLY REPAIRABLE.

With \(\varepsilon=1/128\), the source correctly obtains

\[
 \lambda^{-1}-\varepsilon=\frac{4033}{8064},
 \qquad
 d_{1,\varepsilon}=\frac{3527}{8064},
\]

\[
 \lambda^{-2}-(\lambda^{-1}-\varepsilon)^2
 =\frac{8129}{1032192}>0,
\]

and

\[
 G_1-\frac{d_{1,\varepsilon}^2}{132}
 =\frac{536399}{8583708672}>0.
\]

Consequently a free squared-kernel replacement leaves the exponentially
wrong factor in source (2.11).  This is only a no-go for that replacement;
it is not a lower bound for the true packet and not a counterexample to the
desired upper estimate.  Source (2.12) and the following OPEN discussion
respect this distinction.

The proof fixes one value of \(x_3\) and then exhibits a nonzero
\(x_1\)-chord.  A single \(x_3\)-slice still has three-dimensional measure
zero, so that alone does not prove the words “on positive volume.”  The
repair is immediate.  Put

\[
 \eta=\lambda^{-1}-\varepsilon,\qquad 0<\delta<\varepsilon,
\]

and restrict to the one-sided slab

\[
 \eta r_j\le x_3\le(\eta+\delta)r_j.
\]

For sufficiently small fixed \(\delta\), choose \(c_*>0\) with

\[
 2c_*^2<\lambda^{-2}-(\eta+\delta)^2.
\]

Then \(|x_1|,|x_2|<c_*r_j\) gives a genuine positive-volume box inside
\(A_{j-1}(R_j)\).  Moreover
\(c_h-x_3/r_j\le d_{1,\varepsilon}\), so throughout this one-sided slab the
wrong-sign margin is at least (2.10).  If a lower box for the derivative
reference kernel is desired, one may further restrict \(x_2-Q_j(t)\) to a
fixed \(R_j\)-window away from its zero; this costs only a polynomial volume
factor.  The proposition survives, but its current positive-volume sentence
needs this thickening argument.

## 3. Lemma 3.1

**Verdict:** PASS.

R0.74E (4.12b)--(4.12c) and R0.74H (2.1)--(2.2) give two radial transition
collars, each of thickness \(O(R_j)\), radii comparable with
\(2^jR_j\asymp L_jR_j\), and
\(|\nabla\psi_j^{R_j}|\le C/R_j\).  At fixed \(x_3\), the planar area of
each transition collar is at most

\[
 C(L_jR_j)R_j.
\]

Fubini and the derivative bound therefore give, uniformly through spherical
tangencies,

\[
 \sup_{x_3}\int_{\mathbb R}M_j(x_2,x_3)\,dx_2
 =\sup_{x_3}\int_{\mathbb R^2}
   |\partial_2\psi_j^{R_j}|\,dx_1dx_2
 \le CL_jR_j.
\]

The integrated planar area has no hidden square-root chord singularity.  No
periodic copy is missing: this is the nonperiodized lift-side cutoff, while
R0.74H (2.3)--(2.7) supplies the exact unfolding to its periodization.

## 4. Lemma 3.2 and the periodic-kernel moments

**Verdict:** PASS WITH DISPLAYED-QUANTIFIER CLARIFICATION.

On \(I_{2R_j}=(61R_j^2,65R_j^2)\), \(T=R_j^2+t\) obeys
\(T/R_j^2\in[62,66]\).  If \(d_{\mathbb T}\) denotes circular distance, the
all-copy periodic Gaussian bounds imply, uniformly for that compact heat-age
interval,

\[
 \sup_{T/R_j^2\in[62,66]}K_T(x)
 \le CR_j^{-1}e^{-c d_{\mathbb T}(x,0)^2/R_j^2}
      +CR_j^{-1}e^{-c/R_j^2},
\]

\[
 \sup_{T/R_j^2\in[62,66]}|\partial K_T(x)|
 \le CR_j^{-2}
      \left(1+\frac{d_{\mathbb T}(x,0)}{R_j}\right)
      e^{-c d_{\mathbb T}(x,0)^2/R_j^2}
      +CR_j^{-2}e^{-c/R_j^2}.
\]

Squaring and integrating proves exactly the powers in source (3.7):

\[
 \int_{\mathbb T}\sup_TK_T^2\le CR_j^{-1},
 \qquad
 \int_{\mathbb T}\sup_T|\partial K_T|^2\le CR_j^{-3}.
\]

The supremum is correctly inside the integral, and all noncentral periodic
images are included.

R0.74F (1.8)--(1.9) and R0.74G (4.12)--(4.14) give

\[
 Q_j'(t)=B_j\theta_j(t,h_j)\ge\frac34B_j,
 \qquad B_j^{-1}\le128R_j^2
\]

for all sufficiently large \(j\).  The path stays in the central arc
\([-1/2,q_j]\), so the monotone change \(t\mapsto Q_j(t)\) has no wrap or
multiplicity.  Extending its image to one torus period, then applying Lemma
3.1 and the two moments above, gives

\[
 R_j^6R_j^{-1}R_j^{-3}\frac{L_jR_j}{B_j}
 =\frac{L_jR_j^3}{B_j}
 \le128L_jR_j^5.
\]

Thus source (3.6)--(3.8) has the correct powers and constant quantifiers.  The
displayed bound over all of \(I_{2R_j}\) is stronger than every truncated
bound, but the phrase “uniformly in the upper time endpoint” contains no
endpoint variable.  For exact alignment with the collar observable it should
read, for every \(\tau\in I_{R_j}\),

\[
 \Gamma_j\int_{I_{2R_j}\cap(-\infty,\tau]}
 \int_{\mathbb R^3}|F_{\rm fr}|^2
 |\partial_2\psi_j^{R_j}|\,dx\,dt
 \le C\Gamma_jL_jR_j^5.
\]

This follows from (3.6) because the integrand is nonnegative.  Lemma 3.2
remains a reference-packet estimate; it does not license the same change of
variables after \(Q_j(t)\) is replaced by
\(Q_j(t)-\mathfrak S_t^y\).

## 5. OPEN boundary

**Verdict:** PASS WITH ONE LABEL CLARIFICATION.

The source correctly records that:

1. R0.74F (3.16), (3.20), and (4.1) apply only for \(|y|\le R_j\), not the
   inward scale \(|y|\asymp L_jR_j\);
2. R0.74G (4.10) gives the normalized \(p=2,3\) bridge inequality, while
   (4.13) gives only \(\mathfrak S_t^y\ge-\delta_j\), not the required
   positive inward-bridge displacement;
3. the Peetre reduction after R0.74G (4.22) separates \(y\) from
   \(\mathfrak S_t^y\) and therefore cannot repair Proposition 2.2;
4. Lemma 3.2 controls only the constant-shear reference packet; the true
   target collar still needs a time-coupled bridge--BV estimate; and
5. source hypothesis (4.3), both matching observable uppers, every universal
   endpoint theorem, and every global regularity or singularity conclusion
   remain OPEN.

Section 6 item 1 calls (4.3) “the joint inward-bridge/shear-expulsion
estimate.”  Equation (4.3) is actually the complete conditional signed collar
estimate: source lines 352--366 and 472--477 show that it also contains the
distinct main-collar bridge--BV problem.  The label should be changed to
“the conditional signed collar estimate (4.3), including the main-collar
bridge--BV and nearest-inner shear-expulsion sublemmas.”

Likewise, statements that the next proof “must” use positive shear expulsion
should be read as applying to the selected normalized-bridge route.  The
finite wrong-sign comparison rules out the free-heat replacement, but it
does not rule out every possible proof based on signed cross-collar
cancellation or another correlation-preserving formulation.

Subject to these local repairs, the route reduction is valid and its OPEN
boundary is conservative.  It proves neither (4.3) nor a matching upper bound
for \(X_j\) or \(\mathfrak C_j\).

## Addendum — repaired-source rebind

This addendum supersedes the original bound-source hash for the current
verdict.  It audits only the four repairs requested after the first pass.

- previous source SHA-256:
  20f5c41db46ecb8994a095778106eca0c6a5b2620fb8df85022eba53fd93f72f;
- repaired source SHA-256:
  8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3.

### Repair checks

1. **Proposition 2.1 — PASS.**  Source lines 125--156 now quantify over all
   sufficiently large \(j\) and \(2\le m\le j-1\), while separately recording
   that the algebraic inequality holds for every integer \(m\ge2\).  This
   exactly separates the physical ledger range from the unrestricted numerical
   comparison.

2. **Proposition 2.2 — PASS.**  Source lines 218--248 now take
   \[
   \eta=\frac{4033}{8064},\qquad
   \delta=\frac1{256},\qquad c_*=\frac1{64}.
   \]
   The displayed box has normalized volume
   \[
   4c_*^2\delta=\frac1{262144}>0.
   \]
   Its exact outer-shell containment margin is
   \[
   \lambda^{-2}-(\eta+\delta)^2-2c_*^2
   =\frac{14305}{4128768}>0,
   \]
   while its inner-shell margin is
   \[
   \eta-\frac1{2\lambda}
   =\eta-\frac{16}{63}
   =\frac{1985}{8064}>0.
   \]
   Hence the whole box lies in \(A_{j-1}(R_j)\).  On its one-sided
   \(x_3\)-thickening,
   \(c_h-x_3/r_j\le d_{1,\varepsilon}\), so the squared free-tail decay is no
   stronger than at the audited slice and the wrong-sign margin remains at
   least (2.10).  The former measure-zero gap is fully repaired.

3. **Lemma 3.2 — PASS.**  Source lines 349--384 now state the estimate for
   every \(\tau\in I_{R_j}\) over
   \(I_{2R_j}\cap(-\infty,\tau]\), and explicitly reduce it to the full
   nonnegative \(I_{2R_j}\) integral.  The already-audited periodic
   \(\sup_T\) moments and \(t\mapsto Q_j(t)\) calculation therefore apply
   without a hidden endpoint quantifier.

4. **Route wording and OPEN boundary — PASS.**  Source lines 506--515 limit
   the “must” language to the selected normalized-bridge route.  Source lines
   543--560 distinguish the proved reference-packet result from the OPEN
   conditional signed collar estimate and list its main-collar bridge--BV and
   nearest-inner shear-expulsion sublemmas separately.

**Final repaired-source verdict:** R074K_INWARD_TAIL_ANALYTIC_AUDIT_PASS.

The repairs change no proved exponent, scale, or implication.  The true-packet
estimate (4.3), the matching upper bounds, every universal endpoint claim,
and every Clay-problem conclusion remain OPEN or NOT CLAIMED exactly as
stated.
