# R0.74O problem freeze — amplitude freedom at the scalar endpoint

## Status at freeze

R0.74H proves, for both frozen local frames,

\[
 X_R^\alpha
 \le C\left[(P_R^\alpha)^{2/3}
 +\mathfrak C_R^\alpha\right],
 \qquad \alpha\in\{M,F\},
\tag{F.1}
\]

and also the absolute collar estimate

\[
 \mathfrak C_R^M\le CP_R^M,
 \qquad
 \mathfrak C_R^F\le CP_{0,R}^F\le CP_R^F.
\tag{F.2}
\]

Consequently, when \(P_R^\alpha\le1\),

\[
 \mathfrak C_R^\alpha\le C(P_R^\alpha)^{2/3}.
\tag{F.3}
\]

The unresolved large-payment candidate after R0.74N was

\[
 \boxed{
 \mathfrak C_R^\alpha
 \stackrel{?}{\le}
 C\Phi(P_R^\alpha),
 \qquad
 \Phi(p)=p^{2/3}\sqrt{1+\log_+p},
 \quad
 \log_+p=\log\max\{p,1\}.}
\tag{F.4}
\]

If (F.4) held, (F.1) would give the same square-root-log upper scale for
\(X_R^\alpha\).  R0.74N showed that one frozen-amplitude exact family
saturates that scale.  Saturation is neither a proof nor a refutation of
(F.4).

R0.74O freezes a different question: does the amplitude freedom already
present in the same exact passive-packet solution refute (F.4)?  The
amplitude may be changed because the passive component enters its equation
linearly.  It must not be confused with the fixed geometric constant
\(\kappa=16\) used in the inherited packet construction.  The new amplitude
multiplier will be denoted by \(\varkappa_j\).

This is a scalar-payment endpoint question.  It is not a singularity
construction, a regularity theorem, or a solution of the Millennium
problem.  **NOT CLAY.**

## 1. Frozen exact solution and its free amplitude

Retain the R0.74F--N constants and fields

\[
 \rho=\frac1{320},
 \qquad
 c_\gamma=\frac8{3969},
 \qquad
 L_j=\frac{63}{32}2^j,
 \qquad
 R_j=e^{-\rho L_j^2},
\tag{F.5}
\]

\[
 \Gamma_j=e^{-c_\gamma L_j^2},
 \qquad
 B_jR_j^2\longrightarrow\frac1{128},
\tag{F.6}
\]

and the exact passive scalar \(F_j\) and odd heat shear \(\theta_j\).
For every \(\mathfrak a_j>0\),

\[
 u_j^{(\mathfrak a)}
 =(\mathfrak a_jF_j,B_j\theta_j,0),
 \qquad
 p_j^{(\mathfrak a)}=0
\tag{F.7}
\]

is a smooth periodic mean-zero unforced Navier--Stokes solution.  The
inversion symmetry and the even frozen mollifier imply

\[
 X_{R_j}(t)\equiv0,
 \qquad
 a_{R_j}(t)\equiv0,
 \qquad
 a_{R_j}'(t)\equiv0.
\tag{F.8}
\]

Thus Versions M and F coincide for every choice of \(\mathfrak a_j\), not
only for the amplitude used in R0.74G--N.

The inherited normalized amplitude is

\[
 \mathfrak a_{0,j}=B_j\Gamma_j^{-1/2}.
\tag{F.9}
\]

R0.74O permits

\[
 \mathfrak a_{*,j}
 =\varkappa_j\mathfrak a_{0,j}
\tag{F.10}
\]

with a new positive multiplier \(\varkappa_j\).

## 2. Frozen general-amplitude ledgers

The proof may use only the general-\(\mathfrak a\) inequalities already
proved before the special substitution (F.9).  With
\(R=R_j\), \(L=L_j\), \(B=B_j\), and
\(\Gamma=\Gamma_j\), they are

\[
 \mathcal E_*
 \le C\left[
 B^2R^2+\mathfrak a_*^2R^2
 \left(e^{-d_EL^2}+e^{-c/R^2}\right)\right],
 \qquad
 d_E=\frac{98}{29475},
\tag{F.11}
\]

\[
 \mathcal G_{u,*}
 \le C\left(B^3R^3+\mathfrak a_*^3R^4L^{-2}\right),
\tag{F.12}
\]

\[
 \mathcal G_{p,*}\le C\mathcal E_*^{3/2},
\tag{F.13}
\]

and

\[
 \mathcal H_{u,*}
 \le C\left(B^3R^3+\mathfrak a_*^3R^4L^{-7/2}\right).
\tag{F.14}
\]

All constants in (F.11)--(F.14) are independent of \(j\) and of the
amplitude.  The Version-F acceleration payment is exactly zero by (F.8).

The amplitude-independent fifth-shell shear lower bound is

\[
 P_{R_j}^M=P_{R_j}^F
 \ge 8e^{-8}B_j^3R_j^3.
\tag{F.15}
\]

The passive component cannot cancel this row because the two velocity
components are pointwise orthogonal.

## 3. Frozen flux and endpoint lower bounds

For the exact family, R0.74H reduces the complete signed collar flux to

\[
 \mathfrak F_R^{(\mathfrak a)}(\tau)
 =\frac{\mathfrak a^2B}{2R}
 \int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}
 \theta(t,x_3)F(t,x_2,x_3)^2
 \partial_2\vartheta_R^{\rm ann}(x)\,dx\,dt.
\tag{F.16}
\]

Therefore changing only \(\mathfrak a\) gives the exact identity

\[
 \mathfrak C_R^{(\varkappa\mathfrak a_0)}
 =\varkappa^2\mathfrak C_R^{(\mathfrak a_0)}.
\tag{F.17}
\]

The inherited lower bound and the completed R0.74N normalized-packet upper
bound give

\[
 cB^2LR^2
 \le\mathfrak C_R^{(\mathfrak a_0)}
 \le CB^2LR^2.
\tag{F.18}
\]

Independently, the general-amplitude terminal-lobe theorem gives

\[
 X_R^{(\mathfrak a)}
 \ge c\mathfrak a^2LR^2\Gamma.
\tag{F.19}
\]

Equations (F.11)--(F.19) are the complete inherited input.  No new
simulation, DNS, DGX computation, or finite-precision evidence is part of
the problem.

## 4. Primary R0.74O question and promotion gate

Find an explicit \(\varkappa_j\) for which

\[
 P_{R_j}^{M,*}=P_{R_j}^{F,*}
 \asymp B_j^3R_j^3
\tag{F.20}
\]

but

\[
 \frac{\mathfrak C_{R_j}^{\alpha,*}}
 {(P_{R_j}^{\alpha,*})^{2/3}
 \sqrt{1+\log_+P_{R_j}^{\alpha,*}}}
 \longrightarrow\infty,
 \qquad \alpha\in\{M,F\}.
\tag{F.21}
\]

The same construction should then be tested against \(X_R^\alpha\) through
the non-circular combination of the direct lower bound (F.19), the direct
collar upper bound from R0.74N, and the signed-flux closure (F.1).

Promotion requires all of the following.

1. Every row in (F.11)--(F.14) must be recomputed after the new amplitude
   substitution.
2. The exact exponential reserve must be positive and recorded as a rational
   number.
3. The shear-only lower bound (F.15) must be retained.
4. Both the lower and upper collar bounds must use the exact quadratic
   scaling (F.17).
5. The upper bound for \(X_R^\alpha\) must not assume the conclusion being
   proved.
6. The final statement must distinguish a refutation of the scalar-payment
   endpoint from any theorem with additional structural hypotheses.
7. Novelty and priority remain open pending a separate bounded literature
   audit.

## 5. Claim boundary at freeze

The following statements are not licensed merely by a successful
counterexample to (F.4):

- existence of a singular or blowing-up Navier--Stokes solution;
- failure of an endpoint involving an additional temporal, geometric,
  Carleson, BV, or flux observable;
- failure of the already proved small-payment implication;
- failure of epsilon regularity;
- failure or proof of global regularity.

The only frozen target is the universal large-payment scalar estimate
(F.4), together with the \(X_R^\alpha\) estimate that would follow from it
and (F.1).  **NOT CLAY.**
