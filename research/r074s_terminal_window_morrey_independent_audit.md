# R0.74S Step 12 — independent audit of terminal-window packing

## 1. Verdict

**PASS, CONDITIONAL RESULTS ONLY.**

The independent review reconstructed every finite and analytic step in
(S.273)--(S.306).  It found four issues in the draft: a collision between
the duration symbol and the defect-ancestor symbol, an unsupported
(r=\infty) Calderon--Zygmund endpoint, an imprecise description of the
dissipation-measure decomposition, and omitted terminal domains in the
combined open gate.  All four were repaired before the source was locked.
The review also required an explicit (delta\in(0,4)) condition for the
averaged-terminal optimizer and removal of an embedded carriage return.

The locked main note is

research/r074s_terminal_window_morrey_packing.md

at SHA-256

03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f.

The universal estimates (S.280), (S.288), and (S.303) remain open.  This
audit does not turn a conditional Morrey theorem, an abstract sequence
test, or a bounded literature search into a regularity theorem.  **NOT
CLAY.**

## 2. Locked primary artifact set

| Artifact | SHA-256 |
|---|---|
| Main note | 03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f |
| Primary audit | 77397f923a20cb51382031bc4a8da82944190d4273aca8c316864e053e4c9396 |
| Primary generator | 90529ecfd080d3554fc45b63f5734a86f8736834cd6a65365c03fc82fb927a5a |
| Primary JSON | 741cb443b35a447df112d8078b79150eb21d5de308c4835219e0aa54f5e5b9d6 |
| Primary report | e9d5ebee782751b2cad17a4b7a78829ee7c4da6b6d7b828a9d5bb8faadba36ad |

The primary report records 16/16 exact checks, 12/12 finite check groups,
51/51 structural checks, and 11/11 rejected semantic mutations.  Its
overall status is PASS.  Those finite checks support the audit; they do not
serve as an oracle for the reconstructions below.

## 3. Independent common-window reconstruction

For a short residual coordinate with (d_k\le\delta),

\[
 J_k^{\rm LE}=(\ell_k,\tau)
 \subset(\max\{s_R,\tau-\delta R^2\},\tau)=J_{\tau,\delta}.
\]

Absolute continuity therefore gives

\[
 r_k^{\rm sh}
 \le\int_{J_{\tau,\delta}}|\dot F_{k,R}|.
\]

The complementary indices satisfy (d_k>\delta) and are exactly the
indices to which Step 11 (S.259) applies.  Both bounds are taken after one
common deletion set is fixed.  Adding them and only then taking the
best-(N) infimum proves (S.275) without duplicating the exception budget.

For fixed (delta), the (ell^1) distance between two window vectors is
bounded by the (g_R\,dt)-mass of the symmetric difference of their
intervals.  This tends to zero.  Independently,

\[
 |\mathcal S_N(a)-\mathcal S_N(b)|
 \le\|a-b\|_{\ell^1}
\]

because every fixed deletion functional has Lipschitz constant one.  The
full-measure good-time set is dense, so its supremum agrees with the
supremum over the whole open terminal interval.

Uniform absolute continuity of a single (L^1) function proves the
(delta\downarrow0) modulus for fixed ((u,R)).  It supplies no modulus
uniform over all solutions and scales, and the main note makes no such
claim.

## 4. Independent layer-cake and temporal-spike audit

Let (z_1^*\ge z_2^*\ge\cdots) be the decreasing rearrangement of
(z\in\ell^1_+).  Tonelli gives

\[
 \int_0^\infty(n_z(t)-N)_+\,dt
 =\sum_{j>N}\int_0^{z_j^*}dt
 =\mathcal S_N(z).
\]

This verifies (S.278) and the all-threshold implication (S.279).  If
(A_R=0), the linear absolute-variation ledger vanishes, so no division by
zero is needed.

For the synchronized spikes, each of the (M=N+1) coordinates has window
mass (H).  Hence

\[
 \sum_k\operatorname {TV}F_k=MH,
 \qquad
 \mathcal S_N=H,
 \qquad
 {\mathcal S_N\over(MH)^{2/3}}
 ={H^{1/3}\over M^{2/3}}\longrightarrow\infty.
\]

This is a valid counterexample to the abstract implication from a scalar
(L_t^1) ledger.  It is not a Navier--Stokes solution.

Fubini gives the averaged window mass (C\delta R^2P).  Markov therefore
removes a set of terminal times of measure at most (eta R^2).  Balancing

\[
 \eta^{-1}\delta P+\delta^{-2/3}P^{2/3}
\]

at an admissible interior value gives
(delta\asymp\eta^{3/5}P^{-1/5}) and the bound
(C\eta^{-2/5}P^{4/5}).  The exponent and its limitation are both stated
correctly.

## 5. Independent ancestor and Morrey audit

The defect ancestor is denoted (d^{\rm def}), separately from the
duration (d).  Although (d^{\rm def}) and (h) may share shell support,
the union of an (N_D)-point deletion set and an (N_H)-point deletion set
has size at most (N_D+N_H).  This proves (S.286).  For the mechanism-level
lemma,

\[
 \sum_kc_kp_k^{2/3}
 \le\left(\sum_kc_k^3\right)^{1/3}
     \left(\sum_kp_k\right)^{2/3},
\]

which proves (S.287) outside the one declared exceptional set.

For the moving tube, stop a time piece when either its length reaches
(O(R^2)) or its lifted path variation reaches (O(2^kR)).  There are at
most

\[
 C(1+L2^{-k})
\]

pieces.  One piece lies in a spatial ball of radius (C2^kR), requiring
(C2^{3k}) radius-(R) balls.  The resulting cylinder count is

\[
 C(2^{3k}+L2^{2k}).
\]

The identity

\[
 d\boldsymbol\mu=|\nabla u|^2dxdt+d\boldsymbol D
\]

is exact.  The full defect integral plus the high-Rayleigh restriction of
the viscous integral is therefore no larger than one copy of the tube's
total (oldsymbol\mu)-mass.  There is no factor two.  The uniform Morrey
coefficient and normalized path length then give the finite cap
(B(M,L)).  Combining that cap with (C_0P) separately on (P\le1) and
(P\ge1) proves (S.294).

This theorem is conditional.  Allowing (M) or (L) to depend on the
solution or scale does not prove the universal gate.

## 6. Independent mixed-norm scale audit

The final admissible range is

\[
 q\in[3,\infty],\qquad r\in[3,\infty).
\]

The finite-(r) restriction is necessary for the displayed periodic
Calderon--Zygmund estimate; no unsupported
(L^\infty\to L^\infty) pressure bound remains.  The value (q=\infty)
uses the standard convention (1/q=0).

With (	heta=3/r+2/q) and
(|u|_{L_t^qL_x^r}\le M_*R^{\theta-1}), the three local-energy terms
have final scales

\[
 RM_*^2,\qquad RM_*^3,\qquad RM_*^3.
\]

The normalized path exponent is independently

\[
 -1-{3\over r}+2-{2\over q}+\theta-1=0.
\]

Thus the mixed-norm ball supplies the two additional uniform coefficients
claimed in Section 8.  It does not derive such a ball from the bare payment.

## 7. Independent partial-regularity boundary

The finite atomic measure in (S.301) tests only a logical implication:
zero parabolic one-dimensional measure of a support does not control the
mass placed on many annular tubes.  The note does not claim that the atomic
measure is an NSE defect.

The high-Rayleigh ancestor belongs to the regular viscous part of the total
dissipation measure and can be large for a smooth high-frequency field.
Consequently a singular-point count cannot, without another theorem,
control the full-history (h) vector.  The CKN and Type-I statements are
not used beyond their actual singular-set scopes.

## 8. Independent single-packet screen

The literal R0.74F speed bound gives

\[
 {65R^2\over32R^2}={65\over32}<2\pi,
 \qquad
 {4R^2\over32R^2}={1\over8}.
\]

Thus the inherited packet centre does not make a physical torus winding.
For a hypothetical monotone path, the change of variables (s=q(t))
gives

\[
 {1\over B}\le{dt\over ds}\le{1\over\beta B}.
\]

Each complete period contributes exactly (|J|) to the
(s)-occupation; one remainder contributes between zero and (|J|).
This reconstructs (S.305).  In a many-winding regime, the number of visits
is proportional to (BT), while the residence per visit is proportional
to (B^{-1}).

For

\[
 a_\ell=H2^{p\ell}\Gamma^{4^\ell},
\]

the adjacent ratio is

\[
 {a_{\ell+1}\over a_\ell}
 =2^p\Gamma^{3\cdot4^\ell}.
\]

After deleting the first (N) coordinates, this ratio is at most
(q_N<1), which proves the geometric tail in (S.306).  Uniform speed-up
does not change that shell ratio.  Earlier deposited dissipation is not
identified with the ancestor vector, so this remains a kinematic screen and
not a universal PDE no-go.

## 9. Independent machine audit

The standard-library Ruby verifier reconstructs the finite mathematics
before it reads any primary artifact.  It passes 12/12 independent groups
and 153,237 exact Rational or integer assertions.  It also passes 39/39
main-note structure checks, 6/6 artifact locks, 6/6 dependency locks, and
2/2 negative-mutation groups, with `release_ready=true`.

The verifier runs under the installed Ruby without external gems.  A
warning-enabled syntax check passes.  External environment overrides of the
main note and of the Step 8 dependency both cause a nonzero exit as required.
These tests certify finite algebra, source integrity, and lock behavior;
they do not machine-prove an open PDE antecedent.

## 10. Final scope

The independent audit confirms:

- **proved in scope:** (S.273)--(S.279), (S.281)--(S.287), the conditional
  implications (S.289)--(S.300), the logical boundary tests
  (S.301)--(S.302), and the kinematic/discrete statements
  (S.304)--(S.306);
- **open:** (S.280), (S.288), (S.303), Step 11 (S.272), Q.12, Q.1,
  uniform critical Morrey/path control in the bare class, deposited-tube
  identification, a universal shell count, scale contraction, and
  regularity; and
- **not claimed:** NSE realizability of the abstract tests, an
  (r=\infty) pressure endpoint, an exhaustive literature search,
  novelty, or a solution of the Millennium problem.

**Independent audit verdict: PASS / CONDITIONAL RESULTS ONLY / NOT CLAY.**
