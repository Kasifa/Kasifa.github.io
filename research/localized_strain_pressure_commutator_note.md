# R0.69I — Exact localization of strain, pressure, and Betchov cancellation

## 1. Result

R0.69H proves that the principal pressure-Hessian sign is not determined by
the local pair \((S,\omega)\). The next possibility is that pressure becomes
favorable only after integration, because on the periodic domain

\[
 \int_{\mathbb T^3} S:\nabla^2p\,dx=0.
 \tag{1.1}
\]

R0.69I localizes (1.1) exactly. Let \(u,p\) be smooth and periodic, with
\(\nabla\cdot u=0\), and let \(\phi\) be a smooth scalar weight. Write

\[
 A=\nabla u,\qquad S=\frac12(A+A^T),\qquad
 H=\nabla^2p,qquad q=\operatorname{tr}(A^2)=-\Delta p.
 \tag{1.2}
\]

Then the weighted pressure pairing satisfies

\[
 \boxed{
 \int_{\mathbb T^3}\phi S:H\,dx
 =\int_{\mathbb T^3}(\Delta p)u\cdot\nabla\phi\,dx
 +\int_{\mathbb T^3}u_i(\partial_jp)(\partial_{ij}\phi)\,dx.}
 \tag{1.3}
\]

The right side is supported where the weight varies, but both terms have the
same Navier--Stokes scaling as the left side. Localization alone produces no
small scale factor.

The second global cancellation needed for the strain energy is Betchov's
identity. Its exact weighted form is

\[
 \boxed{
 \int_{\mathbb T^3}\phi
 \left(\operatorname{tr}(S^3)+\frac34\omega\cdot S\omega\right)dx
 =\int_{\mathbb T^3}
 \left(\frac12qu-A^2u\right)\cdot\nabla\phi\,dx.}
 \tag{1.4}
\]

Equations (1.3)--(1.4) give the complete localized strain budget. They also
give a strict route decision:

\[
 \boxed{
 \text{bare spatial localization converts both global cancellations into}
 \text{ nonzero, scale-equal boundary commutators}.}
 \tag{1.5}
\]

This does not rule out controlling those commutators with additional
multiscale, harmonic, Morrey, or geometric information. It proves that the
cutoff operation itself supplies neither a sign nor a subcritical power.

## 2. Weighted pressure orthogonality

Because \(H\) is symmetric,

\[
 S:H=A:H=\partial_j u_i\,\partial_{ij}p.
 \tag{2.1}
\]

Integrating first in \(x_j\) gives

\[
 \begin{aligned}
 \int\phi\,\partial_j u_i\,\partial_{ij}p
 &=-\int u_i(\partial_j\phi)(\partial_{ij}p)
   -\int\phi u_i\partial_i\Delta p\\
 &=-\int u_i(\partial_j\phi)(\partial_{ij}p)
   +\int(\Delta p)u\cdot\nabla\phi.
 \end{aligned}
 \tag{2.2}
\]

The first term in the last line is integrated in \(x_i\):

\[
 -\int u_i(\partial_j\phi)(\partial_{ij}p)
 =\int(\partial_jp)\partial_i(u_i\partial_j\phi)
 =\int u_i(\partial_jp)(\partial_{ij}\phi),
 \tag{2.3}
\]

where \(\partial_i u_i=0\). This proves (1.3). Setting \(\phi=1\)
recovers (1.1).

For a cutoff equal to one on \(B_r\) and zero outside \(B_{2r}\), equation
(1.3) places the pressure defect in the annulus:

\[
 \left|\int\phi S:H\right|
 \le \frac{C}{r}\int_{B_{2r}\setminus B_r}|u|\,|q|,dx
 +\frac{C}{r^2}\int_{B_{2r}\setminus B_r}|u|\,|\nabla p|\,dx.
 \tag{2.4}
\]

This is an exact localization bound, not a closure: the second term still
contains a genuinely nonlocal pressure gradient.

## 3. Weighted Betchov identity

For the convention \(A_{ij}=\partial_j u_i\),

\[
 \operatorname{tr}(A^3)
 =\partial_j u_i\,\partial_k u_j\,\partial_i u_k.
 \tag{3.1}
\]

Integrating the first derivative in \(x_j\), using incompressibility, and
averaging the last term with the same expression after interchanging
\(j,k\), gives

\[
 \begin{aligned}
 \int\phi\operatorname{tr}(A^3)
 &=-\int u_i(\partial_j\phi)(\partial_k u_j)(\partial_i u_k)
   +\frac12\int q\,u\cdot\nabla\phi\\
 &=\int\left(\frac12qu-A^2u\right)\cdot\nabla\phi.
 \end{aligned}
 \tag{3.2}
\]

Writing \(A=S+\Omega\), with

\[
 \Omega^2=\frac14(\omega\otimes\omega-|\omega|^2I),
 \tag{3.3}
\]

shows pointwise that

\[
 \operatorname{tr}(A^3)
 =\operatorname{tr}(S^3)+\frac34\omega\cdot S\omega.
 \tag{3.4}
\]

Equations (3.2)--(3.4) prove (1.4). Since a trace-free three-by-three
matrix satisfies \(\operatorname{tr}(S^3)=3\det S\), there is also the
pointwise reduction

\[
 \boxed{
 \operatorname{tr}(S^3)+\frac14\omega\cdot S\omega
 =2\det S+\frac13\operatorname{tr}(A^3).}
 \tag{3.5}
\]

## 4. Complete localized strain budget

The strain equation is

\[
 (\partial_t+u\cdot\nabla-\Delta)S+S^2+\Omega^2+H=0.
 \tag{4.1}
\]

Multiplying by \(\phi S\), integrating, and applying (1.3), (1.4), and
(3.5) yields

\[
\boxed{
\begin{aligned}
 \frac12\frac d{dt}\int\phi|S|^2
 +\int\phi|\nabla S|^2
 +2\int\phi\det S
 ={}&\frac12\int(\Delta\phi+u\cdot\nabla\phi)|S|^2\\
 &-\frac13\int\left(\frac12qu-A^2u\right)\cdot\nabla\phi\\
 &-\int(\Delta p)u\cdot\nabla\phi
 -\int u_i(\partial_jp)(\partial_{ij}\phi).
\end{aligned}}
 \tag{4.2}
\]

No pressure term remains in the interior where \(\phi=1\), but it has not
disappeared: it is exactly transferred to the cutoff annulus. The cubic
Betchov correction is transferred to the same annulus.

## 5. Scaling audit

Under the Navier--Stokes scaling

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),\qquad
 p_\lambda(x,t)=\lambda^2p(\lambda x,\lambda^2t),\qquad
 \phi_\lambda(x)=\phi(\lambda x),
 \tag{5.1}
\]

and after changing variables in a correspondingly scaled local region, all
of the following quantities scale as \(\lambda^3\):

\[
 \int\phi S:H,quad
 \int(\Delta p)u\cdot\nabla\phi,quad
 \int u_i(\partial_jp)(\partial_{ij}\phi),
 \tag{5.2}
\]

and

\[
 \int\phi\operatorname{tr}(A^3),quad
 \int qu\cdot\nabla\phi,quad
 \int(A^2u)\cdot\nabla\phi.
 \tag{5.3}
\]

Thus the annular location of the commutators is useful bookkeeping, but
localization does not lower their scaling degree.

## 6. Exact finite Fourier witness

The audit uses four real cosine carriers on \(\mathbb T^3\):

\[
\begin{array}{c|c|c}
k&a&c\\ \hline
(1,1,0)&(1,-1,2)&1\\
(1,0,1)&(2,1,-2)&2/3\\
(0,1,1)&(1,2,-2)&3/5\\
(1,-1,1)&(1,2,1)&4/7.
\end{array}
 \tag{6.1}
\]

Each \(k\cdot a=0\), and the weight is

\[
 \phi(x)=1+\frac17\sin x_3-\frac1{11}\sin x_1.
 \tag{6.2}
\]

Exact rational Fourier convolution gives

\[
 \int\phi S:H=-\frac{676}{40425},
 \tag{6.3}
\]

while the two terms on the right of (1.3) are

\[
 \int(\Delta p)u\cdot\nabla\phi=-\frac{332}{8085},
 \qquad
 \int u_i(\partial_jp)(\partial_{ij}\phi)=\frac{328}{13475}.
 \tag{6.4}
\]

Their sum is exactly (6.3). The global pressure pairing is zero. The same
field gives

\[
 \int\phi\operatorname{tr}(A^3)=\frac{228}{2695}\ne0,
 \tag{6.5}
\]

equal exactly to the boundary flux in (1.4), while the unweighted Betchov
pairing is zero. Hence both localized commutators are genuinely nonzero,
not merely artifacts of an upper bound.

## 7. Claim boundary and route decision

R0.69I proves the exact weighted identities (1.3), (1.4), and (4.2), and
exhibits a finite Fourier field on which both boundary commutators are
nonzero. It does not prove that no additional structure can control them.

The result closes only the bare-localization route: multiplying the global
strain identity by a cutoff does not itself create a favorable sign or a
small scale factor. It gives no Navier--Stokes regularity or singularity
conclusion and does not solve the Millennium Problem.

R0.69J will split the pressure on a ball into a near-field Newtonian part and
a harmonic far-field part. The next test is whether subtracting low harmonic
multipoles, together with trace-free strain and annular flux identities, gives
a genuine scale-decaying remainder. If the harmonic tail retains a leading
quadrupole of the same critical size, I will record that obstruction.
