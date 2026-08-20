# R0.66 — A nonzero dominant spectral projection for the heat-weighted cycle

## 1. The asymptotic theorem

R0.65 certified twenty-four finite scales of the complete heat-weighted
quartic target.  The block ratios approached the dominant zero-time
eigenvalue, but a finite list could not decide whether the corresponding
spectral coefficient vanished.  This note resolves that question.

Let

\[
 M_r=16^r,\qquad q_r=2\frac{16^r-1}{15},\qquad m_r=q_r+1,
\tag{1.1}
\]

and retain the exact dimensionless quartic coefficient
\(S_r=S_{4,m_r}\) from R0.61, including all three time orders, the heat
kernel, and the complete time simplex.  Let \(\lambda\) be the unique root
in \((25,26)\) of

\[
 p(x)=x^4-25x^3-120x^2+3248x-8192.
\tag{1.2}
\]

The exact rational root enclosure used below is

\[
 25.1515893341015<\lambda<25.1515893341016.
\tag{1.3}
\]

There is a real constant \(C_*\) such that

\[
 \boxed{S_r=C_*\lambda^r+O(r16^r).}
\tag{1.4}
\]

The certified interval produced by the R0.66 audit is

\[
 -2.3044567988960\times10^{-5}
 <C_*<
 -2.2865275054844\times10^{-5}.
\tag{1.5}
\]

In particular,

\[
 \boxed{C_*< -2\times10^{-5}<0.}
\tag{1.6}
\]

Consequently,

\[
 \boxed{\frac{|S_r|}{M_r}\longrightarrow\infty.}
\tag{1.7}
\]

Thus the candidate uniform quartic estimate \(|S_{4,m}|\le CM\) fails on
the explicit packet family (1.1).  This is an asymptotic theorem, rather
than an inference from the first twenty-four values.

## 2. The stationary affine block operator

At the end of a four-bit block, normalize the two free convolution indices
by \(M_r\):

\[
 x=\frac a{M_r},\qquad y=\frac b{M_r}.
\tag{2.1}
\]

The forty-eight states are

\[
 (s,\boldsymbol\sigma,k)\in
 \{0,1\}\times\{0,1\}^3\times\{-1,0,1\}.
\tag{2.2}
\]

For each state, the signed atomic measure \(\mu_r^{s,\boldsymbol\sigma,k}\)
places the exact Rudin--Shapiro convolution weight at \((a/M_r,b/M_r)\).
The moment in R0.65 is

\[
 \int x^iy^j\,d\mu_r^{s,\boldsymbol\sigma,k}
 =M_r^{-(i+j)}
 X_{4r}^{s,\boldsymbol\sigma,k;i,j}(q_r).
\tag{2.3}
\]

One \(0100\) block is a fixed signed affine operator \(\mathcal P\).  Each
branch has the form

\[
 (x,y)\longmapsto
 \left(\frac{x+e}{16},\frac{y+f}{16}\right),
 \qquad 0\le e,f\le15,
\tag{2.4}
\]

with an integer state-transition weight.  Exact composition of the four
digit operators gives 12,288 nonzero affine branch records.  On the mass
vector, \(\mathcal P\) reduces to the R0.64 matrix \(W\).

Ordering moments by total degree makes the operator triangular.  Its
degree-\(d\) diagonal block is

\[
 16^{-d}W.
\tag{2.5}
\]

Equation (2.5) explains why the degree-zero eigenvalue survives the full
analytic observable: all positive-degree diagonal spectra are contracted.

## 3. Exact mass spectrum

The cycle has rank six.  Its restriction to its image has characteristic
polynomial

\[
 (x-16)^2p(x).
\tag{3.1}
\]

The complete characteristic polynomial is therefore

\[
 x^{42}(x-16)^2p(x).
\tag{3.2}
\]

The audit verifies

\[
 \operatorname{rank}W=\operatorname{rank}W^2=6,
\tag{3.3}
\]

so the zero eigenvalue is semisimple, and

\[
 \dim\ker(W-16I)=2,
\tag{3.4}
\]

so the double eigenvalue \(16\) is also semisimple.  The four roots of
\(p\) lie separately in

\[
 (-13,-12),\quad(3,4),\quad(8,9),\quad(25,26).
\tag{3.5}
\]

They are simple.  Hence \(\lambda\) is the unique dominant mass
eigenvalue, and the remaining mass contribution is \(O(16^r)\).

## 4. A rigorous spatial remainder bound

The missing step in a purely finite-moment argument is control of the
infinite-dimensional spatial part of \(\mathcal P\).  It is supplied by a
weighted Kantorovich norm.

Give a state the positive weight

\[
 w_{s,\boldsymbol\sigma,k}=
 \begin{cases}
 4,&k=-1,\\
 277,&k=0,\\
 169,&k=1.
 \end{cases}
\tag{4.1}
\]

Let \(A\) be the matrix obtained by taking absolute values of the
aggregated affine branch weights.  Direct integer arithmetic gives

\[
 Aw=256w.
\tag{4.2}
\]

For a vector \(\zeta\) of signed measures whose every component has zero
mass, define

\[
 \|\zeta\|_{KR,w}
 =\max_j\frac1{w_j}
 \sup_{\substack{f(0,0)=0\\\operatorname{Lip}_{\ell^1}(f)\le1}}
 \left|\int f\,d\zeta_j\right|.
\tag{4.3}
\]

Every affine branch contracts \(\ell^1\) distance by \(1/16\).  Combining
this with (4.2) gives the exact operator bound

\[
 \boxed{\|\mathcal P\zeta\|_{KR,w}\le16\|\zeta\|_{KR,w}.}
\tag{4.4}
\]

This is the decisive spectral gap: \(16<\lambda\).

Let \(Jv\) place the mass \(v_j\) of every state at the atom \((0,0)\),
and put

\[
 R=\mathcal PJ-JW.
\tag{4.5}
\]

Every component of \(Rv\) has zero mass.  Exact enumeration of all affine
branches gives

\[
 \|Rv\|_{KR,w}\le
 \frac{36161}{104}\|v\|_w,
 \qquad
 \|v\|_w=\max_j\frac{|v_j|}{w_j}.
\tag{4.6}
\]

Let \(a\) be the dominant mass projection of the initial state.  Since
\(\lambda>16\), the Neumann series

\[
 \eta=(\lambda-\mathcal P)^{-1}Ra
 =\sum_{n=0}^{\infty}\lambda^{-n-1}\mathcal P^nRa
\tag{4.7}
\]

converges in (4.3).  The vector distribution

\[
 \rho=Ja+\eta
\tag{4.8}
\]

satisfies

\[
 \mathcal P\rho=\lambda\rho.
\tag{4.9}
\]

Exact spectral-projector norm bounds for \(W\), together with (4.4)--(4.7),
then give

\[
 \mu_r=\lambda^r\rho+O_{(C^1)^*}(r16^r).
\tag{4.10}
\]

The factor \(r\) is retained because the elementary norm estimate permits
a resonance at the boundary value \(16\).  It has no effect on (1.7).

## 5. The complete heat observable

Write

\[
 \theta_r=\frac{q_r}{M_r}
 =\frac2{15}\left(1-16^{-r}\right),
 \qquad \theta_\infty=\frac2{15}.
\tag{5.1}
\]

After division by \(H=4M_r\), the three ordered heat rates are quadratic
functions of \((x,y,\theta_r)\).  Let \(F_\theta(x,y)\) be the sum of the
three complete simplex kernels.  Then the exact quartic coefficient is

\[
 S_r=\mu_r^{0,\boldsymbol0,0}(F_{\theta_r}).
\tag{5.2}
\]

On \([0,1]^2\) and \(0\le\theta\le2/15\), every rate obeys

\[
 0\le\alpha_j\le\frac{75}{8}.
\tag{5.3}
\]

The exact normalized rate formulas also give

\[
 \max_j\{|\partial_x\alpha_j|,|\partial_y\alpha_j|\}
 \le\frac{15}{8},
 \qquad
 \max_j|\partial_\theta\alpha_j|\le\frac32.
\tag{5.4}
\]

Thus \(F_\theta\) is uniformly \(C^1\), and

\[
 \|F_{\theta_r}-F_{\theta_\infty}\|_\infty=O(16^{-r}).
\tag{5.5}
\]

Although the total variation of the finite signed packet can grow like
\(256^r\), the combination of (5.5), \(M_r=16^r\), and normalization by
\(\lambda^r\) leaves an error of order \((16/\lambda)^r\).

Pairing (4.10) with (5.2) therefore yields (1.4), with

\[
 \boxed{C_*=\rho^{0,\boldsymbol0,0}(F_{2/15}).}
\tag{5.6}

## 6. Infinite-series control

For each path, the complete simplex series remains

\[
 K_T(\alpha_0,\alpha_1,\alpha_2,0)
 =\sum_{d=0}^{\infty}(-1)^d
 \frac{T^{d+3}}{(d+3)!}h_d(\alpha_0,\alpha_1,\alpha_2),
 \qquad T=\frac{\log2}{2}.
\tag{6.1}
\]

The publication audit truncates at \(D=24\), so moments only through total
degree \(48\) are required.  In addition to the uniform remainder from
R0.65, differentiating the homogeneous polynomial gives

\[
 |\partial_xh_d|,|\partial_yh_d|
 \le \binom{d+2}{2}d\frac{15}{8}
 \left(\frac{75}{8}\right)^{d-1}.
\tag{6.2}

The resulting \(C^1\) tail is a positive, geometrically decreasing rational
series after enclosing \(T=\operatorname{atanh}(1/3)\).  Hence the pairing
of the omitted infinite tail with \(\rho\) is bounded without assuming that
\(\rho\) is a positive measure.

## 7. Publication certificate

The formal run uses

\[
 r_0=100,\qquad D=24,\qquad \deg_{x,y}=48.
\tag{7.1}
\]

The degree-48 moment transport at \(M=16^{100}\) is exact integer
arithmetic.  The polynomial in \(T\), the root interval (1.3), all
projector bounds, and every error term use rational outward enclosures.

The final certificate records four disjoint contributions:

1. the normalized exact finite iterate;
2. convergence from cycle 100 to the dominant spectral projection;
3. the finite-target correction \(\theta_{100}-2/15\);
4. the complete simplex tail beyond order 24.

The normalized finite polynomial interval is

\[
 -2.29549215219066\times10^{-5}
 <\lambda^{-100}S_{100}^{(24)}<
 -2.29549215218974\times10^{-5}.
\tag{7.2}
\]

The three outward error bounds are

\[
 \begin{array}{c|c}
 \text{source}&\text{absolute bound}\\ \hline
 \text{finite spectral convergence}&2.560\times10^{-9}\\
 \text{finite target parameter}&2.529\times10^{-21}\\
 \text{infinite simplex tail projection}&8.709\times10^{-8}.
 \end{array}
\tag{7.3}
\]

Their sum is less than \(8.965\times10^{-8}\).  Adding it outward to
(7.2) gives the complete interval (1.5).

The exact endpoints, their hashes, resource log, and all decimal displays
are stored in `research/certificates/r066/`.  No random sampling or
floating-point root is used in the proof.

## 8. Consequence and boundary

### Proved

1. The stationary affine block representation (2.4) and triangular spectrum
   (2.5).
2. The exact weighted zero-mass contraction (4.4).
3. The asymptotic expansion (1.4).
4. The strict nonvanishing (1.5), and therefore the divergence (1.7).

### Not proved

The theorem concerns one explicit quartic Picard coefficient.  It does not
show that the full mild solution becomes singular: higher Picard orders may
interact with the quartic contribution, and the present argument does not
control those orders.  It does not treat arbitrary divergence-free data,
does not prove finite-time blowup, and does not prove global regularity.

The mathematical value is narrower and precise: a natural critical
\(O(M)\) quartic estimate is false even after the genuine heat kernel and
complete time ordering are retained.  Any successful perturbative route
through this packet must therefore exploit cancellations beyond the isolated
quartic coefficient.
