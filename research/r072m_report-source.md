# R0.72M -- a frozen full-lattice phase-mixing screen

**Date:** 2026-08-27

**Status:** an exact scalar danger-window theorem and a sharp phase-mixing benchmark
inside the one-carrier sector inherited from R0.72L.  The calculation uses
the complete infinite Fourier chain, not a finite Galerkin closure.  It
identifies the exact action interval in which the R0.72L cubic scalar term
can be large.  The zero-diffusion reference chain lies below that interval:
its exact action is \(\asymp\sigma^{4/3}\log\sigma\), its enstrophy scale is
\(\asymp\sigma^2\), and its true cubic mass is only logarithmic.  Proving
the corresponding safety branch or logarithmic cubic upper bound for the
dissipative chain remains open.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, strong
coupling, phase mixing, full Fourier lattice, Bessel functions, cubic
variation, enhanced dissipation

---

## 0. Direct decision

R0.72L isolated the extreme common-band remainder

\[
 \frac{\varepsilon^{7/3}p^{4/3}}
 {K+\max\{\varepsilon^2p/R,Z\}}.
 \tag{0.1}
\]

That expression came from optimizing the exact scalar term

\[
 T(x)=\frac{\min\{U,Vx\}}{K+x},
 \qquad H=\frac UV,
 \tag{0.2}
\]

over every \(x\ge Z\).  R0.72M first removes that optimization loss.  For
any \(A>0\),

\[
 \boxed{
 T(x)>A
 \iff
 \frac{AK}{V-A}<x<\frac UA-K,}
 \tag{0.3}
\]

provided \(A<U/(K+H)\); otherwise the set is empty.  Thus a large cubic
ratio requires action in a specific middle window.  Either
\(Vx=o(K)\) (action-poor) or \(U=o(K+x)\) (denominator-rich) forces
\(T(x)=o(1)\).

With the inherited floor \(x\ge Z\), the exact set is simply

\[
 [Z,\infty)\cap
 \left(\frac{AK}{V-A},\frac UA-K\right).
 \tag{0.3a}
\]

The rest of R0.72M tests the action-poor branch in the smallest full-lattice
strong-coupling sector.

After parabolic rescaling, phase rotation, and removal of the common scalar
heat factor, the one-carrier chain has coupling parameter
\(\sigma=\varepsilon\) and zero-diffusion reference equation

\[
 \partial_y f_n
 =\sigma e^{-y}(f_{n-1}-f_{n+1}),
 \qquad n\in\mathbb Z.
 \tag{0.4}
\]

For the row-aligned launch

\[
 f_1(0)=2^{-1/2},\qquad
 f_{-1}(0)=-2^{-1/2},\qquad
 f_n(0)=0\quad(n\ne\pm1),
 \tag{0.5}
\]

put \(s=\sigma(1-e^{-y})\).  The exact full-lattice solution is

\[
 \boxed{f_n(s)=\sqrt2\,J_n'(2s).}
 \tag{0.6}
\]

Three different scales follow.

1. The exact Fourier-gradient moment is

   \[
    \boxed{\sum_{n\in\mathbb Z}n^2|f_n(s)|^2=1+s^2.}
 \tag{0.7}
   \]

   Hence the frozen enstrophy contrast is \(\asymp\sigma^2\), which is
   \(o(\sigma^{7/3})\).

2. Let \(Bf=(f_{n-1}-f_{n+1})_n\), fix \(\mu>0\), and define the
   complete negative-norm density

   \[
   q(s)=\sum_{n\in\mathbb Z}
   \frac{|(Bf(s))_n|^2}{\mu+n^2}.
   \tag{0.8}
   \]

   Its frozen critical action is

   \[
   A_\sigma=\int_0^1
   y^{-1/3}[1+\log(1/y)]e^{-2(1+\mu)y}
   q(\sigma(1-e^{-y}))\,dy.
   \tag{0.9}
   \]

   Then

   \[
   \boxed{
   A_\sigma\sim A_0\sigma^{-2/3}\log\sigma,
   \qquad
   A_0=\int_0^\infty s^{-1/3}q(s)\,ds\in(0,\infty).}
   \tag{0.10}
   \]

   After the inherited \(\Theta\asymp\sigma^2\) lift, this is the
   \(\sigma^{4/3}\log\sigma\) scale already seen in the R0.72L local
   floor.  For fixed one-carrier geometry, the lifted action satisfies
   \(x_{\rm fr}\asymp\sigma^{4/3}\log\sigma\).

3. The exact frozen true-cubic mass on \(0\le y\le1\) is

   \[
   \mathcal C_{\rm fr}(\sigma)
   =4a^2\int_0^{\sigma(1-e^{-1})}
   \left(1-\frac{s}{\sigma}\right)^{2+2\mu}
   |u(s)u'(s)|\,ds.
   \tag{0.11}
   \]

   Its sharp asymptotic is

   \[
   \boxed{
   \mathcal C_{\rm fr}(\sigma)
   =\frac{16}{\pi^2}a^2\log\sigma+O(a^2).}
   \tag{0.12}
   \]

   Thus

   \[
   \frac{\mathcal C_{\rm fr}(\sigma)}
   {\sigma a^2}
   \longrightarrow0.
   \tag{0.13}
   \]

For this one-carrier benchmark, \(p=1\) and the carrier \(R=R_0\) is fixed
while \(\sigma\to\infty\).  Suppressing constants depending on \(R_0\),
\(U\asymp\sigma^{7/3}\), \(V\asymp\sigma^{1/3}\), and
\(H\asymp\sigma^2\).  Hence

\[
 \frac{x_{\rm fr}}H\asymp\sigma^{-2/3}\log\sigma\to0,
 \qquad
 \frac{Vx_{\rm fr}}{K_{\rm fr}}
 \asymp\sigma^{-1/3}\log\sigma\to0.
 \tag{0.14}
\]

The frozen chain is therefore action-poor and already safe in the original
\(Vx/(K+x)\) branch.  The optimized remainder (0.1) is not sharp on this
family.  The logarithmic true-cubic law independently confirms that the
raw \(O(\sigma)\) estimate has a large variation loss.

R0.72M replaces the former three slogans by two precise open routes for the
dissipative chain: prove \(Vx=o(K)\), or prove a sublinear true-cubic bound,
with constants uniform in the declared common band.

This is not an arbitrary-strong-coupling closure for the Navier--Stokes
system.  Removing the diagonal heat operator is a benchmark operation, not
an exact PDE reduction.  The Clay problem remains open.

---

## 1. Exact one-carrier normalization

Take one real carrier \(R\) orthogonal to a fixed nonzero target frequency
\(q_*\), as in the inherited \(K_y=0\) geometry.  The passive frequencies
are \((nR,q_*)\), so their squared lengths are \(n^2R^2+q_*^2\), with no
linear cross term.  Put \(\mu=q_*^2/R^2>0\).  After the time change
\(y=R^2x\), the phase rotation, and

\[
 F_n(y)=e^{-\mu y}(-i)^nf_n(y),
 \tag{1.0}
\]

the dissipative chain for \(f\) is

\[
 \partial_y f_n
 =-n^2f_n+\sigma e^{-y}(f_{n-1}-f_{n+1}),
 \qquad \sigma=\frac{|\delta|a}{R^2}=\varepsilon.
 \tag{1.1}
\]

The reference chain (0.4) deletes only the relative diagonal
\(-n^2f_n\).  It keeps the
complete convolution lattice and the physical carrier envelope \(e^{-y}\).
The common target heat \(e^{-\mu y}\) is restored explicitly in every
physical action and cubic row below.  No coordinate cutoff is introduced.

Let \(B\) be the skew-adjoint difference operator

\[
 (Bf)_n=f_{n-1}-f_{n+1}.
 \tag{1.2}
\]

The frozen propagator is unitary on \(\ell^2(\mathbb Z)\).  With

\[
 s=\sigma(1-e^{-y}),\qquad ds=\sigma e^{-y}\,dy,
 \tag{1.3}
\]

equation (0.4) becomes

\[
 \partial_sf=Bf.
 \tag{1.4}
\]

The launch (0.5) has unit \(\ell^2\) norm and lies in the real symmetry
sector preserved by (1.4).

---

## 2. Full-lattice Bessel solution

For a point mass at index \(m\), the solution of (1.4) is

\[
 (e^{sB}e_m)_n=J_{n-m}(2s),
 \tag{2.1}
\]

because

\[
 \frac d{ds}J_k(2s)=J_{k-1}(2s)-J_{k+1}(2s).
 \tag{2.2}
\]

Applying (2.1) to (0.5) gives

\[
 f_n(s)=\frac{J_{n-1}(2s)-J_{n+1}(2s)}{\sqrt2}
 =\sqrt2J_n'(2s).
 \tag{2.3}
\]

This proves (0.6).  Parseval and unitarity give

\[
 \sum_n|f_n(s)|^2=1.
 \tag{2.4}
\]

The generating function is even more useful:

\[
 G(s,\theta)=\sum_nf_n(s)e^{in\theta}
 =i\sqrt2\sin\theta\,e^{2is\sin\theta}.
 \tag{2.5}
\]

Differentiation gives

\[
 |\partial_\theta G|^2
 =2\cos^2\theta+8s^2\sin^2\theta\cos^2\theta.
 \tag{2.6}
\]

Therefore Parseval yields

\[
 \sum_nn^2|f_n(s)|^2
 =\frac1{2\pi}\int_0^{2\pi}|\partial_\theta G|^2\,d\theta
 =1+s^2.
 \tag{2.7}
\]

At \(y=1\), \(s=(1-e^{-1})\sigma\).  Any fixed positive background and
fixed carrier geometry therefore give

\[
 K_{\rm fr}(\sigma)\asymp1+\sigma^2.
 \tag{2.8}
\]

The exponent \(2\) is strictly below \(7/3\).  The full lattice can spread
to \(O(\sigma)\) Fourier indices without forcing the stronger lower bound
proposed in R0.72L.

---

## 3. Complete frozen critical action

Put \(u(s)=f_1(s)=\sqrt2J_1'(2s)\).  Near zero,
\(u(s)=2^{-1/2}+O(s^2)\), while fixed-order Bessel asymptotics give
\(u(s)=O(s^{-1/2})\).  Thus the target-row integral

\[
 0<\int_0^\infty s^{-1/3}|u(s)|^2\,ds<\infty
 \tag{3.1}
\]

is a valid lower signal.  It is not the complete negative-norm action.

For the latter, fix \(\mu>0\), set

\[
 (Av)_n=(\mu+n^2)v_n,
 \tag{3.2}
\]

and define

\[
 q(s)=\langle A^{-1}Bf(s),Bf(s)\rangle
 =\sum_{n\in\mathbb Z}
 \frac{|\partial_sf_n(s)|^2}{\mu+n^2}.
 \tag{3.3}
\]

The generating function of \(Bf\) is

\[
 2i\sin\theta\,G(s,\theta)
 =-2\sqrt2\sin^2\theta\,e^{2is\sin\theta}.
 \tag{3.4}
\]

Write \(c_n(s)=(Bf(s))_n\).  The following coefficient bounds are uniform
for \(s\ge1\):

\[
 |c_n(s)|\le
 \begin{cases}
 Cs^{-1/2},& |n|\le s,\\
 Cs^{-1/3},& s<|n|\le3s,\\
 C_N|n|^{-N},& |n|>3s
 \end{cases}
 \qquad(N=1,2,\ldots).
 \tag{3.4a}
\]

For completeness, these estimates can be read directly from the Fourier
integral in (3.4).  In the central region, the stationary points of
\(2s\sin\theta-n\theta\) obey \(|\sin\theta|\ge\sqrt3/2\), so uniform
one-dimensional stationary phase gives the first line.  In the transition
region, the large-order Airy expansion for \(J_n(2s)\), uniformly through
\(|n|\simeq2s\), gives the second line for the finite combination
\(J_{n-2}-2J_n+J_{n+2}\); this is the real-variable uniform expansion in
[DLMF Sections 10.19(iii) and 10.20(i)](https://dlmf.nist.gov/10.20.i).
For \(|n|>3s\), the phase derivative has size comparable to \(|n|\), and
\(N\) integrations by parts give the last line.

Consequently,

\[
 0<q(s)\le\frac{C_\mu}{1+s}.
 \tag{3.5}
\]

Indeed, the first line of (3.4a) contributes at most
\(Cs^{-1}\sum_n(\mu+n^2)^{-1}=O(s^{-1})\).  The second contributes
\(O(s^{-2/3})O(s^{-2})O(s)=O(s^{-5/3})\), and the final line is summable.
For \(0\le s\le1\), unitarity and \(\|B\|_{\ell^2\to\ell^2}\le2\) give
\(q(s)\le4/\mu\).  Therefore

\[
 A_0=\int_0^\infty s^{-1/3}q(s)\,ds
 \tag{3.6}
\]

is finite and strictly positive.

Make the change of variables (1.3) in (0.9).  With

\[
 y_\sigma(s)=-\log(1-s/\sigma),
 \tag{3.7}
\]

one obtains

\[
 A_\sigma
 =\frac1\sigma\int_0^{\sigma(1-e^{-1})}
 y_\sigma(s)^{-1/3}
 [1+\log(1/y_\sigma(s))]
 \left(1-\frac{s}{\sigma}\right)^{1+2\mu}q(s)\,ds.
 \tag{3.8}
\]

To make the growing domain and the logarithmic endpoint explicit, put
\(c=1-e^{-1}\), take \(\sigma\ge e\), and extend by zero outside
\((0,c\sigma)\) the normalized integrand

\[
 F_\sigma(s)=
 \mathbf 1_{(0,c\sigma)}(s)
 (\sigma y_\sigma(s))^{-1/3}
 \frac{1+\log(1/y_\sigma(s))}{\log\sigma}
 \left(1-\frac{s}{\sigma}\right)^{1+2\mu}q(s).
 \tag{3.8a}
\]

Then \(\sigma^{2/3}A_\sigma/\log\sigma=\int_0^\infty F_\sigma(s)\,ds\).
For every fixed \(s>0\), \(y_\sigma(s)\sim s/\sigma\), hence
\(F_\sigma(s)\to s^{-1/3}q(s)\).  Moreover
\(y_\sigma(s)\ge s/\sigma\), and, on the support of \(F_\sigma\),
\(s/\sigma<y_\sigma(s)\le1\).  Thus

\[
 0\le F_\sigma(s)
 \le C s^{-1/3}\bigl[1+\log_+(1/s)\bigr]q(s).
 \tag{3.8b}
\]

The right side is integrable: near zero use \(q(s)\le4/\mu\), while at
infinity (3.5) gives \(O(s^{-4/3})\).  Dominated convergence now gives

\[
 \lim_{\sigma\to\infty}
 \frac{\sigma^{2/3}A_\sigma}{\log\sigma}=A_0.
 \tag{3.9}
\]

The physical factor \(ae^{-(1+\mu)y}\) and the fixed geometry change only
the constant.  Multiplication by the inherited
\(\Theta\asymp\sigma^2\) yields

\[
 \boxed{x_{\rm fr}\asymp\sigma^{4/3}\log\sigma.}
 \tag{3.10}
\]

The target row \(|h|=2ae^{-(1+\mu)y}|u|\) gives the same exponent with a different
constant.  The two quantities must not be identified.

---

## 4. Sharp logarithmic true-cubic mass

In the symmetry sector (0.5), the two physical rows reduce to

\[
 h=-2ae^{-(1+\mu)y}f_1,
 \qquad
 b=-2a^2e^{-(2+\mu)y}(f_0-f_2).
 \tag{4.1}
\]

Equation (1.4) gives

\[
 f_0-f_2=u'(s).
 \tag{4.2}
\]

Using \(|\delta|a/R^2=\sigma\), \(y=R^2x\), and (1.3), the true cubic
integral becomes (0.11) exactly.

For fixed order, the differentiated Bessel expansion gives, with
\(\phi=2s-3\pi/4\),

\[
 u(s)=-\sqrt{\frac2{\pi s}}\sin\phi+O(s^{-3/2}),
 \tag{4.3}
\]

\[
 u'(s)=-2\sqrt{\frac2{\pi s}}\cos\phi+O(s^{-3/2}).
 \tag{4.4}
\]

Hence

\[
 |u(s)u'(s)|
 =\frac4{\pi s}|\sin\phi\cos\phi|+O(s^{-2}).
 \tag{4.5}
\]

The periodic factor has mean

\[
 \frac1\pi\int_0^\pi|\sin t\cos t|\,dt=\frac1\pi.
 \tag{4.6}
\]

Abel summation over its periods gives

\[
 \int_1^S|u(s)u'(s)|\,ds
 =\frac4{\pi^2}\log S+O(1).
 \tag{4.7}
\]

Finally,

\[
 \int_1^{c\sigma}
 \left[\left(1-\frac{s}{\sigma}\right)^{2+2\mu}-1\right]
 \frac{ds}{s}=O(1)
 \qquad(0<c<1),
 \tag{4.8}
\]

and the \(O(s^{-2})\) remainder is integrable.  Multiplying (4.7) by
the factor \(4a^2\) in (0.11) proves (0.12).

This logarithm is sharp.  It is not a cancellation obtained by removing the
absolute value.  It comes from the decay of successive full-lattice Bessel
oscillations.

---

## 5. Exact action danger window

The R0.72L cubic scalar term is

\[
 T(x)=\frac{\min\{U,Vx\}}{K+x},
 \qquad U,V,K>0,
 \qquad H=\frac UV.
 \tag{5.1}
\]

It is strictly increasing on \(0\le x\le H\), strictly decreasing on
\(x\ge H\), and has maximum

\[
 T(H)=\frac{U}{K+H}.
 \tag{5.2}
\]

### Theorem 5.1 -- exact superlevel interval

For \(A>0\), the set \(\{x\ge0:T(x)>A\}\) is empty when
\(A\ge U/(K+H)\).  When \(0<A<U/(K+H)\),

\[
 \boxed{
 \{T>A\}
 =\left(\frac{AK}{V-A},\frac UA-K\right).}
 \tag{5.3}
\]

#### Proof

For \(x\le H\),

\[
 T(x)=\frac{Vx}{K+x}>A
 \iff
 x>\frac{AK}{V-A}.
 \tag{5.4}
\]

For \(x\ge H\),

\[
 T(x)=\frac U{K+x}>A
 \iff
 x<\frac UA-K.
 \tag{5.5}
\]

The hypothesis \(A<U/(K+H)\) is exactly the condition that the left
endpoint in (5.3) lies below \(H\) and the right endpoint lies above it.
This proves the statement. \(\square\)

If the inherited action floor \(x\ge Z\) is imposed, the superlevel set is
the intersection of (5.3) with \([Z,\infty)\).  This formulation keeps the
endpoint correct when \(Z\) lies strictly inside the open danger interval.

Two consequences are immediate:

\[
 Vx=o(K)\quad\Longrightarrow\quad T(x)=o(1),
 \tag{5.6}
\]

\[
 U=o(K+x)\quad\Longrightarrow\quad T(x)=o(1).
 \tag{5.7}
\]

More generally, along any parameter sequence for which \(x>0\) eventually,

\[
 T(x)\to\infty
 \iff
 \frac{K+x}{Vx}\to0
 \quad\text{and}\quad
 \frac{K+x}{U}\to0.
 \tag{5.8}
\]

Thus action that is too small is safe, action that is large enough to enter
the denominator is also safe, and only an intermediate action window can
make the scalar cubic term large.  Optimizing over every \(x\ge Z\) hides
this distinction.

---

## 6. Placement of the frozen full-lattice chain

For the one-carrier sequence, \(p=N=B=1\) and \(R=R_0\) is fixed.  Up to
constants depending only on that declared geometry,

\[
 U\asymp\sigma^{7/3},\qquad
 V\asymp\sigma^{1/3},\qquad
 H\asymp\sigma^2.
 \tag{6.1}
\]

Equations (2.8) and (3.10) give

\[
 K_{\rm fr}\asymp\sigma^2,
 \qquad
 x_{\rm fr}\asymp\sigma^{4/3}\log\sigma.
 \tag{6.2}
\]

Therefore

\[
 \frac{x_{\rm fr}}H
 \asymp\sigma^{-2/3}\log\sigma\to0,
 \tag{6.3}
\]

\[
 T(x_{\rm fr})
 =\frac{Vx_{\rm fr}}{K_{\rm fr}+x_{\rm fr}}
 \asymp\sigma^{-1/3}\log\sigma\to0.
 \tag{6.4}
\]

The chain lies below the danger window.  Its actual action selects the
\(Vx\) branch, so the optimized residual (0.1) is not sharp on this family.
Separately,

\[
 \frac{\mathcal C_{\rm fr}}
 {\sigma a^2}
 \sim\frac{16}{\pi^2}\frac{\log\sigma}{\sigma}\to0.
 \tag{6.5}
\]

The last limit shows that the raw cubic estimate also loses a factor
\(\sigma/\log\sigma\) in the zero-diffusion reference.  It is not needed
for the scalar closure (6.4), but it supplies a second possible route for
the dissipative chain.

None of these statements disprove a different dissipative alternative.
Diagonal heat can change modal phases, reduce the norm, and modify the
absolute variation.  A semigroup decay estimate alone also does not control
\(\int|u u'|\): the latter is a time-variation functional, not just an
endpoint norm.

---

## 7. Dissipative diagnostic

The exact dissipative chain (1.1) was integrated by two independent finite
methods:

1. a Fourier pseudospectral Strang splitting, exact for the diagonal heat
   and the frozen convolution phase at each midpoint;
2. a finite-chain diagonal split with a Cayley step for the skew
   tridiagonal coupling.

Both methods use expanding Fourier cutoffs, step refinement, and an explicit
boundary-tail check.  Across the certified grid, the dissipative cubic mass
grows slowly and is compatible with a logarithm.  This is a numerical
diagnostic only.  It does not prove

\[
 \mathcal C_\times\lesssim a^2[1+\log(1+\sigma)]
 \tag{7.1}
\]

for the infinite dissipative chain.

The diagnostic is kept because it selects the next analytic object: a
uniform bounded-variation or flux estimate for the first two shell
coordinates.  More brute-force root counting would not address that gate.

---

## 8. Literature boundary

Classical triad analysis shows that energy transfer depends on Fourier
geometry and polarization, not only on coefficient size.  Waleffe's triad
classification is therefore consistent with the need to retain the signed
full convolution, but it does not imply the estimates above
([Physics of Fluids A 4 (1992)](https://doi.org/10.1063/1.858309)).

Bedrossian and Coti Zelati proved quantitative enhanced dissipation and
hypoelliptic regularization for passive scalars in shear flows
([Archive for Rational Mechanics and Analysis 224 (2017)](https://doi.org/10.1007/s00205-017-1099-y)).
Coti Zelati and Gallay later gave optimal enhanced-dissipation rates for
Morse shear profiles
([Journal of the London Mathematical Society 108 (2023)](https://doi.org/10.1112/jlms.12782)).
Those results concern semigroup decay.  They do not directly bound the
absolute cubic variation in (0.11), especially with the decaying coupling
amplitude used here.

The Bessel recurrence and fixed-order derivative asymptotics used in
Sections 2 and 4 are recorded in the
[NIST Digital Library of Mathematical Functions, Sections 10.6 and 10.17](https://dlmf.nist.gov/10.17).
The uniform large-order Airy control through the turning region used in
(3.4a) is recorded in
[DLMF Sections 10.19(iii) and 10.20(i)](https://dlmf.nist.gov/10.20.i).

Moffatt's exact-versus-truncated comparison remains relevant
([Journal of Fluid Mechanics 741 (2014)](https://doi.org/10.1017/jfm.2013.637)):
the Bessel wave in (0.4) occupies the whole lattice and cannot be replaced
by an isolated three-mode orbit.

I found no primary source in the bounded search that states the exact
full-lattice cubic asymptotic (0.12) for this project-specific row.  This is
not a priority claim.  The result is presented with its derivation and
finite audit.

---

## 9. Claim boundary

R0.72M proves:

1. the exact Bessel formula (0.6) on the complete frozen one-carrier lattice;
2. the exact Fourier-gradient moment (0.7);
3. the complete frozen critical-action asymptotic (0.10);
4. the sharp frozen true-cubic asymptotic (0.12);
5. the exact scalar danger-window theorem (5.3);
6. placement of the frozen chain in the action-poor safe branch;
7. two independently converged finite diagnostics for the dissipative
   chain.

It does not prove:

1. the logarithmic cubic upper bound (7.1) for the dissipative chain;
2. arbitrary-carrier or multiscale strong-coupling closure;
3. a lower bound for signed enstrophy flux in general three-dimensional
   flow;
4. a continuation criterion for arbitrary three-dimensional solutions;
5. finite-time singularity or global smoothness for general Navier--Stokes.

The Clay Millennium problem remains open.

---

## 10. Next exact gate

R0.72N should work with the dissipative chain (1.1) and prove or disprove a
uniform estimate of the form

\[
 \mathcal C_{\rm diss}(\sigma)
 \le Ca^2[1+\log(1+\sigma)]
 \tag{10.1}
\]

for the row-aligned one-carrier launch.  A weaker bound
\(o(\sigma a^2)\) would already validate a direct cubic route.  In parallel,
one can prove the action-poor inequality

\[
 \sigma^{1/3}x_{\rm diss}=o(K_{\rm diss}).
 \tag{10.2}
\]

Either result would close the dangerous cubic contribution for this launch,
but by different mechanisms.  Estimate (10.2) would place the action below
the scalar danger window; estimate (10.1) would bypass that window by
controlling the true cubic directly.  The first proof must control absolute
modal transfer, not merely \(L^2\) decay; the second must compare the full
negative-norm action with actual enstrophy contrast.

Only after that one-carrier theorem is settled should the estimate be
tested for common-band multi-carrier phases and then inserted into the
physical denominator of R0.72L.  The multiscale Schur interface remains
parallel work, not a substitute for (10.1).
