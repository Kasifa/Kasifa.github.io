# R0.74M — final-segment expulsion at the nearest inward collar

## Status

This note proves the question frozen in r074m_problem_freeze.md.  The
statement is familywise and local to the complete \(k=j-1\) annular row:

\[
 \sup_{\tau\in I_{R_j}}
 [\mathcal J_{j,j-1}(\tau)]_+
 \le C\Gamma_jL_jR_j^5
\tag{0.1}
\]

for all sufficiently large \(j\).  The proof is stronger than the signed
claim: it bounds a nonnegative one-packet Jensen majorant and uses inversion
plus a factor-four inequality for the two packets.  It neither assumes nor
claims cancellation.

The mechanism is a short **physical-time** segment under the exact common
forward law from R0.74L.  If the endpoint lies in the inward collar, a typical
Brownian path remains close to that endpoint for \(R_j^2/64\).  The heat
defect there produces a positive shear displacement of order
\(e^{-L_j^2/640}\), which is much larger than the collar radius
\(L_jR_j=L_je^{-L_j^2/320}\).  The horizontal derivative kernel is therefore
forced into a super-Gaussian tail.  The exceptional fast-return paths cost
\(e^{-L_j^2/16}\), enough to pay both the missing factor \(R_j\) and the
weight ratio \(\Gamma_{j-1}/\Gamma_j\).

This is not a theorem for arbitrary Navier--Stokes solutions.  It does not
yet synthesize every remaining shell row or prove the full R0.74K condition.
It gives no universal endpoint estimate and no global regularity result.
**NOT CLAY.**

The complete argument below has also passed the independent analytic
reconstruction recorded in r074m_nearest_inward_independent_audit.md.  That
audit is bound to the source bytes and is evidence for this familywise row
only; it does not enlarge the theorem's scope.

Throughout, suppress the index \(j\) and write

\[
 R=e^{-L^2/320},\qquad h=\frac{15}{16}LR,\qquad
 q=\frac{\sqrt{31}}{16}LR,\qquad
 G_1=\frac2{1323}.
\tag{0.2}
\]

The inherited calibration gives

\[
 -\frac12\le Q(t)\le q,\qquad
 \frac1{128R^2}\le B\le\frac1{64R^2},
 \qquad R^2\le t\le65R^2
\tag{0.3}
\]

for every sufficiently large \(j\).

---

## 1. Exact positive Jensen majorant

Define the positive chord of the complete \(j-1\) cutoff derivative by

\[
 D^-(t,x_2,x_3)
 =\int_{\mathbb R}
 [\theta(t,x_3)\partial_2\psi_{j-1}^R
 (x_1,x_2,x_3)]_+\,dx_1
\tag{1.1}
\]

and let \(\overline D^-\) be its two-variable periodization.  The padded
outer radius of this shell is

\[
 r_-:=2^jR+\frac R8
 =\left(\frac{32}{63}L+\frac18\right)R.
\tag{1.2}
\]

For all sufficiently large \(j\), \(r_-<1\), so at most one lift in each
periodic coordinate can meet the support.  The cutoff construction gives

\[
 0\le\overline D^-\le CL,
\tag{1.3}
\]

and

\[
 \overline D^-(t,\bar x_2,\bar x_3)\ne0
 \quad\Longrightarrow\quad
 |x_2|_{\rm lift}\le r_-,
 \qquad |x_3|_{\rm lift}\le r_-.
\tag{1.4}
\]

Indeed, \(|\partial_2\psi_{j-1}^R|\le C/R\), while the \(x_1\)-chord has
length at most \(2r_-=O(LR)\).

For the positive packet, Jensen applied to the exact normalized periodic
bridge representation, followed by exact unfolding in \(x_2,x_3\), gives

\[
\begin{aligned}
 \mathcal P^-(\tau)
 :={}&R^6\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb T}|\partial K_T(u)|^2\\
 &\times\mathbb E^{\rm fw}\!\left[
 K_T(X_t)\overline D^-
 (t,q_\omega(t)+u,h+X_t)
 \right]du\,dt,
\end{aligned}
\tag{1.5}
\]

where \(T=R^2+t\), \(X\) is the R0.74L forward periodic Brownian motion,
and

\[
 q_\omega(t)=Q(t)-\mathfrak S_t^\leftarrow[X],
\qquad
 \mathfrak S_t^\leftarrow[X]
 =B\int_0^t[\theta(s,h)-\theta(s,h+X_s)]\,ds.
\tag{1.6}
\]

More precisely,

\[
\begin{aligned}
 &\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}
 [\theta(t,x_3)\partial_2\psi_{j-1}^R(x)]_+
 |F^+(t,x_2,x_3)|^2\,dx\,dt\\
 &\hspace{4cm}\le \mathcal P^-(\tau).
\end{aligned}
\tag{1.7}
\]

No central winding has been selected in deriving (1.5).  The periodized
chord, the periodic heat kernels, and the common forward law contain every
copy.

---

## 2. A quantitative heat defect near the inward endpoint

Put

\[
 A(s,x)=1-\theta(s,x)\ge0,\qquad
 a=\frac{49}{14625},\qquad c_{\rm def}=\frac1{640}.
\tag{2.1}
\]

The inherited plateau estimate is

\[
 0\le A(s,h)\le4e^{-aL^2},
 \qquad 0\le s\le65R^2.
\tag{2.2}
\]

### Lemma 2.1 — lower caloric defect

If \(L\ge9216\), \(R\) is sufficiently small,

\[
 \left(61-\frac1{64}\right)R^2\le s\le65R^2,
 \qquad |x|_{\rm lift}\le\frac35LR,
\tag{2.3}
\]

then

\[
 \boxed{A(s,x)\ge e^{-L^2/640}.}
\tag{2.4}
\]

**Proof.**  The initial shear is

\[
 g(\xi)=\sigma\!\left(\frac{\sin\xi}{16R}\right),
\tag{2.5}
\]

where \(\sigma=-1\) when its argument is at most \(-1\).  For sufficiently
small \(R\), \(|\sin\xi|\ge|\xi|/2\) on
\([-64R,-32R]\).  Hence \(g=-1\) throughout that interval.  Positivity of
the periodic heat kernel, with only its central Gaussian copy retained for
a lower bound, yields

\[
\begin{aligned}
 A(s,x)
 &\ge2\int_{-64R}^{-32R}
 \frac1{\sqrt{4\pi s}}
 \exp\!\left(-\frac{|x-\xi|^2}{4s}\right)d\xi\\
 &\ge\frac{32}{\sqrt{65\pi}}
 \exp\!\left[
 -\frac{16}{3903}\left(\frac35L+64\right)^2
 \right].
\end{aligned}
\tag{2.6}
\]

The prefactor is larger than one because
\(65\pi<260<1024\).  The exponent comparison is exact:

\[
\begin{aligned}
 \frac{L^2}{640}
 -\frac{16}{3903}\left(\frac35L+64\right)^2
 ={}&\frac{361}{4163200}L^2
 -\frac{2048}{6505}L-\frac{65536}{3903}.
\end{aligned}
\tag{2.7}
\]

The right side is positive at \(L=9216\) and increasing thereafter.
Equations (2.6)--(2.7) prove (2.4). \(\square\)

The two decisive exponent gaps are

\[
 a-c_{\rm def}
 =\frac{3347}{1872000}>0,
\qquad
 \rho-c_{\rm def}
 =\frac1{640}>0.
\tag{2.8}
\]

Consequently, after increasing the base index,

\[
 \theta(s,h)-\theta(s,x)
 =A(s,x)-A(s,h)
 \ge\frac12e^{-L^2/640}
\tag{2.9}
\]

whenever (2.3) holds.

---

## 3. The final Brownian segment

Let \(\widetilde X\) be a continuous real lift of the forward Brownian path.
For each \(t\in I_{2R}\), set

\[
 \ell=\frac1{64},\qquad
 \mathcal H_t
 =\left\{
 \sup_{t-\ell R^2\le s\le t}
 |\widetilde X_s-\widetilde X_t|
 \le\frac1{16}LR
 \right\}.
\tag{3.1}
\]

The reversed increments over this fixed final segment have the law of a
real Brownian motion with generator \(\partial_x^2\).  The reflection
principle and the Gaussian tail bound therefore give

\[
 \boxed{\mathbb P(\mathcal H_t^c)\le4e^{-L^2/16}}
\tag{3.2}
\]

uniformly in \(t\in I_{2R}\).  Indeed,

\[
 \frac{(LR/16)^2}{4\ell R^2}=\frac{L^2}{16}.
\tag{3.3}
\]

Suppose now that

\[
 \overline D^-
 (t,q_\omega(t)+u,h+X_t)\ne0.
\tag{3.4}
\]

Use the unique vertical lift selected by (1.4).  On \(\mathcal H_t\),

\[
\begin{aligned}
 |h+X_s|_{\rm lift}
 &\le r_-+\frac1{16}LR\\
 &=\left(\frac{32}{63}+\frac1{16}\right)LR+\frac R8
 \le\frac35LR
\end{aligned}
\tag{3.5}
\]

for \(t-\ell R^2\le s\le t\).  The last inequality follows from

\[
 \frac35-\frac{32}{63}-\frac1{16}
 =\frac{149}{5040}>0
\tag{3.6}
\]

and already holds for \(L\ge63/8\).

### Lemma 3.1 — support-conditioned positive displacement

There is \(j_0\) such that, for \(j\ge j_0\), (3.4) and
\(\mathcal H_t\) imply

\[
 \boxed{
 \mathfrak S_t^\leftarrow[X]\ge\Sigma_L,
 \qquad
 \Sigma_L:=\frac1{32768}e^{-L^2/640}.}
\tag{3.7}
\]

**Proof.**  At every time,

\[
 \theta(s,h)-\theta(s,h+X_s)
 \ge-[1-\theta(s,h)]\ge-4e^{-aL^2}.
\tag{3.8}
\]

On the final segment, (2.9) and (3.5) improve this to
\(\frac12e^{-L^2/640}\).  Thus (0.3) gives

\[
\begin{aligned}
 \mathfrak S_t^\leftarrow[X]
 &\ge -4Bte^{-aL^2}
 +\frac12B\ell R^2e^{-L^2/640}\\
 &\ge-\frac{65}{16}e^{-aL^2}
 +\frac1{16384}e^{-L^2/640}.
\end{aligned}
\tag{3.9}
\]

Because \(a-1/640>0\), the first term in (3.9) is at most
\((1/32768)e^{-L^2/640}\) in magnitude for all sufficiently large \(j\).
This proves (3.7). \(\square\)

The expulsion scale is asymptotically much larger than the entire inward
collar:

\[
 \frac{\Sigma_L}{LR}
 =\frac1{32768L}e^{L^2/640}\longrightarrow\infty.
\tag{3.10}
\]

Increase \(j_0\) once more so that

\[
 q\le\frac14\Sigma_L,\qquad
 r_-\le\frac14\Sigma_L,\qquad
 2R\le\Sigma_L<1.
\tag{3.11}
\]

The inherited pathwise bounds

\[
 \mathfrak S_t^\leftarrow\le2Bt\le\frac{65}{32},
 \qquad Q(t)\ge-\frac12
\tag{3.12}
\]

and (3.7) imply, on the support and good event,

\[
 -\frac{81}{32}\le q_\omega(t)
 \le q-\Sigma_L\le-\frac34\Sigma_L.
\tag{3.13}
\]

If (3.4) holds, the horizontal support condition is

\[
 {\rm dist}_{\mathbb T}(q_\omega(t)+u,0)\le r_-.
\tag{3.14}
\]

Since \(81/32<\pi\), equation (3.13) places \(q_\omega\) in the central
interval \((-\pi,0)\).  The torus triangle inequality and (3.11)--(3.14)
therefore give, without selecting a horizontal winding,

\[
\begin{aligned}
 {\rm dist}_{\mathbb T}(u,0)
 &\ge {\rm dist}_{\mathbb T}(q_\omega,0)
 -{\rm dist}_{\mathbb T}(q_\omega+u,0)\\
 &\ge\frac34\Sigma_L-r_-
 \ge\frac12\Sigma_L.
\end{aligned}
\tag{3.15}
\]

This is the quantitative expulsion: the inward radial endpoint makes the
horizontal derivative kernel sample a distance exponentially larger than
its heat scale \(R\).

---

## 4. Good/bad path ledger

For \(62R^2\le T\le66R^2\), the periodic heat kernel satisfies

\[
 \|K_T\|_\infty\le\frac CR,\qquad
 \int_{\mathbb T}|\partial K_T(u)|^2du\le\frac C{R^3}.
\tag{4.1}
\]

The Gaussian series also gives, for \(R\le d\le1\),

\[
 \int_{{\rm dist}_{\mathbb T}(u,0)\ge d}
 |\partial K_T(u)|^2du
 \le\frac C{R^4}
 \exp\!\left(-\frac{d^2}{264R^2}\right).
\tag{4.2}
\]

The deliberately nonsharp \(R^{-4}\) prefactor follows directly from
\[
 |\partial K_T(u)|
 \le CT^{-1}
 \exp[-{\rm dist}_{\mathbb T}(u,0)^2/(8T)]
\]
and is sufficient because the exponential in (4.2) will be
super-Gaussian in \(L\).  Noncentral copies are included in the Gaussian
series and obey the same weaker bound for \(d\le1\).

### Bad final segments

Insert \(1_{\mathcal H_t^c}\) into (1.5), use (1.3), (3.2), and (4.1), and
enlarge the time interval to all of \(I_{2R}\).  Uniformly in
\(\tau\in I_R\),

\[
\begin{aligned}
 \mathcal P^-_{\rm bad}(\tau)
 &\le
 C R^6\cdot R^2\cdot R^{-1}\cdot L\cdot R^{-3}
 e^{-L^2/16}\\
 &\le C L R^4e^{-L^2/16}.
\end{aligned}
\tag{4.3}
\]

The exact exponent reserve is

\[
 \frac1{16}-\rho-G_1
 =\frac{24497}{423360}>0.
\tag{4.4}
\]

Therefore

\[
 \mathcal P^-_{\rm bad}(\tau)
 \le C e^{-G_1L^2}LR^5
\tag{4.5}
\]

for every sufficiently large \(j\).

### Good final segments

On \(\mathcal H_t\), the integrand vanishes unless (3.15) holds.  Apply
(1.3), (4.1), and (4.2) with \(d=\Sigma_L/2\):

\[
\begin{aligned}
 \mathcal P^-_{\rm good}(\tau)
 &\le
 C R^6\cdot R^2\cdot R^{-1}\cdot L\cdot R^{-4}
 \exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right)\\
 &\le
 C L R^3
 \exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right).
\end{aligned}
\tag{4.6}
\]

Here

\[
 \frac{\Sigma_L^2}{1056R^2}
 =\frac1{1056\cdot32768^2}
 \exp\!\left(\frac{L^2}{320}\right).
\tag{4.7}
\]

The right side of (4.7) grows faster than every multiple of \(L^2\).
Consequently,

\[
 \exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right)
 \le R^2e^{-G_1L^2}
\tag{4.8}
\]

for every sufficiently large \(j\).  Combining (4.6)--(4.8) gives

\[
 \mathcal P^-_{\rm good}(\tau)
 \le C e^{-G_1L^2}LR^5.
\tag{4.9}
\]

Equations (4.5) and (4.9) prove the one-packet bound

\[
 \boxed{
 \sup_{\tau\in I_R}\mathcal P^-(\tau)
 \le C e^{-G_1L^2}LR^5.}
\tag{4.10}
\]

---

## 5. Return to the original signed row

Let

\[
 w(t,x)=\eta_R(t)\theta(t,x_3)
 \partial_2\psi_{j-1}^R(x).
\tag{5.1}
\]

The function \(w\) is even under \(x\mapsto-x\), because both
\(\theta(t,x_3)\) and \(\partial_2\psi_{j-1}^R(x)\) are odd under that
inversion.  The packet relation

\[
 F^-(t,x_2,x_3)=-F^+(t,-x_2,-x_3)
\tag{5.2}
\]

therefore makes the two positive self-majorants equal.  Since

\[
 |F^++F^-|^2\le2(|F^+|^2+|F^-|^2),
\tag{5.3}
\]

we have, without any cancellation claim,

\[
\begin{aligned}
 [\mathcal J_{j,j-1}(\tau)]_+
 &\le4\Gamma_{j-1}\mathcal P^-(\tau)\\
 &\le C\Gamma_{j-1}e^{-G_1L^2}LR^5\\
 &=C\Gamma_jLR^5.
\end{aligned}
\tag{5.4}
\]

This proves (0.1).

### Theorem 5.1 — nearest-inward expulsion

For the exact R0.74F--H smooth periodic unforced family, there exist
\(C<\infty\) and \(j_0\) such that, for every \(j\ge j_0\),

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}
 [\mathcal J_{j,j-1}(\tau)]_+
 \le C\Gamma_jL_jR_j^5.}
\tag{5.5}
\]

The constant may depend on the frozen cutoff profile but not on \(j\).
Only \(0\le\eta_R\le1\) was used, so the estimate is uniform over the
inherited admissible time cutoffs.

---

## 6. What the theorem does and does not close

### Proved in this note

1. The full \(j-1\) cutoff derivative, not merely one radial face, obeys
   the target one-sided scale.
2. Every periodic winding is retained through exact periodization and the
   common forward law.
3. The positive displacement is proved only on the correlated collar
   support and a high-probability final-segment event; no false deterministic
   endpoint principle is used.
4. Fast-return paths have an explicit \(e^{-L^2/16}\) cost.
5. Both packet signs and their cross term are controlled without assuming
   cancellation.

### Still open after this note

1. the analytic synthesis of all remaining shell rows into the complete
   R0.74K signed condition;
2. the resulting matching upper bound for \(\mathfrak C_j\);
3. the stronger weighted kinetic-and-dissipation estimate for \(X_j\);
4. a universal square-root-log endpoint inequality;
5. any regularity or singularity theorem for arbitrary three-dimensional
   Navier--Stokes data; and
6. novelty or priority.

The finite certificate accompanying this note checks the rational geometry,
caloric exponent, Brownian rarity, and annular-weight comparisons.  It does
not replace the analytic support-conditioned argument above.
