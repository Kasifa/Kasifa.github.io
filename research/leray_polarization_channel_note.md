# R0.56 — Exact Leray polarization channels and the surviving normal obstruction

## 1. Scope and literature boundary

R0.55 proved that the scale-critical ordered Fourier--Leray symbol has
constant one and that this constant remains sharp on arbitrarily separated
high--high-to-low triads.  It also showed why a nontrivial additive scalar
charge cannot be rotation invariant on arbitrary Fourier data.  The next
minimal state must therefore retain the two transverse polarizations rather
than replace each Fourier coefficient by its Euclidean magnitude at the
start.

This note gives an exact two-channel formula in a frame attached to one
frequency triad.  Two transverse Fourier polarizations are classical; the
construction is a triad-adapted Craya--Herring frame and is closely related to
Waleffe's helical triad decomposition.  I do **not** claim to have invented
that decomposition.  The new, narrower result recorded here is its alignment
with the critical \(\mathcal X^{-1}\) symbol:

1. the exact ordered critical operator norm and equality condition;
2. a strict high--high-to-low gap for the in-plane polarization channel;
3. an exact proof that the normal channel retains constant one and has no
   shell decay under pure angular averaging;
4. the corresponding channel formula for the symmetrized cross interaction.

These are pointwise triad statements.  They do not yet construct a closed
anisotropic solution space, control a sum over different triads, or prove a
large-data estimate.  Nothing here proves or disproves global regularity for
three-dimensional Navier--Stokes.

## 2. Fourier--Leray symbol and triad frame

Let

\[
 p,q,k=p+q\in\mathbb R^3\setminus\{0\},
 \qquad p\times q\ne0,
\tag{2.1}
\]

and let the input polarizations satisfy

\[
 p\cdot a=0,
 \qquad q\cdot b=0.
\tag{2.2}
\]

For one ordered interaction define the scale-critical symbol

\[
 \mathcal K_{p,q}(a,b)
 =\frac1{|k|}P_k\!\left[(q\cdot a)b\right],
 \qquad
 P_k=I-\widehat k\otimes\widehat k.
\tag{2.3}
\]

Set

\[
 n=\frac{p\times q}{|p\times q|},
 \qquad
 t_p=n\times\widehat p,
 \qquad
 t_q=n\times\widehat q,
 \qquad
 t_k=n\times\widehat k.
\tag{2.4}
\]

Then \((n,t_p)\), \((n,t_q)\), and \((n,t_k)\) are oriented orthonormal
bases of \(p^\perp\), \(q^\perp\), and \(k^\perp\), respectively.  Write

\[
 a=a_n n+a_t t_p,
 \qquad
 b=b_n n+b_t t_q.
\tag{2.5}
\]

The frame is fixed without an external axis.  For every \(R\in SO(3)\), the
frame of \((Rp,Rq,Rk)\) is exactly \((Rn,Rt_p,Rt_q,Rt_k)\), so the
construction is rotation covariant.  If the triad is collinear, the frame is
undefined but the ordered symbol vanishes because \(q\parallel p\) and
\(a\perp p\).

## 3. Exact two-channel theorem

Define

\[
 g_N(p,q)=\frac{|p\times q|}{|p||k|},
 \qquad
 c_q=\widehat q\cdot\widehat k.
\tag{3.1}
\]

### Theorem 1 — ordered channel identity

For every noncollinear triad satisfying (2.1)--(2.2),

\[
 \boxed{
 \mathcal K_{p,q}(a,b)
 =g_N(p,q)a_t
 \left(b_n n+c_qb_t t_k\right).
 }
\tag{3.2}
\]

Consequently the two right-polarization channel gains are

\[
 \boxed{
 g_N=\frac{|p\times q|}{|p||k|},
 \qquad
 g_T=g_N|c_q|
 =\frac{|p\times q|\,|q\cdot k|}
 {|p||q||k|^2}.
 }
\tag{3.3}
\]

The exact bilinear operator norm is

\[
 \boxed{
 \|\mathcal K_{p,q}\|_{p^\perp\times q^\perp\to k^\perp}
 =g_N
 =\sin\angle(p,k)\le1.
 }
\tag{3.4}
\]

For a noncollinear triad, \(0\le g_T<g_N\).  The critical constant one is
attained if and only if

\[
 p\cdot k=0.
\tag{3.5}
\]

One maximizing pair is \(a=t_p\), \(b=n\), and the output is \(n\).

### Proof

Input incompressibility and the frame give

\[
 \frac{q\cdot a}{|k|}
 =\frac{q\cdot t_p}{|k|}a_t
 =\frac{|p\times q|}{|p||k|}a_t
 =g_Na_t.
\tag{3.6}
\]

The normal vector already belongs to \(k^\perp\), while

\[
 P_kt_q=(t_q\cdot t_k)t_k
 = (\widehat q\cdot\widehat k)t_k=c_qt_k.
\tag{3.7}
\]

Equations (3.6)--(3.7) prove (3.2).  The two input coefficients are
independent, so the largest right-channel gain is one in the normal
direction, and (3.4) follows.  The Gram identity

\[
 |p|^2|k|^2-(p\cdot k)^2=|p\times k|^2=|p\times q|^2
\tag{3.8}
\]

gives the sine formula and characterizes equality.  Finally,
\(|c_q|<1\) for every noncollinear triad, proving the strict channel
ordering. \(\square\)

The squared gains in (3.3) are rational whenever \(p,q\in\mathbb Z^3\):

\[
 g_N^2=\frac{|p\times q|^2}{|p|^2|k|^2},
 \qquad
 g_T^2=\frac{|p\times q|^2(q\cdot k)^2}
 {|p|^2|q|^2|k|^4}.
\tag{3.9}
\]

This makes the theorem suitable for an exact integer regression without
floating-point angle decisions.

## 4. High--high-to-low channel separation

Let \(P=|p|\), \(K=|k|\), and introduce

\[
 \varepsilon=\frac KP,
 \qquad
 \mu=\widehat p\cdot\widehat k,
 \qquad
 q=k-p.
\tag{4.1}
\]

Then

\[
 \frac{|q|}{P}=\sqrt{1+\varepsilon^2-2\varepsilon\mu}
\tag{4.2}
\]

and Theorem 1 becomes

\[
 \boxed{g_N(\varepsilon,\mu)=\sqrt{1-\mu^2},}
\tag{4.3}
\]

\[
 \boxed{
 g_T(\varepsilon,\mu)
 =\frac{\sqrt{1-\mu^2}\,|\varepsilon-\mu|}
 {\sqrt{1+\varepsilon^2-2\varepsilon\mu}}.
 }
\tag{4.4}
\]

The first formula is exactly independent of the shell ratio
\(\varepsilon\).  Thus the R0.55 saturation is not a loss caused by merging
different output directions: the normal channel itself remains scale
critical.

The planar channel behaves differently.

### Theorem 2 — strict planar gap

For every noncollinear triad,

\[
 \boxed{
 g_T\le\frac{|q|}{2|p|}\le\frac{1+\varepsilon}{2}.
 }
\tag{4.5}
\]

Hence, in the high--high-to-low cell \(K/P\le\rho<1\),

\[
 \boxed{g_T\le\frac{1+\rho}{2}<1.}
\tag{4.6}
\]

As \(\rho\downarrow0\), the limiting constant \(1/2\) is sharp.

### Proof

Set

\[
 A=\sqrt{1-\mu^2},
 \qquad B=|\varepsilon-\mu|.
\]

Then \(|q|/P=\sqrt{A^2+B^2}\) and

\[
 g_T=\frac{AB}{\sqrt{A^2+B^2}}
 \le\frac{\sqrt{A^2+B^2}}2
 =\frac{|q|}{2|p|},
\tag{4.7}
\]

where the inequality is \(2AB\le A^2+B^2\).  The triangle inequality
\(|q|=|k-p|\le P+K\) proves the second bound.

For sharpness of the limiting constant, take

\[
 p_N=(N,N,0),
 \qquad k=(-1,0,0),
 \qquad q_N=(-N-1,-N,0).
\tag{4.8}
\]

Then \(K/P=1/(\sqrt2N)\to0\), while

\[
 g_N^2=\frac12,
 \qquad
 g_T^2=\frac{(N+1)^2}{2(2N^2+2N+1)}
 \longrightarrow\frac14.
\tag{4.9}
\]

Therefore \(g_T\to1/2\). \(\square\)

The R0.55 constant-one family has the complementary behavior:

\[
 p_N=(N,0,0),
 \quad q_N=(-N,1,0),
 \quad k=(0,1,0),
\tag{4.10}
\]

for which

\[
 g_N^2=1,
 \qquad
 g_T^2=\frac1{N^2+1}.
\tag{4.11}
\]

The planar channel vanishes in the separated limit, while the normal channel
remains exactly saturated.

## 5. Angular averaging cannot create shell decay in the normal channel

Fix \(p\ne0\) and \(K>0\), and average the output direction
\(\widehat k\in S^2\).  The scalar \(\mu=\widehat p\cdot\widehat k\) is
uniform on \([-1,1]\) with normalized spherical measure.  From (4.3), for
every \(s>-2\),

\[
 \boxed{
 \fint_{S^2}g_N(\widehat k)^s\,d\widehat k
 =\frac{\sqrt\pi\,\Gamma(1+s/2)}
 {2\Gamma(3/2+s/2)}.
 }
\tag{5.1}
\]

In particular,

\[
 \fint_{S^2}g_N\,d\widehat k=\frac\pi4,
 \qquad
 \fint_{S^2}g_N^2\,d\widehat k=\frac23.
\tag{5.2}
\]

Neither number depends on \(K/P\).  More sharply, for
\(0\le\delta\le1\),

\[
 \boxed{
 \frac{\big|\{\widehat k:g_N(\widehat k)\ge1-\delta\}\big|}
 {|S^2|}
 =\sqrt{2\delta-\delta^2}.
 }
\tag{5.3}
\]

The exact equality set \(p\cdot k=0\) is a great circle and has zero surface
measure, but every near-saturation band has positive measure independent of
shell separation.  Consequently, any positive angular envelope or fixed
\(L^s\) angular average of the normal channel inherits a non-decaying
high--high-to-low constant.  This does not exclude cancellation between
different triads, because such cancellation is destroyed before (5.1) when
absolute values are taken.

## 6. Symmetrized cross interaction

For two Fourier modes of the same velocity field, the cross coefficient at
\(k=p+q\) contains both orders:

\[
 \mathcal S_{p,q}(a,b)
 =\frac1{|k|}P_k\!\left[(q\cdot a)b+(p\cdot b)a\right].
\tag{6.1}
\]

Define

\[
 g_p=\frac{|p\times q|}{|p||k|},
 \qquad
 g_q=\frac{|p\times q|}{|q||k|},
 \qquad
 c_p=\widehat p\cdot\widehat k,
 \qquad
 c_q=\widehat q\cdot\widehat k.
\tag{6.2}
\]

Direct substitution into the same frame gives

\[
 \boxed{
 \begin{aligned}
 \mathcal S_{p,q}(a,b)
 ={}&\left(g_pa_tb_n-g_qa_nb_t\right)n\\
 &+a_tb_t\left(g_pc_q-g_qc_p\right)t_k,
 \end{aligned}}
\tag{6.3}
\]

where

\[
 g_pc_q-g_qc_p
 =\frac{|p\times q|\,(|q|^2-|p|^2)}
 {|p||q||k|^2}.
\tag{6.4}
\]

Equation (6.3) exposes two cancellations that an isotropic absolute value
cannot see.  The in-plane output vanishes when \(|p|=|q|\), and the normal
output can cancel between the two orders for correlated polarizations.
However, the constant-one obstruction survives: for the family (4.10), take
\(a=t_p\) and \(b=n\).  Then the reverse coefficient \(p\cdot b\) is zero and

\[
 |\mathcal S_{p_N,q_N}(t_p,n)|=1
 \qquad\text{for every }N.
\tag{6.5}
\]

Thus symmetrization alone does not remove the remaining normal channel.

## 7. Research decision

R0.56 resolves the minimal kernel question posed at the end of R0.55.

1. **A finite direction-resolved kernel exists.**  It has exactly two output
   polarization channels and depends only on scale ratios and triangle
   angles.
2. **One channel improves.**  The planar channel has the uniform strict gap
   (4.6) in every genuinely separated high--high-to-low cell.
3. **One channel remains obstructive.**  The normal channel attains one at
   every separation and its entire angular profile is independent of the
   separation ratio.
4. **The next useful state cannot be a positive angular envelope alone.**  It
   must preserve phase/sign correlation across different normal-channel
   triads, exploit time/heat organization, or use a coupled directional norm
   rather than separately summing absolute cell amplitudes.

This is a genuine structural refinement of R0.55, but its direct value for
the millennium problem is still limited.  It does not close a critical norm
for arbitrary large data and it does not rule out singularity formation.  As
a standalone result, the algebra is probably too elementary for a high-level
PDE paper because the underlying polarization frames are classical.  Its
potential value is as a precise lemma that reduces the unresolved interface
to one explicitly identified normal channel.

## 8. Exact reproducibility

`research/leray_polarization_channel_audit.py` uses only Python integers and
`fractions.Fraction`.  It records:

- exhaustive ordered noncollinear triads in a deterministic integer cube;
- direct rational Leray projections for both channels;
- the exact squared gains (3.9) and symmetrized coefficient (6.4);
- the all-\(N\) families (4.8) and (4.10);
- a machine-readable separation between formal theorems and finite
  regressions.

The audit uses no random seed, GPU, or floating-point sign decision.  Its
decimal fields are display values only.  Increasing the cube radius or family
cutoff strengthens the implementation regression, not the analytic theorem.

## References

1. F. Waleffe, *The nature of triad interactions in homogeneous turbulence*,
   Physics of Fluids A **4** (1992), 350--363.
   DOI: <https://doi.org/10.1063/1.858309>.
2. C. Cambon, *L'héritage de Craya, pour une approche statistique à points
   multiples de la turbulence homogène anisotrope*, C. R. Mécanique **345**
   (2017), 627--641. DOI: <https://doi.org/10.1016/j.crme.2017.05.004>.
3. Z. Lei and F.-H. Lin, *Global Mild Solutions of the Navier--Stokes
   Equations*, Communications on Pure and Applied Mathematics **64** (2011),
   1297--1304. DOI: <https://doi.org/10.1002/cpa.20361>;
   arXiv: <https://arxiv.org/abs/1203.2699>.
4. R0.55, *A critical Fourier bridge and a no-go theorem for scalar charge*.
