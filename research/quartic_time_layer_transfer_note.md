# R0.63 — Time-layer factorization and the lifted Rudin--Shapiro transfer

## 1. Result and correction to the roadmap

R0.62 proved

\[
 |S_{4,m}|\leq C L^2M^{3/2}
\]

for every dyadic \(L,M\), while the desired uniform quartic estimate is

\[
 |S_{4,m}|\leq C L^2M.
\tag{1.1}
\]

The proposed next step was to retain the three-simplex time integral and use
the two-state Rudin--Shapiro recursion at each time layer.  This note carries
out the exact algebra and makes one necessary correction: the base
Rudin--Shapiro recursion has two states, but the cubic carrier product closes
on eight states.  Incorporating the target sign gives a natural sixteen-state
lift, and the relation \(A+B-C=Q\) also transports a carry.  A bare two-state
matrix is therefore not a closed object for (1.1).

Two exact reductions are obtained.

1. Before integration, each of the three time orderings is a coefficient of
   three independently heat-weighted Rudin--Shapiro polynomials.  The heat
   kernel is no longer an opaque four-index multiplier.
2. Every such cubic coefficient satisfies an exact eight-state dyadic
   recursion.  The target sign lifts it to sixteen states.  This identifies
   the precise non-autonomous transfer operator whose integrated norm must be
   bounded to prove (1.1).

These are all-index algebraic identities.  They do **not** prove (1.1).

## 2. Exact factorization before time integration

Put \(N=LM\), \(H=4N\), and write \(x_X=X/H\) for a positive carrier
\(X\in I_N=\{H,\ldots,H+N-1\}\).  For a fixed target carrier \(Q\), define

\[
 \mathcal C_Q(u,v,w)
 :=c_Q\!\sum_{\substack{A,B,C\in I_N\\A+B-C=Q}}
 c_Ac_Bc_C\,u_Av_Bw_C.
\tag{2.1}
\]

Equivalently, after shifting all carrier exponents by \(H\), (2.1) is one
coefficient of a product of two weighted polynomials and one reversed
weighted polynomial.

Let

\[
 \Delta_T=\{(\tau_0,\tau_1,\tau_2):\tau_j\geq0,
 \ \tau_0+\tau_1+\tau_2\leq T\},
 \qquad T=\frac{\log2}{2}.
\]

For each \(Q\), each \(\tau\in\Delta_T\), and each carrier, define the three
families of weights

\[
\begin{array}{lll}
 u_A^{(1)}=e^{-\tau_0x_A^2-\tau_1(x_A-x_Q)^2},
 &v_B^{(1)}=e^{-(\tau_0+\tau_1)x_B^2},
 &w_C^{(1)}=e^{-(\tau_0+\tau_1+2\tau_2)x_C^2},\\[2mm]
 u_A^{(2)}=e^{-\tau_0x_A^2-\tau_1(x_A-x_Q)^2},
 &v_B^{(2)}=e^{-(\tau_0+\tau_1+2\tau_2)x_B^2},
 &w_C^{(2)}=e^{-(\tau_0+\tau_1)x_C^2},\\[2mm]
 u_A^{(3)}=e^{-(\tau_0+\tau_1)x_A^2},
 &v_B^{(3)}=e^{-(\tau_0+\tau_1+2\tau_2)x_B^2},
 &w_C^{(3)}=e^{-\tau_0x_C^2-\tau_1(x_Q+x_C)^2}.
\end{array}
\tag{2.2}
\]

Then the complete heat-weighted quartic sum from R0.61 satisfies

\[
 \boxed{
 S_{4,m}=\int_{\Delta_T}\sum_{Q\in J_m}e^{-\tau_0x_Q^2}
 \sum_{j=1}^3\mathcal C_Q
 \bigl(u^{(j)},v^{(j)},w^{(j)}\bigr)\,d\tau.}
\tag{2.3}
\]

To verify (2.3), consider the three orders

\[
 (A,B,-C),\qquad(A,-C,B),\qquad(-C,A,B).
\]

For the first order, the exponent in the simplex integrand is

\[
 \tau_0(Q^2+A^2+B^2+C^2)
 +\tau_1((A-Q)^2+B^2+C^2)+2\tau_2C^2,
\]

divided by \(H^2\).  This is exactly the outside target factor and the
first row of (2.2).  The other two orders give the second and third rows.
Thus the factorization is termwise and does not invoke an estimate.

## 3. The exact cubic lift of the two-state recursion

Let \(P_n,Q_n\) be the Rudin--Shapiro pair of length \(M=2^n\), and write

\[
 R_{0,n}=P_n,\qquad R_{1,n}=Q_n.
\]

For an arbitrary weight vector \(w=(w_0,\ldots,w_{2M-1})\), let
\(w^{[0]}\) and \(w^{[1]}\) be its first and second halves.  The weighted
two-state identity is

\[
 R_{\sigma,n+1}[w](z)
 =P_n[w^{[0]}](z)+(-1)^\sigma z^M Q_n[w^{[1]}](z).
\tag{3.1}
\]

For \(\boldsymbol\sigma=(\sigma_1,\sigma_2,\sigma_3)\in\{0,1\}^3\), define

\[
 C_n^{\boldsymbol\sigma}
 (q;u,v,w)
 =[z^q]R_{\sigma_1,n}[u](z)
 R_{\sigma_2,n}[v](z)
 R_{\sigma_3,n}[w](z^{-1}).
\tag{3.2}
\]

Expanding (3.1) in the three factors gives the exact recursion

\[
 \boxed{
 C_{n+1}^{\boldsymbol\sigma}(q;u,v,w)
 =\sum_{\boldsymbol\varepsilon\in\{0,1\}^3}
 (-1)^{\boldsymbol\sigma\cdot\boldsymbol\varepsilon}
 C_n^{\boldsymbol\varepsilon}
 \left(q-M(\varepsilon_1+\varepsilon_2-\varepsilon_3);
 u^{[\varepsilon_1]},v^{[\varepsilon_2]},w^{[\varepsilon_3]}\right).}
\tag{3.3}
\]

The signs in (3.3) form the order-eight Walsh--Hadamard matrix.  The shift
\(\varepsilon_1+\varepsilon_2-\varepsilon_3\in\{-1,0,1,2\}\) is the
coefficient carry.  Multiplication by the target coefficient \(c_Q\) adds a
fourth \(P/Q\) bit, so the target-signed system naturally closes on sixteen
states, together with its carry positions.

Equation (3.3) is the precise meaning of a “two-state Rudin--Shapiro
recursion at each time layer.”  Two states generate the signs, but they do
not by themselves close the quartic quantity.

## 4. What the desired estimate has become

Substituting (3.3) into (2.3) shows that (1.1) will follow from an integrated
operator estimate of the form

\[
 \int_{\Delta_T}
 \|\mathfrak T_{n,\tau}\mathfrak T_{n-1,\tau}\cdots
 \mathfrak T_{1,\tau}V_{0,\tau}\|_{\mathrm{target}}\,d\tau
 \leq C\,2^n,
\tag{4.1}
\]

where \(\mathfrak T_{j,\tau}\) is the sixteen-state, carry-resolved transfer
obtained from (3.3) after restricting the Gaussian weights in (2.2).  It is
non-autonomous: the two half-blocks inherit different restrictions of the
quadratic exponential weights.

There are now three logically distinct possibilities.

1. A common weighted norm makes the integrated transfer in (4.1)
   contractive after division by \(2\).  This proves (1.1).
2. The norm is marginal and produces a logarithm.  Then the sharp result may
   be \(L^2M\log M\), still improving R0.62 but not giving a uniform quartic
   ratio.
3. A carry cycle has spectral radius above \(2\).  Then the proposed uniform
   quartic estimate is false for this packet, and the cycle supplies an
   explicit obstruction.

The next proof task is therefore a finite-dimensional norm or joint-spectral-
radius problem for the **integrated lifted transfer**, not for an ordinary
unweighted correlation matrix.

## 5. New finite stress test

The exact long-double path scanner was evaluated at the targets where the
ordinary unweighted outer cubic correlation is maximal.  These are hostile
targets for any argument that discards the heat kernel.

| \(M\) | target \(m\) | \(S_{4,m}/M\) | cancellation condition |
|---:|---:|---:|---:|
| 4096 | 292 | 0.0106986336319614 | 1804 |
| 8192 | 7643 | 0.0105185691214613 | 3395 |
| 16384 | 2388 | 0.00643209739230688 | 13164 |
| 32768 | 30583 | 0.00968791882738416 | 14735 |
| 65536 | 5291 | 0.0190323021553157 | 16445 |
| 131072 | 122331 | 0.0112788561436631 | 50625 |

All six values remain at scale \(10^{-2}\).  The largest run sums
28,977,859,974 ordered paths.  This is useful evidence that the heat-weighted
transfer behaves differently from the unweighted cubic correlation, but the
rapidly growing cancellation condition makes the boundary explicit: these
numbers do not certify (1.1) and are not substitutes for an operator norm.

## 6. Relation to prior work

Mazáč derives renormalisation equations for infinite-volume Rudin--Shapiro
correlation functions, including the two ordinary/signed correlation types
and a detailed four-point system.  Tarnu relates maximal finite
Rudin--Shapiro autocorrelation to a joint spectral radius.  Those works
support the renormalisation and matrix viewpoint, but neither theorem covers
the finite, boundary-sensitive, Gaussian-weighted simplex operator (2.3).
The present reduction therefore uses their structural lesson without
claiming that the required Navier--Stokes multiplier bound is already in the
literature.

- J. Mazáč, *Correlation functions of the Rudin--Shapiro sequence*,
  arXiv:2211.01090.
- D. Tarnu, *On maximal autocorrelations of Rudin--Shapiro sequences*,
  arXiv:2202.05897.

## 7. Claim boundary and next lemma

### Proved here for every index and every time layer

1. The exact factorization (2.3) of the heat-weighted quartic sum.
2. The exact eight-state weighted cubic recursion (3.3).
3. The natural target-signed closure requires sixteen \(P/Q\) states plus
   carry positions; a bare two-state norm is not closed.

### Finite evidence only

1. Six hostile targets through \(M=131072\) have bounded-looking
   \(S_{4,m}/M\).
2. Their positive sign and numerical scale are not all-index statements.

### Not proved

There is no proof yet of (1.1), no all-index positivity theorem, no complete
even-order Picard control, and no result for general three-dimensional data.
This note does not solve the Navier--Stokes Millennium problem.

The next lemma is concrete: build the carry-resolved sixteen-state operator
for a certified simplex quadrature envelope, then either exhibit a common
norm with scale factor at most \(2\), or return an explicit supercritical
cycle.  That calculation will decide whether the R0.62 square-root loss can
be removed on this packet.
