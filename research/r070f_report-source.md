# R0.70F — Fixed-annulus affine jets: exact Taylor gain and initial-face saturation

> **Status:** internal canonical research report; not a public theorem chapter.
> **Date:** 2026-08-24.
> **Scope:** Yu's fixed-source harmonic module, a project-defined instantaneous
> jet observable, and the precise boundary to a common-top-time Navier--Stokes
> packing theorem.

## 1. Result in one page

Yu's Section 8.3 proposes replacing moving shells by a fixed smooth annular
partition and expanding the resulting exterior-source strain harmonically in
the core. R0.70F resolves what this operation gives unconditionally and what
it cannot give.

Let \(r_k=2^{-k}\), \(j<k\), \(\theta=r_k/r_j\), and

\[
 H_{j,k}(x,t)
 =\int_{\mathbb R^3}K(x-y)\psi_j(y)\Omega_k(y,t)\,dy,
 \tag{1.1}
\]

where the fixed annulus supporting \(\psi_j\) stays a distance comparable to
\(r_j\) from the core. If

\[
 H_{j,k}(x,t)=A_{j,k}(t)+B_{j,k}(t)[x-x_0]+R^{\rm aff}_{j,k}(x,t),
 \tag{1.2}
\]

then the normalized constant, linear, and affine-remainder works obey

\[
 \boxed{
 |\mathcal W^{(0)}_{j,k}|
 \lesssim\theta\,\mathfrak A^{\psi}_{j,k}\mathcal Q_k,
 \quad
 |\mathcal W^{(1)}_{j,k}|
 \lesssim\theta^2\,\mathfrak A^{\psi}_{j,k}\mathcal Q_k,
 \quad
 |\mathcal W^{\rm aff,rem}_{j,k}|
 \lesssim\theta^3\,\mathfrak A^{\psi}_{j,k}\mathcal Q_k.}
 \tag{1.3}
\]

Expansion through the quadratic jet leaves a \(\theta^4\) work remainder.
These powers are exact consequences of the kernel homogeneity and the Yu
normalization.

The low-order tensors have real structure: \(H_{j,k}\) is symmetric,
trace-free, divergence-free, and componentwise harmonic in the core. That
structure does **not** annihilate either affine work. The constant work sees
the deviatoric zeroth enstrophy moment, and the linear work sees the compatible
part of the first enstrophy moment:

\[
 \mathcal W^{(0)}_{j,k}
 =r_k\int_{I_k}A_{j,k}:M_k^{(0)}\,dt,
 \qquad
 \mathcal W^{(1)}_{j,k}
 =r_k\int_{I_k}B_{j,k}:M_k^{(1)}\,dt.
 \tag{1.4}
\]

R0.70F constructs explicit compact smooth divergence-free fields for which
both pairings are positive. More strongly, for every finite \(N\) there are
two smooth nested families \(f_N^{(0)}\) and \(f_N^{(1)}\), with

\[
 \sup_N\bigl(\|f_N^{(q)}\|_2+
                 \|f_N^{(q)}\|_{BMO^{-1}}\bigr)<\infty,
 \qquad q=0,1,
 \tag{1.5}
\]

whose project-defined **initial-face** fixed-annulus jet works satisfy

\[
 \sum_{n=1}^N\mathcal J_n^{(0)}\ge c_0N,
 \qquad
 \sum_{n=1}^N\mathcal J_n^{(1)}\ge c_1N.
 \tag{1.6}
\]

After multiplication by one sufficiently small \(\varepsilon>0\), independent
of \(N\), every \(\varepsilon f_N^{(q)}\) launches a unique small global
solution in the Koch--Tataru \(X\) class, classical for \(t>0\). Thus neither
harmonicity, finite energy, small \(BMO^{-1}\), nor membership in the globally
regular small-data class imposes an algebraic initial-face cancellation of the
raw constant or linear jet.

There is a second, independent obstruction. For every \(\beta>0\),

\[
 \sum_{k=1}^N\sum_{j=0}^{k-1}2^{-\beta(k-j)}
 =\frac{N}{2^\beta-1}
  -\frac{1-2^{-\beta N}}{(2^\beta-1)^2}.
 \tag{1.7}
\]

Therefore even the ideal removal of the complete affine jet, which changes
the kernel from \(\beta=1\) to \(\beta=3\), leaves linear growth with slope
\(1/7\) when the two reservoir sequences are merely bounded. Taylor gain is
not unweighted packing.

Together, (1.6) and (1.7) rule out one specific proof architecture:
**take absolute values term by term and try to close a raw, direct,
unweighted affine-jet Taylor majorant using only bounded reservoir
sequences**. This is not a no-go theorem for an actual spacetime packing
estimate. In particular, it does not exclude source-aware martingale
differences, telescoping between adjacent annuli, an actual Carleson bound for
deviatoric enstrophy moments, or a quantitative Besov decorrelation
hypothesis.

Most importantly, (1.6) is an initial-face statement. It is not a
counterexample on the nested backward cylinders \(I_k=(t_0-r_k^2,t_0)\) with
one common interior \(t_0>0\). Producing the same recurrence at such a point
would require nonlinear regeneration of arbitrarily fine jets against heat
smoothing; that is part of the original regularity problem, not something
proved here.

## 2. Source boundary

The source object is [Yu v1, Section 8.3](https://arxiv.org/html/2606.27560v1#S8.SS3):

\[
 H_{j,k}(x,t)=\int K(x-y)\psi_j(y)\Omega_k(y,t)\,dy.
 \tag{2.1}
\]

Yu states that a fixed smooth annular partition is required before harmonic
Taylor expansion is legitimate. The same section calls the route a separate
conditional module and does not identify it with the moving-shell quantity in
Proposition 8.6.

R0.70F preserves that distinction:

- \(H_{j,k}\) is the fixed-source tensor in (2.1).
- \(\mathcal W_{j,k}\), defined below, is project notation for its signed
  contraction with core filtered enstrophy.
- \(\mathcal J_n^{(q)}\) is a project-defined scale-invariant instantaneous
  observable on an initial face.
- None of these is renamed as Yu's positive moving-shell scalar
  \(\mu_k^{\rm far,ann}\).

The initial-face construction is allowed to choose one even compactly
supported filter and one compatible smooth partition. It is not uniform over
all filters or partitions.

## 3. Fixed-annulus Taylor-work lemma

Translate \(x_0\) to zero. Assume

\[
 \operatorname{supp}\psi_j
 \subset\{c_0r_j\le |y|\le C_0r_j\},
 \qquad
 \operatorname{dist}(\operatorname{supp}\psi_j,B_{\gamma r_k})
 \ge c_1r_j,
 \tag{3.1}
\]

with fixed positive \(c_0,C_0,c_1,\gamma\), and
\(\|\psi_j\|_\infty\le C_\psi\). The separation in (3.1), rather than the
bare label \(j<k\), is the exact geometric hypothesis.

Put

\[
 F_{j,k}=\psi_j\Omega_k,
 \qquad
 S_{j,k}(t)=\|F_{j,k}(t)\|_2.
 \tag{3.2}
\]

For every multi-index \(\alpha\), the strain kernel satisfies off the origin

\[
 |\partial^\alpha K(z)|\le C_\alpha|z|^{-3-|\alpha|}.
 \tag{3.3}
\]

Taylor's formula on \(B_{\gamma r_k}\) gives

\[
 H_{ij}(x,t)
 =A_{ij}(t)+B_{ij\ell}(t)x_\ell
  +C_{ij\ell m}(t)x_\ell x_m+R^{(3)}_{ij}(x,t),
 \tag{3.4}
\]

where

\[
 \begin{aligned}
 A_{ij}&=\int K_{ijn}(-y)F_n(y)\,dy,\\
 B_{ij\ell}&=\int\partial_\ell K_{ijn}(-y)F_n(y)\,dy,\\
 C_{ij\ell m}&=\frac12\int\partial_{\ell m}K_{ijn}(-y)F_n(y)\,dy.
 \end{aligned}
 \tag{3.5}
\]

The annular volume bound and Cauchy--Schwarz imply

\[
 \begin{array}{c|c}
 \text{field on }B_{\gamma r_k}&L^\infty\text{ bound}\\ \hline
 A&Cr_j^{-3/2}S_{j,k}\\
 Bx&C\theta r_j^{-3/2}S_{j,k}\\
 C[x,x]&C\theta^2r_j^{-3/2}S_{j,k}\\
 R^{(3)}&C\theta^3r_j^{-3/2}S_{j,k}.
 \end{array}
 \tag{3.6}
\]

Let \(0\le\chi_k\le1\) be supported in the core and define

\[
 e_k(t)=\int\chi_k|\Omega_k|^2\,dx,
 \qquad
 \mathcal Q_k=\|e_k\|_{L^2(I_k)},
 \tag{3.7}
\]

and the fixed-partition reservoir

\[
 \mathfrak A^{\psi}_{j,k}
 =\left(r_j^{-1}\int_{I_k}\!\int_{\operatorname{supp}\psi_j}
       |\Omega_k|^2\,dx\,dt\right)^{1/2}.
 \tag{3.8}
\]

The signed fixed-source work is

\[
 \mathcal W_{j,k}
 =r_k\int_{I_k}\!\int
 \chi_k H_{j,k}:\Omega_k\otimes\Omega_k\,dx\,dt.
 \tag{3.9}
\]

For the homogeneous Taylor term of degree \(n=0,1,2\), (3.6), time
Cauchy--Schwarz, and

\[
 \|S_{j,k}\|_{L^2(I_k)}
 \le C r_j^{1/2}\mathfrak A^{\psi}_{j,k}
 \tag{3.10}
\]

give

\[
 \boxed{
 |\mathcal W^{(n)}_{j,k}|
 \le C\theta^{n+1}\mathfrak A^{\psi}_{j,k}\mathcal Q_k,
 \qquad n=0,1,2.}
 \tag{3.11}
\]

The cubic field remainder has work bounded by

\[
 |\mathcal W^{(3+)}_{j,k}|
 \le C\theta^4\mathfrak A^{\psi}_{j,k}\mathcal Q_k.
 \tag{3.12}
\]

In particular,

\[
 \boxed{
 |\mathcal W_{j,k}-\mathcal W^{(0)}_{j,k}
                    -\mathcal W^{(1)}_{j,k}|
 \le C\theta^3\mathfrak A^{\psi}_{j,k}\mathcal Q_k.}
 \tag{3.13}
\]

Equation (3.13) is the narrow unconditional gain after subtracting the
affine jet. For a positive-part work one may dominate the positive part by
the sum of the absolute values of the three pieces, but a signed cancellation
between pieces cannot be passed through \(s\mapsto s_+\).

## 4. Exact structural constraints and enstrophy moments

Away from the source, the strain kernel has

\[
 K_{ijm}=K_{jim},\qquad K_{iim}=0,
 \qquad\partial_iK_{ijm}=0,\qquad\Delta K_{ijm}=0.
 \tag{4.1}
\]

Hence \(H_{j,k}\) is symmetric, trace-free, divergence-free, and
componentwise harmonic in the core. Its first coefficients obey

\[
 A_{ij}=A_{ji},\quad A_{ii}=0,
 \tag{4.2}
\]

and

\[
 B_{ij\ell}=B_{ji\ell},\quad B_{ii\ell}=0,
 \quad\sum_iB_{iji}=0.
 \tag{4.3}
\]

The quadratic coefficient, with the convention in (3.5), obeys

\[
 \begin{gathered}
 C_{ij\ell m}=C_{ji\ell m}=C_{ijm\ell},\qquad
 C_{ii\ell m}=0,\\
 \sum_i C_{ijim}=0,\qquad
 \sum_\ell C_{ij\ell\ell}=0.
 \end{gathered}
 \tag{4.3a}
\]

The last two identities are respectively the quadratic coefficients of
\(\nabla\!\cdot H=0\) and \(\Delta H=0\). Thus the first three Taylor tensors
are constrained, but none of these identities alone removes the constant or
linear work below.

Define the spatial enstrophy moments

\[
 M^{(0)}_{ij}(t)=\int\chi_k\Omega_i\Omega_j\,dx,
 \qquad
 M^{(1)}_{ij\ell}(t)
 =\int\chi_kx_\ell\Omega_i\Omega_j\,dx.
 \tag{4.4}
\]

Then

\[
 \mathcal W^{(0)}_{j,k}
 =r_k\int_{I_k}A_{ij}M^{(0)}_{ij}\,dt,
 \qquad
 \mathcal W^{(1)}_{j,k}
 =r_k\int_{I_k}B_{ij\ell}M^{(1)}_{ij\ell}\,dt.
 \tag{4.5}
\]

Trace-freeness gives only

\[
 A:M^{(0)}
 =A:\left(M^{(0)}-\frac{\operatorname{tr}M^{(0)}}3I\right).
 \tag{4.6}
\]

Thus a constant jet vanishes under the additional isotropy condition
\(M^{(0)}=(\operatorname{tr}M^{(0)}/3)I\), not under incompressibility alone.
The constraints in (4.3) similarly remove only trace subspaces from
\(M^{(1)}\); an anisotropic, off-centre core vorticity packet can have a
strictly positive first-moment pairing.

If \(H=\operatorname{sym}\nabla V\), integration by parts using
\(\nabla\cdot\Omega=0\) gives

\[
 \int\chi H_{ij}\Omega_i\Omega_j
 =-\int\chi V_j\Omega_i\partial_i\Omega_j
  -\int V_j\Omega_i\Omega_j\partial_i\chi.
 \tag{4.7}
\]

The first term in (4.7) remains even when \(\chi\equiv1\). Incompressibility
therefore reorganizes the work; it does not make it zero.

Reflection symmetry gives only a conditional statement. If \(\psi_j\), the
filter, and \(\chi_k\) are inversion even, then even exterior vorticity makes
\(H\) even and removes the linear jet. Odd exterior vorticity removes the
constant jet, but the corresponding anti-fixed velocity class is not
preserved by the nonlinear Navier--Stokes evolution. R0.70E already showed
that mixed parity survives signed annular averaging. No parity conclusion is
available for a general partition.

## 5. Compact generators for constant and linear harmonic strain

Fix \(0<\delta<1/4\). Let
\(\zeta\in C_c^\infty(\mathbb R^3)\) be radial, equal to one on
\(B_{1+2\delta}\), and supported in \(B_{2-2\delta}\). In particular, it is
one on \(B_1\), supported in \(B_2\), and its derivative support has a fixed
buffer from both annular endpoints. If \(P\) is a homogeneous divergence-free
polynomial vector field of degree \(d\), put

\[
 \mathcal L[P]
 :=\nabla\times\left[-\frac1{d+2}\zeta(x)\,x\times P(x)\right].
 \tag{5.1}
\]

The vector identity

\[
 \nabla\times(x\times P)=-(d+2)P
 \tag{5.2}
\]

uses \(\nabla\cdot P=0\) and Euler homogeneity. Therefore

\[
 \mathcal L[P]=P\quad\hbox{on }B_1,
 \qquad
 \mathcal L[P]\in C_{c,\sigma}^\infty(B_2).
 \tag{5.3}
\]

### 5.1 Constant strain

Set

\[
 A=\operatorname{diag}(1,-1/2,-1/2),
 \qquad P_0(x)=Ax,
 \qquad G_0=\mathcal L[P_0].
 \tag{5.4}
\]

Then \(G_0=Ax\), \(\nabla\times G_0=0\), and
\(\operatorname{sym}\nabla G_0=A\) on \(B_1\). All vorticity producing
that core strain lies in the cutoff transition.

### 5.2 Linear strain

Set

\[
 \Phi(x)=x_1^3-3x_1x_2^2,
 \qquad P_1=\nabla\Phi,
 \qquad G_1=\mathcal L[P_1].
 \tag{5.5}
\]

Because \(\Delta\Phi=0\), \(P_1\) is divergence-free and curl-free. On
\(B_1\),

\[
 \operatorname{sym}\nabla G_1
 =L(x):=\nabla^2\Phi(x)
 =\begin{pmatrix}
 6x_1&-6x_2&0\\
 -6x_2&-6x_1&0\\
 0&0&0
 \end{pmatrix}.
 \tag{5.6}
\]

In particular, \(e_1\cdot L(ce_1)e_1=6c>0\).

### 5.3 Core vorticity carrier

Let

\[
 W x=\frac12e_1\times x=(0,-x_3/2,x_2/2),
 \qquad V=\mathcal L[Wx].
 \tag{5.7}
\]

On \(B_1\), \(V=Wx\),

\[
 \nabla\times V=e_1,
 \qquad \operatorname{sym}\nabla V=0.
 \tag{5.8}
\]

All three fields are explicit compact smooth divergence-free localizations.
The return vorticity created by \(\zeta\) is retained; it is precisely the
fixed exterior source that generates the core strain.

## 6. Exact finite-chain initial-face saturation

Choose \(\Lambda=2^M\) sufficiently large and define interlaced scales

\[
 R_n=\Lambda^{-2n},
 \qquad r_n=R_n/\Lambda,
 \qquad 1\le n\le N.
 \tag{6.1}
\]

With Yu's \(r_k=2^{-k}\), these are exactly
\(R_n=r_{j_n}\), \(r_n=r_{k_n}\), where

\[
 j_n=2Mn,\qquad k_n=(2n+1)M,\qquad k_n-j_n=M.
 \tag{6.1a}
\]

Thus every selected pair has \(j_n<k_n\) and the fixed separation ratio
\(r_{k_n}/r_{j_n}=\Lambda^{-1}\).

For \(q=0,1\), scale the generators and carrier by

\[
 G_{q,R}(x)=R^{-1}G_q(x/R),
 \qquad V_r(x)=r^{-1}V(x/r),
 \tag{6.2}
\]

and set

\[
 f_N^{(q)}=\sum_{n=1}^N\bigl(G_{q,R_n}+V_{r_n}\bigr).
 \tag{6.3}
\]

Fix \(0<\eta<c\), choose a small filter ratio \(\sigma>0\), and require

\[
 c+\eta+\sigma<1,
 \qquad
 \sigma+\frac2\Lambda<c-\eta,
 \qquad
 \frac{\sigma}{\Lambda}<\delta.
 \tag{6.4}
\]

Let \(\chi\in C_c^\infty(B_1)\) be nonnegative, radial, and nonzero, and put

\[
 \chi_n(x)=\chi\!\left(\frac{x-cr_ne_1}{\eta r_n}\right),
 \qquad c_\chi=\int\chi(x)\,dx.
 \tag{6.5}
\]

The support of \(\chi_n\) lies in the affine core of every coarser carrier,
outside every finer carrier, and in the harmonic core of the selected
generator. Hence the core vorticity is exactly

\[
 \Omega^{\rm core}_n
 =\left(\sum_{m=1}^nr_m^{-2}\right)e_1
 =r_n^{-2}b_n e_1,
 \qquad
 b_n=\sum_{a=0}^{n-1}\Lambda^{-4a}.
 \tag{6.6}
\]

Fix
\[
 \varphi\in C_c^\infty(B_1),\qquad
 \varphi(-x)=\varphi(x),\qquad \int\varphi=1,
 \tag{6.6a}
\]
and use \(\varphi_{\ell_n}(x)=\ell_n^{-3}\varphi(x/\ell_n)\) with
\(\ell_n=\sigma r_n\). For every vector field \(f\), write

\[
 \Omega_{\ell_n}[f]
 :=\varphi_{\ell_n}*(\nabla\times f).
 \tag{6.6aa}
\]

The buffer in (6.4) makes (6.6) valid for \(\Omega_{\ell_n}[f_N^{(q)}]\),
not only for the unfiltered vorticity, throughout \(\operatorname{supp}\chi_n\).

Fix once and for all, independently of \(N\), a **radial** smooth annular
partition \(\{\psi_j\}_{j\in\mathbb Z}\). At every active index choose

\[
 \operatorname{supp}\psi_{j_n}
 \subset\{R_n\le |y|\le2R_n\},\qquad
 \psi_{j_n}=1
 \quad\hbox{when}\quad
 (1+\delta)R_n\le |y|\le(2-\delta)R_n.
 \tag{6.6ab}
\]

The second region contains the \(\ell_n\)-expanded vorticity transitions of
both \(G_{0,R_n}\) and \(G_{1,R_n}\), while the inner hole contains
\(\operatorname{supp}\chi_n\) and every target or finer transition. The
derivative buffer in Section 5, (6.4), and the \(\Lambda^2\) separation of the
active source bands permit this construction first for all \(n\ge1\), after
which the unused dyadic gaps are filled to complete one fixed partition.

There is one cross source that must be retained. On
\(\operatorname{supp}\psi_{j_n}\), each coarser carrier \(V_{r_m}\),
\(m<n\), has constant filtered vorticity \(r_m^{-2}e_1\). It contributes no
core strain by the following radial-shell lemma. If

\[
 F_n=(-\Delta)^{-1}\psi_{j_n},
 \tag{6.6b}
\]

then \(F_n\) is radial and harmonic in the inner hole. Regularity at the
origin makes it constant there. Consequently, for any scalar \(a\),

\[
 \nabla\times(-\Delta)^{-1}(a\psi_{j_n}e_1)
 =a\,\nabla F_n\times e_1=0
 \quad\hbox{in the inner hole},
 \tag{6.6c}
\]

so its strain is also zero. Coarser generator vorticity vanishes on the
selected band, while target and finer carrier transitions lie in the inner
hole.

Define the actual fixed-source tensor

\[
 H_{n,\psi}^{(q)}[f](x)
 :=\int K(x-y)\psi_{j_n}(y)\Omega_{\ell_n}[f](y)\,dy.
 \tag{6.6d}
\]

An even unit-mass convolution fixes constants and linear functions. The
selected generator transition, including its return field, therefore gives
the exact identities on \(\operatorname{supp}\chi_n\)

\[
 H_{n,\psi}^{(0)}[f_N^{(0)}](x)=R_n^{-2}A,
 \qquad
 H_{n,\psi}^{(1)}[f_N^{(1)}](x)=R_n^{-3}L(x).
 \tag{6.7}
\]

Define the scale-invariant instantaneous observables

\[
 \mathcal J_n^{(q)}[f]
 :=r_n^3\int\chi_n
 H_{n,\psi}^{(q)}[f]:
 \Omega_{\ell_n}[f]\otimes\Omega_{\ell_n}[f]\,dx.
 \tag{6.8}
\]

Equations (5.6), (6.5)--(6.7), and radial symmetry of \(\chi\) give the exact
values

\[
 \boxed{
 \mathcal J_n^{(0)}[f_N^{(0)}]
 =c_\chi\eta^3\Lambda^{-2}b_n^2>0,}
 \tag{6.9}
\]

and

\[
 \boxed{
 \mathcal J_n^{(1)}[f_N^{(1)}]
 =6c\,c_\chi\eta^3\Lambda^{-3}b_n^2>0.}
 \tag{6.10}
\]

Since \(b_n\ge1\), summing (6.9)--(6.10) proves

\[
 \sum_{n=1}^N\mathcal J_n^{(0)}
 \ge c_\chi\eta^3\Lambda^{-2}N,
 \qquad
 \sum_{n=1}^N\mathcal J_n^{(1)}
 \ge6c\,c_\chi\eta^3\Lambda^{-3}N.
 \tag{6.11}
\]

No cross source was deleted. The coarser-carrier source on the selected band
is retained and annihilated by the radial-shell lemma (6.6b)--(6.6c);
coarser carriers still contribute the explicit positive core-vorticity factor
\(b_n\); finer fields are absent from the lobe by (6.4); and all cutoff
return fields remain in (6.3).

## 7. Uniform energy, critical control, and the NSE transfer boundary

Critical scaling gives

\[
 \|G_{q,R}\|_2=R^{1/2}\|G_q\|_2,
 \qquad
 \|V_r\|_2=r^{1/2}\|V\|_2.
 \tag{7.1}
\]

The geometric series in (6.1) therefore implies

\[
 \sup_N\|f_N^{(q)}\|_2<\infty.
 \tag{7.2}
\]

Every base profile vanishes at least linearly at the origin. Splitting at
the smallest active scale comparable to \(|x|\) gives the pointwise bound

\[
 |f_N^{(q)}(x)|\le\frac{C_{\Lambda,q}}{|x|},
 \qquad x\ne0,
 \tag{7.3}
\]

uniformly in \(N\). The heat estimate

\[
 |e^{t\Delta}f_N^{(q)}(x)|
 \le\frac{C}{|x|+\sqrt t}
 \tag{7.4}
\]

and a near-origin/far-origin split in each parabolic cylinder give directly

\[
 \sup_N\|f_N^{(q)}\|_{BMO^{-1}}<\infty.
 \tag{7.5}
\]

Indeed, near the origin the change of variables \(x=RX,\ t=R^2s\)
normalizes

\[
 R^{-3}\int_0^{R^2}\!\int_{B_R}
 (|x|+\sqrt t)^{-2}\,dx\,dt,
 \tag{7.6}
\]

and a cylinder at distance at least \(2R\) costs \(O(R^2/d^2)\).

By the small-data theorem of
[Koch--Tataru](https://math.berkeley.edu/~tataru/papers/nas.pdf), there is one
\(\varepsilon_*>0\), independent of \(N\), such that every

\[
 u_{0,N}^{(q)}=\varepsilon f_N^{(q)},
 \qquad 0<\varepsilon<\varepsilon_*,
 \tag{7.7}
\]

launches a unique small global Navier--Stokes solution in the Koch--Tataru
\(X\) class. Since every fixed \(f_N^{(q)}\) is compact and smooth, standard
mild smoothing makes that solution classical for \(t>0\). Cubic homogeneity
changes (6.9)--(6.10) by the factor \(\varepsilon^3\).

This transfer has a strict boundary:

1. It proves that globally regular NSE initial data can carry arbitrarily
   many same-sign raw affine jet pairings at the initial face.
2. For each fixed \(N\), classical continuity preserves all finitely many
   signs for some positive time \(\tau_N\).
3. No \(N\)-independent lower bound \(\tau_N\gtrsim r_N^2\) is proved.
4. The forward intervals from the initial face are not the nested backward
   intervals with one common interior terminal time used by Yu.

At a fixed \(t_0>0\), heat analyticity suppresses preloaded scales
\(r_n\ll\sqrt{t_0}\). Recreating them near one common terminal point would
require a nonlinear cascade. R0.70F neither constructs nor excludes that
cascade.

## 8. Why every fixed Taylor power still grows linearly

Let \(q=2^{-\beta}\), \(\beta>0\). The triangular dyadic sum is

\[
 \begin{aligned}
 D_{\beta,N}
 &=\sum_{k=1}^N\sum_{j=0}^{k-1}2^{-\beta(k-j)}\\
 &=\sum_{m=1}^N(N-m+1)q^m\\
 &=\frac{N}{2^\beta-1}
   -\frac{1-2^{-\beta N}}{(2^\beta-1)^2}.
 \end{aligned}
 \tag{8.1}
\]

Consequently

\[
 \lim_{N\to\infty}\frac{D_{\beta,N}}N
 =\frac1{2^\beta-1}>0.
 \tag{8.2}
\]

The slopes associated with the Taylor ledger are

\[
 \begin{array}{c|c|c}
 \text{retained work}&\beta&\text{asymptotic slope}\\ \hline
 \text{constant}&1&1\\
 \text{linear}&2&1/3\\
 \text{affine remainder}&3&1/7\\
 \text{quadratic remainder}&4&1/15.
 \end{array}
 \tag{8.3}
\]

Thus no finite Taylor subtraction makes the **termwise absolute-value
majorant** of a bounded--bounded convolution into an \(N\)-uniform sum. The
high-order kernel controls multiplicity in the scale gap \(k-j\), not the
number of coarse reservoirs \(j\). This discrete statement does not rule out
cancellation in the true spacetime sum.

This conclusion is entirely compatible with Yu's Theorem 8.7: the latter
assumes dual \(\ell^p\)--\(\ell^q\) summability of the reservoir sequences.
R0.70F proves that Taylor improvement alone cannot manufacture that
summability inside this direct-majorant proof architecture.

## 9. Focused primary-literature audit

The audit found no primary theorem that supplies the missing raw affine-jet
packing for arbitrary finite-energy Navier--Stokes solutions.

1. [Yu v1, Sections 8.2--8.3](https://arxiv.org/html/2606.27560v1#S8.SS2)
   obtains an \(N\)-uniform **unweighted** bound for
   \(\sum_{k=0}^N\mu_k^{\rm far,ann}\) under explicit dual sequence
   summability and calls the fixed-annulus harmonic route conditional. This
   does not negate Yu's separate energy-level weighted packing estimate.
2. [Wolf](https://arxiv.org/html/1611.01482v1#S1) notes that for any harmonic
   \(\phi\) and scalar time profile \(\eta\), the local field
   \(u=\eta(t)\nabla\phi\), with a corresponding pressure, solves the local
   NSE distributionally. Harmonic quadratic and cubic potentials therefore
   permit nonzero constant and linear strain jets even under local NSE
   dynamics. These fields are not global finite-energy examples; the compact
   construction in Sections 5--7 supplies that missing initial-data boundary.
3. [Brandolese--Vigneron](https://arxiv.org/html/0706.1489v1) obtain explicit
   far-field potential profiles for decaying mild solutions. Their leading
   profile vanishes only under an isotropy condition on a time-integrated
   energy matrix. This is a useful analogy for (4.6), not a theorem about
   Yu's core strain.
4. [Bradshaw--Tsai](https://arxiv.org/html/2001.11526v1) use a fixed-center
   subtraction in local pressure expansions to gain far-field decay. A
   pressure constant is a gauge; a constant strain paired with
   \(\Omega\otimes\Omega\) is not. Their subtraction does not cancel (4.5).
5. [Eyink--Aluie](https://arxiv.org/html/0909.2386v1) prove infrared locality
   of coarse-grained energy flux under explicit structure-function/Besov
   scaling. Their stress contains velocity increments and therefore built-in
   cancellation. The result is a template for a conditional route, not an
   energy-level estimate for external strain against filtered enstrophy.
6. The \(BMO^{-1}\) norm in Koch--Tataru is a parabolic tent norm of the
   caloric extension of the initial datum; the solution space \(X\) contains
   an analogous spacetime \(L^2\) tent component. Neither object itself
   implies a Carleson packing of the physical annular affine coefficients.
   R0.70F uses the theorem only to place the saturating initial data inside a
   known globally regular small-\(X\) solution class.

The novelty claim is deliberately narrow: the Taylor-work ledger, the exact
compact initial-face saturation of both raw affine modes, and their NSE
small-data embedding are project results. No claim of literature priority is
made without journal-level external review.

## 10. What is closed and what remains open

### Closed

- The exact fixed-annulus Taylor powers in Yu's normalization.
- The symmetry, trace, divergence, and harmonic constraints on the first
  three jet tensors.
- The precise zeroth- and first-enstrophy moments seen by the affine jet.
- Exact compact smooth constant- and linear-jet generators with retained
  return vorticity.
- An \(N\)-scale initial-face family with same-sign raw jet work and uniform
  \(L^2\cap BMO^{-1}\) control.
- Embedding of the small-amplitude family into unique small global
  Koch--Tataru \(X\)-solutions, classical for positive time.
- The discrete theorem that every fixed Taylor power still permits linear
  cumulative growth for bounded reservoirs.

### Not closed

- A common-interior-terminal-time realization on Yu's nested cylinders.
- An identification of the fixed-source work with the moving-shell positive
  quantity.
- A pointwise or absolute-value cancellation suitable for positive parts.
- A Carleson theorem for the deviatoric zeroth and compatible first
  enstrophy moments.
- Uniformity over every admissible filter and partition.
- Large-data regularity, blow-up, or the Millennium problem.

## 11. Research value and next gate

R0.70F is a rigorous elimination of that direct-majorant route. It shows that
the sentence
“the exterior field is harmonic, so subtract its affine jet and sum the
remainder” omits two independent difficulties:

1. the raw constant and linear jet pair nontrivially with anisotropic
   enstrophy moments, even in globally regular small-data initial states; and
2. after ideal affine cancellation, a faster geometric gap kernel still does
   not sum over an unbounded number of merely bounded reservoirs.

This narrows the positive route. The saturation family has nearly recurrent
**raw normalized jets**, so it does not exclude cancellation of
source-aware differences. The next gate is therefore:

> **R0.70G:** replace raw annular affine coefficients by adjacent-source
> martingale differences, derive the exact dilation/transport law for their
> constant and linear parts, and test whether a square-function or Carleson
> estimate follows from finite energy without losing the positive-part and
> localization budgets.

A positive result would have to show why the differences telescope or become
orthogonal. A negative result would require a family whose **jet
differences**, not merely its raw jets, remain non-summable.

## 12. Certificate, figure, and compute boundary

research/r070f_affine_jet_audit.py reproduces with exact symbolic arithmetic:

1. the two homotopy vector-potential identities;
2. the constant and linear harmonic strain tensors;
3. the carrier vorticity and zero core strain;
4. the exact finite-chain work factors in (6.9)--(6.10);
5. the closed triangular sum (8.1) and its four slopes.

The script does not computer-prove the smooth cutoff gluing, support buffers,
the heat-kernel \(BMO^{-1}\) estimate, or Koch--Tataru theory. Those are
analytic arguments in this report.

The journal figure plots exact formulas and construction geometry. It is not
DNS, a trajectory simulation, or evidence for a singular cascade.

**DGX:** not justified. This gate is algebraic, harmonic, and functional
analytic. More floating-point samples would not certify the common-top-time
boundary.

**Publication boundary:** the internal audits are archived in
`research/r070f_independent_audit.md`. Do not push, merge, or present R0.70F
as a public Millennium advance unless the user separately approves
publication.
