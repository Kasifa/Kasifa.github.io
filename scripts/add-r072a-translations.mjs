import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const source = await collectSiteStrings(publicDirectory);
const current = JSON.parse(await readFile(translationPath, "utf8"));

const translationRows = String.raw`
001 ||| : the frozen target is \(J_1(2\tau)\); a growing-window \(C^1\) comparison preserves selectable positive roots near the first \(R\) zeros and gives selected row mass \((8/\pi^2)\log R+O(1)\). The launch root contributes another 1, and any other exact roots not excluded here can only increase the complete nonnegative mass; the page does not claim that the selected roots exhaust the complete root set.
002 ||| show that fixed nonconstant profiles typically produce enhanced dissipation at large coupling, with quantitative rates depending on critical-point degeneracy and sublevel control. These results control the semigroup norm at the observation time; they do not directly control coordinate zeros or slope mass accumulated earlier, and they do not automatically cover uniformly the heat-decaying profile that varies with \(M\) in this section. For the frozen \(2\cos\theta\) comparison, the rate is \(R^2/(\log R)^2\), whereas the layer here is \(O(R^{-3})\), so this family lies before the comparison time; this remains only an autonomous frozen-profile comparison. The bounded search does not support a claim of originality, priority, or a general NSE conclusion.
003 ||| Open the complete 91-note index
004 ||| Test whether the one-carrier logarithmic root mass extends to a growing carrier count while also paying the \(M^{-2}\) lattice cost, the complete rotational charge, and the enhanced-dissipation comparison.
005 ||| Open interface · R0.72B
006 ||| cumulative recap and 91-note index
007 ||| The actual observation-layer quantity \(\ell_2(I)\) changes the sufficient decay region to \(\alpha<\min\{3/2,(6+3\beta)/7\}\). A finite-support launch may take \(A_0=0\); an exact one-carrier family also gives \(G_R^{\rm sel}=(8/\pi^2)\log R+O(1)\). These are an upper bound and a narrow lower obstruction, not normalized nonlinear divergence.
008 ||| Literature review v1.13 · 2026-08-27
009 ||| Published theorems are listed as established results, 2026 preprints are marked separately, and this site's R0.69P–R0.72A material is classified only as research notes. Calculations and notes are not extrapolated into regularity theorems.
010 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U gives the conditional-incidence, genuine-internal-entry, second-time-jet, and finite-recurrence boundaries. R0.71V–W separates the fixed zero-level trace and rules out the data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint inside a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation; R0.72A further localizes the strong-coupling loss to the actual observation layer, closes finite-support exact launch, and uses an exact Bessel family to prove that selected row mass can grow at least logarithmically. General Navier–Stokes regularity remains open.
011 ||| DLMF on Jacobi–Anger expansions, Bessel zeros, and derivative asymptotics
012 ||| local exposure, exact launch, and the Bessel obstruction
013 ||| The lower side uses
014 ||| R0.72A retains the quadratic-multiplier exposure on the actual observation interval and obtains \(G_{\rm all}^{\rm ex}(I)\le e^{2\lambda_0L}M\Omega^2[1+q_I+\eta\ell_2(I)]\). For \(\eta=M^\alpha\) and \(L=M^{-\beta}\), the current complete normalized upper bound tends to zero when \(\alpha<\min\{3/2,(6+3\beta)/7\}\). Finite-support vectors permit exact launch, and the payment window coincides completely with the counted window only when \(A=A_0=0\).
015 ||| Primary and official source boundary for R0.72A
016 ||| How R0.72A connects to the Bessel and enhanced-dissipation literature
017 ||| \(\beta=0\) recovers \(6/7\) for a fixed layer. If the layer shrinks fast enough that \(\eta L=O(1)\), the sufficient region reaches every \(\alpha<3/2\). The equality line only marks where the current upper bound no longer guarantees decay; it proves no sharpness, singularity, or normalized lower bound.
018 ||| \(\tau=0\) remains an exact launch root with row mass 1; any other roots not excluded here can only increase the nonnegative complete mass. Therefore
019 ||| 02 · Local exposure
020 ||| 04 · Strong-coupling phase diagram
021 ||| 07 · Double certificate
022 ||| 08 · Formal figure
023 ||| 11 · Claim boundary
024 ||| treating the fixed-layer \(6/7\) as the threshold for every shrinking layer; deleting all strong-coupling dependence; conflating exact launch with an arbitrary positive pre-observation layer.
025 ||| Version v0.72A · 2026-08-27
026 ||| If and only if this section's exact-launch specialization \(A=A_0=0\) holds, \(K_t=I_t=[a,b]\). The launch enstrophy then cancels the contrast factor inside the original counting window, with no matched background or separate retention hypothesis.
027 ||| 's fixed-profile theory shows that a large imaginary shear potential typically produces enhanced dissipation at positive times. Those results control the semigroup norm at the observation time; they do not directly control coordinate zeros or slope mass accumulated earlier.
028 ||| First, R0.71Z's global heat-tail loss is not the true cost on a short layer; local exposure gives a larger rigorous exclusion region. Second, the \(A_0=0\) endpoint for finite-support launch enters the BV proof directly and yields floor cancellation in the same counting window. Third, the exact Bessel family proves that coupling dependence is not merely an artifact of the estimate.
029 ||| For \(g=e^{\lambda_0(x-A)}F_0\), the BV zero lemma gives \(\sum|g'(\tau)|^2\le|g'(\tau_1)|^2+\|g'\|_\infty\int|g''|\). Exact contraction pays \(\|g'\|_\infty\), while \(QF\) and \(V_z^2F\) give \(q_I\) and \(\eta\ell_2(I)\), respectively. The complete zero set is handled by the monotone supremum over finite subsets.
030 ||| For the frozen \(b(\theta)=2\cos\theta\) comparison, \(\lambda_{\rm ED,R}\asymp R^2/(\log R)^2\), while \(L_R\asymp R^{-3}\), so \(L_R\lambda_{\rm ED,R}\to0\). This is only an autonomous frozen-profile comparison, not a theorem for the current nonautonomous heat-decaying system. R0.72B must record profile degeneracy, sublevel constants, freezing error, and the enhanced-dissipation scale together.
031 ||| Its value for the Millennium problem remains indirect: it rules out one coarse strong-coupling scenario inside the declared triangular 2.5D class and shows that any later construction must overcome the \(M^{-2}\) lattice cost, enhanced dissipation, and full nonlinear charge payment simultaneously. It does not constrain general three-dimensional vortex-stretching geometry.
032 ||| The setting remains real shear, a fixed target, and a triangular Fourier lattice
033 ||| The fixed-layer \(6/7\) is not the final upper boundary for a shrinking layer, but \(3/2\) is still only the envelope of a sufficient condition
034 ||| A shorter observation layer strengthens the upper bound;
035 ||| Dissipation
036 ||| The analytic proof and two distinct numerical paths serve different roles
037 ||| Local exposure
038 ||| Set \(\nu=d=q=K_z=z_1=r_1=1\), \(K_y=0\), and \(F(0)=ie_{-1}\), and let \(\delta_R=R^4\) and \(U_R(\tau)=F(\tau/\delta_R)\). The frozen system's target coordinate is
039 ||| If \(\eta_M=M^\alpha\), \(L_M=M^{-\beta}\), and \(\lambda_{0,M}L_M\) is uniformly bounded, then a sufficient condition for the right-hand side to tend to zero is
040 ||| If a unified upper bound still forces the many-carrier structure to zero, record it as an exclusion theorem; if a nonvanishing candidate appears, exact roots and an independent certificate are still required before it enters a public conclusion.
041 ||| Real shear makes \(V_z\) skew-adjoint and \(D_q\) self-adjoint nonpositive, so \(\|F(x)\|_2\le\sqrt M\). If \(\Omega=0\), \(\delta=0\), or the shear amplitude \(S=0\), the target charge vanishes; only the nontrivial branch is considered below.
042 ||| Figure R0.72A-1. A: the certified sufficient region for \(\eta=M^\alpha\) and \(L=M^{-\beta}\). B: two finite certificates and the frozen Bessel sum; equality corresponds only to the selected positive roots. C: the observation layer \(L_R=O(R^{-3})\) and the physical root displacement obtained by dividing the \(\tau\)-displacement by \(\delta_R\), namely \(O(R^{-6})\); both curves use the \(x\)-coordinate. The figure summarizes evidence and does not replace the analytic proof.
043 ||| Next object: many carriers / full nonlinear charge
044 ||| The next section retains the exact local-exposure ledger and first attempts to lift the logarithmic one-carrier family to a many-carrier sequence with growing \(M\); every candidate must report complete slope mass, \(M^{-2}\) suppression, full nonlinear rotational charge, freezing error, and a uniform enhanced-dissipation comparison together.
045 ||| Phase diagram
046 ||| a converse to the phase diagram, normalized nonlinear divergence, a continuation criterion, finite-time singularity, global regularity, or a conclusion about originality or priority.
047 ||| The phase diagram, logarithmic Bessel mass, and physical shrinking scales are shown separately
048 ||| Research note R0.72A · LOCAL EXPOSURE · EXACT LAUNCH · BESSEL ROOTS
049 ||| Research note R0.72A: within the declared real-shear triangular Fourier-lattice class, the all-root upper bound is localized to the actual observation layer, the exact-launch endpoint is closed, and an exact Bessel obstruction with logarithmic selected-root mass is constructed; this is not a general three-dimensional regularity theorem.
050 ||| One local squared integral and one local target-row payment retain all required information
051 ||| A finite-carrier launch belongs to every diagonal graph domain, and finite shifts preserve these domains. Hence \(g'=e^{\lambda_0(x-A)}F_0'\) is absolutely continuous and \(g''\in L^1\), including at exact launch with \(A_0=0\).
052 ||| On \(T_R=j_{1,R}/2+\rho=O(R)\), the \(C^1\) error between the exact and frozen targets is \(O(R^{-1})\), smaller than the weakest Bessel slope \(R^{-1/2}\). Thus one simple positive exact root can be selected near each of the first \(R\) Bessel zeros, and \(L_R=T_R/R^4=O(R^{-3})\).
053 ||| This does not extend to arbitrary delayed observation. An arbitrarily short positive pre-observation layer can still lose order-one launch enstrophy through high-frequency heat shear; the exact endpoint must not be conflated with a uniform positive-layer statement as \(A_0\downarrow0\).
054 ||| Here \(G_R^{\rm sel}\) is the mass of the rescaled-time row \(h=P_0VF\), without division by \(\Omega^2\). The original \(x\)-derivative is \(\delta_R h\). This family has only \(M=1\); it does not prove divergence of the normalized nonlinear ledger and does not saturate the \(O(1+\eta L)\) upper bound.
055 ||| This is the local-exposure version of R0.71Z's complete all-root theorem. It still does not count raw roots or require a minimum gap; the improvement comes from no longer replacing a short observation layer by the entire future half-line.
056 ||| This section turns the strong-coupling interface from a vague threshold into a testable two-scale problem
057 ||| The proof, literature boundary, double certificate, and journal-figure package are all retained
058 ||| Direct conclusion
059 ||| Launch cancellation can be written in the same window only when observation starts at the reference layer
060 ||| Status · R0.72A completed
061 ||| Bessel roots still leave logarithmic mass
062 ||| complex bilateral lattice; roots bracketed near Bessel zeros; \(R=4,8,16,32,64\); truncation doubling also performed. Selected masses increase from 1.3469595614 to 3.5652919858.
063 ||| Local exposure turns the complete normalized ledger into a two-scale condition
064 ||| sharpness of the local upper loss; a many-carrier exact lower family; full nonlinear charge; uniform nonautonomous enhanced dissipation; nontriangular three-dimensional feedback.
065 ||| a local-exposure complete all-root upper theorem; the finite-support exact-launch endpoint; a two-scale sufficient decay region; logarithmic asymptotics of the one-carrier selected Bessel mass and a lower bound for complete mass.
066 ||| In this section the normalized ledger specifically takes \(I_x=[A_0,A_0+L]\); the physical-time payment interval is
067 ||| A one-carrier infinite lattice already rules out an eta-independent complete constant
068 ||| producer / independent certificates
069 ||| The producer uses a right margin of 0.35 and the independent path uses 0.30; both verify the same first \(R\) selected roots and masses without taking the layer endpoint as identical input. Both JSON files, commands, environments, progress logs, and SHA-256 checksums are archived. The finite matrix only corroborates the infinite-lattice analytic argument; it is neither DNS nor an interval proof.
070 ||| R0.71Z's strong-coupling loss used the entire future heat tail. This section retains the quadratic exposure on the actual observation layer and changes the complete all-root upper bound to \(1+q_I+\eta\ell_2(I)\). For \(\eta=M^\alpha\) and \(L=M^{-\beta}\), the sufficient decay region becomes \(\alpha<\min\{3/2,(6+3\beta)/7\}\); exact launch also makes the payment and counting intervals coincide. On the other side, inside an \(O(R^{-3})\) layer, an exact one-carrier infinite lattice preserves \(R\) selectable positive roots with rescaled row mass \((8/\pi^2)\log R+O(1)\). Thus the coupling loss can be localized but cannot be deleted entirely.
071 ||| R0.72A · 2026-08-27 · Personal mathematics research log
072 ||| R0.72A | Local-exposure strong-coupling closure and the exact Bessel obstruction
073 ||| R0.72B tests whether many-carrier Bessel amplification can enter the complete nonlinear charge
074 ||| real invariant phase; fixed step 0.004; no producer import; roots found from unseeded sign changes and refined by cubic Hermite interpolation. On shared \(R\) values, mass differences are below \(4\times10^{-10}\) and root differences are below \(4\times10^{-9}\).
075 ||| A shrinking layer expands the sufficient decay region from alpha<6/7 to alpha<3/2; an exact one-carrier family still has logarithmic selected-root mass.
076 ||| A shrinking layer can remove the \(\eta L\) portion but cannot remove the first-root term. The phase diagram gives a sufficient region where the upper bound still tends to zero, not a converse theorem asserting counterexamples outside it.
077 ||| Strong coupling is not an independent escape parameter
078 ||| 01 · Eighteen research phases
079 ||| 02 · Complete 91-note index
080 ||| Open the latest node, R0.72A
081 ||| A complementary exact nearest-neighbor construction follows the frozen Bessel flow with \(\delta_R=R^4\) and \(L_R=O(R^{-3})\), preserves one simple exact root near each of the first \(R\) simple Bessel zeros, and gives selected rescaled target-row mass \((8/\pi^2)\log R+O(1)\); the corresponding physical \(x\)-derivative mass carries an additional factor \(\delta_R^2\). This rules out an \(\eta\)-independent all-root constant for the rescaled target row; it proves neither divergence of the normalized nonlinear ledger nor a general NSE conclusion.
082 ||| Recap endpoint: R0.72A
083 ||| Public notes at the recap endpoint: 151
084 ||| Through R0.72A, there is no new unconditional continuation criterion, no reduction of the set of all potential singular solutions, and no proof of finite-time breakdown. The 91 nodes cannot be interpreted as completing some percentage of the Millennium problem.
085 ||| Local exposure closes one strong-coupling region, while the Bessel construction marks an obstruction on the other side; the general problem remains open
086 ||| Cumulative recap · R0.61–R0.72A · 2026-08-27
087 ||| Eighteen phases and 91 nodes: from reduced recurrences and the dynamic route after R0.70A to the fixed-zero ledger, the family-internal one-third endpoint, bounded-coupling all-root suppression, the local-exposure phase diagram, and the exact Bessel obstruction.
088 ||| Included nodes: 91
089 ||| The exact Bessel strong-coupling time scale is also compared separately with fixed-profile enhanced-dissipation results. The aim is to obtain a unified region with explicit quantifiers or a construction identifying exactly which uniformity fails, without inferring a general NSE conclusion from model time scales.
090 ||| The complete-root upper bound for the same real-shear triangular lattice can be paid by the actual exposure inside the observation layer: let \(\eta=|\delta|\Omega\) and \(I=[A,A+L]\). Then \(\ell_2(I)\le\min\{L,C_\kappa\}\), and the normalized launch-inclusive ledger is at most \(C\nu^{-2}e^{2\lambda_0L}M^{-2}\eta^{4/3}[4+\eta\min\{L,C_\kappa\}]\). When \(\eta=M^\alpha\) and \(L=M^{-\beta}\), this sufficient upper bound vanishes for \(\alpha<\min\{3/2,(6+3\beta)/7\}\). Finite-support launch allows \(A_0=0\), but the normalized ledger must start at the reference launch; the observation and payment layers coincide only when \(A=A_0=0\).
091 ||| The next finite task extends R0.72A's single-row local-exposure theorem to a many-carrier profile and checks whether carrier geometry, local \(L^2\) exposure, and the full nonlinear rotational charge can be paid uniformly on the same shrinking layer.
092 ||| This page follows the R0.00–R0.60 phase recap and organizes the 91 research nodes from R0.61 through R0.72A. Each phase records what was actually proved, which proposal was ruled out by a concrete counterexample or scale analysis, and which assumptions have not been derived from the Navier–Stokes equations.
093 ||| The exact Bessel construction shows that, even when the observation layer shrinks to \(O(R^{-3})\), the first \(R\) simple roots can retain logarithmic rescaled target-row mass; the corresponding physical \(x\)-derivative mass carries one additional factor \(\delta_R^2\). Hence no \(\eta\)-independent all-root constant exists for the rescaled target row. This does not prove divergence of the normalized nonlinear ledger or control the full nonlinear rotational charge. The conclusion remains confined to the declared triangular lattice and is not a general NSE complete-atom theorem.
094 ||| The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concluded that the complete Fourier–Leray structure and higher-order calculations could continue, but the critical quantity for general three-dimensional solutions was still uncontrolled. The next 91 nodes follow that gap; every completed release after R0.70A is retained in the route and index.
095 ||| The route after R0.60 has eighteen phases
096 ||| Research recap after R0.60: the 91 research nodes from R0.61 through R0.72A are organized chronologically; the latest section gives a local-exposure strong-coupling upper bound, a layer-width phase diagram, and an exact Bessel obstruction with logarithmic rescaled target-row mass.
097 ||| The 91 public notes from R0.61 through R0.72A
098 ||| R0.61–R0.72A recap · 2026-08-27
099 ||| R0.61–R0.72A research nodes
100 ||| R0.61–R0.72A | Research recap after R0.60
101 ||| R0.71X–Z successively close the fixed-small-coupling endpoint, selected growing roots, and bounded-coupling complete roots. R0.72A further proves that the complete-root cost of strong coupling can be paid by the actual exposure inside the observation layer; when \(\eta=M^\alpha\) and \(L=M^{-\beta}\), the normalized upper bound vanishes for \(\alpha<\min\{3/2,(6+3\beta)/7\}\). This region is a sufficient upper bound, not a sharp converse.
102 ||| R0.72A · Local-exposure phase diagram and exact Bessel obstruction
103 ||| R0.72A's local-exposure closure: the strong-coupling cost in the complete-root ledger tightens to \(\eta\min\{L,C_\kappa\}\). For \(\eta=M^\alpha\) and \(L=M^{-\beta}\), this yields the sufficient vanishing region \(\alpha<\min\{3/2,(6+3\beta)/7\}\); finite-support launch may begin at \(A_0=0\). A complementary exact Bessel construction produces selected rescaled target-row mass \((8/\pi^2)\log R+O(1)\), ruling out an \(\eta\)-independent all-root constant for the rescaled target row without proving divergence of the normalized nonlinear ledger.
104 ||| R0.72A figure
105 ||| R0.72A certificates
106 ||| R0.72B compares many-carrier local exposure with the complete nonlinear charge
107 ||| Extend R0.72A's single-row local-exposure theorem to a many-carrier profile and check whether the full nonlinear rotational charge and the enhanced-dissipation time scale can be paid uniformly at the same layer width; if not, give a failure family with explicit quantifiers.
108 ||| Place the local-exposure upper bound, the exact Bessel strong-coupling obstruction, and the complete nonlinear rotational charge in one many-carrier comparison framework.
109 ||| Compare many-carrier local exposure, the full nonlinear rotational charge, and the enhanced-dissipation time scale, seeking either a region with uniform payment or a failure family with explicit quantifiers.
110 ||| From the family-internal one-third endpoint to the local-exposure strong-coupling boundary
111 ||| For the same real-shear exact triangular lattice, let \(\eta=|\delta|\Omega\), \(I=[A,A+L]\), and record local exposure by \(\ell_2(I)=\Omega^{-2}\int_I\|V_z(x)\|^2dx\). Exact contraction, BV zero sampling, and dissipation give \[ G_{\rm all}^{\rm ex}(I) \le e^{2\lambda_0L}M\Omega^2 \bigl[4+\eta\min\{L,C_\kappa\}\bigr]. \] For a mixed window starting at the reference launch, the normalized ledger is therefore at most \[ C\nu^{-2}e^{2\lambda_0L}M^{-2}\eta^{4/3} \bigl[4+\eta\min\{L,C_\kappa\}\bigr]. \]
112 ||| Shortening the observation layer reduces the strong-coupling upper bound, but Bessel roots still leave logarithmic slope mass
113 ||| annulus exclusion → source-core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → shared-response first-order channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction
114 ||| After the static annular families are rigorously excluded, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–V separates the second-time jet, Leray-paid excursion, and fixed zero-level trace; R0.71W–Z successively closes the data-uniform complete first row, the fixed-small-coupling endpoint, selected growing roots, and bounded-coupling complete roots. R0.72A rewrites strong coupling as local exposure: the all-root upper bound pays only \(\eta\min\{L,C_\kappa\}\), finite-support launch may be placed at \(A_0=0\), and a vanishing region is obtained for \(\eta=M^\alpha\) and \(L=M^{-\beta}\). The exact Bessel construction simultaneously proves that the rescaled target-row slope-mass constant cannot be independent of \(\eta\); it does not imply divergence of the normalized nonlinear ledger.
115 ||| Cumulative recap R0.61–R0.72A · 2026-08-27
116 ||| At the other end, the exact nearest-neighbor lattice with \(\delta_R=R^4\) follows the frozen Bessel flow inside an \(O(R^{-3})\) shrinking layer. There is one simple exact root near each of the first \(R\) simple Bessel zeros, and the selected rescaled target-row mass is \((8/\pi^2)\log R+O(1)\); the corresponding physical \(x\)-derivative mass carries an additional factor \(\delta_R^2\). Therefore an all-root constant for the rescaled target row cannot be independent of \(\eta\); this construction proves neither divergence of the normalized nonlinear ledger nor a general three-dimensional Navier–Stokes result.
117 ||| There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. Within the declared real-shear exact triangular class, R0.72A turns the complete all-root ledger into a local-exposure upper bound and gives a strong-coupling–layer-width vanishing region; the exact Bessel construction rules out a rescaled target-row slope-mass constant independent of \(\eta\) without proving divergence of the normalized nonlinear ledger. This is a rigorous boundary inside a model class, not a general NSE regularity result.
118 ||| If \(\eta=M^\alpha\) and \(L=M^{-\beta}\), the upper bound vanishes for \(\alpha<\min\{3/2,(6+3\beta)/7\}\); fixed layer width recovers \(6/7\), while sufficiently fast layer shrinkage covers every \(\alpha<3/2\). Finite-support launch allows \(A_0=0\), but the normalized ledger must start at that reference launch; the observation and payment layers coincide only when \(A=A_0=0\).
119 ||| Previous review v1.12 · 2026-08-27
120 ||| A separate systematic review places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019–2026, and this site's R0.69P–R0.72A route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap.
121 ||| Next step R0.72B:
122 ||| The phase diagram gives a sufficient vanishing region, not a sharp converse. The Bessel construction refutes only an \(\eta\)-independent rescaled target-row slope-mass constant; it does not close the full nonlinear rotational charge, many-carrier feedback, or general NSE.
123 ||| Research note R0.72A · 2026-08-27
124 ||| Read research note R0.72A →
125 ||| Expand 61 public notes
126 ||| Review v1.13 · 2026-08-27
127 ||| Local exposure closes one strong-coupling / shrinking-layer region; the exact Bessel model rules out an \(\eta\)-independent rescaled target-row slope-mass constant.
128 ||| many-carrier local exposure and the complete nonlinear charge
129 ||| The route after the R0.60 recap has eighteen phases: reduced Picard analysis and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source-core duality; defect tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, internal-entry scaling, the second-time jet, finite recurrence, Leray-paid excursions, the fixed-zero boundary, the complete first-row data-uniform no-go, fixed-small-coupling one-third internal saturation, bounded-coupling selected-root suppression, BV all-root slope-mass closure, launch-inclusive mixed-window floor cancellation, the local-exposure phase region, and the exact Bessel logarithmic obstruction. R0.70A–R0.72A contains 53 completed releases.
130 ||| The cumulative recap after the R0.60 recap contains 91 nodes; the full site now has 151 public research notes
131 ||| R0.70A–R0.72A completed releases
132 ||| R0.72A completed:
`;

const englishRows = translationRows
  .trim()
  .split("\n")
  .map((row, index) => {
    const expected = String(index + 1).padStart(3, "0") + " ||| ";
    if (!row.startsWith(expected)) {
      throw new Error("unexpected R0.72A translation row " + (index + 1));
    }
    return row.slice(expected.length);
  });

const currentWithoutBatch = current.filter(
  (entry) => !/^r072a\d+$/.test(entry.id),
);
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.72A batch");
}

const missingFileOrder = [
  "literature-review.html",
  "notes/r0-72a.html",
  "recap-r0-61-r0-72a.html",
  "research-review.html",
];
function priority(entry) {
  const value = missingFileOrder.indexOf(entry.files[0]);
  return value < 0 ? 9 : value;
}
const missing = source
  .filter((entry) => !currentByChinese.has(entry.zh))
  .sort(
    (left, right) =>
      priority(left) - priority(right) ||
      left.zh.localeCompare(right.zh, "zh-CN"),
  );
const missingHash = createHash("sha256")
  .update(JSON.stringify(missing.map((entry) => entry.zh)))
  .digest("hex");
if (
  missing.length !== 132 ||
  englishRows.length !== missing.length ||
  missingHash !== "f4b3695a70e23b26a5a350a01e8f8c58f7fe791ef38cfe545836e410f1f19bab"
) {
  throw new Error(
    "R0.72A translation source drift: missing=" +
      missing.length +
      " rows=" +
      englishRows.length +
      " hash=" +
      missingHash,
  );
}

function same(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

const translated = missing.map((entry, index) => {
  const en = englishRows[index];
  if (!same(extractProtectedTokens(entry.zh), extractProtectedTokens(en))) {
    throw new Error(
      "protected-token mismatch at row " +
        String(index + 1) +
        ": " +
        entry.zh,
    );
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("blank or Chinese-containing translation: " + entry.zh);
  }
  if (/\b(?:we|our|ours|us)\b/i.test(en)) {
    throw new Error("first-person plural voice: " + entry.zh);
  }
  return {
    ...entry,
    id: "r072a" + String(index + 1).padStart(3, "0"),
    en,
  };
});

for (const relative of [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-72a.html",
  "notes/r0-72a.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.13')) {
    throw new Error(relative + ": expected i18n cache version v1.13");
  }
}

const merged = [...currentWithoutBatch, ...translated];
if (new Set(merged.map((entry) => entry.zh)).size !== merged.length) {
  throw new Error("translation merge produced duplicate Chinese keys");
}
if (new Set(merged.map((entry) => entry.id)).size !== merged.length) {
  throw new Error("translation merge produced duplicate IDs");
}

await writeFile(translationPath, JSON.stringify(merged, null, 2) + "\n");
console.log(
  JSON.stringify(
    {
      source: source.length,
      existingWithoutBatch: currentWithoutBatch.length,
      activeMissingBefore: missing.length,
      missingHash,
      added: translated.length,
      firstId: translated.at(0)?.id,
      lastId: translated.at(-1)?.id,
      total: merged.length,
      protectedTokenMismatches: 0,
      englishWithChinese: 0,
      firstPersonPlural: 0,
    },
    null,
    2,
  ),
);
