import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const projectRoot = resolve(import.meta.dirname, "..");
const translationsPath = resolve(projectRoot, "translations", "en.json");
const publicDirectory = resolve(projectRoot, "public");
const snapshotPath = resolve(
  projectRoot,
  "scripts",
  "i18n-snapshots",
  "r072h-missing.json",
);

const raw = String.raw;
// Positional translations are tied to the checked, tracked snapshot below.
// The updater verifies every live count/file occurrence before merging them.
const english = [
  raw`This section does not invoke a general non-autonomous bilinear embedding. It directly uses the scalar target coordinate, common heat factor, diagonal dissipation, and reciprocal-weight moment. A bounded search of primary sources found no theorem directly giving this carrier-count-independent mixed-row estimate. This is a bounded non-collision check through 2026-08-27, not a claim of novelty, priority, or exhaustiveness.`,
  raw`Open the complete 98-note index`,
  raw`'s bilinear or vector-valued heat-flow estimates likewise have no differentiated observation row.`,
  raw`'s BV indicatrix and`,
  raw`'s scattered-zero inequality likewise does not control squared slopes on an endogenous single temporal zero level.`,
  raw`Check whether (E_A,m_*,B_A,\rho_A) are jointly paid by the full physical critical-log normalization, or construct a normalized growing-carrier counterfamily.`,
  raw`Open interface · R0.72I`,
  raw`controls spatial commutators, not the temporal coefficient derivative (V').`,
  raw`Cumulative recap and 98-note index`,
  raw`The target row, diagonal dissipation, and reciprocal critical-log envelope give a carrier-count-independent moment-resolved upper bound. The all-odd Rudin–Shapiro family excludes an action-only payment and attains the required (M)-power; the complete-root corollary requires a compatible real gauge and \(\delta\ne0\).`,
  raw`shows that general vector Carleson embeddings can grow with the finite dimension; this is not a countertheorem for the structured scalar heat row in this section.`,
  raw`provides non-autonomous maximal regularity or observation admissibility, but does not simultaneously control two time-dependent target rows from the internal negative-Sobolev action.`,
  raw`Literature review v1.21 · 2026-08-27`,
  raw`I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72H on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.`,
  raw`. R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U establishes the boundaries for conditional incidence, genuine internal entries, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and excludes a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation. R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C obtains the sharp phase-uniform exact-launch (M^{-8/3}) and fixed-positive-tail (M^{-3}) algebraic scales. R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a nonvanishing but nondivergent normalized complete-root ledger. R0.72E returns to a fixed-carrier Bessel family and uses a quantitative negative-Sobolev action estimate to make the complete-root ledger relative to the candidate (D^{1/3}\Lambda_1) payment diverge as (R^{4/3}). R0.72F then uses regularly varying initial-layer weights to separate the selected-root threshold (1/3) from the Leray-payment threshold (1/2), selecting the minimal critical-log boundary. On the exact real one-carrier lattice, R0.72G uses a phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass has exactly logarithmic order and obtains sharp critical-log complete-root saturation. In a finite conjugate-paired multi-carrier system, R0.72H proves a carrier-count-independent moment-resolved payment for the mixed row; an all-odd Rudin–Shapiro family excludes the action-only version and attains the carrier power encoded by that moment. General Navier–Stokes regularity remains open.`,
  raw`Finite multi-carrier mixed-row payment and action-only no-go`,
  raw`R0.72H non-autonomous mixed-row boundary`,
  raw`R0.72H primary-source boundary`,
  raw`The condition \(\delta\ne0\) cannot be omitted: \((e^{\lambda_0x}F_0)'=\delta e^{\lambda_0x}h\), and the Rolle step divides by \(\delta\). When \(\delta=0\), the physical slope ledger is zero, but after division by \(\delta^2\), the raw \(h\)-ledger is outside this corollary. The displayed estimate remains a row-level conclusion and cannot yet be rewritten as (D^{1/3}\Lambda_{1,*}) for general physical solutions.`,
  raw`At (M=64), the mixed row is 4095.9421, with normalized value 0.99998587; (Q_*=57.33143), (m_*=2126.94965), and the moment-resolved ratio is 0.68204208. The first run failed because the small-(M) threshold and profile tolerance were too strict; the second stopped because of a length-check error. Both logs, their causes, and the final corrections are archived with the certificates. The finite audit checks only the implementation and scaling; it neither replaces the analytic proof nor constitutes an interval-arithmetic certificate.`,
  raw`01 · Finite-carrier lattice`,
  raw`02 · Mixed-row proof`,
  raw`03 · Critical envelope`,
  raw`04 · Sharp RS family`,
  raw`05 · Exact positive-time root`,
  raw`06 · Complete real target row`,
  raw`07 · Dual-path certificates`,
  raw`Decompose (A_1^2) using the reciprocal envelope of the critical-log weight, then apply \(|h|\le\sqrt{\lambda_0\mathfrak q}\), Cauchy–Schwarz, and \(\int_I\mathcal D\le E_A/2\) to obtain the main theorem. Only \(\ell^2\) carrier moments appear, so the constant does not grow with (M).`,
  raw`Absorption of all (E_A,m_*,B_A,\rho_A) into the final physical (D^{1/3}\Lambda_{1,*}); an equally strong complete-root reduction for an arbitrary complex target gauge; an infinite-carrier limit; transfer from the triangular 2.5D class to general three-dimensional weak solutions; or a Navier–Stokes continuation or singularity theorem.`,
  raw`Version v0.72H · 2026-08-27`,
  raw`This family is not a complete physical counterexample, however: at fixed coupling, the normalized scale of a single atom is about (M^{-2}); within the perturbative range, taking \(\delta a=\gamma M^{3/2}\) with fixed small \(\gamma>0\) gives an available single-atom scale of at most (M^{-2/3}/\log M).`,
  raw`But it leaves a shear scale that cannot be removed`,
  raw`Define the reciprocal-weight shear moment`,
  raw`An independent route recomputes every diagnostic with a separate gauge, sign generation, convolution, integration, and truncation. The maximum relative difference between the two routes is (3.31\times10^{-6}). Peak RSS is 122 MB for the producer and 80 MB for the independent route.`,
  raw`Multiple carriers introduce no dimension loss,`,
  raw`Return to R0.72G`,
  raw`Both the numerator and denominator are real in the all-odd gauge. The corrected normalized initial state produces an exact target root at (x=\tau_M>0); for fixed nonzero \(\delta\), it also has \(|h(\tau_M)|\gtrsim aM\). The sharp scale therefore does not arise solely from the launch atom.`,
  raw`The coverage is (M=4,8,16,32,64). The successive values of \(\mathcal E_Q/(a^2M^2)\) are 0.996346, 0.999092, 0.999774, 0.999943, and 0.999986; the exact-root residual falls to (8.67\times10^{-19}).`,
  raw`Conjugate pairing preserves skew coupling and energy contraction`,
  raw`Conjugate pairing gives (V_w^*=-V_w), hence`,
  raw`Fix \(\nu>0\), \(d\ge1\), a target frequency \(k_*=(K_y,K_z)\) with \(K_z\ne0\), and choose \(q\ge\max\{1,2|K_y|/d\}\), distinct positive carriers \(r_l\), and coefficients \(w_l\in\mathbb C\), with lattice index \(r\in\mathbb Z\). Starting from finitely supported initial data, the finite-carrier system is`,
  raw`Mixing even and odd carriers destroys the required real target gauge. Let \(U_M(x,s)\) be the evolution operator of the system above and \(e_0\) the standard basis vector of the target coordinate; take \(\tau_M=M^{-3}\) and add the target-coordinate correction`,
  raw`In the bounded search of primary sources through 2026-08-27, I found no result directly giving the mixed-row theorem in this section. This is a bounded non-collision check, not a claim of novelty, priority, or exhaustiveness.`,
  raw`Exact root`,
  raw`Both independent implementations pass, and failed attempts are retained`,
  raw`The critical logarithm lowers the high-frequency moment to order (4/3)`,
  raw`A coarse bound without the weighted action is also available`,
  raw`The target coordinate is only one component of (V_wF), so \(|h|^2\le\lambda_0\mathfrak q\). These two identities avoid any \(\ell^1\) carrier sum in the proof.`,
  raw`Take (M=2^n) and place the Rudin–Shapiro signs \(\varepsilon_j\in\{\pm1\}\) on an all-odd high-frequency block`,
  raw`The all-odd block keeps the target correction real`,
  raw`Weight`,
  raw`If (E_A=\lVert F(A)\rVert_2^2), while`,
  raw`Under a real target gauge, every remainder in the complete-root reduction is explicit`,
  raw`The numerical constant is independent of the carrier count, carrier locations, and physical shear phases. Because (w_*\ge1), the available data quantity (K_{v,A}=\sum_l r_l^2|w_l|^2e^{-2\kappa r_l^2A}) can replace (m_*), but this loses the frequency gain supplied by heat decay.`,
  raw`Dual-path finite certificates and failed attempts`,
  raw`Every constructed solution remains in the globally smooth triangular 2.5D class. This page neither constructs a finite-time singularity nor proves global smoothness for general three-dimensional solutions; the Clay Millennium Problem remains unsolved.`,
  raw`The same sharp family shows that the result cannot be compressed to (CQ_*^I): the critical-log action alone is insufficient, and some additional data control is necessary. This route naturally produces (E_A,m_*,B_A,\rho_A); the next gate asks whether the physical ledger can pay for them.`,
  raw`Figure R0.72H-1. Left: the ratio between the reciprocal critical-log envelope and the analytic comparison quantity shows a bounded transition from low to high frequencies. Center: the producer and independent finite audits are normalized by \(\mathcal E_Q/(a^2M^2)\), \(Q_* /(a^2M^{2/3}\log M)\), and \(m_* /(a^2M^{7/3}/\log M)\), respectively. Right: the action-only quotient grows on the reference scale \(M^{4/3}/\log M\), while the moment-resolved ratio remains bounded, with the exact-root residual for \(M=64\) marked. The finite points audit the implementation; the analytic conclusions follow from the termwise estimates.`,
  raw`The complete report, claim matrix, dual-path certificates, and formal figure are all public`,
  raw`Complete row`,
  raw`The next step fixes the row theorem from this section instead of repeating carrier counting. I will compare (E_A,m_*,B_A,\rho_A) term by term with the physical energy, full-frequency rotational charge, critical-log action, and restart geometry, aiming for a unified (D^{1/3}\Lambda_{1,*}) absorption.`,
  raw`Available maximal regularity or Carleson embedding cannot replace this row estimate`,
  raw`Phase flatness gives \(\lVert V_M(x)\rVert\lesssim a\sqrt M e^{-cM^2x}\), while at (x\asymp M^{-2}) the row-aligned initial state simultaneously gives \(|h|\asymp aM\) and \(|QF|\asymp aM^3\). The rigorous scales are`,
  raw`The row-level theorem is closed; physical transfer remains open`,
  raw`The one-dimensional envelope to optimize is`,
  raw`Research note R0.72H · MIXED ROW · CRITICAL LOG · RUDIN–SHAPIRO`,
  raw`Research note R0.72H: in a finite conjugate-paired multi-carrier triangular Navier–Stokes system, the mixed row is paid by the critical-log action and an explicit shear moment with a constant independent of carrier count; an all-odd Rudin–Shapiro family proves sharpness of the power encoded by that moment.`,
  raw`A carrier derivative pairs with diagonal dissipation`,
  raw`Therefore the contribution of one high-frequency carrier to (m_*) satisfies`,
  raw`The skew-energy identity for finitely many conjugate-paired carriers; a carrier-count-independent mixed-row upper bound; the critical envelope; an all-odd RS counterfamily to the action-only payment; sharpness of the moment-resolved (M)-power; and a complete-root row estimate for \(\delta\ne0\) with a compatible real target gauge.`,
  raw`The finite gate has only two acceptable exits: complete this absorption and state its coverage conditions, or construct a growing-carrier counterfamily with the full physical normalization. If neither can be completed, I will record the precise missing data interface.`,
  raw`Here \(E_0=\lVert G_M\rVert_2^2=M\). Thus \(\mathcal E_Q/Q_*\asymp M^{4/3}/\log M\to\infty\), so no uniform action-only estimate holds, whereas \([E_0m_*Q_*]^{1/2}\asymp a^2M^2\) has the same order as the left side. This proves that (m_*) encodes an attained (M)-scale, but it does not exclude estimates built from other data functionals.`,
  raw`On the restart window (I=[A,A+X]), set`,
  raw`Define \(G_{\rm all}^{\rm ex}(I)\) on \(I\) as the extended nonnegative sum, over every target root \(F_0(\tau)=0\), of \(|h(\tau)|^2\). From \(\int_I|hP_0V_w^2F|\le\sqrt{\lambda_0}B_AQ_*^I\), if the target gauge is real and \(\delta\ne0\), the Rolle–BV complete-root reduction gives`,
  raw`The obstruction moves from “carrier-count loss” to “can the physical data absorb it?”`,
  raw`This is an analytic theorem within a finite triangular 2.5D model class, not a partial solution of the Millennium Problem. It yields no new unconditional continuation criterion and does not reduce the full set of potential singular solutions.`,
  raw`This is precisely the complementary scale left by the R0.72F weight (s^{-1/3}[1+\log(1/s)]) on the differentiated row. Neither \((\kappa X)^{-1/3}\) nor the logarithmic denominator can be omitted from an (X)-uniform formula.`,
  raw`The formal figure shows the critical envelope, three principal scales, and two payment ratios together`,
  raw`After expanding (QF) term by term, (V_w') supplies the (r_l^2) heat derivative, while (V_w(D_q+\lambda_0)) supplies the frequency difference on the same carrier. From (q\ge\max\{1,2|K_y|/d\}),`,
  raw`Status · R0.72H complete`,
  raw`The action-only payment fails as (M^{4/3}/\log M)`,
  raw`The spatial commutator of Kato–Ponce, the non-autonomous maximal regularity of Haak–Ouhabaz and Trostorff–Waurick, Kharou's observation admissibility, and the bilinear or vector-valued square-function results of Carbonaro–Dragičević and Xu all provide nearby structures. They do not simultaneously control (P_0V_wF) and the time-dependent target row containing (V_w') from the internal negative-Sobolev action used here.`,
  raw`The mixed row has a carrier-count-independent critical-log payment`,
  raw`The mixed-row gate is closed in the finite multi-carrier model; the action-only payment is false, while physical-scale absorption remains open.`,
  raw`Nazarov–Pisier–Treil–Volberg also indicates that general operator-valued Carleson formulations can have finite-dimensional logarithmic loss. This section bypasses that abstraction and uses only the scalar target coordinate, common heat factor, diagonal dissipation, and reciprocal-weight moment. Stadje's BV indicatrix and the scattered-zero inequality of Narcowich–Ward–Wendland likewise do not directly treat an endogenous single temporal zero level.`,
  raw`R0.72G reduces complete-root packing to one mixed row. Here I prove, in a finite conjugate-paired multi-carrier system, that this row is paid by the critical-log action and an explicit reciprocal-weight shear moment, with a constant independent of carrier count, locations, and physical phases. An all-odd Rudin–Shapiro family simultaneously shows that retaining only the action makes the estimate fail as (M^{4/3}/\log M), and the same family attains the (M)-power encoded by the moment. The finite multi-carrier row-level gate is therefore closed, while unified absorption of the data factors into the physical (D^{1/3}\Lambda_{1,*}) remains unfinished.`,
  raw`The generalization risk after R0.72G was that the multi-carrier differentiated row might require an (M), \(\sqrt M\), or \(\ell^1\) cost. R0.72H excludes these dimension losses and gives an explicit upper bound that can enter the complete-root ledger.`,
  raw`R0.72H · 2026-08-27 · Personal mathematics research log`,
  raw`R0.72H | Carrier-count-independent payment for the multi-carrier mixed row`,
  raw`R0.72I tests whether the physical normalization pays the explicit data factors`,
  raw`01 · Twenty-four research phases`,
  raw`02 · Complete 98-note index`,
  raw`Retain the historical R0.72G recap`,
  raw`View the R0.72H dual-path certificates`,
  raw`Open the latest node R0.72H`,
  raw`What can now be retained is a row-level analytic theorem and a matching scaling counterfamily. Unified absorption of (E_A,m_*,B_A,\rho_A) into the physical (D^{1/3}\Lambda_{1,*}) remains unfinished; that issue determines whether this route can leave the exact triangular model.`,
  raw`The multi-carrier row-level dimension loss is excluded; the main obstruction moves to physical absorption`,
  raw`Twenty-four phases and 98 nodes: from reduced recurrences and the temporal-trace ledger, through failure of the unweighted payment, to row-level closure of the finite multi-carrier mixed row.`,
  raw`Recap endpoint: R0.72H`,
  raw`Public notes at the recap endpoint: 158`,
  raw`Through R0.72H, there is no new unconditional continuation criterion, no reduction of the full set of potential singular solutions, and no proof of finite-time breakdown. The 98 nodes or 60 published releases cannot be interpreted as a percentage completion of the Millennium Problem.`,
  raw`Cumulative recap · R0.61–R0.72H · 2026-08-27`,
  raw`The all-odd Rudin–Shapiro family gives \(\mathcal E_Q\asymp a^2M^2\), \(Q_*\asymp a^2M^{2/3}\log M\), and \(m_*\asymp a^2M^{7/3}/\log M\): the action-only payment fails, while the moment-resolved (M)-power is attained. The complete-root corollary for a compatible real target also requires \(\delta\ne0\). The next gate is absorption of (E_A,m_*,B_A,\rho_A) into the physical (D^{1/3}\Lambda_{1,*}), not further carrier counting.`,
  raw`Included nodes: 98`,
  raw`The next step fixes the R0.72H mixed-row theorem and compares (E_A,m_*,B_A,\rho_A) term by term with the physical energy, full-frequency rotational charge, critical-log action, and restart geometry.`,
  raw`The finite gate is to prove that a unified (D^{1/3}\Lambda_{1,*}) pays these quantities, or to construct a growing-carrier counterfamily satisfying the full physical normalization. If neither can be completed, I will record the precise missing data interface.`,
  raw`On the finite conjugate-paired multi-carrier triangular lattice, the target-row coordinate, diagonal dissipation, and critical-log reciprocal envelope give \(\mathcal E_Q\le6\sqrt\nu d|K_z|[\lambda_0E_Am_*Q_*]^{1/2}\). The constant is independent of carrier count, locations, and physical phases.`,
  raw`This page follows the R0.00–R0.60 phase recap and organizes the research nodes from R0.61 through R0.72H, 98 in total. I record chronologically what each segment actually proves, which proposal a specific counterexample or scaling analysis excludes, and which conditions have not yet been derived from the Navier–Stokes equations. The node states describe the type of evidence; they do not misstate release archiving as completion of a phase objective.`,
  raw`The R0.00–R0.60 material remains in the previous phase recap. R0.60 concludes that the full Fourier–Leray structure and higher-order computations can continue, but no critical quantity for general three-dimensional solutions is yet controlled. The subsequent 98 nodes advance along this gap; the releases from R0.70A through R0.72H, 60 in total, are published, of which 36 satisfy the current formal-figure complete-archive contract. They still include conditional theorems, counterexamples, finite diagnostics, and open gaps.`,
  raw`The route after R0.60 has twenty-four research phases`,
  raw`Research recap after R0.60: complete coverage from R0.61 through R0.72H, comprising 98 research nodes; the latest section closes the mixed row in a finite multi-carrier system and proves the action-only version false.`,
  raw`Public notes from R0.61 through R0.72H: 98`,
  raw`R0.61–R0.72H recap · 2026-08-27`,
  raw`R0.61–R0.72H research nodes`,
  raw`R0.61–R0.72H | Research recap after R0.60`,
  raw`The releases from R0.70A through R0.72H comprise 60 HTML/PDF releases and research source files on the published route. Under the current formal-figure contract, 36 are fully archived; 24 earlier releases still lack formal status or a formal figure package and remain on an auditable legacy-backfill list. A public page does not by itself mean that the archive contract is complete.`,
  raw`Published releases R0.70A–R0.72H`,
  raw`R0.72E excludes the unweighted candidate; R0.72F selects the minimal critical-log repair; R0.72G closes the complete roots on the exact one-carrier ray. R0.72H then proves that the finite multi-carrier mixed row requires no carrier-count loss and uses an all-odd Rudin–Shapiro family to exclude the action-only version.`,
  raw`R0.72H · Finite multi-carrier mixed row and sharp moment`,
  raw`R0.72H finite-carrier mixed-row theorem: for finitely many conjugate-paired carriers, \(\mathcal E_Q\) is paid by the critical-log action, restart energy, and reciprocal-weight shear moment with a carrier-count-independent constant. An all-odd Rudin–Shapiro family excludes a uniform action-only payment and attains the same moment-resolved (M)-power. The complete-root corollary for a compatible real target requires \(\delta\ne0\); the final physical-normalization absorption remains open.`,
  raw`The main R0.72H theorem is limited to a finite-carrier triangular 2.5D row problem; the compatible-real complete-root corollary additionally requires \(\delta\ne0\). This recap does not prove global smoothness or finite-time breakdown for the three-dimensional Navier–Stokes equations; the formal Clay problem remains open.`,
  raw`R0.72H figure`,
  raw`R0.72H certificates`,
  raw`R0.72I tests physical absorption of the explicit data factors`,
  raw`The constant is independent of carrier count, locations, and physical phases. The all-odd Rudin–Shapiro family satisfies \(\mathcal E_Q\asymp a^2M^2\), \(Q_*\asymp a^2M^{2/3}\log M\), and \(m_*\asymp a^2M^{7/3}/\log M\), so the action-only payment diverges while the moment-resolved (M)-power is attained.`,
  raw`From failure of the candidate payment to row-level closure of the multi-carrier mixed row`,
  raw`For (I=[A,A+X]), define the critical-log action (Q_*^I) and reciprocal-weight moment (m_*(A,X)). The target row, diagonal dissipation, and common heat factor give`,
  raw`Fix the carrier-count-independent row theorem from R0.72H and test whether (E_A,m_*,B_A,\rho_A) are jointly paid by the full physical energy, rotational charge, critical-log action, and restart geometry; otherwise construct a fully normalized counterfamily.`,
  raw`annular exclusion → source–kernel ledger → covariance-spectrum stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → sharp phase-uniform \(M^{-8/3}\) algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go`,
  raw`Check whether the explicit data factors can be jointly absorbed by the full physical critical-log normalization, or construct a normalized growing-carrier counterfamily.`,
  raw`After the static annular family is rigorously excluded, the main route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z treats the second-time jet, complete first row, fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A–C develops the Bessel lower family, target-row participation, and sharp physical-phase scales; R0.72D then realizes a positive-time root and full-charge order-one saturation. R0.72E fixes (q_0>R_*) and controls the complete (H^{-1}) action using Feynman–Kac, stationary phase, and a quantitative Hörmander density bound; the exact one-carrier family ultimately makes the complete-root ledger relative to the candidate (D^{1/3}\Lambda_1) payment diverge as (R^{4/3}). R0.72F then proves that selected roots require the lower endpoint (1/3), while Leray energy pays only up to (1/2); the minimal boundary repair is (s^{-1/3}[1+\log(1/s)]). R0.72G fixes this candidate and uses the real-phase gauge, target-row identities, and the Rolle–BV reduction to prove (G_{\rm all}\asymp\log\delta), obtaining sharp complete-root saturation on the original amplitude sequence. R0.72H turns to the finite conjugate-paired multi-carrier mixed row and proves a carrier-count-independent moment-resolved upper bound; an all-odd Rudin–Shapiro family excludes the action-only payment and attains the required (M)-power.`,
  raw`Cumulative recap R0.61–R0.72H · 2026-08-27`,
  raw`The cumulative recap now has twenty-four problem phases and completely covers R0.61–R0.72H. R0.72E excludes the unweighted payment, R0.72F selects the critical-log repair, R0.72G closes the complete roots on the exact one-carrier ray, and R0.72H closes the finite multi-carrier mixed row while excluding the action-only version. Across R0.70A–R0.72H, 60 releases are public; 36 satisfy the current formal-figure complete-archive contract, while 24 older figure archives remain on the backfill list.`,
  raw`There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. The next obstruction is physical-normalization absorption of the explicit row-level data factors.`,
  raw`The complete-root corollary holds only for a compatible real target gauge with \(\delta\ne0\); the physical (D^{1/3}\Lambda_{1,*}) absorption of (E_A,m_*,B_A,\rho_A) remains unproved. This section is not a general three-dimensional continuation theorem.`,
  raw`I also prepared a systematic review that places the classical theory, five literature strands, the candidate-elimination tree, progress from 2019—2026, and this site's R0.69P–R0.72H route in one diagram. The historical nodes R0.61–R0.69O remain in the cumulative recap.`,
  raw`Next R0.72I:`,
  raw`Research note R0.72H · 2026-08-27`,
  raw`The finite multi-carrier mixed row has no dimension loss, but the action alone is insufficient`,
  raw`Read the R0.72H research note →`,
  raw`Expand 68 public notes`,
  raw`Review v1.21 · 2026-08-27`,
  raw`The finite conjugate-paired multi-carrier mixed row has a carrier-count-independent moment-resolved payment; an all-odd Rudin–Shapiro family excludes the action-only version.`,
  raw`The cumulative recap after R0.60 contains 98 nodes; the site now has 158 public research notes`,
  raw`R0.70A–R0.72H: 60 published, 36 fully archived`,
  raw`R0.72H complete:`,
  raw`R0.72H closes the carrier-count-independent payment for the mixed row in a finite conjugate-paired multi-carrier system and proves the action-only version false; the next step audits only physical-normalization absorption of the explicit data factors.`,
  raw`Previous review v1.20 · 2026-08-27`,
];

function duplicateValues(values) {
  const seen = new Set();
  const duplicates = new Set();
  for (const value of values) {
    if (seen.has(value)) duplicates.add(value);
    seen.add(value);
  }
  return [...duplicates];
}

function numericTokens(value) {
  return [...value.matchAll(/\p{N}+(?:[.,]\p{N}+)*/gu)].map(
    (match) => match[0],
  );
}

function protectedBundle(value) {
  return {
    texAndUrls: extractProtectedTokens(value),
    numbers: numericTokens(value),
  };
}

function rawProtectedTokens(value) {
  return [
    ...value.matchAll(
      /\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|https?:\/\/[^\s<]+/g,
    ),
  ].map((match) => match[0]);
}

function countOccurrences(value, needle) {
  if (!needle) return 0;
  return value.split(needle).length - 1;
}

function restoreProtectedTokens(template, source) {
  let result = template;
  const tokenCounts = new Map();
  for (const token of rawProtectedTokens(source)) {
    tokenCounts.set(token, (tokenCounts.get(token) ?? 0) + 1);
  }
  for (const [token, required] of tokenCounts) {
    let remaining = required - countOccurrences(result, token);
    if (remaining < 0) {
      throw new Error("Extra protected token in English template: " + token);
    }
    if (!remaining) continue;
    const delimiterStripped = token
      .replace(/^\\([([])/, "$1")
      .replace(/\\([)\]])$/, "$1");
    while (remaining > 0) {
      const index = result.indexOf(delimiterStripped);
      if (index < 0) {
        throw new Error(
          "Cannot restore protected token " + token + " in: " + template,
        );
      }
      result =
        result.slice(0, index) +
        token +
        result.slice(index + delimiterStripped.length);
      remaining -= 1;
    }
  }
  return result;
}

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length !== 148) {
  throw new Error(
    "R0.72H snapshot cardinality drift: " +
      (Array.isArray(snapshot) ? snapshot.length : "not-an-array"),
  );
}
if (english.length !== 148) {
  throw new Error("R0.72H English cardinality drift: " + english.length);
}

const expectedFiles = [
  "literature-review.html",
  "notes/r0-72h.html",
  "recap-r0-61-r0-72h.html",
  "research-review.html",
];
const snapshotFiles = [...new Set(snapshot.flatMap((entry) => entry.files))];
if (JSON.stringify(snapshotFiles) !== JSON.stringify(expectedFiles)) {
  throw new Error(
    "R0.72H snapshot file-set drift: " + JSON.stringify(snapshotFiles),
  );
}

for (const field of ["zh"]) {
  const duplicates = duplicateValues(snapshot.map((entry) => entry[field]));
  if (duplicates.length) {
    throw new Error("Duplicate snapshot " + field + " values: " + duplicates.join(" | "));
  }
}

const rows = snapshot.map((entry, index) => [
  `r072h${String(index + 1).padStart(3, "0")}`,
  entry.zh,
  restoreProtectedTokens(english[index], entry.zh),
]);

const translations = JSON.parse(await readFile(translationsPath, "utf8"));
const legacyById = new Map([
  ["r072h021", raw`01 · 有限格点`],
  [
    "r072h041",
    [
      raw`固定目标频率 \(k_*=(K_y,K_z)\)、正载波 \(r_l\) 与系数 \(w_l\in\mathbb C\)。有限格点系统为`,
      raw`固定 \(\nu>0\)、\(d\ge1\)、目标频率 \(k_*=(K_y,K_z)\) 且 \(K_z\ne0\)，取 \(q\ge\max\{1,2|K_y|/d\}\)、互异正载波 \(r_l\) 与系数 \(w_l\in\mathbb C\)。从有限支撑初值出发，有限载波系统为`,
    ],
  ],
  [
    "r072h042",
    raw`混合奇偶载波会破坏所需的实目标 gauge。令 \(\tau_M=M^{-3}\)，并加目标坐标修正`,
  ],
  [
    "r072h058",
    raw`图 R0.72H-1。左：\(\mathcal E_Q\sim a^2M^2\) 与两路有限审计；中：action-only 比随 \(M\) 增长，而 moment-resolved 比保持阶一；右：全奇数 Rudin–Shapiro 族的精确正时刻根及修正尺度。有限点用于实现审计，解析结论来自逐式估计。`,
  ],
  [
    "r072h072",
    raw`于是 \(\mathcal E_Q/Q_*\asymp M^{4/3}/\log M\to\infty\)，统一的 action-only 估计不成立；而 \([E_0m_*Q_*]^{1/2}\asymp a^2M^2\) 与左边同阶。这证明 \(m_*\) 所编码的 \(M\)-尺度被达到，但不排除使用别的数据泛函建立其他估计。`,
  ],
  [
    "r072h074",
    raw`则 \(\int_I|hP_0V_w^2F|\le\sqrt{\lambda_0}B_AQ_*^I\)。若目标 gauge 为实且 \(\delta\ne0\)，Rolle–BV 完整根归约给出`,
  ],
  [
    "r072h078",
    raw`正式附图同时显示主尺度、action-only 发散与精确根`,
  ],
]);
for (const [id, legacyZh] of legacyById) {
  const rowIndex = Number.parseInt(id.slice(-3), 10) - 1;
  const [currentId, zh, en] = rows[rowIndex];
  const existing = translations.find((entry) => entry.id === id);
  if (!existing) continue;
  const acceptedLegacy = Array.isArray(legacyZh) ? legacyZh : [legacyZh];
  if (acceptedLegacy.includes(existing.zh)) {
    const live = snapshot[rowIndex];
    Object.assign(existing, {
      id: currentId,
      zh,
      en,
      count: live.count,
      files: live.files,
    });
  } else if (existing.zh !== zh) {
    throw new Error(
      "Unexpected R0.72H translation migration source for " +
        id +
        ": " +
        existing.zh,
    );
  }
}
const source = await collectSiteStrings(publicDirectory);
const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
const existingByChinese = new Map(
  translations.map((entry) => [entry.zh, entry]),
);

for (const entry of snapshot) {
  const live = sourceByChinese.get(entry.zh);
  if (
    !live ||
    live.count !== entry.count ||
    JSON.stringify(live.files) !== JSON.stringify(entry.files)
  ) {
    throw new Error(
      "R0.72H live-source drift for snapshot key:\n" +
        entry.zh +
        "\nSNAPSHOT " +
        JSON.stringify({ count: entry.count, files: entry.files }) +
        "\nLIVE " +
        JSON.stringify(live ?? null),
    );
  }
}

const missing = source.filter((entry) => !existingByChinese.has(entry.zh));
const snapshotKeys = new Set(snapshot.map((entry) => entry.zh));
const nonSnapshotMissing = missing.filter((entry) => !snapshotKeys.has(entry.zh));
if (nonSnapshotMissing.length) {
  throw new Error(
    "R0.72H translation source drift (" +
      nonSnapshotMissing.length +
      " non-snapshot live strings):\n" +
      nonSnapshotMissing.map((entry) => entry.zh).join("\n---\n"),
  );
}
const expectedMissing = rows
  .filter(([, zh]) => !existingByChinese.has(zh))
  .map(([, zh]) => zh);
if (
  JSON.stringify(missing.map((entry) => entry.zh).sort()) !==
  JSON.stringify(expectedMissing.sort())
) {
  throw new Error("R0.72H missing-set drift after migration");
}

for (const [id, zh, en] of rows) {
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Invalid English translation for: " + zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + zh);
  }
  const zhTokens = protectedBundle(zh);
  const enTokens = protectedBundle(en);
  if (JSON.stringify(zhTokens) !== JSON.stringify(enTokens)) {
    throw new Error(
      "Protected-token mismatch for " +
        id +
        ":\n" +
        zh +
        "\nZH " +
        JSON.stringify(zhTokens) +
        "\nEN " +
        JSON.stringify(enTokens),
    );
  }
  const existing = existingByChinese.get(zh);
  if (existing && (existing.id !== id || existing.en !== en)) {
    throw new Error(
      "Existing R0.72H translation drift for " +
        id +
        ":\n" +
        JSON.stringify(existing),
    );
  }
}

for (const field of ["id", "zh"]) {
  const duplicates = duplicateValues(translations.map((entry) => entry[field]));
  if (duplicates.length) {
    throw new Error(
      "Duplicate existing " + field + " values: " + duplicates.join(" | "),
    );
  }
}

let added = 0;
for (const [id, zh, en] of rows) {
  if (existingByChinese.has(zh)) continue;
  const live = sourceByChinese.get(zh);
  translations.push({ ...live, id, en });
  existingByChinese.set(zh, translations.at(-1));
  added += 1;
}

const sourceAfter = await collectSiteStrings(publicDirectory);
const missingAfter = sourceAfter.filter(
  (entry) => !existingByChinese.has(entry.zh),
);
if (missingAfter.length) {
  throw new Error(
    "R0.72H full-site missing-after check failed (" +
      missingAfter.length +
      " strings):\n" +
      missingAfter.map((entry) => entry.zh).join("\n---\n"),
  );
}

for (const field of ["id", "zh"]) {
  const duplicates = duplicateValues(translations.map((entry) => entry[field]));
  if (duplicates.length) {
    throw new Error(
      "Duplicate final " + field + " values: " + duplicates.join(" | "),
    );
  }
}

await writeFile(translationsPath, JSON.stringify(translations, null, 2) + "\n");
console.log(
  JSON.stringify({
    added,
    total: translations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
    missingAfter: missingAfter.length,
    mappedRows: rows.length,
    snapshotFiles,
  }),
);
