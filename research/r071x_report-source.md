# R0.71X -- exact one-third saturation in the triangular prescribed-root family

**Status:** release source.  The exact normalization, zero-completeness
argument, half-line estimates, endpoint powers, and claim boundary have
passed independent review.  Numerical certificates corroborate but do not
replace the analytic proof.

## 0. Finite decision

The R0.71W uniform implicit-function theorem is valid for every sufficiently
small rescaled coupling

\[
 0<\delta<\delta_0,
 \qquad
 \mathscr A_{q,\delta}=\delta q^2,
\]

not only for power laws \(\mathscr A_q=q^\alpha\) with \(\alpha<2\).
The fixed-\(\delta\) diagonal is therefore still perturbative, even though it
has the endpoint physical amplitude \(q^2\).  The expected scales are

\[
 D_{q,\delta}\asymp\delta^2q^6,
 \qquad
 J_{*,m,q,\delta}\asymp\delta^2q^2,
 \qquad
 \mathcal L_{q,\delta}^{\rm rot}\lesssim\delta^2.
\]

Consequently

\[
 \frac{J_{*,m,q,\delta}}{D_{q,\delta}^{1/3}}
 \asymp \delta^{4/3}.
\]

For fixed \(\delta>0\), the prescribed atom reaches the exponent \(1/3\)
exactly.  For \(\delta_q\to0\), the normalized atom tends to zero.  Thus the
selected-root mechanism reaches but does not cross the one-third boundary.

The stronger R0.71X question is whether the prescribed roots are the complete
positive target-shell zero set on the fixed macroscopic interval.  The tail
argument in Section 3 is intended to close that point.  Without it, the
result applies only to the selected finite atom sum and cannot exclude extra
roots as a possible endpoint countermechanism.

## 1. Theorem

Fix the R0.71W triangular data: viscosity \(\nu>0\), target shell \(T_*\),
macroscopic interval \(I=[a,b]\), scaled left offset \(A_0\), prescribed
times \(A_0<\tau_1<\cdots<\tau_N\), carrier ratios, phase blocks, and the
fixed-frequency background.  After possibly decreasing the uniform
implicit-function radius, there are

\[
 q_0<\infty,
 \qquad
 0<\delta_*<\delta_0,
\]

such that for every admissible integer \(q\ge q_0\) and every
\(0<\delta\le\delta_*\), the exact coefficient curve
\(z_q(\delta)\) produces a smooth unforced triangular NSE solution
\(u_{q,\delta}\), global forward from the launch time \(t=\sigma_q\), with
the following properties.

1. The target coefficient, and hence the entire declared annulus, vanishes
   at the exact times \(t_{m,q}=\sigma_q+\tau_mq^{-2}\); these roots are
   simple.
2. These are the only target-annulus roots in \(I\).
3. With

   \[
    D_{q,\delta}
    =\|u_{q,\delta}(\sigma_q)\|_2^2
     +\|\omega_{q,\delta}(\sigma_q)\|_2^2,
   \]

   there are uniform constants such that

   \[
    c_D\delta^2q^6\le D_{q,\delta}\le C_D\delta^2q^6.
   \]

4. If \(Z_*^+(I)\) is the positive target-annulus root set and

   \[
    \mathcal J_{q,\delta}
    =\sum_{t_*\in Z_*^+(I)}J_*(t_*),
   \]

   then \(Z_*^+(I)=\{t_{1,q},\ldots,t_{N,q}\}\) and

   \[
    c_J\delta^2q^2
    \le \mathcal J_{q,\delta}
    \le C_J\delta^2q^2.
   \]

5. The complete first-row ledger obeys

   \[
    \nu^2
    \le \Lambda_1(I;u_{q,\delta})
    \le C_\Lambda(\nu^2+\delta^2).
   \]

It follows, uniformly for \(0<\delta\le\delta_*\), that

\[
 c\delta^{4/3}
 \le
 \frac{\mathcal J_{q,\delta}}
 {D_{q,\delta}^{1/3}\Lambda_1(I;u_{q,\delta})}
 \le
 C\delta^{4/3}.
\]

For every fixed \(\delta\in(0,\delta_*]\) and \(\beta\ge0\),

\[
 \frac{\mathcal J_{q,\delta}}
 {D_{q,\delta}^{\beta}\Lambda_1(I;u_{q,\delta})}
 \asymp_{\delta,\beta} q^{2-6\beta}.
\]

Hence no \(D^\beta\Lambda_1\) payment with \(\beta<1/3\) can hold uniformly
even on this fixed family.  At \(\beta=1/3\) the family is scale-critical,
and for \(\beta>1/3\) this family alone is absorbed.  This is an internal
sharpness statement for one declared triangular family.  It is not a
universal Navier--Stokes endpoint estimate and does not prove that
\(D^{1/3}\Lambda_1\) pays every triangular solution.

## 2. Scaling proof apart from zero completeness

Write \(\mathscr A=\delta q^2\).  The R0.71W coefficient bound
\(\sup_{q,\delta}|z_q(\delta)|<\infty\), the fixed number of carrier modes,
and Fourier orthogonality give

\[
 D_{q,\delta}\asymp \mathscr A^2q^2=\delta^2q^6.
\]

In the normalized-Haar convention this comparison comes from an exact
identity.  With \(n_{l,q}=dr_lq\), \(|A_l|=1\), and
\(B_{q,\delta}=b_0\mathscr A q\), Parseval gives

\[
\begin{aligned}
 \mathcal D_{q,\delta}
 :=\frac{D_{q,\delta}}{\mathscr A^2q^2}
 ={}&2\sum_{l=1}^{2N+1}
 \left[
 q^{-2}+\left(\frac{K_y}{q}-dr_l\right)^2
 +\frac{K_z^2}{q^2}
 \right]\\
 &+2\sum_{l=1}^{2N+1}z_{l,q}(\delta)^2
 \left(q^{-2}+d^2r_l^2\right)
 +2b_0^2(1+Q^2).
 \tag{2.1}
\end{aligned}
\]

The lower bound already follows from the background pair
\(B_{q,\delta}=b_0\mathscr A q\); the upper bound includes the active seed,
the shear, and the same background.

At every prescribed root, the target factorization is

\[
 F_{q,0}(x)=\delta
 \bigl[\Gamma(x)+o_{q\to\infty}(1)+O(\delta)\bigr]
\]

in \(C^1\) near the fixed root set.  Shrink \(\delta_*\) and enlarge
\(q_0\) so that the error in the derivative is at most half the minimum of
\(|\Gamma'(\tau_m)|\).  Then

\[
 |\partial_ta_{q,\delta}(t_{m,q})|
 \asymp \mathscr A q^2\delta
 =\mathscr A^2
 =\delta^2q^4.
\]

The nonlinear enstrophy proof of R0.71W uses only
\(1+\mathscr A/q^2=1+\delta\), so it is uniform on
\((0,\delta_*]\):

\[
 Y_{q,\delta}(t)\asymp \mathscr A^2q^2
 =\delta^2q^6,
 \qquad t\in I.
\]

The fixed-shell atom is therefore

\[
 J_{*,m,q,\delta}
 \asymp \frac{\mathscr A^4}{\mathscr A^2q^2}
 =\delta^2q^2.
\]

There is also an exact normalized identity behind the comparison.  Put

\[
 \Theta_{m,q,\delta}
 =\delta^{-1}\partial_xF_{q,0}(\tau_m),
 \qquad
 \mathcal Y_{m,q,\delta}
 =\frac{Y_{q,\delta}(t_{m,q})}{\mathscr A^2q^2},
 \qquad \mathcal D_{q,\delta}\text{ as in (2.1)}.
\]

If \(m_*(k_*)\ne0\) is the fixed multiplier value at the conjugate target
pair and the normalized Fourier convention of R0.71W is used, then

\[
 \partial_ta_{q,\delta}(t_{m,q})
 =\mathscr A^2\Theta_{m,q,\delta},
\]

and modular isolation makes the declared annulus exactly that conjugate
pair.  Consequently its atom has the exact value

\[
 J_{*,m,q,\delta}
 =\frac{2|m_*(k_*)|^2}{\kappa_*^2}
 \frac{\mathscr A^4|\Theta_{m,q,\delta}|^2}
 {Y_{q,\delta}(t_{m,q})}.
 \tag{2.2}
\]

Combining (2.1)--(2.2) yields

\[
 \frac{J_{*,m,q,\delta}}{D_{q,\delta}^{1/3}}
 =
 \frac{2|m_*(k_*)|^2\kappa_*^{-2}
 |\Theta_{m,q,\delta}|^2}
 {\mathcal Y_{m,q,\delta}\mathcal D_{q,\delta}^{1/3}}
 \delta^{4/3}.
\]

The three normalized factors \(\Theta\), \(\mathcal Y\), and
\(\mathcal D\) are uniformly bounded above and away from zero after
\(q_0\) and \(\delta_*\) are fixed.  The one-third law is therefore not
only a power-counting consequence; it has a uniformly nondegenerate exact
coefficient on the entire local IFT branch.

More explicitly, let

\[
 g_-:=\min_{1\le m\le N}|\Gamma'(\tau_m)|>0.
\]

The compact \(C^1\) estimate allows \(\delta_*\) and \(q_0\) to be chosen
so that \(|\Theta_{m,q,\delta}|\ge g_-/2\).  The background gives

\[
 \mathcal Y_{m,q,\delta}
 \ge 2Q^2b_0^2e^{-2\nu Q^2(|I|+A_0)},
 \qquad
 \mathcal D_{q,\delta}\ge2b_0^2(1+Q^2),
\]

while the R0.71W upper estimates bound all three quantities from above.
These inequalities supply finite positive endpoint constants without
assigning a numerical value to the nonquantitative IFT radius.

Finally the R0.71W full-frequency estimate gives

\[
 \frac1{|I|}\int_I
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y}
 \,dt
 \lesssim \frac{\mathscr A^2}{q^4}=\delta^2,
\]

while \(1\le\mathcal R_Y(I)\le C\).  This proves every scale in the
the theorem except the assertion that no additional target roots occur.

For later reference, the first ledger factor is defined by

\[
 \Lambda_1(I;u)
 =\mathcal R_Y(I)
 \left[
 \nu^2+\frac1{|I|}\int_I
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y}
 \,dt
 \right].
 \tag{2.3}
\]

Thus \(1\le\mathcal R_Y\le C\) and the rotational-charge estimate give

\[
 \nu^2\le \Lambda_1(I;u_{q,\delta})
 \le C(\nu^2+\delta^2).
 \tag{2.4}
\]

All constants denoted by \(c,C,c_D,C_D,\ldots\) may depend on the fixed
data \(\nu,I,T_*,A_0,\{\tau_m\},\{r_l\},d,Q,b_0\), but not on
\(q\) or \(\delta\) in the stated range.

## 3. No-spurious-root route

Set

\[
 H_{q,\delta}(x)
 =\delta^{-1}F_{q,0}(x;\delta,z_q(\delta)).
\]

The limiting first-Dyson target is

\[
 \Gamma(x)=K_z\sum_{l=1}^{N+1}c_l^\infty
 \frac{1-e^{-b_lx}}{b_l}.
\]

The needed zero count can be proved without importing a black-box
Chebyshev theorem.  If, with real coefficients \(a_j\),

\[
 E(x)=a_0+\sum_{j=1}^{n}a_je^{-b_jx},
 \qquad 0<b_1<\cdots<b_n,
\]

is nonzero, then it has at most \(n\) real zeros counting multiplicity.
For \(n=0\), the statement is immediate.  For the induction step, discard
zero exponential coefficients.  If none remain, then
\(E\equiv a_0\ne0\) and there are no zeros.  Otherwise let \(m\le n\) be
the number of remaining exponential terms and relabel so that \(a_1\ne0\)
is attached to the smallest remaining exponent.  If \(E\) has any finite
collection of \(M\) real zeros counting multiplicity, generalized Rolle
gives at least \(M-1\) zeros of \(E'\).  Multiplication of \(E'\) by the
positive function \(e^{b_1x}\) produces a nonzero constant plus at most
\(m-1\) distinct decaying exponentials.  The induction hypothesis gives
\(M-1\le m-1\), hence \(M\le m\le n\).
This also excludes an infinite zero set, since otherwise one could select
arbitrarily many finite zeros.  This is the extended-Chebyshev zero bound
needed here.

The function \(\Gamma\) is nonzero because \(c_1^\infty=1\), \(K_z\ne0\),
and the \(b_l\) are distinct.  It already has the \(N+1\) distinct zeros

\[
 0,\tau_1,\ldots,\tau_N.
\]

Since it is a constant plus \(N+1\) distinct decaying exponentials, these
zeros exhaust its entire real zero budget.  In particular:

- these are all its roots on \([0,\infty)\);
- every displayed root is simple, because their multiplicities already
  exhaust the \(N+1\)-zero budget;
- \(\Gamma_\infty:=\lim_{x\to\infty}\Gamma(x)\ne0\).

The last assertion has an independent zero-count proof: if
\(\Gamma_\infty=0\), then the nonzero \(\Gamma\) is a combination of only
\(N+1\) decaying exponentials.  Multiplying by the reciprocal of its
slowest-decaying exponential reduces it to a constant plus \(N\) distinct
exponentials, which cannot vanish at all \(N+1\) displayed points.

On a fixed compact interval \([A_0,X]\), the divided-map convergence from
R0.71W gives, uniformly for \(0<\delta\le\delta_*\),

\[
 \|H_{q,\delta}-\Gamma\|_{C^1([A_0,X])}
 \le \varepsilon_q+C\delta,
 \qquad \varepsilon_q\longrightarrow0.
 \tag{3.1}
\]

Choose disjoint closed neighborhoods \(U_m\) of the \(\tau_m\), small enough
that \(\Gamma'\) has a fixed sign on each one, and put

\[
 K=[A_0,X]\setminus\bigcup_{m=1}^N\operatorname{int}U_m,
 \qquad
 \eta_0=\min_K|\Gamma|>0,
 \qquad
 \eta_1=\min_{\cup_mU_m}|\Gamma'|>0.
\]

Require

\[
 \varepsilon_q+C\delta
 <\tfrac12\min(\eta_0,\eta_1).
 \tag{3.1a}
\]

Then \(\operatorname{Re}H_{q,\delta}\ne0\) on \(K\), while its derivative
keeps a strict sign on each \(U_m\).  Thus \(K\) contains no zero of the
complex-valued target curve at real \(x\).  Inside \(U_m\), its real part
has at most one zero; the exact IFT root is a zero of both target components,
so it is the unique zero of the complex-valued target curve there.  No claim
about roots at complex values of \(x\) is being made.

For the tail, the target component satisfies

\[
 \partial_xF_{q,0}
 =-\lambda_qF_{q,0}+\delta P_0V_{z_q(\delta)}(x)F_q(x),
 \qquad
 \lambda_q=\nu|k_*|^2/q^2.
\]

Because \(P_0F_q(0)=0\), variation of constants gives

\[
 \widetilde H_{q,\delta}(x)
 =\int_0^x e^{\lambda_qs}
 P_0V_{z_q(\delta)}(s)F_q(s)\,ds.
 \tag{3.2}
\]

The contraction-Dyson majorant is valid on the entire half-line since
\(\int_0^\infty\|V_z(s)\|\,ds<\infty\).  Uniformly for the bounded IFT
coefficient curve,

\[
 \sup_{x\ge0}\|F_q(x)\|_{\ell^2}
 \le
 \exp\!\left(\delta_*\int_0^\infty\|V_z(s)\|\,ds\right)
 \|F_0\|_{\ell^2}
 =:C_F.
 \tag{3.3}
\]

Choose \(q_0\) also so that \(\lambda_q\le c/2\), where
\(\|V_z(x)\|\le C_Ve^{-cx}\).  Then

\[
 \widetilde H_{q,\delta}(x)
 :=e^{\lambda_qx}H_{q,\delta}(x)
\]

has derivative bounded by \(C_VC_Fe^{-cx/2}\), uniformly in
\(q\ge q_0\) and \(0<\delta\le\delta_*\).  Hence the improper integral
in (3.2) converges to a limit \(M_{q,\delta}\), with the quantitative tail

\[
 |\widetilde H_{q,\delta}(x)-M_{q,\delta}|
 \le C_Te^{-cx/2}.
 \tag{3.4}
\]

It remains to identify that limit uniformly.  At \(\delta=0\), use the
analytic extension of the divided target and put

\[
 M_{q,0}
 =\int_0^\infty e^{\lambda_qs}
 P_0V_{c_q}(s)S_q(s)F_0\,ds.
 \tag{3.5}
\]

The uniform IFT estimate \(|z_q(\delta)-c_q|\le C\delta\), Duhamel's
formula, (3.3), and the integrable bound on \(V_z\) imply

\[
|M_{q,\delta}-M_{q,0}|\le C_M\delta.
\tag{3.6}
\]

For completeness, the uniform estimate used here is

\[
 \sup_{s\ge0}
 \|F_q(s;\delta,z_q(\delta))-S_q(s)F_0\|_{\ell^2}
 \le C\delta.
 \tag{3.6a}
\]

It follows directly from Duhamel's formula, (3.3), and
\(\|V_z(s)\|\le Ce^{-cs}\).  Moreover

\[
 \|V_{z_q(\delta)}(s)-V_{c_q}(s)\|
 \le C|z_q(\delta)-c_q|e^{-cs}
 \le C\delta e^{-cs}.
 \tag{3.6b}
\]

Substitution of (3.6a)--(3.6b) into the difference of the two integrals,
with \(\lambda_q\le c/2\), proves (3.6).  There is no
\(\lambda_q^{-1}\) loss because the interaction kernel has a fixed,
integrable decay rate.

For every fixed \(s\), the semigroup and finite-shift integrand in (3.5)
converges to the limiting first-Dyson integrand.  The common majorant
\(Ce^{-cs/2}\) is integrable, so dominated convergence on the half-line,
together with \(c_q\to c_\infty\), gives

\[
M_{q,0}\longrightarrow\Gamma_\infty.
\tag{3.7}
\]

Indeed, at \(q=\infty\) the initially positive \(K_z\) sector contains only
the modes with coset index \(r=-r_l\), and the second phase block vanishes
because
\(c_{N+2}^\infty=\cdots=c_{2N+1}^\infty=0\).  Hence the limiting integrand
is exactly

\[
 P_0V_{c_\infty}(s)S_\infty(s)F_0
 =K_z\sum_{l=1}^{N+1}c_l^\infty e^{-b_ls},
\]

and its integral is

\[
 K_z\sum_{l=1}^{N+1}\frac{c_l^\infty}{b_l}
 =\Gamma_\infty.
 \tag{3.7a}
\]

Equations (3.6)--(3.7) prove, rather than assume, the uniform expansion

\[
 M_{q,\delta}
 =\Gamma_\infty+o_{q\to\infty}(1)+O(\delta).
\]

First increase the preliminary \(q_0\) until \(\lambda_q\le c/2\).  Next
choose \(X>\tau_N\) so that the tail in (3.4) is sufficiently small.  Then
shrink \(\delta_*\) to control both \(C_M\delta\) in (3.6) and the compact
error \(C_X\delta\) in (3.1).  Finally increase \(q_0\) again to control
both (3.7) and \(\varepsilon_q\) in (3.1).  These choices make the total
tail error less than \(|\Gamma_\infty|/2\) and enforce (3.1a).  This keeps
\(\widetilde H_{q,\delta}\), hence \(F_{q,0}\), nonzero for all
\(x\ge X\).  Since the physical interval \(I\) corresponds to
\(x\in[A_0,A_0+q^2|I|]\), the compact and tail arguments together give the
complete target-root set.

Therefore

\[
 Z_*^+(I)=\{t_{1,q},\ldots,t_{N,q}\},
 \qquad
 \mathcal J_{q,\delta}=\sum_{m=1}^NJ_{*,m,q,\delta}.
 \tag{3.8}
\]

The integer \(N\) is fixed and all \(|\Theta_{m,q,\delta}|\) are uniformly
bounded above and away from zero.  Equations (2.1)--(2.2) now give

\[
 c_J\delta^2q^2
 \le \mathcal J_{q,\delta}
 \le C_J\delta^2q^2.
 \tag{3.9}
\]

Together with (2.3)--(2.4), this closes the complete atom sum and the
\(\Lambda_1\) factor in the theorem.

## 4. Audit disposition

The analytic proof passed independent review after seven explicit repairs:
the ECT multiplicity induction, simplicity of every limiting root, a nonzero
tail limit, quantitative compact separation, a uniform half-line Duhamel
estimate, explicit evaluation of the limiting tail integral, and closure of
the complete atom sum with \(\Lambda_1\).  The exact Parseval and multiplier
normalizations were independently reconstructed.

The release boundary remains strict: this theorem proves no universal
\(D^{1/3}\) payment, no bounded-data continuation criterion, no singularity
conclusion, and no global-regularity result for arbitrary three-dimensional
Navier--Stokes solutions.
