# R0.70S independent mathematical audit

**Verdict:** **PASS** for the locked snapshot below.  No mathematical,
scope, citation, or reproducibility blocker remains.

This verdict is deliberately narrow.  R0.70S excludes an energy-level,
locally bounded control of the positive R0.70R majorant
\(c_\eta\mathcal G\) by the four stated structural inputs.  It does **not**
show that the signed deficit \(\mathcal K_Q-\mathcal D_P\) is large, and it
does not establish singularity, continuation, or global regularity.

## 1. Locked snapshot and audit scope

The final audit used:

- research/r070s_report-source.md, SHA-256
  e96d7e9e7ff77e2df2bb5020d757416897731be27cb0f569b1bb2546a3b9e7c9;
- research/r070s_exact_audit.py, SHA-256
  15f6474e03630037c50ff07dbb4412e56761cf9b59cb4b2a7f4427de743ea8c8;
- research/certificates/r070s/result.json, SHA-256
  030b0da407f2af1aabb134d6acf6f2a729f188ca84e35b939f50a95d4bbf8846;
- research/certificates/r070s/README.md, SHA-256
  fd8fef32bcb0e7fbc9fd8631b0d19d425c999cba08bb038adb8159227ebaf96d;
- tests/r070s-energy-palinstrophy-gate.test.mjs, SHA-256
  613f9075d02837b09abdfad818a67586a77ca9e47b8b2e4be66aeaae15c0e9ad.

The audit independently checked:

1. the two-frequency shear heat solution and its Biot--Savart signs;
2. the fixed complete frame, all-integer active-index argument, and star
   block;
3. the covariance spectrum, absolute and relative gap, residual ratio, and
   positivity of the base majorant integral;
4. normalized-Haar pullback, dyadic index shift, projector scaling, and
   \(u_*=u\);
5. every fixed-time scaling identity for \(R\), the exact commutator square,
   \(\mathfrak W_L\), kinetic energy, and \(I\);
6. the \(A_N=N^{1/4}\) exponent contradiction and its exact quantifiers;
7. the boundary between machine-checked finite algebra and the analytic
   operator lemmas.

## 2. Global shear heat family

On normalized \(\mathbb T^3\), let

\[
 v_n=(0,\cos nx_1,\sin nx_1),
 \qquad
 w_m=(0,\sin mx_1,\cos mx_1).
\]

Direct differentiation gives

\[
 \nabla\times v_n=-nv_n,
 \qquad
 \nabla\times w_m=mw_m,
 \qquad
 \Delta v_n=-n^2v_n,
 \qquad
 \Delta w_m=-m^2w_m.
\]

Consequently the report's base fields

\[
 \omega_1=e^{-\nu s}v_1
 +M^{-1}e^{-\nu M^2s}w_M,
\]

\[
 u_1=-e^{-\nu s}v_1
 +M^{-2}e^{-\nu M^2s}w_M
\]

satisfy \(\nabla\times u_1=\omega_1\) and
\(\partial_su_1=\nu\Delta u_1\).  They have zero first component, depend
only on \(x_1\), and are mean zero.  Hence

\[
 (u_1\cdot\nabla)u_1=0,
\]

so this is an exact smooth global unforced Navier--Stokes solution, not a
linearized or approximate solution.

For the rescaled family,

\[
 \omega_N=A_N\mathcal S_N\omega_1(\cdot,N^2t),
 \qquad
 u_N=\frac{A_N}{N}\mathcal S_Nu_1(\cdot,N^2t),
\]

the same statements hold.  With the periodic convention
\(u_*:=u-\int_{\mathbb T^3}u\,dx\), every displayed velocity is mean zero,
so \(u_{N,*}=u_N\) exactly.

## 3. Fixed frame and the star block

The report fixes

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\}
\]

with a real-even tight symbol supported in
\(\{1/2<|\xi|<2\}\).  If \(N=2^J\), the strict support condition gives

\[
 \frac12<2^{J-j}<2
 \iff -1<J-j<1.
\]

Because \(J-j\) is an integer, the \(N\)-mode activates only \(j=J\).
The \(MN=2^{J+4}\)-mode similarly activates only \(j=J+4\).  Thus the two
active sets are disjoint over the full integer index set.  Exact tightness
then makes the sole response square equal to one; this is an analytic
consequence of the pinned frame hypotheses, not a numerical evaluation of
an unspecified multiplier profile.

The vorticity has zero mean, so the star block contributes nothing to its
covariance.  It cannot be removed from the commutator ledger: although
\(\Pi_0\omega=0\), generally

\[
 [\Pi_0,P]\omega=\Pi_0(P\omega)\ne0.
\]

The report correctly retains this term in
\(\mathfrak C_P=\sum_\alpha\|[T_\alpha,P]\omega\|_2^2\).

## 4. Covariance, gap, and positive target

Writing

\[
 a=e^{-\nu s},
 \qquad
 b=M^{-1}e^{-\nu M^2s},
 \qquad
 d=v_1\cdot w_M=\sin((M+1)x_1),
\]

disjointness gives

\[
 Q_1=a^2v_1\otimes v_1+b^2w_M\otimes w_M.
\]

Its nonzero eigenvalues are

\[
 \lambda_{1,2}
 =\frac12\left[
 a^2+b^2
 \pm\sqrt{(a^2-b^2)^2+4a^2b^2d^2}
 \right],
 \qquad \lambda_3=0.
\]

Since \(0<b/a\leq1/M\) for \(s\geq0\),

\[
 \lambda_1-\lambda_2\geq a^2-b^2>0,
\]

\[
 \frac{\lambda_1-\lambda_2}{E_1}
 \geq\frac{M^2-1}{M^2+1}
 =\frac{255}{257},
\]

and, with \(r_1=\lambda_2\),

\[
 0\leq\eta_1=\frac{r_1}{E_1}
 \leq\frac{b^2}{a^2+b^2}
 \leq\frac1{257}.
\]

Thus the top projector is defined at every finite \(s\geq0\), and the
relative gap survives every dyadic rescaling.

Tightness and the two exact frequencies give

\[
 \mathcal G_1(s)
 =e^{-2\nu s}+e^{-2\nu M^2s}.
\]

At \(x_1=0,s=0\), the two directions are orthogonal, so

\[
 \eta_1=\frac1{M^2+1},
 \qquad
 c_{\eta_1}=\frac1{M-1}=\frac1{15},
 \qquad
 \mathcal G_1=2.
\]

The integrand is therefore \(2/15>0\) at that point.  The simple finite-time
gap makes it continuous, so it is positive on a one-sided
positive-measure neighbourhood.  Hence \(I_1(S)>0\) for every \(S>0\).
Moreover,

\[
 0<I_1(\infty)
 \leq\frac1{M-1}
 \left(\frac1{2\nu}+\frac1{2\nu M^2}\right)
 =\frac{257}{7680\nu}<\infty.
\]

No numerical quadrature is used in either conclusion.

## 5. Normalized Haar and exact fixed-time scaling

For \((\mathcal S_Nf)(x)=f(Nx)\) with integer \(N\), normalized Haar
measure gives

\[
 \|\mathcal S_Nf\|_p=\|f\|_p,
 \qquad
 \Pi_0\mathcal S_Nf=\Pi_0f.
\]

For \(N=2^J\), the Fourier symbols give

\[
 T_j\mathcal S_N=\mathcal S_NT_{j-J}.
\]

Consequently

\[
 [T_j,P_N]\omega_N
 =A_N\mathcal S_N([T_{j-J},P_1]\omega_1),
\]

and the star block obeys the corresponding identity

\[
 [\Pi_0,P_N]\omega_N
 =A_N\mathcal S_N([\Pi_0,P_1]\omega_1).
\]

The covariance and projectors scale as

\[
 Q_N=A_N^2\mathcal S_NQ_1,
 \qquad
 L_N=\mathcal S_NL_1,
 \qquad
 P_N=\mathcal S_NP_1.
\]

For every fixed physical \(T>0\), changing variables \(s=N^2t\) gives the
exact truncated identities

\[
 \|R_N\|_{L^2(0,T)}
 =\frac{A_N^2}{N}
  \|R_1\|_{L^2(0,N^2T)},
\]

\[
 \|\mathfrak C_{P_N}\|_{L^2(0,T)}
 =\frac{A_N^2}{N}
  \|\mathfrak C_{P_1}\|_{L^2(0,N^2T)},
\]

\[
 \mathfrak W_{L_N}(0,T)
 =\frac{A_N^4}{N^2}
  \mathfrak W_{L_1}(0,N^2T),
\]

\[
 \|u_{N,*}(0)\|_2^2
 =\frac{A_N^2}{N^2}\|u_1(0)\|_2^2,
\]

and

\[
 I_N(T)=A_N^2I_1(N^2T).
\]

The upper bounds use the infinite-horizon base quantities only after these
finite-window equalities.  In particular,

\[
 0\leq R_1(s)\leq M^{-2}e^{-2\nu M^2s}
\]

and complete-frame tightness, including the star block, gives

\[
 \mathfrak C_{P_1}(s)\leq4\|\omega_1(s)\|_2^2.
\]

The normalized covariance has a uniform spectral gap and uniformly bounded
spatial derivative, so \(\|\nabla L_1\|_\infty\) is uniformly bounded.
Together with heat decay, this proves
\(\mathfrak W_{L_1}(0,\infty)<\infty\).

## 6. The exact no-go quantifier

Set \(A_N=N^{1/4}\).  Then

\[
 \|u_{N,*}(0)\|_2^2=O(N^{-3/2}),
\]

\[
 \|R_N\|_{L_t^2}
 +\|\mathfrak C_{P_N}\|_{L_t^2}
 =O(N^{-1/2}),
\]

\[
 \mathfrak W_{L_N}=O(N^{-1}),
\]

whereas

\[
 I_N(T)
 =N^{1/2}I_1(N^2T)
 \geq N^{1/2}I_1(T)
 \longrightarrow\infty.
\]

All members retain

\[
 0\leq r_N/E_N\leq1/257,
 \qquad
 (\lambda_{1,N}-\lambda_{2,N})/E_N\geq255/257.
\]

Theorem 7.1 now has the required uniform quantifiers: \(T,\nu,\eta_0\), and
the frame are fixed; one function
\(F_{T,\nu,\eta_0,\mathscr T}:[0,\infty)^4\to[0,\infty)\) must work for
every dyadic member; and there must be \(\delta,C>0\) such that

\[
 \sup_{z\in[0,\delta]^4}
 F_{T,\nu,\eta_0,\mathscr T}(z)\leq C.
\]

The four inputs eventually lie in this cube while \(I_N(T)>C\), giving the
claimed contradiction.  No monotonicity or continuity of \(F\) is assumed.

## 7. Essential claim boundary

The initial enstrophy is

\[
 \|\omega_N(0)\|_2^2
 =N^{1/2}\|\omega_1(0)\|_2^2
 \longrightarrow\infty.
\]

Therefore the construction does not exclude a bound using initial
enstrophy, velocity \(H^1\), palinstrophy, higher Sobolev norms, a frequency
moment, absolute covariance, or another quantity that detects this rising
scale.  It also does not exclude a right-hand side deliberately singular at
the zero four-tuple.

Most importantly, the divergent object is the positive upper majorant

\[
 \int c_\eta\mathcal G,
\]

not a proved lower bound for the actual signed quantity
\(\mathcal K_Q-\mathcal D_P\).  A more structured estimate may retain
cancellation that this majorization discards.  The family consists entirely
of global smooth solutions, so the result supplies no blow-up mechanism.
Nor does it propagate near-rank geometry for general Navier--Stokes data.

The logically correct route conclusion is only that a locally bounded
majorant closure needs information that does not remain in a compact set
along this sequence.  Initial enstrophy is one natural candidate, not the
only possible route.

## 8. Certificate integrity and reproducibility

The finite producer directly checks:

- the full curl and heat-equation residuals, rather than initializing them
  to zero;
- \(\operatorname{tr}Q\) from the actual covariance;
- the covariance characteristic polynomial and endpoint slacks;
- the singleton active sets through the full integer intersections
  \((-1,1)\cap\mathbb Z\) and \((3,5)\cap\mathbb Z\);
- the displayed \(N\)-family against the pulled-back base fields;
- the amplitude, derivative, and time-Jacobian factor residuals;
- the \(A_N=N^{1/4}\) exponent arithmetic.

The universal normalized-Haar identity, complete-frame lifting, spectral
projector equivariance, commutator identities, continuity, decay, and
change-of-variable statements are correctly identified as analytic
dependencies proved in the report.  They are not presented as consequences
of one finite trigonometric sample or of JSON strings.

Using the pinned Python 3.12 / SymPy 1.14 environment, two independent
producer runs were byte-identical to each other and to the archived result,
whose SHA-256 is
030b0da407f2af1aabb134d6acf6f2a729f188ca84e35b939f50a95d4bbf8846.
All five entries in research/certificates/r070s/SHA256SUMS verified.  The
focused Node gate passed 7/7 tests, and the audited files passed
git diff --check.

## 9. Corrections closed during audit

Earlier snapshots contained issues that were corrected before this verdict:

1. the theorem now fixes \(T,\nu,\eta_0,\mathscr T\), uses one \(F\) across
   all dyadic \(N\), and states an explicit local boundedness condition;
2. the complete frame and star block are self-contained, and the rescaled
   relative gap is explicit;
3. the \(I_N\) change of variables cites mean preservation, and every
   \(\mathfrak W_L\) occurrence carries its time window;
4. route language no longer claims that enstrophy is the unique possible
   next input;
5. the report explicitly separates the positive majorant from the signed
   diffusion deficit and records the diverging initial enstrophy;
6. the producer's initially hard-coded zero residuals and tautological trace
   check were replaced by actual calculations;
7. finite offset sampling was replaced by an all-integer support argument;
8. scale-factor arithmetic and the analytic operator dependencies are now
   described at their true proof levels.

No blocker or major issue remained after the final locked replay.
