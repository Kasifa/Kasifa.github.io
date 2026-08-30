# R0.73L proof: uniform nonselfadjoint adiabatic tracking on the full slow window

**Status:** continuum proof closed; independent analytic and adversarial
audits PASS

**Window:** \(0\le s\le d\le D_*:=1/450\)

## 1. Statement

Let

\[
 B_\varepsilon(d)=\widetilde A(d)-\varepsilon L,
 \qquad D(B_\varepsilon(d))=H^2_{\rm per},
 \tag{1.1}
\]

and let \(P_\varepsilon(d)\) be the rank-one Riesz projection constructed in
R0.73K, with \(Q_\varepsilon(d)=I-P_\varepsilon(d)\) and selected eigenvalue
\(\lambda_\varepsilon(d)\).  Write \(U_\varepsilon(d,s)\) for the evolution
of

\[
 \varepsilon\partial_d u=B_\varepsilon(d)u.
 \tag{1.2}
\]

Define

\[
 \Phi_\varepsilon(d,s)
 :=\frac1\varepsilon\int_s^d\lambda_\varepsilon(r)\,dr.
 \tag{1.3}
\]

There are \(0<\varepsilon_L\le\varepsilon_K\) and constants
\(0<c_L\le C_L<\infty\), independent of \(\varepsilon,d,s\), such that for
every \(0<\varepsilon\le\varepsilon_L\), every \(D\in[0,D_*]\), and every
unit vector \(h_\varepsilon(0)\in P_\varepsilon(0)H\),

\[
 c_Le^{\Phi_\varepsilon(D,0)}
 \le
 \|U_\varepsilon(D,0)h_\varepsilon(0)\|
 \le
 C_Le^{\Phi_\varepsilon(D,0)}.
 \tag{1.4}
\]

Since R0.73K proves

\[
 \sup_{d\le D_*}|\lambda_\varepsilon(d)-\lambda_0(d)|
 \le C_\lambda\varepsilon,
 \tag{1.5}
\]

(1.4) is equivalent, after changing its constants, to

\[
 c_L\exp\!\left(\frac1\varepsilon
          \int_0^D\lambda_0(r)\,dr\right)
 \le
 \|U_\varepsilon(D,0)h_\varepsilon(0)\|
 \le
 C_L\exp\!\left(\frac1\varepsilon
          \int_0^D\lambda_0(r)\,dr\right).
 \tag{1.6}
\]

Moreover, for every \(0\le s\le D\le D_*\),

\[
 \frac{\|U_\varepsilon(s,0)h_\varepsilon(0)\|}
      {\|U_\varepsilon(D,0)h_\varepsilon(0)\|}
 \le C_L\exp\!\left[-\frac1\varepsilon
                \int_s^D\lambda_0(r)\,dr\right].
 \tag{1.7}
\]

The vector-level relative tracking estimate also holds:

\[
 \|U_\varepsilon(D,0)h_\varepsilon(0)
      -U_{\varepsilon,P}^{\rm a}(D,0)h_\varepsilon(0)\|
 \le C_L\varepsilon e^{\Phi_\varepsilon(D,0)}.
 \tag{1.8}
\]

Thus the exact endpoint is \(O(\varepsilon)\) relative to the moving selected
line; it is not asserted to lie exactly in that line.

In the fast variable \(\theta=d/\varepsilon\), (1.4)--(1.7) apply at
\(0\le\theta\le D_*/\varepsilon\).

## 2. Uniform inputs and notation

All constants below are inherited from R0.73K or follow directly from the
explicit two-harmonic profile.  After reducing \(\varepsilon_K\) once, if
needed,

\[
 c_K:=0.16<\lambda_\varepsilon(d)<0.173,
 \qquad b_K:=0.12,
 \tag{2.1}
\]

\[
 \|P_\varepsilon(d)\|\le P_K:=\frac95,
 \qquad \|Q_\varepsilon(d)\|\le Q_K:=1+P_K,
 \qquad
 \|P_\varepsilon'(d)\|\le P_1,
 \tag{2.2}
\]

\[
 \|e^{tB_\varepsilon(d)}Q_\varepsilon(d)\|
 \le C_Ke^{b_Kt},
 \qquad
 \|e^{tB_\varepsilon(d)}\|\le e^{K_Kt},
 \tag{2.3}
\]

for all \(t\ge0\), and

\[
 \|B_\varepsilon(d)-B_\varepsilon(s)\|
 =\|\widetilde A(d)-\widetilde A(s)\|
 \le L_B|d-s|.
 \tag{2.4}
\]

The norm in (2.4) is the bounded-operator norm on \(H\).  No estimate of
\(L P_\varepsilon\), no graph-norm derivative of an eigenvector, and no
second derivative of \(P_\varepsilon\) is used.

For each fixed \(\varepsilon>0\), R0.73K also gives real-analytic dependence
of \(P_\varepsilon(d)\) on \(d\).  Hence
\(\mathcal K_\varepsilon=[P_\varepsilon',P_\varepsilon]\) is norm continuous.
Only its uniform norm bound is used below; no uniform bound on
\(P_\varepsilon''\) is introduced.

Riesz invariance from R0.73K also gives

\[
 P(d)D(B(d))\subset D(B(d)),\qquad
 Q(d)D(B(d))\subset D(B(d)),\qquad
 B(d)P(d)=P(d)B(d)
 \tag{2.5}
\]

on the common domain.  These domain facts, rather than a formal block matrix,
justify the selected and complementary restrictions below.

To reduce notation, the subscripts on \(B,P,Q,\lambda\) are suppressed inside
the proof.  Every bound remains uniform in \(\varepsilon\).

## 3. Evolution existence without a uniform graph norm

For each fixed positive \(\varepsilon\), the operators \(B(d)\) have the
common domain \(H^2_{\rm per}\).  For any fixed \(s\),

\[
 B(d)=B(s)+V_s(d),
 \qquad V_s(d):=\widetilde A(d)-\widetilde A(s)\in\mathcal B(H),
 \tag{3.1}
\]

and \(V_s\) is norm continuous.  The standard bounded-perturbation Dyson
construction based on \(e^{tB(s)}\) therefore gives the unique evolution for
(1.2).  The same argument applies after adding any bounded norm-continuous
operator to the generator.

This construction is used only at each fixed \(\varepsilon>0\).  Its uniform
estimates below come from (2.3)--(2.4), not from comparing the graph norms of
\(B_\varepsilon(0)\) as \(\varepsilon\downarrow0\).

## 4. Kato transport and the exact intertwining sign

Set

\[
 \mathcal K(d):=[P'(d),P(d)]
 =P'(d)P(d)-P(d)P'(d).
 \tag{4.1}
\]

Differentiating \(P^2=P\) gives

\[
 PP'P=0,
 \qquad P'=P'P+PP',
 \qquad [P,\mathcal K]=-P'.
 \tag{4.2}
\]

Consequently \(\mathcal K\) is off diagonal:

\[
 P\mathcal KP=0,
 \qquad Q\mathcal KQ=0,
 \qquad
 \|\mathcal K(d)\|\le\kappa_K:=2P_KP_1.
 \tag{4.3}
\]

Let \(U^{\rm a}(d,s)\) solve

\[
 \partial_dU^{\rm a}(d,s)
 =\left(\frac1\varepsilon B(d)+\mathcal K(d)\right)U^{\rm a}(d,s),
 \qquad U^{\rm a}(s,s)=I.
 \tag{4.4}
\]

On the common domain, \(PB=BP\), and (4.2) gives

\[
 P'+\left[P,\frac1\varepsilon B+\mathcal K\right]=0.
 \tag{4.5}
\]

Thus both \(P(d)U^{\rm a}(d,s)\) and
\(U^{\rm a}(d,s)P(s)\) solve the same initial-value problem.  By uniqueness,

\[
 \boxed{P(d)U^{\rm a}(d,s)=U^{\rm a}(d,s)P(s)},
 \qquad
 Q(d)U^{\rm a}(d,s)=U^{\rm a}(d,s)Q(s).
 \tag{4.6}
\]

No backward evolution of \(B(d)|_{Q(d)H}\) is used.

Let \(W(d,s)\) solve the bounded equation

\[
 \partial_dW(d,s)=\mathcal K(d)W(d,s),
 \qquad W(s,s)=I.
 \tag{4.7}
\]

Then

\[
 P(d)W(d,s)=W(d,s)P(s),
 \qquad
 \|W(d,s)^{\pm1}\|\le M_W:=e^{\kappa_KD_*}.
 \tag{4.8}
\]

Because \(B(d)P(d)=\lambda(d)P(d)\), the selected part of the adiabatic
evolution is exact:

\[
 U_P^{\rm a}(d,s)
 :=U^{\rm a}(d,s)P(s)
 =e^{\Phi_\varepsilon(d,s)}W(d,s)P(s).
 \tag{4.9}
\]

In particular,

\[
 \|U_P^{\rm a}(d,s)\|
 \le M_WP_Ke^{\Phi_\varepsilon(d,s)}.
 \tag{4.10}
\]

If \(h\in P(s)H\), then

\[
 M_W^{-1}e^{\Phi_\varepsilon(d,s)}\|h\|
 \le\|U_P^{\rm a}(d,s)h\|
 \le M_We^{\Phi_\varepsilon(d,s)}\|h\|.
 \tag{4.11}
\]

## 5. A fixed-fast-time block contracts the moving complement

The next lemma is the central point.  It turns the frozen estimate (2.3) into
a non-autonomous estimate without invoking \(P''\) or a singular graph norm.

### Lemma 5.1 (one-block relative contraction)

There are a finite \(T>0\) and \(\varepsilon_B>0\), independent of the block
start \(s\), such that whenever
\(0<\varepsilon\le\varepsilon_B\) and
\(s+\varepsilon T\le D_*\),

\[
 \|U^{\rm a}(s+\varepsilon T,s)Q(s)\|
 \le\frac12e^{\Phi_\varepsilon(s+\varepsilon T,s)}.
 \tag{5.1}
\]

#### Proof

Choose \(T\) so large that

\[
 C_Ke^{-(c_K-b_K)T}\le\frac14.
 \tag{5.2}
\]

This is possible because \(c_K-b_K=1/25\).  In the fast coordinate
\(0\le\tau\le T\), set

\[
 V_s(\tau):=U^{\rm a}(s+\varepsilon\tau,s).
 \tag{5.3}
\]

It solves

\[
 \partial_\tau V_s(\tau)
 =[B(s)+E_s(\tau)]V_s(\tau),
 \tag{5.4}
\]

where

\[
 E_s(\tau)
 =B(s+\varepsilon\tau)-B(s)
  +\varepsilon\mathcal K(s+\varepsilon\tau),
 \qquad
 \|E_s(\tau)\|\le\varepsilon E_T,
 \tag{5.5}
\]

with \(E_T:=L_BT+\kappa_K\).  Variation of constants and (2.3) give

\[
 \|V_s(\tau)\|
 \le e^{(K_K+\varepsilon E_T)\tau}.
 \tag{5.6}
\]

For \(x\in Q(s)H\), a second use of variation of constants yields

\[
 \begin{aligned}
 \|V_s(T)x-e^{TB(s)}x\|
 &\le \varepsilon E_T
       \int_0^T e^{K_K(T-r)}
       e^{(K_K+\varepsilon E_T)r}\,dr\,\|x\|\\
 &\le \delta_T(\varepsilon)\|x\|,
 \end{aligned}
 \tag{5.7}
\]

where

\[
 \delta_T(\varepsilon)
 :=\varepsilon E_TT e^{(K_K+\varepsilon E_T)T}
 \longrightarrow0.
 \tag{5.8}
\]

The frozen complementary estimate therefore implies, as an operator on the
full space after precomposition with \(Q(s)\),

\[
 \|V_s(T)Q(s)\|
 \le C_Ke^{b_KT}+Q_K\delta_T(\varepsilon).
 \tag{5.9}
\]

Meanwhile \(\lambda_\varepsilon\ge c_K\), so

\[
 e^{\Phi_\varepsilon(s+\varepsilon T,s)}\ge e^{c_KT}.
 \tag{5.10}
\]

Choose \(\varepsilon_B\) small enough that
\(Q_Ke^{-c_KT}\delta_T(\varepsilon)\le1/4\).  Equations
(5.2), (5.9), and (5.10) prove (5.1).  By (4.6), the endpoint of the block
lies exactly in \(Q(s+\varepsilon T)H\), so the estimate can be iterated.
Replace \(\varepsilon_B\) by \(\min\{\varepsilon_B,1\}\); this harmless
normalization is used in the explicit remainder-block constant below.
\(\square\)

### Lemma 5.2 (relative moving-complement evolution)

There are \(M_Q<\infty\) and \(\gamma_Q>0\), independent of
\(\varepsilon,d,s\), such that

\[
 \boxed{
 \|U_Q^{\rm a}(d,s)\|
 \le M_Qe^{\Phi_\varepsilon(d,s)}
          e^{-\gamma_Q(d-s)/\varepsilon}},
 \tag{5.11}
\]

where \(U_Q^{\rm a}(d,s):=U^{\rm a}(d,s)Q(s)\).

#### Proof

For a final block of fast length \(0\le r<T\), the same frozen variation
argument as in (5.6) gives, after increasing a constant,

\[
 \|U^{\rm a}(s+\varepsilon r,s)\|
 \le M_0e^{\Phi_\varepsilon(s+\varepsilon r,s)},
 \tag{5.12}
\]

where one may take

\[
 M_0=\exp[(K_K+E_T+c_K)T].
 \tag{5.13}
\]

Write \((d-s)/\varepsilon=nT+r\) with \(n\in\mathbb N_0\) and
\(0\le r<T\).  Exact intertwining (4.6), the evolution law, (5.1), and
(5.12) give

\[
 \|U_Q^{\rm a}(d,s)\|
 \le M_0\,2^{-n}e^{\Phi_\varepsilon(d,s)}.
 \tag{5.14}
\]

Since

\[
 2^{-n}\le2\exp\!\left[-\frac{\log2}{T}
                   \frac{d-s}{\varepsilon}\right],
 \tag{5.15}
\]

(5.11) follows with

\[
 M_Q:=2M_0,
 \qquad \gamma_Q:=\frac{\log2}{T}.
 \tag{5.16}
\]

Only forward evolution and bounded perturbations occur in this proof.
\(\square\)

## 6. Exact evolution as an off-diagonal Volterra system

The exact equation can be written as

\[
 \partial_du
 =\left(\frac1\varepsilon B+\mathcal K\right)u
  -\mathcal Ku.
 \tag{6.1}
\]

For the selected initial vector \(h=h_\varepsilon(0)\), variation of constants
against \(U^{\rm a}\) gives

\[
 u(d)=U^{\rm a}(d,0)h
 -\int_0^dU^{\rm a}(d,s)\mathcal K(s)u(s)\,ds.
 \tag{6.2}
\]

Set

\[
 p(d):=P(d)u(d),
 \qquad q(d):=Q(d)u(d).
 \tag{6.3}
\]

Using (4.3) and (4.6), (6.2) splits exactly into

\[
 p(d)=U_P^{\rm a}(d,0)h
 -\int_0^dU_P^{\rm a}(d,s)P(s)\mathcal K(s)q(s)\,ds,
 \tag{6.4}
\]

\[
 q(d)=-\int_0^dU_Q^{\rm a}(d,s)Q(s)\mathcal K(s)p(s)\,ds.
 \tag{6.5}
\]

This is the place where the rank-one selected block and moving-complement
decay meet.  There is no term that couples \(p\) directly back into \(p\) or
\(q\) directly back into \(q\), because \(\mathcal K\) is off diagonal.

Define the action-normalized suprema

\[
 X_D:=\sup_{0\le d\le D}
       e^{-\Phi_\varepsilon(d,0)}\|p(d)\|,
 \qquad
 Y_D:=\sup_{0\le d\le D}
       e^{-\Phi_\varepsilon(d,0)}\|q(d)\|.
 \tag{6.6}
\]

Lemma 5.2 and (6.5) imply

\[
 \begin{aligned}
 e^{-\Phi_\varepsilon(d,0)}\|q(d)\|
 &\le M_Q\kappa_K
   \int_0^d e^{-\gamma_Q(d-s)/\varepsilon}
       e^{-\Phi_\varepsilon(s,0)}\|p(s)\|\,ds\\
 &\le \frac{M_Q\kappa_K}{\gamma_Q}\varepsilon X_D.
 \end{aligned}
 \tag{6.7}
\]

Hence

\[
 Y_D\le C_Q\varepsilon X_D,
 \qquad C_Q:=\frac{M_Q\kappa_K}{\gamma_Q}.
 \tag{6.8}
\]

The selected formula (4.9), (4.11), and (6.4) give

\[
 e^{-\Phi_\varepsilon(d,0)}\|p(d)\|
 \le M_W+M_WP_K\kappa_KD_*Y_D,
 \tag{6.9}
\]

and, by the reverse triangle inequality,

\[
 e^{-\Phi_\varepsilon(d,0)}\|p(d)\|
 \ge M_W^{-1}-M_WP_K\kappa_KD_*Y_D.
 \tag{6.10}
\]

Combining (6.8)--(6.9), choose \(\varepsilon_L\le\varepsilon_B\) so small
that

\[
 M_WP_K\kappa_KD_*C_Q\varepsilon_L\le\frac12.
 \tag{6.11}
\]

Then \(X_D\le2M_W\) for every \(D\le D_*\), and therefore

\[
 Y_D\le2C_QM_W\varepsilon.
 \tag{6.12}
\]

Decrease \(\varepsilon_L\) once more so that

\[
 4M_W^3P_K\kappa_KD_*C_Q\varepsilon_L\le1.
 \tag{6.13}
\]

Equation (6.10) now gives the pointwise lower bound

\[
 e^{-\Phi_\varepsilon(d,0)}\|p(d)\|
 \ge\frac1{2M_W}.
 \tag{6.14}
\]

Equations (6.4), (6.12), and (4.10) also give

\[
 e^{-\Phi_\varepsilon(d,0)}
 \|p(d)-U_P^{\rm a}(d,0)h\|
 \le C\varepsilon.
 \tag{6.14a}
\]

Combining this with (6.12) proves the vector estimate (1.8).

Together with (6.9) and (6.12),

\[
 \|u(d)\|
 \le\|p(d)\|+\|q(d)\|
 \le C_Le^{\Phi_\varepsilon(d,0)}.
 \tag{6.15}
\]

For the lower bound, no angle estimate between \(p\) and \(q\) is needed:

\[
 \|p(d)\|=\|P(d)u(d)\|
 \le P_K\|u(d)\|.
 \tag{6.16}
\]

Thus (6.14) implies

\[
 \|u(d)\|\ge\frac1{2M_WP_K}
 e^{\Phi_\varepsilon(d,0)}.
 \tag{6.17}
\]

Equations (6.15) and (6.17) prove (1.4).

## 7. Inviscid action and backward localization

By (1.5), for every \(0\le s\le d\le D_*\),

\[
 \left|\Phi_\varepsilon(d,s)
 -\frac1\varepsilon\int_s^d\lambda_0(r)\,dr\right|
 \le C_\lambda(d-s)\le C_\lambda D_*.
 \tag{7.1}
\]

Absorbing \(e^{C_\lambda D_*}\) into the two constants converts (1.4) into
(1.6).

Apply the upper half of (1.4) at time \(s\) and the lower half at time
\(D\).  Their quotient is bounded by

\[
 C\exp[-\Phi_\varepsilon(D,s)].
 \tag{7.2}
\]

Using (7.1) once more gives (1.7).  This argument never evolves the stable
complement backward.

## 8. Result ledger and exact boundary

The independent analytic audit and the adversarial audit have passed, so the proof closes

```text
commonDomainEvolution=CLOSED
katoIntertwining=CLOSED
movingComplementRelativeStability=CLOSED
nonselfadjointAdiabaticTracking=CLOSED
matchingSelectedGainAction=CLOSED
actionResolvedBackwardLocalization=CLOSED
explicitAdiabaticThreshold=OPEN
prefactorLimit=OPEN
twoTermWKB=OPEN
nonlinearNavierStokes=OPEN
threeDimensionalClosure=OPEN
Clay=OPEN
```

The constants in the theorem are existential because \(C_K,K_K,P_1,L_B\)
were sealed qualitatively upstream.  No finite-dimensional computation can
make \(\varepsilon_L\) explicit without a new quantitative continuum audit.
