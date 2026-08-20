# R0.69C — The transverse sideband symbol and critical linearized stability

## 1. Result

Let \(U_r\) be the exact R0.69A periodic invariant-shear solution and put

\[
 \delta_r:=\|U_r(0)\|_{BMO^{-1}_{\rm per}}
 \le C_0\rho^r,
 \qquad C_0=6+4\sqrt2,
 \qquad \rho<0.797586.
\tag{1.1}
\]

R0.69B showed that the base data become small in a scaling-critical norm.
The present note determines what that fact does to the complete linearized
propagator, including every non-normal Fourier interaction.

Let \(E_{\rm per}=BMO^{-1}_{\rm per}\), let \(X_{\rm per}\) be the periodic
Koch--Tataru path space, and write

\[
 S f=e^{t\Delta}f,
 \qquad
 \mathcal B(a,b)(t)
 =-\int_0^t e^{(t-\tau)\Delta}\mathbb P\nabla\!\cdot(a\otimes b)(\tau)\,d\tau.
\tag{1.2}
\]

Fix admissible constants \(C_H,C_B>0\) in the standard periodic estimates

\[
 \|Sf\|_{X_{\rm per}}\le C_H\|f\|_{E_{\rm per}},
 \qquad
 \|\mathcal B(a,b)\|_{X_{\rm per}}
 \le C_B\|a\|_{X_{\rm per}}\|b\|_{X_{\rm per}}.
\tag{1.3}
\]

If

\[
 \kappa_r:=4C_BC_HC_0\rho^r<1,
\tag{1.4}
\]

then the global linearization about \(U_r\),

\[
 w=Sw_0+\mathcal B(U_r,w)+\mathcal B(w,U_r),
\tag{1.5}
\]

has a unique solution for every divergence-free \(w_0\in E_{\rm per}\), and

\[
 \boxed{
 \|w\|_{X_{\rm per}}
 \le \frac{C_H}{1-\kappa_r}\|w_0\|_{E_{\rm per}},
 \qquad
 \|w-Sw_0\|_{X_{\rm per}}
 \le \frac{C_H\kappa_r}{1-\kappa_r}
       \|w_0\|_{E_{\rm per}}.}
\tag{1.6}
\]

Thus the linearized propagator converges in critical operator norm to the
free heat map at the certified geometric rate \(O(\rho^r)\).  This statement
allows \(\|w_0\|_{E_{\rm per}}\) to be of order one: smallness is required of
the base, not of the vector on which the linear operator acts.

Consequently, no linear non-normal sideband around the R0.69A packet can
produce an order-one critical amplification as \(r\to\infty\).  Any remaining
route through this packet must use the nonlinear self-interaction
\(\mathcal B(w,w)\) at order-one perturbation size.  The theorem does not
control that term and is not a large-data regularity result.

## 2. Exact Fourier--Leray linearization

Use the Fourier convention

\[
 f(x)=\sum_{k\in\mathbb Z^3}\widehat f(k)e^{ik\cdot x},
 \qquad
 P_k=I-\frac{k\otimes k}{|k|^2}\quad(k\ne0).
\tag{2.1}
\]

The linearized equation

\[
 \partial_tw-\Delta w
 +(U\cdot\nabla)w+(w\cdot\nabla)U+\nabla q=0,
 \qquad \nabla\cdot w=0,
\tag{2.2}
\]

is exactly

\[
 \boxed{
 \partial_t\widehat w(k)+|k|^2\widehat w(k)
 =-iP_k\sum_{\ell\in\mathbb Z^3}
 \left[
   \bigl(\widehat U(\ell)\cdot(k-\ell)\bigr)
       \widehat w(k-\ell)
  +\bigl(\widehat w(k-\ell)\cdot\ell\bigr)
       \widehat U(\ell)
 \right].}
\tag{2.3}
\]

Every base frequency of \(U_r\) has third component zero.  Therefore the
right-hand side of (2.3) preserves \(k_3\).  Each plane

\[
 \{k\in\mathbb Z^3:k_3=s\},\qquad s\in\mathbb Z,
\tag{2.4}
\]

is an exact invariant sideband of the full linearized equation.  Choosing
\(s\ne0\) gives a genuinely three-dimensional perturbation sector.

## 3. One carrier gives an exact non-normal matrix

Take one positive shear carrier and one transverse seed,

\[
 p=(R,0,0),\qquad q=(-R,m,s),\qquad k=p+q=(0,m,s),
\tag{3.1}
\]

where \(R,m\ge1\) and \(s\ne0\).  Put

\[
 d=\sqrt{m^2+s^2},\qquad Q=\sqrt{R^2+d^2},
\tag{3.2}
\]

and define two orthonormal polarizations in \(q^\perp\),

\[
 n=\frac{(0,-s,m)}d,
 \qquad
 b=\frac1Q\left(d,\frac{Rm}{d},\frac{Rs}{d}\right).
\tag{3.3}
\]

The carrier polarization is \(e_2\).  For a seed polarization
\(\beta\in q^\perp\), the complete ordered-plus-exchanged linearized symbol
at \(k\) is

\[
 \mathscr T_{R,m,s}\beta
 :=P_k\left[m\beta+R\beta_1e_2\right].
\tag{3.4}
\]

The first term is base transport and the second is transverse stretching.
In the domain basis \((b,n)\) and output basis \((e_1,n)\), (3.4) is the
lower triangular matrix

\[
 \boxed{
 [\mathscr T_{R,m,s}]
 =\begin{pmatrix}
  \dfrac{md}{Q}&0\\[4pt]
  -\dfrac{Rs}{Q}&m
 \end{pmatrix}.}
\tag{3.5}
\]

The off-diagonal entry is nonzero exactly when \(s\ne0\); this is the
non-normal stretch that is absent in the invariant shear class.  Leray
projection does not erase it.

Nevertheless, the exact matrix has the sharp derivative-scale bound

\[
 \boxed{\|\mathscr T_{R,m,s}\|_{\ell^2\to\ell^2}\le d=|k|.}
\tag{3.6}
\]

Indeed, if \(T\) denotes the matrix in (3.5), then

\[
 d^2I-T^*T=
 \begin{pmatrix}
  \dfrac{R^2m^2+d^2s^2}{Q^2}&\dfrac{Rsm}{Q}\\[6pt]
  \dfrac{Rsm}{Q}&s^2
 \end{pmatrix},
\qquad
 \det(d^2I-T^*T)=\frac{d^2s^4}{Q^2}\ge0.
\tag{3.7}
\]

Both principal minors are nonnegative, proving (3.6).  The matrix can be
strongly non-normal while still carrying no derivative larger than the
target frequency.

## 4. The heat denominator defeats a single transverse carrier

Let the heat-evolved carrier at \(p\) have coefficient \(Ae_2\) and the
heat-evolved seed at \(q\) have coefficient \(B\beta\).  The first
linearized Duhamel response at \(k\) is exactly

\[
 \boxed{
 \widehat D^{(1)}(k,t)
 =-iABe^{-d^2t}
 \frac{1-e^{-2R^2t}}{2R^2}
 \mathscr T_{R,m,s}\beta.}
\tag{4.1}
\]

The denominator is exactly \(2R^2\), for

\[
 |p|^2+|q|^2-|k|^2=R^2+(R^2+d^2)-d^2=2R^2.
\tag{4.2}
\]

Moreover,

\[
 \sup_{t\ge0}e^{-d^2t}
 \frac{1-e^{-2R^2t}}{2R^2}
 =\frac1{d^2+2R^2}
 \left(\frac{d^2}{d^2+2R^2}\right)^{d^2/(2R^2)}.
\tag{4.3}
\]

Measure a single Fourier coefficient by the scaling-critical proxy
\(|\widehat f(\xi)|/|\xi|\).  Equations (3.6)--(4.3) imply, uniformly in
the transverse frequency \(s\),

\[
 \boxed{
 \frac{\sup_t|\widehat D^{(1)}(k,t)|/|k|}
 {|B|/|q|}
 \le \frac{|A|Q}{d^2+2R^2}
 \le\frac{|A|}{2R}.}
\tag{4.4}
\]

The last inequality is the identity

\[
 (d^2+2R^2)^2-4R^2Q^2=d^4\ge0.
\tag{4.5}
\]

For an R0.69A carrier, \(R\ge H_r\) and
\(A=A_r=\varepsilon_r\sqrt{H_r}\).  Thus the one-carrier critical gain is
at most

\[
 \frac{\varepsilon_r}{2\sqrt{H_r}},
\tag{4.6}
\]

which tends to zero even faster than the complete packet norm.  Coherent
summation over the packet can restore the larger \(O(\varepsilon_r)\) scale,
but (1.6) proves that it cannot exceed that scale after all repeated
linearized interactions are included.

## 5. Full propagator proof

The small-data fixed-point estimate applied to the base gives

\[
 \|U_r\|_{X_{\rm per}}\le2C_H\delta_r
 \le2C_HC_0\rho^r
\tag{5.1}
\]

whenever \(4C_BC_H\delta_r<1\).  Define

\[
 K_rw=\mathcal B(U_r,w)+\mathcal B(w,U_r).
\tag{5.2}
\]

Then

\[
 \|K_r\|_{X_{\rm per}\to X_{\rm per}}
 \le2C_B\|U_r\|_{X_{\rm per}}
 \le4C_BC_HC_0\rho^r=\kappa_r<1.
\tag{5.3}
\]

Hence \(I-K_r\) is invertible by the Neumann series and

\[
 w=(I-K_r)^{-1}Sw_0.
\tag{5.4}
\]

The resolvent bounds

\[
 \|(I-K_r)^{-1}\|\le\frac1{1-\kappa_r},
 \qquad
 \|(I-K_r)^{-1}-I\|\le\frac{\kappa_r}{1-\kappa_r}
\tag{5.5}
\]

give (1.6).  This proof sums the complete linearized interaction series; it
is not a first-Picard truncation.

## 6. What this decides

R0.69C closes the linear-instability branch for the canonical deep packet:

1. genuinely three-dimensional sidebands are exact invariant Fourier
   sectors;
2. transverse stretching survives pressure projection and gives an explicit
   non-normal matrix;
3. one carrier pays the exact parabolic denominator and has vanishing
   critical gain;
4. after every carrier and every repeated interaction is restored, the full
   linearized propagator differs from free heat by only \(O(\rho^r)\) in the
   Koch--Tataru critical path norm.

The conclusion is negative but decisive: the large physical Fourier
amplitudes in R0.69A do not generate a hidden linear critical instability.
Their collective critical size is small, and the complete critical
propagator detects that smallness.

## 7. Hard boundary and next problem

The result does **not** imply that \(U_r+w_0\) is globally regular when
\(\|w_0\|_{E_{\rm per}}\) is order one.  The exact perturbation equation also
contains

\[
 \mathcal B(w,w),
\tag{7.1}
\]

which is absent from the linearized problem and is not perturbative at
order-one critical size.  Nor does (1.6) assert decay in every conceivable
critical norm; it is a theorem in the Koch--Tataru data/path-space pair.

The next falsifiable problem is therefore nonlinear and comparative.  Given
an order-one smooth transverse datum \(w_0\), compare the solution from
\(w_0+U_r(0)\) with the solution from \(w_0\) on every interval where the
latter has a finite critical path norm.  A scale-uniform difference estimate
would show that the deep invariant packet is asymptotically irrelevant even
in the nonlinear dynamics.  Failure would have to identify a concrete
order-one nonlinear resonance, not a linear non-normal transient.

This note proves neither large-data global regularity nor finite-time
singularity and does not resolve the Navier--Stokes Millennium problem.

## References

1. H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations*,
   Advances in Mathematics 157 (2001), 22--35,
   <https://math.berkeley.edu/~tataru/papers/nas.pdf>.
2. P. Germain, N. Pavlovi\'c, and G. Staffilani, *Regularity of solutions to
   the Navier--Stokes equations evolving from small data in
   \(BMO^{-1}\)*, International Mathematics Research Notices 2007,
   rnm087, <https://arxiv.org/abs/math/0609781>.

