# Primary audit of R0.74W remote adjacent-inward comparison

## 1. Audit identity and verdict

Audited candidate:

\[
\texttt{research/r074w\_remote\_adjacent\_inward\_comparison.md}.
\]

Frozen candidate SHA-256:

\[
\boxed{\texttt{d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10}}.
\]

Audit date: 2026-09-03.

Verdict:

\[
\boxed{\textbf{PASS}}
\]

Blocker count: \(0\).

The proof supports exactly the stated conclusion: the frozen matching
all-shell \(O(T_*)\) upper estimate fails because the packet-2 adjacent
inward coordinate diverges.  It does not establish failure of every
fixed-deletion estimate, a whole-shell upper or lower estimate, time
occupation, accumulated viscosity, regularity, or singularity.

## 2. Frozen dependency and integrity checks

The following dependency hashes were recomputed from the local files:

| dependency | recomputed SHA-256 |
|---|---|
| r074e | \(3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7\) |
| r074f | \(0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb\) |
| r074h | \(8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1\) |
| r074p | \(a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867\) |
| r074q common-shear | \(60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695\) |
| r074q relaxed | \(ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d\) |
| r074t | \(8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd\) |
| r074u | \(e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99\) |
| r074v | \(031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c\) |

The candidate contains 89 displayed equation tags, all unique.  The
sequence is W.1 through W.84 with the five intentional suffix tags
W.24a, W.24b, W.49b, W.52a, and W.68a.  Every internal W-reference has a
matching tag.  Display delimiters, inline delimiters, braces, and the
three aligned environments balance.  UTF-8 decoding succeeds; there are
no carriage returns or other non-printing control characters.  The
candidate also passes the whitespace-error check.

## 3. Geometry and free comparator

For the strip in W.10, the adjacent shell has outer radius \(pLR\) and
inner radius \(pLR/2\).  Its lower vertical coordinate satisfies

\[
pLR-R>\frac{pLR}{2}
\]

for the frozen range.  At the worst outer corner,

\[
(pLR)^2-
\left(\frac{pL}{16}R^2+\frac94R^2+(pLR-R/2)^2\right)
=\left(\frac{15}{16}pL-\frac52\right)R^2>0.
\]

Thus W.11 is valid, including the central-chart assertion
\(\Psi_{k_m-1}^R=1\).  The three side lengths give

\[
|\mathcal S_m|
=\frac12\sqrt{pL}\,R\cdot\frac14R\cdot\frac12R
=\frac1{16}\sqrt{pL}\,R^3,
\]

which verifies W.13 exactly.

For \(z/R\in(5/4,3/2)\) and \(a=1+\ell\in[65,66]\), the central
horizontal derivative is of size \(R^{-2}\), the central vertical heat
factor is of size

\[
R^{-1}\exp\!\left[-\frac{(dL+\delta)^2}{4a}\right],
\]

and the prefactor \(R^3\) cancels these powers.  The horizontal derivative
has a fixed sign on the strip.  Noncentral copies are
\(O(e^{-c/R^2})\).  This verifies W.15--W.18.

## 4. W.19--W.25: exact all-winding disintegration

The sign in W.19 agrees with the time-reversed shear formula: the
horizontal derivative is evaluated at \(z+\mathfrak S_t\).  Appending the
final \(R^2\) vertical heat interval makes the bridge duration

\[
T=t+R^2=(\ell+1)R^2,
\]

although the displacement integral itself ends at \(t\).

For the \(n\)-th lifted bridge, direct conditioning gives

\[
Y_s^{(n)}
=\left(1-\frac{s}{T}\right)y+\frac{s}{T}2\pi n
+\sqrt2\left(W_s-\frac{s}{T}W_T\right).
\]

Its mean is \(\mu_{n,s}\), its ordinary Gaussian variance is
\(2s(T-s)/T\), and its heat-time parameter is

\[
v_s=\frac{s(T-s)}{T}.
\]

Thus the terminology heat variance in W.24 is consistent with generator
\(\partial_y^2\).  The exact density identity

\[
k_s(\xi-y)k_{T-s}(2\pi n-\xi)
=k_T(2\pi n-y)k_{v_s}(\xi-\mu_{n,s})
\]

verifies W.24b and hence W.22.  Tonelli is applied only to the
nonnegative vertical winding weights; the signed horizontal derivative is
conditioned afterwards.  Both W.22 and its comparator W.23 retain the
full sum over \(n\in\mathbb Z\), so no central-copy replacement is hidden
in the relative comparison.

For \(|y|<1\),

\[
(2\pi n-y)^2-y^2\ge24n^2\qquad(n\ne0).
\]

Since \(4T\le264R^2\), the relative winding mass is bounded by
\(C e^{-1/(11R^2)}\).  Moreover,

\[
\frac1{11R^2}
\ge\frac1{11}\left(\frac{144}{5}\right)^2L^2
>75L^2.
\]

Together with the U-reserve this also controls the later extra
\(R^{-1}\) derivative factor.  W.25 is therefore valid with all windings
retained.

## 5. W.26--W.42: deficit, semigroup, and the \(L^{-2}\) layer

The deficit

\[
A(r,x)=e^{r\partial_x^2}(1-g_R)(x)
\]

is nonnegative.  The upper tail W.28 already includes all periodic defect
copies.  The lower bound W.29 uses only the interval
\([-2\delta_R,-\delta_R]\), where \(g_R=-1\), and therefore uses no
unassumed monotonicity of \(\sigma\).  Both bounds yield the remote
exponent \(q(\ell)=p^2/(4\ell)\).  At the reference height the exponent
is strictly larger because

\[
\frac{c_h^2}{260}-q_{64}
=\frac{125357}{52835328}>0.
\]

For the central bridge, convolution of the heat deficit with its
conditional density gives the exact semigroup identity

\[
\mathbb E_{0,y}^{\rm br}A(t-s,h_m+Y_s)
=A(t-s+v_s,h_m+\mu_s).
\]

Substitution \(s=\varsigma R^2\) gives exactly

\[
\frac{h_m+\mu_s}{R}
=\left(p+\frac{d\varsigma}{\ell+1}\right)L
-\left(1-\frac{\varsigma}{\ell+1}\right)\delta,
\qquad
\frac{t-s+v_s}{R^2}
=\ell-\frac{\varsigma^2}{\ell+1}.
\]

The exponent obeys

\[
f_\ell(\varsigma)-q(\ell)
\ge\frac{pd}{2\ell(\ell+1)}\varsigma,
\]

whose smallest coefficient on \([64,65]\) is

\[
\frac{433}{17027010}>0.
\]

Consequently the \(\varsigma\)-integral is localized to width
\(L^{-2}\); restoring \(ds=R^2d\varsigma\) yields precisely the
\(R^2L^{-2}\) factor in W.38.  Multiplication by
\(1/128\le BR^2\le1/96\), addition of the smaller reference deficit, and
the pathwise bound \(|\mathfrak S_t|\le65/48\) establish W.40--W.42.
The last estimate again averages every winding rather than deleting
noncentral paths.

## 6. W.43--W.53: positive displacement and sweeping

On the short interval \(s_*=R^2/L^2\), the bridge mean drift is
\(O(R/L)\), whereas the allowed tube has radius \(\epsilon LR\).  The
Gaussian reflection estimate therefore gives the \(e^{-c\epsilon^2L^4}\)
failure probability in W.45.

On the good event, W.29 supplies the positive remote-deficit contribution.
Outside the short interval, the exact identity

\[
\theta_R(r,h_m)-\theta_R(r,h_m+Y_s)
=A(r,h_m+Y_s)-A(r,h_m)
\]

and \(A\ge0\) leave only the negative reference-height contribution.
The former has size

\[
cL^{-2}\exp\!\left[-\frac{(p+\epsilon)^2}{4\ell}L^2-CL\right],
\]

while the latter is at most
\(Ce^{-c_h^2L^2/260+CL}\).  For \(\epsilon<d/4\), the exact worst-case
absorption margin is

\[
\frac{c_h^2}{260}-\frac{(p+d/4)^2}{256}
=\frac{11430203}{6011486208}>0.
\]

Thus W.49 proves \(\mathfrak S_t\ge\Delta_{\epsilon,\ell}(L)>0\) on
the good event.  W.49b, by contrast, is a probabilistic upper bound
obtained from the first moment.  Hence W.3 is correctly stated as
convergence in probability at logarithmic scale, not as a deterministic
two-sided pathwise estimate.

If the rate exceeds \(q(\ell_\infty)\), W.51 can be imposed with one
fixed \(\epsilon\), and \(\Delta/R\to\infty\).  The chart computation is
exact:

\[
0<z+\mathfrak S_t
\le\frac3{64}+\frac{65}{48}
=\frac{269}{192}<\frac32<\frac\pi2.
\]

Thus its distance from \(2\pi\mathbb Z\) is at least \(\Delta\), and W.53
gives a central contribution that is the sum of an \(e^{-cL^4}\) term
and a doubly exponential term.  W.25 adds a still negligible winding
remainder.  This validates the sweeping mechanism without replacing the
packet by an unjustified absolute \(o(1)\).

## 7. W.54--W.57: survival and sweeping quantifiers

The mean-value loss is exactly one factor \(R^{-1}\), as recorded in
W.56.  Therefore W.54 is the correct sufficient condition for relative
survival.  Because \(q(\ell)\ge q_{65}\) over the closed slab, the strict
limsup condition below \(q_{65}\) supplies one uniform gap and proves
W.55 uniformly in \(\ell\in[64,65]\).

For sweeping, \(q(\ell)\le q_{64}\).  A strict liminf rate above
\(q_{64}\) supplies one \(\epsilon>0\) that works throughout the slab,
so W.57 is also uniform.  In the sequential form W.50, the conclusion is
only asserted after \(\ell_j\to\ell_\infty\), which is the correct
quantifier order.  The equality and intervening band are not silently
claimed.

## 8. W.59--W.69: amplitudes, inversion, cross packets, and copies

The amplitude ratios in W.59 follow from \(L_2=2L_1\) and
\(\Gamma_2=\Gamma_1^4\).  The inherited vertical bound W.60 contains all
periodic windings.

The inversion-partner separation gives

\[
\frac{(c_h+p)^2-d^2}{4a}
=\frac{c_hp}{a}\ge\frac5{693}>0.
\]

After inserting the actual amplitude ratio, the two cross-packet margins
are

\[
\delta_{1\leftarrow2}
=\frac{100043}{29804544}>0,
\qquad
\delta_{2\leftarrow1}
=\frac{3667}{17611776}>0.
\]

The smaller geometric separation in W.66 is correctly

\[
2p-c_h=\frac{79}{1008},
\]

and is compensated by the packet-1 amplitude loss.  The negative partner
is farther away.

The periodic-copy reserve is explicit:

\[
c_*=\frac3{22}\left(\frac{144}{5}\right)^2-q_{64}
=\frac{123450676}{1091475}>0.
\]

It absorbs the largest amplitude ratio under \(L_2R\le5/144\).  Hence
W.69 is an amplitude-weighted relative noncancellation statement, which
is the form needed at the endpoint.

## 9. W.70--W.75: the U-reserve and the two packet regimes

The key reserve margin is

\[
4q_{65}-a_S
=\frac{3719797}{5811886080}>0.
\]

The factorization in W.71 therefore converts the frozen U-reserve into
W.54 for packet \(2\), uniformly for every admissible
\(\tau_2\in[64R^2,65R^2]\).  This proves W.72 with inversion and the
other packet already absorbed by W.69.

For the original scale \(\rho=1/320\),

\[
\rho-q_{64}
=\frac{2689}{1270080}>0,
\qquad
q_{65}-\frac{\rho}{4}
=\frac{13939}{66044160}>0.
\]

Thus packet \(1\) lies strictly in the sweeping regime while packet \(2\)
lies strictly in the survival regime.  W.75 states relative, not absolute,
limits and uses the correct strip-specific comparators.

## 10. W.76--W.82: smooth-time endpoint and weighted divergence

At the selected re-centring time \(\tau_m\), the completed clock has a
nonnegative endpoint row.  The proof uses that pointwise smooth-time row
only; it does not infer an interval occupation estimate or differentiate
an almost-everywhere representative.

The inward-shell weight is exactly

\[
\frac{\gamma_{k_m-1}}{\Gamma_m}
=e^{(3/4)c_\gamma L_m^2}.
\]

On the surviving strip,
\(|U|^2\) contributes \(\mathfrak a_m^2\), the vertical Gaussian
contributes
\(e^{-(dL+\delta)^2/(2a)}\), the endpoint prefactor is
\(\gamma_{k_m-1}/(2R)\), and the strip volume is
\(\frac1{16}\sqrt{pL_m}R^3\).  With
\(\mathfrak a_m^2=A_*^2/(\Gamma_mL_m)\) and
\(T_*=A_*^2R^2\), the remaining polynomial is exactly \(L_m^{-1/2}\).
This verifies every power in W.78.

The exponential coefficient is minimized at \(a=65\):

\[
\chi(65)
=\frac34c_\gamma-\frac{d^2}{130}
=\frac{12191}{132088320}>0.
\]

Therefore packet \(2\), whose survival is unconditional under the frozen
hypotheses, gives W.80:

\[
K_{k_2-1,R}(\tau_2)/T_*\longrightarrow\infty.
\]

For packet \(1\) on the original scale, the exact comparison margin

\[
2\delta_{1\leftarrow2}-\chi(66)
=\frac{221281}{33530112}>0
\]

supports W.82.  That conclusion is explicitly restricted to the displayed
strip; sweeping can move mass elsewhere in the same shell.

## 11. Exact rational ledger

Independent exact-arithmetic reduction gives:

| quantity | exact value |
|---|---:|
| \(p\) | \(32/63\) |
| \(d\) | \(433/1008\) |
| \(q_{64}\) | \(4/3969\) |
| \(q_{65}\) | \(256/257985\) |
| \(q_{64}-q_{65}\) | \(4/257985\) |
| W.32 margin | \(125357/52835328\) |
| minimum W.37 slope | \(433/17027010\) |
| W.49 absorption margin | \(11430203/6011486208\) |
| W.52a chart upper bound | \(269/192\) |
| inversion margin | \(5/693\) |
| \(2p-c_h\) | \(79/1008\) |
| \(\delta_{1\leftarrow2}\) | \(100043/29804544\) |
| \(\delta_{2\leftarrow1}\) | \(3667/17611776\) |
| \(c_*\) | \(123450676/1091475\) |
| \(4q_{65}-a_S\) | \(3719797/5811886080\) |
| \(\rho-q_{64}\) | \(2689/1270080\) |
| \(q_{65}-\rho/4\) | \(13939/66044160\) |
| \(\chi(65)\) | \(12191/132088320\) |
| \(\chi(66)\) | \(15263/134120448\) |
| W.81 margin | \(221281/33530112\) |

All claimed strict margins are positive.

## 12. Claim boundary

The proved obstruction is to the frozen matching all-shell
\(O(T_*)\) upper estimate, because the coordinate \(k_2-1=k_1\) diverges.
A fixed-deletion functional may delete precisely that coordinate.
Moreover, W.82 controls only one strip and does not imply a whole-shell
upper bound.  The critical transition law, whole-shell \(H^1\)
occupation, positive-variation upper bounds, time-duration transfer,
accumulated viscosity, fixed deletion, suitable weak-solution transfer,
and regularity remain open.

The candidate states these limitations explicitly.  Its conclusion is
therefore correctly classified as a frozen-family endpoint obstruction
and not as a Navier--Stokes regularity result:

\[
\boxed{\textbf{NOT CLAY}.}
\]
