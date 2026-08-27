# R0.72E claim--evidence matrix

**Date:** 2026-08-27
**Scope:** fixed-\(q_0\), one-carrier triangular 2.5D Navier--Stokes family.

| id | claim or possible gap | evidence | disposition | boundary |
|---|---|---|---|---|
| E1 | The triangular ansatz is an exact unforced three-dimensional NSE class. | Direct substitution gives \(v_t=v_{yy}\), \(f_t+vf_z=\Delta f\), and \(\mathbb P(u\times\omega)=(-vf_z,0,0)\). | proved | Special invariant class only. |
| E2 | Taking \(q_0=1\) isolates the target shell. | The shear frequency then has the same radius as the target. | rejected | Fix \(q_0>R_*\) instead. |
| E3 | A fixed \(q_0>R_*\) isolates the conjugate target pair. | All shear and non-target active frequencies have radius greater than \(R_*\). | proved | Constants depend on fixed \(q_0\). |
| E4 | The fixed-\(q_0\) lattice has the same frozen Bessel limit as R0.72A. | Only the \(O(\delta^{-1})\) diagonal term changes after \(\tau=\delta x\). | proved | No uniformity for \(q_0=q_0(R)\). |
| E5 | The first \(R\) Bessel roots persist as exact simple roots. | Growing-window \(C^1\) error is \(O_{q_0}(R^{-1})\), below the weakest slope \(R^{-1/2}\). | proved | One selected root per Bessel neighborhood; no exhaustion claim. |
| E6 | Selected exact slope mass is logarithmic. | Bessel zero and derivative asymptotics give \(G_R^{\rm sel}=(8/\pi^2)\log R+O_{q_0}(1)\). | proved | Additional roots only increase the complete mass. |
| E7 | Every selected scalar root is a positive complete target-shell entry. | Shell isolation, simplicity, and nonzero target Lamb component invoke the inherited global-shell identity. | proved | Depends on the fixed compact target multiplier. |
| E8 | The negative Sobolev action follows from terminal enhanced dissipation. | Available deterministic transfers give only coarser norm decay and do not state the required observation estimate. | rejected as proof | Feynman--Kac is used instead. |
| E9 | The Feynman--Kac potential weight is \(e^{-s}\). | Initial-value time ordering gives the reverse weight \(e^{-(t-s)}\). | rejected | The sign and weight are checked directly from the mild equation. |
| E10 | Fixed-phase oscillation gains two inverse powers uniformly. | When the random phase is near the real direction, stationary phase gives only squared \(H^{-1}\) gain \(O(\kappa^{-1})\). | rejected | Some special orientations gain \(O(\kappa^{-2})\), but they are not uniform. |
| E11 | The \(A_q^{-1}\) oscillatory bound is uniform in \(q_0\). | The zero-mode weight is \(q_0^2\). | rejected | \(q_0\) is fixed before \(R\to\infty\). |
| E12 | Smoothness of the kinetic density alone closes the negative moment. | The bad-event estimate needs polynomial small-time control. | rejected as insufficient | Kusuoka--Stroock Part II, Cor. 3.25 and (3.27), pp. 22--23, supply the quantitative bound. |
| E13 | Strong Hörmander from the noise field alone applies. | The two \(Z\)-directions arise only after brackets with the drift. | rejected | The correct condition is uniform parabolic/weak Hörmander. |
| E14 | The Kusuoka--Stroock theorem applies to the lifted process. | \(X_1,[X_1,X_0],[X_1,[X_1,X_0]]\) have absolute determinant \(4\) everywhere; the drift has allowed linear growth. | proved from cited theorem | Part II is the correct source; Part III is not used. |
| E15 | Marginalizing over the lifted angle loses the density bound. | The polynomial terminal-angle weight in (3.27) is integrable when its order is chosen above one. | rejected | Gives \(\|\rho_t\|_\infty\le C_Tt^{-N}\). |
| E16 | The negative moment is uniformly bounded as \(t\downarrow0\). | On the high-probability event, \(|Z_t|\asymp t\). | rejected | The exact bound is \(\mathbb E|Z_t|^{-1}\le C_T/t\). |
| E17 | The action costs order one at large coupling. | Stationary phase, the negative moment, and time integration give \(Q_{\delta,q_0}\lesssim(1+\log\delta)/\delta\). | proved | Sharp constant and logarithmic sharpness are not claimed. |
| E18 | Active enstrophy can overwhelm the shear. | The moment barrier gives \(S_R^2\|\phi_\theta\|^2\lesssim\delta_R^{5/3}/\log\delta_R=o(\delta_R^2)\). | rejected for the chosen amplitudes | Other amplitude choices may differ. |
| E19 | A separate background is needed to control enstrophy contrast. | The fixed shear frequency decays by only the fixed factor \(e^{-q_0^2T}\) on \([0,T]\). | rejected | This uses a fixed interval and fixed \(q_0\). |
| E20 | The rotational-charge estimate keeps only the target coordinate. | Fourier identity (6.1) sums every lattice coefficient of \(-vf_z\) in \(\dot H^{-1}\). | rejected | The proof is full-frequency in the exact class. |
| E21 | The amplitude \(S_R^2=\delta_R/\log(2+\delta_R)\) makes the charge diverge. | It cancels the action factor and leaves an \(O_{T,q_0}(1)\) normalized charge. | rejected | The logarithmic Bessel mass remains in the root ledger. |
| E22 | The complete root ledger grows only logarithmically. | Multiplication by \(S_R^2\) gives \(\mathcal J_{\rm all}\gtrsim\delta_R\). | rejected | Raw row mass is logarithmic; the physical atom is amplitude weighted. |
| E23 | The candidate ratio stays order one as in R0.72D. | \(D_R^{1/3}\asymp\delta_R^{2/3}\), \(\Lambda_1=O(1)\), and \(\mathcal J_R\gtrsim\delta_R\). | rejected | Ratio grows at least as \(\delta_R^{1/3}=R^{4/3}\). |
| E24 | Divergence of the ratio is evidence of finite-time blow-up. | Every family member solves a globally regular triangular parabolic system. | rejected | The result invalidates one intermediate estimate only. |
| E25 | No data-dependent replacement can work. | Only the exact \(D^{1/3}\Lambda_1\) form is contradicted. | open | Frequency-sensitive or stronger data factors remain possible. |
| E26 | The theorem transfers to arbitrary three-dimensional feedback. | The shear evolves independently of the active scalar. | not proved | Nontriangular feedback remains outside the release. |
