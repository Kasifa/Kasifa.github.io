# R0.73X pressure-tail independent audit

**Audit date:** 2026-09-01

**Audited source:** `research/r073x_exterior_tail_freeze.md`

**Audited source SHA-256:**
`155f5937a668dfd959ea833c43365bad74742dd8fc2707360347b9f4c56403cd`

**Scope:** Sections 4--6, together with Sections 1--3 definitions used by
(5.7) and (6.3)

**Verdict:** `FAIL_AS_WRITTEN / PASS_AFTER_LISTED_CORRECTIONS`

**DGX used:** false

The mathematical pressure-tail mechanism is sound: the torus pressure admits
the asserted local/free-space split, the gauge cancels, the far kernel is
absolutely summable, the dimensions of \(\Lambda_R\), \(\mathcal H_u\),
\(\mathcal G_{u,p}\), (5.7), and (6.3) agree, and the core--exterior covariance
pair is present with the correct multiplicity.  The current text nevertheless
fails a publication-level audit for two required reasons:

1. (3.8c), which is part of the stated derivation of (3.9) and hence (6.3), is
   false as typeset: it juxtaposes the core and exterior contributions as a
   product instead of adding them;
2. the theorem-level quantifiers omit the ambient time interval condition
   needed to define \(\mathcal E^\square(z_0,4R)\), and the exact equivalence
   between the periodic pressure multiplier and the lifted free-space kernel
   in (4.6) is asserted but not proved or formulated distributionally.

These are repairable defects.  I found no counterexample to (5.7) or (6.3)
after making the corrections below.

---

## 1. Required quantifier freeze

Before Sections 4--6 are stated as suitable-weak results, insert one common
quantifier block.  A sufficient version is:

\[
 \nu>0,\qquad 0<\theta\le1,\qquad 0<R<\pi/8,
 \qquad I_{4R}^{\square}\Subset(0,T),
 \quad \square\in\{\mathrm{std},\nu\}.
\tag{A1}
\]

Let \((u,p)\) be a periodic suitable weak solution on
\(\mathbb T^3\times(0,T)\), with

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1,
 \qquad p\in L^{3/2}_{t,x}.
\tag{A2}
\]

Every identity involving a fixed time is for almost every
\(t\in I_{4R}^{\square}\).  In (5.7)--(6.3), require

\[
 s:I_R^\square\to(0,\theta R^2]
 \quad\hbox{measurable a.e.},
 \qquad
 \eta_R\in W^{1,\infty}_0(B_R),
 \quad \|\nabla\eta_R\|_\infty\le C_\eta/R,
\tag{A3}
\]

and allow the constants to depend on the fixed cutoff constant \(C_\eta\).
Without \(I_{4R}^{\square}\subset(0,T)\), the right side of (6.3) is not even
defined for a solution specified only on \((0,T)\).  This is a quantifier
failure, not a failure of the inequality.

---

## 2. Torus/free-space pressure representation

### 2.1 Local split: PASS, after an explicit convention

Put \(F_{ij}=u_i u_j\).  On the torus,

\[
 -\Delta p=\partial_i\partial_jF_{ij}
\tag{A4}
\]

in distributions.  With the standard convention
\(\mathcal R_j=(-\Delta)^{-1/2}\partial_j\),

\[
 p_R^{\rm loc}=\mathcal R_i\mathcal R_j(\zeta_RF_{ij})
\tag{A5}
\]

satisfies
\(-\Delta p_R^{\rm loc}=\partial_i\partial_j(\zeta_RF_{ij})\).
Since \(\zeta_R=1\) on \(B_{3R}\),

\[
 h_R=p-p_R^{\rm loc},\qquad \Delta h_R=0\quad\hbox{in }B_{3R}
\tag{A6}
\]

is correct.  The Riesz convention must be stated because changing its sign
convention without changing (A5) would reverse the local pressure.

The standard near-pressure/harmonic-remainder structure is consistent with
[Jia--Šverák, equations surrounding their local split](https://arxiv.org/pdf/1204.0529)
and with the local harmonic components in
[Wolf, Corollary 6.5](https://arxiv.org/pdf/1611.01482) and
[Kwon, Definition 2.1 and Remark 2.3](https://arxiv.org/pdf/2104.03160).
Those papers support the decomposition mechanism; the exact periodic-lift
formula here should still be proved directly rather than attributed to a
whole-space theorem with different hypotheses.

### 2.2 Lifted kernel identity (4.6): TRUE, but proof insertion required

For publication-level exactness, insert the following lemma before (4.6).
For a.e. \(t\), the periodic pressure gradient with zero spatial mean is
represented, in distributions and then a.e., by

\[
 \partial_\ell p(t,x)
 =\operatorname{p.v.}\!\int_{\mathbb R^3}
   \partial_\ell K_{ij}(\widetilde x-y)
   \widetilde F_{ij}(t,y)\,dy,
\tag{A7}
\]

where
\(K_{ij}=\partial_i\partial_j(4\pi|\cdot|)^{-1}\).
One direct proof expands \(F\) in integer Fourier modes: for every
\(k\in\mathbb Z^3\setminus\{0\}\), both sides have multiplier

\[
 -\,i\,\frac{k_\ell k_i k_j}{|k|^2},
\tag{A8}
\]

while the zero mode is zero.  Approximation in \(L^{3/2}(\mathbb T^3)\)
then yields the distributional identity.  Equivalently, one may start from
the periodic Green function and unfold its differentiated lattice sum.

Subtracting the compactly supported operator (A5) cancels the principal-value
singularity because \(1-\zeta_R\) vanishes on \(B_{3R}\).  Thus, for
\(x\in B_{2R}\),

\[
 \nabla h_R(t,x)=\int_{\mathbb R^3}\nabla K_{ij}(x-y)
 (1-\zeta_R(y))\widetilde F_{ij}(t,y)\,dy
\tag{A9}
\]

is an ordinary absolutely convergent integral.  Its far convergence follows
from

\[
 |\nabla K(z)|\lesssim |z|^{-4},\qquad
 \sum_{n\in\mathbb Z^3\setminus\{0\}}|n|^{-4}<\infty.
\tag{A10}
\]

The gauge-free difference formula (4.6a) is also correct; its kernel gains
one power by the mean-value theorem.  This agrees with the far-field kernel
difference in
[Bradshaw--Tsai, equations (1.5)--(1.8)](https://arxiv.org/pdf/2001.11526).
Bradshaw--Tsai also warn that such an expansion is not automatic for every
nondecaying whole-space distributional solution.  That obstruction does not
invalidate (A7): here periodicity excludes a spatially linear pressure, and
the periodic Poisson solution is unique modulo a function of time.  The note
should say this explicitly.

### 2.3 Gauge: PASS

The choice

\[
 c_R(t)=(h_R(t,\cdot))_{B_{2R}}
\tag{A11}
\]

is valid and gauge covariant.  Under \(p\mapsto p+C(t)\), one has
\(h_R\mapsto h_R+C(t)\) and \(c_R\mapsto c_R+C(t)\); hence every occurrence
of \(p-c_R\), every pressure difference in (5.2), and \(Q_s\) is unchanged.
At the stated integrability level, \(c_R\in L^{3/2}(I_R^\square)\) follows
from Jensen on \(B_{2R}\), because both \(p\) and \(p_R^{\rm loc}\) belong
locally to \(L^{3/2}\).

---

## 3. \(\Lambda_R\), \(\mathcal H_u\), convergence, and scaling

### 3.1 Pointwise tail estimate: PASS

For \(x\in B_{2R}\), the part of the first annulus on which
\(1-\zeta_R\ne0\) is at least distance \(R\) from \(x\); for \(m\ge2\),
the distance is comparable to \(2^mR\).  Therefore (A9) gives

\[
 \|\nabla h_R(t)\|_{L^\infty(B_{2R})}
 \lesssim
 \sum_{m\ge1}(2^mR)^{-4}
 \int_{A_m(R)}|\widetilde u(t,y)|^2\,dy.
\tag{A12}
\]

With

\[
 \Lambda_R(t)=R\sum_{m\ge1}(2^mR)^{-4}
 \int_{A_m(R)}|\widetilde u(t,y)|^2\,dy,
\tag{A13}
\]

this is exactly \(R\|\nabla h_R\|_\infty\lesssim\Lambda_R\).  No annular
factor is missing.

### 3.2 Absolute convergence and finiteness: PASS

The periodic lift obeys

\[
 \int_{A_m(R)}|\widetilde u(t)|^2
 \lesssim [1+(2^mR)^3]\|u(t)\|_{L^2(\mathbb T^3)}^2.
\tag{A14}
\]

For the large annuli, the summand in (A13) is therefore
\(O(R(2^mR)^{-1})\|u(t)\|_2^2=O(2^{-m})\|u(t)\|_2^2\).
Thus \(\Lambda_R(t)<\infty\) a.e.; the energy essential supremum makes

\[
 \mathcal H_u^\square=R\int_{I_R^\square}\Lambda_R(t)^{3/2}\,dt
\tag{A15}
\]

finite for each fixed \(R>0\).

Using
\(|h_R-(h_R)_{B_{2R}}|\lesssim R\|\nabla h_R\|_\infty
\lesssim\Lambda_R\) and \(|B_{2R}|\simeq R^3\) gives

\[
 R^{-2}\int_{I_R^\square}\!\int_{B_{2R}}
 |h_R-(h_R)_{B_{2R}}|^{3/2}
 \lesssim R\int_{I_R^\square}\Lambda_R^{3/2}
 =\mathcal H_u^\square.
\tag{A16}
\]

Hence (4.10) has the correct power of \(R\).

### 3.3 Scale audit: PASS

Under \(u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x)\),

\[
 \Lambda_{R/\lambda}[u_\lambda](t)=
 \lambda^2\Lambda_R[u](\lambda^2t),
\tag{A17}
\]

so

\[
 (R/\lambda)\int
 \Lambda_{R/\lambda}[u_\lambda]^{3/2}\,dt
 =R\int\Lambda_R[u]^{3/2}\,dt.
\tag{A18}
\]

Thus \(\Lambda_R\) has pressure degree two and \(\mathcal H_u\) is
dimensionless.  The Gaussian payment has the same invariance because
\(R^{-2}\int(|u|^3+|p-c_R|^{3/2})\,dx\,dt\) is dimensionless and
\(\gamma_m(\theta)\) is dimensionless.  I found no missing \(R\)- or
\(\theta\)-power in these definitions.

---

## 4. Exact covariance pair split

### 4.1 Definition and integrability: PASS after one explicit line

Section 5 should first restate

\[
 Q_s=P_s(pu)-(P_sp)(P_su).
\tag{A19}
\]

At the energy level, local interpolation gives \(u\in L^3_{t,x}\) on every
finite cylinder.  Together with \(p-c_R\in L^{3/2}_{t,x}\), this yields
\((p-c_R)u\in L^1_{t,x}\).  Hence (A19) and its pair integral are defined
for a.e. \(t\) and every \(s>0\).  Moreover, Young's inequality gives an
integrable majorant for the pair integrand, so Fubini is legitimate.

For a probability measure \(d\Gamma\), direct expansion gives

\[
 \int pu\,d\Gamma-\int p\,d\Gamma\int u\,d\Gamma
 =\frac12\iint[p(y)-p(z)][u(y)-u(z)]\,d\Gamma(y)d\Gamma(z).
\tag{A20}
\]

Thus (5.2) is exact, including the factor \(1/2\).

### 4.2 Core--exterior multiplicity: PASS

Let \(C=C_R\), \(E=E_R\), and
\(Y=|u|^3+|p-c_R|^{3/2}\).  Because
\(\Omega_{\rm ext}=(E\times E)\cup(E\times C)\cup(C\times E)\), symmetry
and the factor \(1/2\) give the exact counting identity

\[
 \frac12\iint_{\Omega_{\rm ext}}[Y(y)+Y(z)]\,d\Gamma_y d\Gamma_z
 =\int_EY\,d\Gamma+\Gamma(E)\int_CY\,d\Gamma.
\tag{A21}
\]

Consequently (5.6) contains the core value paired with an exterior sample.
There is no missing factor two and no missing \(E\times E\) term.

On \(C\times C\), inserting \(p=p_R^{\rm loc}+h_R\) gives exactly the
three rows in (5.4).  For a fully auditable proof, add the two displayed
bounds

\[
 \begin{aligned}
 |Q_s^{\rm loc,cc}(x)|
 &\lesssim\int_C(|p_R^{\rm loc}|^{3/2}+|u|^3)\,d\Gamma_{s,x},\\
 |Q_s^{h,cc}(x)|
 &\lesssim\int_C(|h_R-c_R|^{3/2}+|u|^3)\,d\Gamma_{s,x}.
 \end{aligned}
\tag{A22}
\]

They follow from the same Young inequality as (5.5) and make transparent
where (4.10)--(4.11) enter.

---

## 5. Inequality (5.7)

**Verdict:** `PASS_UNDER_(A1)--(A3)`.

For \(x\in B_R\), the three kernel rows imply

\[
 \begin{aligned}
 \int_{B_R}|Q_s^{\rm ext}(x)|\,dx
 \lesssim{}&
 \sum_{m\ge1}\gamma_m(\theta)
 \int_{A_m(R)}Y(t,y)\,dy\\
 &+C_\theta\int_{B_{2R}}Y(t,y)\,dy.
 \end{aligned}
\tag{A23}
\]

The first term follows from
\(g_s(\widetilde x-y)\lesssim R^{-3}\gamma_m(\theta)\) and
\(|B_R|\simeq R^3\).  The second is precisely the second term in (A21).
For (A22), integration in \(x\) uses
\(\int_{B_R}g_s(\widetilde x-y)\,dx\le1\).

The outside normalization and cutoff contribute

\[
 \frac1R\|\nabla\eta_R\|_\infty\lesssim R^{-2}.
\tag{A24}
\]

Thus the annular part of (A23) is exactly paid by
\(\mathcal G_{u,p}\); the core pressure is paid by (4.10)--(4.11), and the
core velocity by \(R^{-2}\int_{B_{4R}}|u|^3\).  This proves (5.7), with a
constant depending on \(\theta\) and the fixed cutoff constant.  There is no
unjustified estimate of \(pu\) beyond
\(L^{3/2}\cdot L^3\subset L^1\), and no hidden replacement of the original
covariance by a different pressure projection.

---

## 6. Inequality (6.3)

### 6.1 Local interpolation: PASS

The scaled local Gagliardo--Nirenberg inequality is

\[
 \|u(t)\|_{L^3(B_{4R})}^3
 \lesssim
 \|u(t)\|_2^{3/2}
 \bigl(\|\nabla u(t)\|_2+R^{-1}\|u(t)\|_2\bigr)^{3/2}.
\tag{A25}
\]

Hölder in time gives (6.1a).  From the definition of
\(\mathcal E^\square(z_0,4R)\),

\[
 \operatorname*{ess\,sup}\|u\|_2^2\lesssim R\mathcal E^\square,
 \qquad
 \int\|\nabla u\|_2^2\lesssim R\nu^{-1}\mathcal E^\square,
\tag{A26}
\]

and the lower-order term has the same \(R\)-degree.  Since
\(|I_R^{\rm std}|=R^2\) and \(|I_R^\nu|=R^2/\nu\), this yields

\[
 R^{-2}\int_{I_R^\square}\!\int_{B_{4R}}|u|^3
 \lesssim C_\nu\,[\mathcal E^\square(z_0,4R)]^{3/2}.
\tag{A27}
\]

The power \(R^{-2}\), exponent \(3/2\), and allowed fixed-viscosity
dependence are correct.

### 6.2 Required correction to (3.8c)

As printed, (3.8c) is dimensionally and algebraically false because it
multiplies the core and exterior integrals.  Replace it by

\[
 \boxed{
 \begin{aligned}
 \int_{B_R}|v_s(x)|^3\,dx
 &\le\int_{B_R}P_s(|u|^3)(x)\,dx\\
 &\le\int_{B_{2R}}|u(y)|^3\,dy
 +C\sum_{m\ge1}\gamma_m(\theta)
       \int_{A_m(R)}|\widetilde u(y)|^3\,dy.
 \end{aligned}}
\tag{A28}
\]

The first line is Jensen.  In the second, the core kernel integrates to at
most one in \(x\), while on each annulus
\(g_s\lesssim R^{-3}\gamma_m\) and \(|B_R|\simeq R^3\).  With (A28), the
proof of (3.9) is valid.  Without this correction, the written derivation of
(6.3) is not valid even though the intended inequality is true.

### 6.3 Final combination: PASS after (A28) and the quantifier freeze

Corrected (3.9) pays the exterior centered-production row by the local cubic
term plus \(\mathcal G_u\).  Equation (5.7) pays the full pressure covariance
by the local cubic term plus
\(\mathcal G_u+\mathcal G_p+\mathcal H_u\).  Equation (A27) pays the local
cubic term.  Therefore

\[
 \begin{aligned}
 &R^{-1}\int_{I_R^\square}\!\int_{B_R}
 |\mathscr S_{s(t)}^{\rm ext}|
 +R^{-1}\int_{I_R^\square}\!\int_{B_R}
 |Q_{s(t)}\cdot\nabla\eta_R|\\
 &\qquad\lesssim C_{\theta,\nu,C_\eta}
 \left([\mathcal E^\square(z_0,4R)]^{3/2}
       +\mathcal A_{\rm ext}^\square(z_0,R;\theta)\right)
\end{aligned}
\tag{A29}
\]

holds for all quantifiers in (A1)--(A3).  The unsigned core
\(\mathscr S_s^{\rm core}\) is not on the left and is not silently
controlled.  This boundary in the source note is correct.

---

## 7. Exact correction list and release decision

The source can move from `FAIL_AS_WRITTEN` to `PASS` only after all of the
following are made explicit:

1. replace (3.8c) by the additive inequality (A28);
2. add \(I_{4R}^\square\Subset(0,T)\), a.e.-time language, measurable
   positive \(s(t)\), and a precise cutoff class;
3. state the Riesz-transform sign convention;
4. add the periodic Fourier/Green-function lemma (A7)--(A10), including why
   the whole-space parasitic-solution caveat does not apply to periodic
   pressure;
5. restate the definition (A19) before the pair formula and state
   \((p-c_R)u\in L^1\);
6. preferably display (A22) so the two core--core payments can be audited
   independently.

Items 1--5 are required.  Item 6 is expository but strongly recommended.
After those changes, Sections 4--6 support a **positive-scale absolute size
lemma only**.  They do not imply smallness, absorption, epsilon regularity,
or any Clay conclusion.

`NOT CLAY.`

---

## 8. Re-audit of the revised source

**Re-audit date:** 2026-09-01

**Revised source SHA-256:**
`9e2658713d4ffa5892a4a0365b3fa60429ffc4d3f9d0c20e1eafd091f2eb41b9`

**Re-audit verdict:**
`FAIL_AS_WRITTEN / ONE_KERNEL-DISTRIBUTION_CORRECTION_REMAINS`

The six corrections requested by the first audit were checked individually.
Five are complete.  The periodic Fourier/lift correction contains the right
Fourier multiplier and leads to the right far-field formula (4.6), but its
principal-value notation omits or obscures the contact terms at the kernel
origin.  That point must be repaired before the source receives a final
`PASS`.

### 8.1 Six-item checklist

| Required correction | Revised location | Result |
|---|---:|---|
| additive replacement of (3.8c) | lines 361--371 | `PASS` |
| common time, scale, measurability, and cutoff quantifiers | lines 109--152 | `PASS` |
| Riesz-transform convention and sign | lines 450--468 | `PASS` |
| periodic Fourier multiplier / lifted free-space lemma | lines 497--543 | `FAIL_AS_WRITTEN`; multiplier sign passes, kernel distribution notation does not |
| explicit definition and integrability of \(Q_s\) | lines 634--650 | `PASS` |
| separate core--core covariance bounds | lines 696--708 | `PASS` |

The revised (3.8c) is now the correct additive Jensen estimate.  The common
quantifiers include \(I_{4R}^{\square}\Subset(0,T)\), a.e.-time language,
measurable \(s(t)>0\), \(W^{1,\infty}_0\) cutoffs, and the cutoff-constant
dependence.  The convention

\[
 \widehat{\mathcal R_i f}(\xi)=i\xi_i|\xi|^{-1}\widehat f(\xi)
\tag{R1}
\]

implies

\[
 \widehat{\partial_\ell\mathcal R_i\mathcal R_jF_{ij}}(k)
 =-i\,{k_\ell k_i k_j\over|k|^2}\widehat F_{ij}(k),
 \qquad k\ne0.
\tag{R2}
\]

Thus the sign in revised (4.5b) is correct.

### 8.2 Remaining defect in (4.5a): contact terms

Let

\[
 G(x)={1\over4\pi|x|},
 \qquad
 K^0_{ij}(x)=\partial_i\partial_jG(x)\quad(x\ne0).
\tag{R3}
\]

The **full distributional** third derivative is not, without qualification,
the naive principal-value integral of the classical function
\(\partial_\ell K^0_{ij}\).  In three dimensions its contact-term formula is

\[
 \boxed{
 \partial_\ell\partial_i\partial_jG
 =\operatorname{p.v.}[\partial_\ell K^0_{ij}]
 -{1\over5}
  (\delta_{ij}\partial_\ell
   +\delta_{i\ell}\partial_j
   +\delta_{j\ell}\partial_i)\delta_0.}
\tag{R4}
\]

The coefficient is checked immediately by tracing \(i=j\): the classical
kernel has zero trace away from the origin, while (R4) gives
\(-\partial_\ell\delta_0=\partial_\ell\Delta G\), as required.  Fourier
transformation of the **complete** distribution in (R4), not of the bare
classical principal-value kernel alone, gives (R2).

Accordingly, revised (4.5a),

\[
 \partial_\ell p
 =\operatorname{p.v.}\int_{\mathbb R^3}
   \partial_\ell K_{ij}(\widetilde x-y)\widetilde F_{ij}(y)\,dy,
\tag{R5}
\]

is ambiguous and is false if `p.v.` is read as the ordinary principal value
of the pointwise kernel with no contact terms.  Approximation by
trigonometric polynomials proves convergence to the Fourier multiplier (R2)
only after the kernel is defined as the full tempered distribution.

### 8.3 Exact source correction

Replace (4.5a) by a distributional statement that does not identify the full
operator with a bare principal-value function, for example

\[
 \boxed{
 \partial_\ell p
 =\operatorname{Per}
   (\partial_\ell\partial_i\partial_jG)*_{\mathbb T^3}F_{ij}
 \quad\hbox{in }\mathcal D'(\mathbb T^3),}
\tag{R6}
\]

where `Per` denotes periodization of the full distribution in (R4).  State
that its nonzero Fourier multiplier is (R2).  Either display (R4), or say
explicitly that \(\partial_\ell\partial_i\partial_jG\) includes all
origin-supported contact terms and is **not** the naive principal value of
the classical kernel.

This correction leaves (4.6) unchanged.  Indeed, after subtraction of the
compact local pressure, the operator acts on

\[
 (1-\zeta_R)F,
\tag{R7}
\]

which vanishes identically in a neighborhood of every \(x\in B_{2R}\).
All contact terms in (R4) therefore vanish there, the principal-value
singularity disappears, and the remaining order \(-4\) far-field integral
is the ordinary absolutely convergent integral displayed in (4.6).

### 8.4 Recheck of (5.7), (6.3), and the claim boundary

Subject to the distributional correction (R6), the first audit's conclusions
about (5.7) and (6.3) remain unchanged:

1. \(Q_s\) is now explicitly gauge-centered and integrable;
2. the two core--core estimates are present;
3. the core--exterior pair has the correct multiplicity;
4. the \(R^{-2}\) payment generated by the outside \(R^{-1}\) normalization
   and \(\|\nabla\eta_R\|_\infty\lesssim R^{-1}\) is correct;
5. (6.3) controls only \(\mathscr S^{\rm ext}\) plus the pressure covariance;
   it does not absorb the unsigned characteristic core.

The added tent statement (6.5) is also only an absolute size estimate: its
\(s\)-integration is over positive scales \(0<s\le\theta R^2\) and does not
assert a pointwise trace at \(s=0\).  Sections 6, 9, and 10 explicitly retain
smallness, coercivity, epsilon regularity, global regularity, and the Clay
conclusion as open.

One claim-boundary wording should nevertheless be softened: Section 9 calls
\(\Lambda_R\) the "sharp" visible obstruction without proving an optimality
or saturation theorem.  Replace "sharp visible obstruction" by "explicit
visible obstruction" unless a separate sharpness construction is supplied.
This wording does not affect (5.7) or (6.3), but it should not survive a
publication claim audit.

### 8.5 Final re-audit decision

The revised manuscript is one local analytic correction away from passing.
After replacing (4.5a) by (R6), or equivalently adding the complete contact
terms (R4), and softening the unsupported word "sharp", the pressure-tail
proof can be marked:

`PASS_FOR_POSITIVE-SCALE_SIZE_ONLY`.

At the audited SHA, however, the final result remains:

`FINAL_REAUDIT_VERDICT=FAIL_AS_WRITTEN`.

`NOT CLAY.`

---

## 9. Final re-audit after the complete-distribution correction

**Final re-audit date:** 2026-09-01

**Final audited source SHA-256:**
**f16b610b9d264ed912bbeeb70df36b6ccd50dbfbda52f7fdc2344f8869a78a20**

**Final verdict:** **PASS_FOR_POSITIVE_SCALE_ABSOLUTE_SIZE_ONLY**

The source hash was read twice one second apart and was stable.  This final
re-audit supersedes the intermediate verdict in Section 8 while retaining it
as an audit trail.

### 9.1 Required-correction matrix

| Audit requirement | Final source evidence | Final result |
|---|---:|---|
| additive Jensen/core--exterior estimate (3.8c) | lines 361--371 | **PASS** |
| common ambient-time, a.e.-time, measurable-scale, and cutoff quantifiers | lines 109--152 | **PASS** |
| fixed Riesz sign convention | lines 450--468 | **PASS** |
| periodic Fourier multiplier and lifted free-space representation | lines 490--566 | **PASS** |
| gauge-centered definition and \(L^1\) integrability of \(Q_s\) | Section 5, equations (5.0)--(5.2) | **PASS** |
| separately auditable local-pressure and harmonic core--core bounds | equation (5.4a) | **PASS** |
| origin contact terms distinguished from the off-diagonal kernel | lines 493--508 and 546--566 | **PASS** |
| unsupported sharpness wording removed | Section 9, “an explicit visible obstruction” | **PASS** |

### 9.2 Final multiplier and contact-term check

The frozen convention

\[
 \widehat{\mathcal R_i f}(k)=i{k_i\over|k|}\widehat f(k)
\tag{F1}
\]

gives

\[
 \widehat{\partial_\ell\mathcal R_i\mathcal R_jF_{ij}}(k)
 =-i\,{k_\ell k_i k_j\over|k|^2}\widehat F_{ij}(k),
 \qquad k\ne0.
\tag{F2}
\]

The final Lemma 4.1 no longer identifies this multiplier with a naive
principal-value function.  It defines

\[
 \mathcal T_{\ell ij}
 =\partial_\ell\partial_i\partial_j(4\pi|\cdot|)^{-1}
 \quad\hbox{in }\mathcal D'(\mathbb R^3)
\tag{F3}
\]

as the complete distribution, periodizes that distribution by the
coefficients (F2), and states the periodic pressure identity in
\(\mathcal D'(\mathbb T^3)\).  This includes the origin-supported contact
terms discussed in (R4).

After subtracting the complete local operator, the remaining source
\((1-\zeta_R)F\) vanishes on \(B_{3R}\).  Hence, for every evaluation point in
\(B_{2R}\), all origin-supported terms vanish and the distribution reduces to
the classical order \(-4\) kernel away from the diagonal.  This justifies
(4.6) as an ordinary absolutely convergent integral.  The sign, gauge,
periodization, local subtraction, and convergence mechanisms are mutually
consistent.

### 9.3 Final check of (5.7) and (6.3)

The proof chain now has no missing row:

1. the pair identity has its exact factor \(1/2\);
2. \(\Omega_{\rm ext}\) contributes
   \(\int_EY\,d\Gamma+\Gamma(E)\int_CY\,d\Gamma\), so the core value in an
   exterior pair is retained exactly once;
3. the two core--core terms are paid separately by Calderón--Zygmund,
   harmonic oscillation, and local \(L^3\);
4. \(p-c_R\in L^{3/2}\) and \(u\in L^3\) give the required
   \((p-c_R)u\in L^1\);
5. the outside \(R^{-1}\) normalization and the cutoff gradient
   \(R^{-1}\) produce exactly the \(R^{-2}\) critical payment in (5.7);
6. corrected (3.8c), (3.9), (5.7), and (6.2) combine with no missing
   \(R\)- or \(\theta\)-power to give (6.3).

Thus (5.7) and (6.3) pass for every quantifier frozen in (1.2), (1.6)--(1.9).
The added tent estimate (6.5) also passes as an integral over positive heat
scales.

### 9.4 Non-overclaim boundary

The final source makes only the following proved claim:

\[
 \text{finite, scale-compatible absolute size at positive heat scale}.
\tag{F4}
\]

It does **not** obtain signed-to-absolute coercivity, smallness of
\(\mathcal A_{\rm ext}\), control by one local cylinder, a pointwise
\(s=0\) trace, epsilon regularity, exclusion of blow-up, global regularity, or
the Clay conclusion.  The unsigned descending-characteristic core remains
open.  These limitations are stated explicitly in Sections 3, 5, 6, 9, and
10 of the source.

The word “sharp” has been replaced by “explicit”, so the manuscript no longer
claims an unproved optimality theorem for \(\Lambda_R\).

### 9.5 Final release decision

For the exact source
**f16b610b9d264ed912bbeeb70df36b6ccd50dbfbda52f7fdc2344f8869a78a20**:

**FINAL_REAUDIT_VERDICT=PASS_FOR_POSITIVE_SCALE_ABSOLUTE_SIZE_ONLY**.

This PASS licenses the R0.73X pressure/exterior-tail **size lemma** for the
next independent certificate and release gate.  It does not license any
regularity or Millennium-problem claim.

**NOT CLAY.**
