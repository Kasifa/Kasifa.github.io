# R0.74S Step 11 — shared-budget recombination and the terminal-trace obstruction

## 0. Result and scope

Step 10 reduced the open full-terminal clock estimate to one combined
best-\(N\) tail supported on two disjoint residual mechanisms.  This note
does not prove that tail estimate.  It determines exactly how the two
mechanisms recombine, derives the strongest estimates presently available
for each one, and identifies the first genuinely new PDE statement that
would close the short branch.

There are four main conclusions.

1. The combined best-\(N\) residual is the exact discrete infimal
   convolution of the two branch tails.  Two independent branch theorems may
   therefore be pursued in parallel, provided their exception counts are
   added honestly.  Since the target asks only for some fixed finite count,
   two separately proved fixed counts would still suffice.
2. On the short non-\(D\) branch, the inherited cubic estimate yields a
   sharp inverse-duration coefficient.  Common terminal endpoints improve
   this to a nested-tent integral estimate and control every residual that
   persists to a fixed positive backward depth.  They do not control the
   terminal trace at depth zero.  A critical quadratic Carleson bound still
   has a logarithmic divergence.
3. On the scalar-excess branch, the stopped residual and the Step 8
   priority-selected excess are equivalent in best-\(N\): the literal
   coordinate constants are \(1/5\) and \(3\).  The inherited theory gives
   linear summability and fixed-solution tail tightness, but no uniform
   solution- and scale-independent count.
4. The existing smooth exact families refute the zero-exception route but
   do not refute a fixed positive exception count.  Their present
   multi-packet implementations pay too much cubic cost to establish the
   required counterexample ratio.  A precise \((N+1)\)-target falsification
   criterion is recorded for future designs.

Thus the remaining short-branch issue is not interval overlap but terminal
anti-concentration; the remaining excess-branch issue is not ancestry but a
uniform weighted packing theorem for that ancestry.  Neither theorem is
proved here.  No claim of novelty, singularity formation, regularity, or a
solution of the Millennium problem is made.  **NOT CLAY.**

## 1. Frozen setting and the two residual vectors

Retain every definition and convention of R0.74S Step 10.  In particular,
fix one admissible deterministic profile
\(\boldsymbol\lambda=(\lambda_k)_{k\ge1}\), independently of the solution,
\(R\), and the terminal time, with

\[
 \mathscr L(\boldsymbol\lambda)
 =\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3<\infty,
 \qquad A_R=(P_R^M)^{2/3}.
\]

Fix a local-energy good terminal time
\(\tau\in\mathcal G_R\cap\mathcal T_R\).  Write
\(T_k=K_{k,R}(\tau)\), let
\(\ell_k=\ell_{k,2/3}^K(\tau)\) be the canonical last exit, put
\(d_k=(\tau-\ell_k)/R^2\), and retain the Step 10 partition into four paid
classes and

\[
 \mathcal R_{\rm sh}
 =\mathcal I_{\neg D}\cap\mathcal I_{\rm short}
                         \cap\mathcal I_{Q-},
 \qquad
 \mathcal R_x=\mathcal I_x.
\]

Split the Step 10 residual into disjointly supported vectors

\[
 \boxed{
 r_k^{\rm sh}(\tau):=\mathbf1_{\mathcal R_{\rm sh}(\tau)}r_k(\tau),
 \qquad
 r_k^x(\tau):=\mathbf1_{\mathcal R_x(\tau)}r_k(\tau),
 \qquad r(\tau)=r^{\rm sh}(\tau)+r^x(\tau).}
\tag{S.248}
\]

All three vectors are nonnegative and belong to \(\ell^1\).  On either
residual support,

\[
 {T_k\over6}<r_k(\tau)<{T_k\over2}\le {v_{k,R}\over2}.
\]

## 2. Exact shared-budget recombination

For \(z\in\ell^1_+\), recall

\[
 \mathcal S_N(z)=\inf_{\#S\le N}\sum_{k\notin S}z_k.
\]

### Proposition 2.1 — discrete infimal convolution

If \(a,b\in\ell^1_+\) have disjoint supports, then for every integer
\(N\ge0\),

\[
 \boxed{
 \mathcal S_N(a+b)
 =\min_{0\le n\le N}
    \bigl[\mathcal S_n(a)+\mathcal S_{N-n}(b)\bigr].}
\tag{S.249}
\]

Indeed, every joint deletion set splits into its intersections with the two
supports.  Conversely, the union of two branch deletion sets is admissible
for the sum of their budgets.  Unused budget may be assigned to either
branch because \(\mathcal S_n\) is nonincreasing in \(n\).  For infinite
sequences, apply this finite-support argument to truncations and use
monotone convergence; equivalently, delete the \(N\) largest coordinates,
breaking ties by the shell index.

Define

\[
 \mathfrak R^{\rm sh}_{n,R}(\mathcal D)
 :=\sup_{\tau\in\mathcal D\cap\mathcal G_R}
      \mathcal S_n(r^{\rm sh}(\tau)),
 \qquad
 \mathfrak R^x_{n,R}(\mathcal D)
 :=\sup_{\tau\in\mathcal D\cap\mathcal G_R}
      \mathcal S_n(r^x(\tau)).
\]

Taking a terminal supremum in (S.249) gives the domain-safe inequality

\[
 \boxed{
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le\min_{0\le n\le N}
   \left[
    \mathfrak R^{\rm sh}_{n,R}(\mathcal D)
    +\mathfrak R^x_{N-n,R}(\mathcal D)
   \right].}
\tag{S.250}
\]

The pointwise formula is an equality.  Formula (S.250) need not be an
equality because a supremum and a finite minimum do not generally commute.
The optimizing split and the top-\(N\) shell set may depend on \(\tau\).
No measurability is needed because neither selector is integrated in time
or inserted as a local-energy test.

Suppose fixed integers \(N_{\rm sh},N_x\) and constants
\(C_{\rm sh},C_x\), independent of the solution and scale, satisfy the two
branch estimates on a domain \(\mathcal D\).  Put
\(N_0=N_{\rm sh}+N_x\).  Then (S.250) and Step 10 give

\[
 \boxed{
 \begin{gathered}
 \mathfrak R_{N_0,R}^{\boldsymbol\lambda}(\mathcal D)
 \le(C_{\rm sh}+C_x)A_R,\\
 \mathcal S^K_{N_0,R}(\mathcal D)
 \le\left[
 6C_Q+C_5\mathscr L(\boldsymbol\lambda)^{1/3}
       +6C_{\rm sh}+6C_x
 \right]A_R,\\
 \mathcal D=I_R\quad\Longrightarrow\quad
 \mathfrak C_R^M
 \le\sqrt{N_0}\,Z_R
 +\left[
 7C_Q+C_5\mathscr L(\boldsymbol\lambda)^{1/3}
       +6C_{\rm sh}+6C_x
 \right]A_R.
 \end{gathered}}
\tag{S.251}
\]

In particular, two independently proved best-\(N\) branch estimates imply
a best-\(2N\) combined estimate, not a best-\(N\) estimate.  This is not
fatal: the open statement (S.243) asks for some fixed finite \(N_0\).

The bookkeeping loss is real.  With \(a=(M,0)\), \(b=(0,M)\),

\[
 \boxed{
 \mathcal S_1(a)=\mathcal S_1(b)=0,
 \qquad \mathcal S_1(a+b)=M,
 \qquad \mathcal S_2(a+b)=0.}
\tag{S.252}
\]

Likewise, at two terminal states with
\((a,b)=(Me_1,e_2)\) and \((e_1,Me_2)\), the pointwise adaptive
one-exception split has worst value one, whereas either fixed branch
allocation has worst value \(M\).  Thus a theorem must not silently freeze
one allocation for all terminal times.

## 3. Short residual: the exact inverse-duration ledger

Put

\[
 \mathcal H_\tau:=\mathcal R_{\rm sh}(\tau),
 \qquad a_k:=2^{3k}\gamma_k,
 \qquad p_k:=p_{k,R}^{u,\eta}(J_k^{\rm LE}).
\]

For \(k\in\mathcal H_\tau\), non-\(D\) persistence gives
\(e_{k,R}(t)>T_k/6\) for almost every \(t\in J_k^{\rm LE}\).  Integrating
(R.214), using \(r_k<T_k/2\), and taking the power \(2/3\) gives

\[
 \boxed{
 d_k\left({T_k\over6}\right)^{3/2}
 <C_1a_k^{1/2}p_k,
 \qquad
 r_k^{\rm sh}
 <3C_1^{2/3}(a_kd_k^{-2})^{1/3}p_k^{2/3}.}
\tag{S.253}
\]

For a common exceptional set \(S\), finite-shell Hölder followed by
(R.211) yields

\[
 \sum_{k\in\mathcal H_\tau\setminus S}r_k^{\rm sh}
 \le3C_1^{2/3}C_P^{2/3}A_R
   \left(\sum_{k\in\mathcal H_\tau\setminus S}
                  a_kd_k^{-2}\right)^{1/3}.
\]

Consequently, with

\[
 \mathfrak D^{\rm sh}_N(\tau)
 :=\inf_{\#S\le N}
       \sum_{k\in\mathcal H_\tau\setminus S}a_kd_k^{-2},
\]

one has the exact sufficient interface

\[
 \boxed{
 \mathcal S_N(r^{\rm sh}(\tau))
 \le3C_1^{2/3}C_P^{2/3}
       \bigl(\mathfrak D_N^{\rm sh}(\tau)\bigr)^{1/3}A_R.}
\tag{S.254}
\]

This is not an estimate on \(\mathfrak D_N^{\rm sh}\).  It exposes the
inverse-square duration debt left by the inherited spatial Hölder bound.

## 4. Normalized depth and the logarithmic Carleson boundary

On the short branch define

\[
 h_k:=d_k\lambda_k^{3/2}\in(0,1),
 \qquad w_k:=a_k\lambda_k^3.
\]

Then

\[
 \boxed{
 w_kh_k^{-2}=a_kd_k^{-2}.
 \quad
 \mathcal H_j:=\{k\in\mathcal H_\tau:
                         2^{-j-1}\le h_k<2^{-j}\},
 \quad W_j:=\sum_{k\in\mathcal H_j}w_k
 \quad\Longrightarrow\quad
 \sum_j4^jW_j
 \le\sum_{k\in\mathcal H_\tau}w_kh_k^{-2}
                  \le4\sum_j4^jW_j.}
\tag{S.255}
\]

Thus changing the fixed admissible profile changes which shells are called
short, but it does not remove the inverse-duration debt on that branch.

Let

\[
 \mu_\tau:=\sum_{k\in\mathcal H_\tau}w_k\delta_{h_k}.
\]

Tonelli applied to
\(h^{-2}=1+2\int_h^1s^{-3}\,ds\) gives the exact layer-cake identity

\[
 \boxed{
 \sum_{k\in\mathcal H_\tau}w_kh_k^{-2}
 =\mu_\tau((0,1))
  +2\int_0^1s^{-3}\mu_\tau((0,s])\,ds.}
\tag{S.256}
\]

Hence a uniform bound
\(\mu_\tau((0,s])\le C_Ds^{2+\varepsilon}\), with
\(\varepsilon>0\), is sufficient for (S.254).  The critical exponent two
is not.

This failure occurs even with the frozen canonical profile
\(\lambda_k=1\).  Since
\(\gamma_k=\exp(-4^{k-1}/32)\), set
\(w_k=a_k=2^{3k}\gamma_k\) and, for all sufficiently large \(k\),
\(h_k=w_k^{1/2}<1\).  The ratio

\[
 {w_{k+1}\over w_k}
 =8\exp\left(-{3\cdot4^{k-1}\over32}\right)
\]

is eventually below \(1/2\).  Therefore the resulting atomic measure obeys
\(\mu((0,s])\le2s^2\), whereas

\[
 \boxed{
 \sum_{k\ge k_0}w_kh_k^{-2}
 =\sum_{k\ge k_0}1=\infty.}
\tag{S.257}
\]

This is the precise logarithmic endpoint obstruction.  It is a coefficient
and clock stress test, not a Navier--Stokes solution.

## 5. What common terminal endpoints really buy

For \(I\subset\mathcal H_\tau\), use normalized backward time
\(s=(\tau-t)/R^2\) and define

\[
 M_I(s):=\sum_{\substack{k\in I\\d_k>s}}r_k^{\rm sh},
 \qquad
 V_I(s):=\sum_{\substack{k\in I\\d_k>s}}a_k.
\]

Every last-exit interval has terminal endpoint \(\tau\), so its indicator
is exactly \(\mathbf1_{\{s<d_k\}}\).  On the active set,
\(r_k<3e_{k,R}(t)\).  Weighted Hölder gives

\[
 {M_I(s)^{3/2}\over V_I(s)^{1/2}}
 \le3^{3/2}
   \sum_{\substack{k\in I\\d_k>s}}
       {e_{k,R}(t)^{3/2}\over a_k^{1/2}}.
\]

Integrating in \(s\), applying (R.214), and then (R.211) proves the
nested-tent estimate

\[
 \boxed{
 \int_0^4{M_I(s)^{3/2}\over V_I(s)^{1/2}}\,ds
 \le3^{3/2}C_1
       \sum_{k\in I}p_k(J_k^{\rm LE})
 \le3^{3/2}C_1C_PP_R^M.}
\tag{S.258}
\]

The integrand is defined as zero when the active set is empty.  Prove the
formula first for finite \(I\), then use Fatou for a countable set.

Let

\[
 \mathscr A_0:=\sum_{k\ge1}a_k
 =\sum_{k\ge1}2^{3k}\gamma_k<\infty.
\]

For every \(0<\delta<4\), monotonicity of \(M_I\) on \((0,\delta)\)
and \(V_I\le\mathscr A_0\) give

\[
 \boxed{
 \sum_{\substack{k\in I\\d_k>\delta}}r_k^{\rm sh}
 \le3C_1^{2/3}C_P^{2/3}
       \mathscr A_0^{1/3}\delta^{-2/3}A_R.}
\tag{S.259}
\]

Thus every residual that survives to a fixed positive backward depth is
already quadratic.  The entire unresolved mass can concentrate in
\(d_k\downarrow0\), where an \(L^{3/2}\)-in-time tent bound has no terminal
trace.

Nesting alone cannot repair this.  Fix \(M>N\), \(R=1\), \(\tau=1\),
and choose
\[
 0<d_M<\cdots<d_1<1/2,
 \qquad d_k<\lambda_k^{-3/2}\quad(1\le k\le M),
 \qquad \sum_{k=1}^Md_ka_k^{-1/2}<\varepsilon.
\]
For \(1\le k\le M\), set \(Q_k=D_k=0\), \(F_k=K_k\), and

\[
 K_k(t)=
 \begin{cases}
 0,&t\le1-2d_k,\\
 2(t-1+2d_k)/d_k,&1-2d_k<t\le1-d_k,\\
 2+(t-1+d_k)/d_k,&1-d_k<t\le1.
 \end{cases}
\]

Set \(E_k=e_k=K_k\).  Then the zero-start clock identity
\(K_k=E_k+D_k=Q_k+F_k\) holds,
\(T_k=3\), \(\ell_k=1-d_k\), \(r_k=1\), and all last-exit
intervals are strictly nested.  The abstract cubic density
\[
 \pi_k(t):={e_k(t)^{3/2}\over C_1a_k^{1/2}}
\]
saturates (R.214), and
\(\sum_k\int\pi_k=O(\sum_kd_ka_k^{-1/2})\) can be made arbitrarily small.
The absolute flux ledger still requires a parameter \(P_M\asymp M\), so

\[
 \boxed{
 \mathcal S_N(r)=M-N,
 \qquad A_M:=P_M^{2/3}\asymp M^{2/3},
 \qquad Z_M=3\sqrt M.}
\tag{S.260}
\]

No bound of the target form follows from these abstract ledgers.  This is a
continuous clock/payment witness, not an NSE solution.

### A sufficient new short-branch PDE lemma

A more natural target than the raw inverse-duration moment is an
amplitude-sensitive terminal anti-concentration statement: find fixed
\(N_{\rm sh}\), \(0<\delta_*<4\), \(0\le\theta_*<1\), and
\(C_{\rm nc}<\infty\), all solution- and scale-independent, such that at
every good terminal there is one set \(S_\tau\),
\(\#S_\tau\le N_{\rm sh}\), for which

\[
 \boxed{
 \sum_{\substack{k\in\mathcal H_\tau\setminus S_\tau\\d_k\le\delta_*}}
        r_k^{\rm sh}
 \le\theta_*
   \sum_{k\in\mathcal H_\tau\setminus S_\tau}r_k^{\rm sh}
   +C_{\rm nc}A_R.
 \quad\textbf{OPEN}}
\tag{S.261}
\]

Combining (S.261) with (S.259) would give

\[
 \mathcal S_{N_{\rm sh}}(r^{\rm sh}(\tau))
 \le{C_{\rm nc}
 +3C_1^{2/3}C_P^{2/3}\mathscr A_0^{1/3}\delta_*^{-2/3}
 \over1-\theta_*}\,A_R.
\]

The implication is proved; the boxed hypothesis is not.  It asks the PDE to
prevent a nonquadratic fraction of the tail from being created entirely in
the last \(\delta_*R^2\) units of time.

## 6. Scalar excess: an exact best-\(N\) equivalence

Retain the Step 8 scalar excess

\[
 x_k(\tau)
 =\left[D_{k,R}(\tau)-\beta_{k,R}(J_\tau)
                    -2\lambda_k\sigma_{k,R}(J_\tau)\right]_+
\]

and put \(x_k^{\rm sel}=\mathbf1_{\mathcal I_x}x_k\).  On
\(\mathcal I_x\), write \(q_k=\Delta Q_k\).  The failed priority tests and
the terminal clock identity give

\[
 |q_k|\le\beta_k<T_k/6,
 \quad 2\lambda_k\sigma_k\le T_k/6,
 \quad T_k/2\le D_k\le T_k,
 \quad r_k^x=T_k/3-q_k.
\]

The upper comparison follows from \(x_k>T_k/6\) and \(r_k<T_k/2\).
For the lower comparison, \(x_k\le T_k-\beta_k\), and

\[
 5r_k-x_k\ge {2T_k\over3}-5q_k+\beta_k>0
\]

whether \(q_k\ge0\) or \(q_k<0\).  Therefore

\[
 \boxed{
 {1\over5}x_k^{\rm sel}<r_k^x<3x_k^{\rm sel}
 \quad(k\in\mathcal I_x),}
\tag{S.262}
\]

with both vectors zero off \(\mathcal I_x\).  The constants are sharp at
the scalar-constraint level: approach
\((q,\beta,D,2\lambda\sigma)=(T/6,T/6,T,0)\) for \(1/5\), and
\((-T/6,T/6,T/2,T/6)\) for \(3\).

Optimizing the same exceptional set gives

\[
 \boxed{
 {1\over5}\mathcal S_N(x^{\rm sel}(\tau))
 \le\mathcal S_N(r^x(\tau))
 \le3\mathcal S_N(x^{\rm sel}(\tau)),}
\tag{S.263}
\]

and the same inequalities after taking the good-terminal supremum on either
terminal domain.  This is an exact reduction of the \(\mathcal R_x\) gate,
not its closure.

Step 8 gives the ancestor vector

\[
 b_k(\tau):=\mathbf1_{\mathcal I_x(\tau)}
 \left[m_{k,R}(\tau)+\int_{H_{k,R}}g_{k,R}(t)\,dt\right].
\]

The proved comparisons are

\[
 \boxed{
 r_k^x\le3x_k^{\rm sel}\le3b_k,
 \qquad
 \sum_kx_k^{\rm sel}\le CP_R^M,
 \qquad
 \sum_kb_k\le\sum_kv_{k,R}
       \le C(A_R+P_R^M).}
\tag{S.264}
\]

The first ancestor is anomalous defect or high-Rayleigh viscous
dissipation.  The estimates are only linear when \(P_R^M>1\), and Markov
counting therefore cannot produce a universal quadratic best-\(N\) tail.

There is nevertheless genuine, nonuniform compactness.  Since
\(r_k^x(\tau)\le v_{k,R}/2\) and \((v_{k,R})\in\ell^1\), for each fixed
solution, fixed \(R\), and \(\varepsilon>0\), one may choose a prefix size
\(N=N(u,R,\varepsilon)\), independent of \(\tau\), such that

\[
 \boxed{
 \sup_{\tau\in\mathcal G_R\cap\mathcal D}
      \mathcal S_N(r^x(\tau))
 \le{1\over2}\sum_{k>N}v_{k,R}<\varepsilon.}
\tag{S.265}
\]

The missing quantifier is exactly uniformity of \(N\) and a rate
\(O(A_R)\) independent of the solution and scale.

## 7. Why ancestry cannot be localized to the last-exit interval

The following rational scalar clocks isolate two forbidden shortcuts.  They
satisfy the displayed clock and threshold algebra but are not asserted to
come from Navier--Stokes solutions.

Normalize \(R^2=\lambda=1\), \(s_R=0\), \(\tau=2\), and \(T=1\).  Let
\(h=0\) on \([0,9/10]\), then set

\[
 h(t)=
 \begin{cases}
 {2\over3}(t-9/10),&9/10<t\le1,\\
 {1\over15}+{t-1\over300},&1<t\le39/20,\\
 {419\over6000}+{1981\over300}(t-39/20),&39/20<t\le2.
 \end{cases}
\]

For a pure-defect row, take \(g=0\), let \(D\) rise linearly from zero to
\(3/5\) on \([1/10,3/5]\), keep it constant afterward, and put
\(E=h\), \(K=F=E+D\), \(Q=0\), \(m=D\).  Direct integration gives

\[
 \boxed{
 \ell=1,
 \quad r^x={1\over3},
 \quad \sigma={959\over12000}<{1\over12},
 \quad x={2641\over6000}>{1\over6},
 \quad D(2)-D(\ell)=0.}
\tag{S.266}
\]

Thus this is an \(\mathcal I_x\) row with defect ancestry, but none of the
defect is created on its last-exit interval.

For a pure high-Rayleigh row, instead put

\[
 e_0(t)={12\over125}(t-1/10)(3/5-t)
          \mathbf1_{[1/10,3/5]}(t),
 \quad g=300e_0,
 \quad m=0,
 \quad D(t)=\int_0^tg(s)\,ds,
 \quad E=e_0+h,
\]

and again take \(K=F=E+D\), \(Q=0\).  Since
\(\int e_0=1/500\), \(\int g=3/5\), and
\(\int_Hg=3/5\ge T/8\),

\[
 \boxed{
 \ell=1,
 \quad r^x={1\over3},
 \quad \sigma={983\over12000}<{1\over12},
 \quad x={2617\over6000}>{1\over6},
 \quad \int_{H\cap J^{\rm LE}}g=0.}
\tag{S.267}
\]

Hence high-Rayleigh ancestry also cannot be retrospectively restricted to
\(J^{\rm LE}\).  Any proof doing so would reverse the direction of the
full-history Step 8 trichotomy.

Repeating the pure-defect scalar row \(M\) times gives an abstract flat
tower with \(r_k^x=1/3\), \(v_k=1\), zero \(Q\)-variation, and a
compatible linear ledger parameter \(P_M\asymp M\).  Therefore, for fixed
\(N\),

\[
 \boxed{
 \mathcal S_N(r^x)={(M-N)_+\over3},
 \qquad A_M:=P_M^{2/3}\asymp M^{2/3},
 \qquad Z_M=\sqrt M.}
\tag{S.268}
\]

This rules out a derivation from the scalar \(\ell^1/\ell^2\) ledgers
alone.  It is not an NSE counterexample and does not disprove (S.243).

The exact minimal \(\mathcal R_x\) target is now

\[
 \boxed{
 \textbf{OPEN:}\quad
 \exists\,N_x\in\mathbb N_0,\ C_x<\infty
 \quad\text{such that for every Version-M suitable weak }(u,p),
 \quad\text{every admissible }R,\quad
 \text{and every }\tau\in\mathcal G_R\cap\mathcal T_R,
 \qquad
 \mathcal S_{N_x}(x^{\rm sel}(\tau))\le C_xA_R.}
\tag{S.269}
\]

By (S.263), this is equivalent up to the literal constants to the
\(\mathcal R_x\) residual gate.  A stronger but more physical sufficient
statement replaces \(x^{\rm sel}\) by the ancestor vector \(b\).  Neither
statement follows from the inherited ledgers.

## 8. Exact-family falsification test

Step 10 implies a simple test for any future smooth exact family.  Fix
\(N\).  If a sequence of solutions, scales, and good terminal times has
\(A_R>0\) and \(N+1\) distinct target shells satisfying

\[
 \boxed{
 \min_{1\le i\le N+1}
 {K_{k_i,R}(\tau)\over A_R}\longrightarrow\infty,}
\tag{S.270}
\]

then the Step 10 paid sum forces every target shell into the combined
residual for all sufficiently late members of the sequence.  Hence

\[
 {\mathcal S_N(r(\tau))\over A_R}
 \ge {1\over6}\min_i{K_{k_i,R}(\tau)\over A_R}\longrightarrow\infty,
\]

and that particular fixed \(N\) is refuted.  This avoids a separate branch
classification of each target shell.

The presently proved lower bound for the inherited R0.74O/P single-packet
family certifies (S.270) only for \(N=0\): it supplies one certified large
residual coordinate, which every positive exception budget may delete.
This does not exclude unproved off-target behavior.  R0.74Q proves exact
common-shear superposition and
simultaneous terminal lobes in distinct shells, but the canonical relaxed
equal-target construction also proves the exterior cubic lower bound

\[
 \boxed{
 {A_R^{(N)}\over NT}
 \ge {c\over N}R^{2/3}L_N^{-1/3}
       \exp\left({5\over6}c_\gamma L_N^2\right)
 \longrightarrow\infty,
 \qquad A_R^{(N)}:=(P_R^{M,(N)})^{2/3}.}
\tag{S.271}
\]

Thus its currently established clock lower scale \(NT\) is overwhelmed by
the nonnegative cubic payment.  It does not establish (S.270), and it does
not refute a fixed positive exception count.  The R0.74R persistent-lobe
audit gives the same warning in another normalization: mass beyond the
first target shell encounters the positive exponent
\(\kappa_2=8831/1905120\).  These are quantitative obstructions to the
existing designs, not a theorem ruling out every multi-packet architecture.

## 9. Bounded literature collision search

A bounded primary-source search was made for a theorem already implying
(S.261) or (S.269).  None of the following results has the required
quantifiers.

| Primary result | What it controls | Why it does not close this gate |
|---|---|---|
| Caffarelli--Kohn--Nirenberg, *Partial regularity of suitable weak solutions of the Navier--Stokes equations*, [CPAM 35 (1982)](https://doi.org/10.1002/cpa.3160350604) | Parabolic size of the singular set | The present residual contains regular viscous dissipation as well as possible anomalous mass, and asks for a weighted physical-shell terminal tail about a prescribed centre. |
| De Rosa--Drivas--Inversi, *On the Support of Anomalous Dissipation Measures*, [arXiv:2301.09603](https://arxiv.org/abs/2301.09603) | Local upper-density/absolute-continuity bounds and support-dimension consequences under stated \(L_t^qL_x^r\) hypotheses | The useful bounds require extra integrability and do not give a universal fixed shell count in the bare suitable-weak setting. |
| Barker, *Higher integrability and the number of singular points...*, [arXiv:2111.14776](https://arxiv.org/abs/2111.14776) | At most \(O(M^{20})\) singular points when \(s_n\uparrow0\) and \(\sup_n\|v(s_n)\|_{L^{3,\infty}}\le M\) | The count depends on the extra norm and concerns spatial singular points, not terminal annular residual coordinates. |
| Dascaliuc--Grujic, *Energy cascades and flux locality in physical scales...*, [arXiv:1101.2193](https://arxiv.org/abs/1101.2193) | Physical-space flux locality through time/ensemble averages under an inertial-range condition | It does not provide a prescribed-terminal-centre last-exit trace estimate. |
| Ożański, *Weak solutions to the Navier--Stokes inequality with arbitrary energy profiles*, [arXiv:1809.02109](https://arxiv.org/abs/1809.02109) | Flexibility compatible with local and strong energy inequalities without solving NSE | It supports only the boundary warning that energy inequalities alone are insufficient; it is not an NSE counterexample. |

The search is evidence against an immediate literature shortcut, not a
proof that no related theorem exists.  Dimension or support estimates would
still need a new bridge to the weighted annular best-\(N\) quantity.

## 10. Route decision

The next PDE stage should keep two independent work packages and one final
budget ledger.

1. **Short terminal trace.**  Try to prove or refute (S.261).  The proof
   must use information absent from R.211/R.214 and continuous clocks, such
   as a summed local-energy identity, pressure/drift cancellation, or a
   genuinely quantitative terminal equi-integrability principle.  Plain
   interval nesting and critical Carleson mass are ruled out.
2. **Selected-excess packing.**  Try to prove or refute (S.269), first
   separating anomalous measure from high-Rayleigh viscous mass.  Do not
   localize either ancestor to the last-exit interval.  A factorized
   R0.74R-style theorem may instead seek, off one common exceptional set,
   \(b_k\le q_k+c_kp_k^{2/3}\) with
   \(\sum q_k\lesssim A_R\), \(\sum p_k\lesssim P_R^M\), and
   \(\sum c_k^3\lesssim1\).
3. **Adversarial exact family.**  Any new multi-packet design must first pass
   (S.270), not merely create several terminal lobes.  Different widths,
   time schedules, common shears, or amplitude distributions remain open,
   but the exterior cubic cost must be computed before expensive simulation.

The combined open theorem can be stated without ambiguity:

\[
 \boxed{
 \begin{gathered}
 \textbf{OPEN: find fixed }N_{\rm sh},N_x\in\mathbb N_0
 \textbf{ and }C_{\rm sh},C_x<\infty
 \textbf{ such that, for every Version-M suitable weak }(u,p)
 \textbf{ and every admissible }R,\\
 \sup_{\tau\in\mathcal T_R\cap\mathcal G_R}
   \mathcal S_{N_{\rm sh}}(r^{\rm sh}(\tau))\le C_{\rm sh}A_R,
 \qquad
 \sup_{\tau\in\mathcal T_R\cap\mathcal G_R}
   \mathcal S_{N_x}(r^x(\tau))\le C_xA_R.
 \end{gathered}}
\tag{S.272}
\]

If (S.272) holds, then (S.251) proves Step 10 (S.243) with
\(N_0=N_{\rm sh}+N_x\), hence R0.74Q (Q.12) and the fixed-scale estimate
(Q.1).  The implication is proved.  The antecedent remains open.

## 11. Decision and claim ledger

The following are **PROVED**:

- the exact pointwise shared-budget identity and its domain consequence
  (S.249)--(S.251);
- the inverse-duration short-branch estimate (S.253)--(S.254);
- the normalized-depth, dyadic, and layer-cake identities
  (S.255)--(S.256);
- the failure of critical quadratic Carleson control at the coefficient
  level (S.257);
- the nested-tent and positive-depth estimates (S.258)--(S.259);
- the exact scalar-excess/residual equivalence (S.262)--(S.263);
- the ancestor, linear-ledger, and fixed-solution compactness statements
  (S.264)--(S.265);
- the conditional implications from (S.261), (S.269), (S.270), and
  (S.272); and
- the quantitative obstruction already proved for the inherited canonical
  multi-packet constructions.

The following are **ABSTRACT STRESS TESTS, NOT NSE COUNTEREXAMPLES**:

- the duplicate-budget fixture (S.252);
- the critical Carleson sequence and nested clock tower
  (S.257), (S.260);
- the defect and high-Rayleigh localization witnesses
  (S.266)--(S.267); and
- the flat selected-excess tower (S.268).

The following remain **OPEN**:

- terminal anti-concentration (S.261);
- uniform selected-excess packing (S.269);
- either branch estimate in (S.272), a fixed universal \(N_0\), Step 10
  (S.243), Q.12, Q.1, scale contraction, prescribed-centre packing, and
  regularity; and
- a new exact multi-packet family satisfying the falsification criterion
  (S.270) without prohibitive full payment.

The following are **NOT CLAIMED**:

- continuity or measurability of the moving branch masks, last-exit
  selectors, top-\(N\) sets, or adaptive budget split;
- that a terminal supremum commutes with the branch-budget minimum;
- that CKN-type singular-set estimates count the present shell residuals;
- that terminal defect or high-Rayleigh ancestry persists on the last-exit
  interval;
- that the bounded collision search is exhaustive;
- novelty or priority; or
- a solution of the Navier--Stokes Millennium problem.

## 12. Frozen source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| Canonical clocks, absolute ledgers, \(\ell^1\) BV closure, and square function | R0.74P, (2.7)--(3.13) | **INHERITED / PROVED** |
| Best-\(N\) terminal reduction and exact-family problem freeze | R0.74Q, (Q.7)--(Q.27) | **INHERITED / PROVED REDUCTIONS; PDE GATE OPEN** |
| Shell-dependent cubic payment and persistence Hölder inequality | R0.74R, (R.209)--(R.215) | **INHERITED / PROVED** |
| Step 8 scalar/Jordan excess, ancestry, and stopped-work bridge | R0.74S Step 8, (S.163)--(S.199) | **INHERITED / PROVED; NO-EXCEPTION GATE REFUTED** |
| Paid/residual partition and best-\(N\) equivalence | R0.74S Step 10, (S.223)--(S.247) | **INHERITED / PROVED; RESIDUAL PDE PACKING OPEN** |

The new content is the exact shared-budget infimal convolution, the
short-branch inverse-duration and nested-tent reductions, the terminal-trace
and critical-Carleson obstructions, the two-sided selected-excess
equivalence, the fixed-solution/nonuniform compactness distinction, and the
\((N+1)\)-target exact-family falsification criterion.  **NOT CLAY.**
