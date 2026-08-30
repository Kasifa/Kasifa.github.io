# R0.73K problem freeze: a parameter-uniform viscous rank-one branch

**Status:** frozen proof contract; no continuum claim is closed until the
analytic proof and both independent audits pass

**Parameter window:** \(0\le d\le D_*=1/450\)

**Operator row:** \((\beta,\xi,\gamma)=(0,0,1/2)\)

## 0. Direct decision

R0.73J certifies one algebraically simple inviscid eigenvalue throughout the
fixed heat-profile interval.  R0.73K asks whether that single branch survives
the singular domain change produced by viscosity, uniformly in the same
parameter interval.

The target is not full norm-resolvent convergence.  Such convergence is
structurally unavailable: for every \(\varepsilon>0\) the viscous resolvent is
compact, whereas at \(\varepsilon=0\) the multiplication part leaves
noncompact essential spectrum on the imaginary axis.  The admissible route is
the profile-uniform version of the compact--Fredholm factorization used at one
fixed profile in R0.73D and R0.73E.

The section is successful only if it closes all of K1--K7 below.  A finite
Fourier calculation is a diagnostic and cannot close any of them.

## 1. Frozen spaces and operators

Let

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad L=-\partial_x^2+\frac14,
 \tag{1.1}
\]

and let \(X\simeq H^{-1}_{\rm per}(\mathbb T_{2\pi})\) have kinetic inner
product

\[
 \langle q_1,q_2\rangle_X
 =4\langle L^{-1}q_1,q_2\rangle_{L^2}.
 \tag{1.2}
\]

The inviscid kinetic generator is

\[
 A_X(d)=-\frac i2\left(M_{W_d}+M_{W_d''}L^{-1}\right).
 \tag{1.3}
\]

Use the fixed unitary map

\[
 U=2L^{-1/2}:X\longrightarrow H:=L^2(\mathbb T_{2\pi}).
 \tag{1.4}
\]

Then

\[
 \widetilde A(d):=UA_X(d)U^{-1}=M_d+K_d,
 \qquad M_d=-\frac i2M_{W_d},
 \tag{1.5}
\]

where

\[
 K_d=-\frac i2\left(
 L^{-1/2}[M_{W_d},L^{1/2}]
 +L^{-1/2}M_{W_d''}L^{-1/2}
 \right)
 \tag{1.6}
\]

is compact.  The singularly perturbed operator used throughout R0.73K is

\[
 B_\varepsilon(d)=M_d+K_d-\varepsilon L,
 \qquad D(B_\varepsilon(d))=H^2_{\rm per}\quad(\varepsilon>0),
 \tag{1.7}
\]

while \(B_0(d)=\widetilde A(d)\) is bounded on all of \(H\).  No step may
treat \(-\varepsilon L\) as a bounded \(O(\varepsilon)\) perturbation.

## 2. Inherited inviscid certificate

Put

\[
 D_*:=\frac1{450},\qquad
 \Gamma_*:=\left\{z:\left|z-\frac{17}{100}\right|
 =\frac3{1000}\right\}.
 \tag{2.1}
\]

R0.73J proves that, for every \(d\in[0,D_*]\), \(B_0(d)\) has exactly
one algebraically simple eigenvalue \(\lambda_0(d)\) inside \(\Gamma_*\),

\[
 \frac{167}{1000}<\lambda_0(d)<\frac{173}{1000},
 \tag{2.2}
\]

and no other spectrum in \(\{\operatorname{Re}z>11/100\}\).  Its kinetic
right and left unit eigenvectors have normalized overlap greater than
\(0.5853\), and the fixed functional

\[
 \mathfrak a_X(q)=(L^{-1}q)(0)
 \tag{2.3}
\]

does not vanish on the branch.  In \(H\), the corresponding bounded anchor is

\[
 \alpha(h)=\mathfrak a_X(U^{-1}h)
 =\frac12(L^{-1/2}h)(0).
 \tag{2.4}
\]

## 3. Frozen theorem contract

Set

\[
 b_K:=\frac3{25}=0.12,
 \qquad c_K:=\frac4{25}=0.16.
 \tag{3.1}
\]

R0.73K must prove that there is \(\varepsilon_K>0\) such that every
\(0<\varepsilon\le\varepsilon_K\) and every \(d\in[0,D_*]\) satisfy:

1. **one common contour:** \(\Gamma_*\subset\rho(B_\varepsilon(d))\);
2. **one simple branch:** the Riesz projection
   \[
    P_\varepsilon(d)=\frac1{2\pi i}\int_{\Gamma_*}
      (z-B_\varepsilon(d))^{-1}\,dz
    \tag{3.2}
   \]
   has rank one, and its unique eigenvalue \(\lambda_\varepsilon(d)\) is
   real and real analytic in \(d\);
3. **uniform singular-limit transfer:**
   \[
    \sup_{0\le d\le D_*}
    \|P_\varepsilon(d)-P_0(d)\|\longrightarrow0;
    \tag{3.3}
   \]
4. **the rate needed by the next section:** for a constant \(C_\lambda\)
   independent of \(\varepsilon,d\),
   \[
    \sup_{0\le d\le D_*}
    |\lambda_\varepsilon(d)-\lambda_0(d)|
    \le C_\lambda\varepsilon;
    \tag{3.4}
   \]
5. **uniform conditioning and motion:** after decreasing
   \(\varepsilon_K\) if needed,
   \[
    \sup_{\varepsilon,d}\|P_\varepsilon(d)\|<\frac95,
    \qquad
    \sup_{\varepsilon,d}\|\partial_dP_\varepsilon(d)\|<\infty;
    \tag{3.5}
   \]
   equivalently, normalized viscous right and left eigenvectors have overlap
   greater than \(5/9\).  The anchor \(\alpha\) remains nonzero and fixes a
   real-analytic right eigenvector;
6. **fixed-half-plane no pollution:**
   \[
    \sigma(B_\varepsilon(d))\cap
    \{\operatorname{Re}z\ge b_K\}
    =\{\lambda_\varepsilon(d)\};
    \tag{3.6}
   \]
7. **uniform complement control:** if \(Q_\varepsilon=I-P_\varepsilon\)
   and \(C_{\varepsilon,d}\) is the part of \(B_\varepsilon(d)\) in
   \(Q_\varepsilon(d)H\), then
   \[
    \sup_{\varepsilon,d,\operatorname{Re}z\ge b_K}
    \|(z-C_{\varepsilon,d})^{-1}Q_\varepsilon(d)\|<\infty,
    \tag{3.7}
   \]
   with the resolvent analytically continued through the selected
   eigenvalue, and
   \[
    \|e^{tB_\varepsilon(d)}Q_\varepsilon(d)\|
      \le C_Ke^{b_Kt},
    \qquad
    \|e^{-tB_\varepsilon(d)}P_\varepsilon(d)\|
      \le C_Ke^{-c_Kt}.
    \tag{3.8}
   \]

Since \(\lambda_\varepsilon(d)>0.167\) and the complement lies strictly
to the left of \(0.12\), each pointwise real-part separation is greater than
\(0.047\); the asserted uniform safe gap is the smaller value \(1/25\).

## 4. Proof obligations

The proof is divided into seven obligations.

| ID | Obligation | Admissible mechanism |
|---|---|---|
| K1 | joint strong convergence of the dissipative base resolvents and their adjoints on compact \((d,z)\)-sets | common \(H^2\) core, uniform multiplier estimates, finite nets |
| K2 | compact sandwiches converge in norm uniformly in \(d,z\) | norm-continuity and collective compactness of \(\{K_d\}\) |
| K3 | common contour, rank one, and (3.3) | Fredholm factor plus analytic cancellation of the base resolvent |
| K4 | (3.4) despite the domain jump | pair the viscous eigen-equation with a smooth inviscid left vector and move \(L\) onto that vector |
| K5 | reality, analyticity, anchor, conditioning, and \(d\)-derivative | reflection--conjugation symmetry, type-A analyticity, Riesz differentiation |
| K6 | (3.6)--(3.7) on an unbounded half-plane | high-imaginary and high-real resolvent bounds plus a compact rectangle |
| K7 | (3.8) | reduced-resolvent continuation and a vertical-line inverse-Laplace argument |

## 5. Forbidden shortcuts

The following implications are invalid and must not appear in the proof.

- Pointwise persistence in \(d\) does not imply a uniform viscosity threshold.
- Strong resolvent convergence alone does not imply norm convergence of Riesz
  projections.
- R0.73J's inviscid Evans nonvanishing is not a viscous Evans theorem.
- The small interval produced in R0.73F cannot be enlarged to \([0,1/450]\)
  without the new parameter-uniform argument.
- A spectral gap alone does not control a nonnormal complementary semigroup.
- A finite Fourier matrix cannot certify the continuous-domain singular limit.

## 6. Exact boundary

Even if K1--K7 close, this section does not prove nonselfadjoint adiabatic
tracking on a time interval of length \(D_*/\varepsilon\).  It also does not
prove a two-sided matching action, a nonlinear instability, a three-dimensional
closure, finite-time blow-up, or the Clay regularity problem.  Those remain
separate gates.
