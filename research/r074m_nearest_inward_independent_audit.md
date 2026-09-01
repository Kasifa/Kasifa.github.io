# R0.74M independent audit — nearest-inward final-segment expulsion

## Audit result

I reconstructed the argument in
r074m_final_segment_expulsion.md from the frozen packet formula, rather
than checking only its displayed arithmetic. I also tried to break the
argument at the points where conditioning, periodic unfolding, Brownian
reversal, and powers of \(R\) interact.

The result is

\[
 \boxed{\text{INDEPENDENT ANALYTIC AUDIT: PASS}.}
\]

For the exact R0.74F--H family and all sufficiently large \(j\), the audited
argument proves

\[
 \sup_{\tau\in I_{R_j}}
 [\mathcal J_{j,j-1}(\tau)]_+
 \le C\Gamma_jL_jR_j^5.
\tag{A.1}
\]

This audit found one incorrect time range for \(Q\) during reconstruction.
It was corrected before this final binding; the error and its effect are
recorded in Section 3 below. I found no remaining gap in the theorem after
that correction and the winding-free torus-triangle formulation now used
in the proof.

## 1. Audited-source binding

The SHA-256 values below bind this audit to the files actually read.

| source | SHA-256 | role |
|---|---|---|
| research/r074m_problem_freeze.md | 5a6a95aae1fd00f7b7ddc79a5387b3ad3c7c675ca7eb1c92f51604f42fa4747c | exact row, target, packet reduction, exclusions |
| research/r074m_final_segment_expulsion.md | 0077326ca97cfe40a0a43019caf0118504cf9ed770979595d63bf9d2ec281ef0 | theorem and analytic proof audited here; rebound after the status-only edit below |
| scripts/r074m_nearest_inward_certificate.py | a888185d84252280ace748c75c07c08de808af3b1af54f74f9683299bbc414d5 | author-side finite rational certificate |
| research/r074m_nearest_inward_certificate.json | 5aed76e6c2aac58c1507784dd014a132560967a1bb89e69080fa0e170f65462f | recorded finite-certificate output |
| research/r074f_two_packet_survival.md | 0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb | exact packet and bridge representation |
| research/r074g_complete_payment_counterexample.md | 95548d6225389b9cfd1822a8abaf89e495e7f15ca5ff30c6b92aaa8ac5f2d6be | calibration and plateau bounds |
| research/r074l_forward_bridge_bv_reduction.md | d920e3845b38f75f187a78193b874e18d4551adf7dc03db59d5e785451654bf8 | common-forward-law identity |

The worktree base at the time of the audit was
a575c4e4affdf8d2cf363fd6eb1040f06098c1ac. The R0.74M files were not
yet committed at that base, so the content hashes above, rather than the
base commit alone, are the operative binding.

### Status-only proof rebind

The first final audit was bound to proof SHA-256
5832c742000f1879874de7170403b2d1a78f44c2c511b6f65a1dd25c5c84deca.
After that PASS, the proof source received two declared state edits:

1. its Status section gained a paragraph recording that the independent
   analytic reconstruction had passed; and
2. Section 6 removed the now-completed independent-reconstruction item
   from the open list and renumbered the remaining items.

I checked this fail-closed by applying the exact inverse of those two text
edits to the current proof bytes. The reconstructed byte stream has
SHA-256
5832c742000f1879874de7170403b2d1a78f44c2c511b6f65a1dd25c5c84deca,
exactly the previous audited hash. Therefore the change from the former
binding to the current proof SHA-256
0077326ca97cfe40a0a43019caf0118504cf9ed770979595d63bf9d2ec281ef0
consists only of those two state edits. No formula, estimate, constant,
logical implication, theorem scope, or NOT CLAY boundary changed. The
analytic PASS below is consequently rebound to the current proof bytes.

## 2. Independent reconstruction ledger

### A1. Original signed row and the factor-four reduction

Put

\[
 w(t,x)=\eta_R(t)\theta(t,x_3)
 \partial_2\psi_{j-1}^R(x).
\]

For a nonnegative function \(f\),

\[
 \left[\int wf\right]_+\le\int[w]_+f.
\]

The radial cutoff is even under full inversion, so its \(x_2\)-derivative
is odd. The shear is odd. Hence \(w(t,-x)=w(t,x)\). The exact packet
symmetry is

\[
 F^-(t,x_2,x_3)=-F^+(t,-x_2,-x_3).
\]

Using

\[
 |F^++F^-|^2\le2(|F^+|^2+|F^-|^2)
\]

and changing \(x\mapsto-x\) in the negative-packet self term gives

\[
 [\mathcal J_{j,j-1}(\tau)]_+
 \le4\Gamma_{j-1}\mathcal I^+(\tau),
\tag{A.2}
\]

where \(\mathcal I^+\) is the positive-packet integral with \([w]_+\).
The factor is exactly four. No packet cancellation is assumed.

### A2. Jensen, exact periodization, and common-forward law

First integrate in \(x_1\). This gives exactly

\[
 D^-(t,x_2,x_3)
 =\int_{\mathbb R}
 [\theta(t,x_3)\partial_2\psi_{j-1}^R
 (x_1,x_2,x_3)]_+\,dx_1.
\tag{A.3}
\]

In the reference variables \(z=x_2-Q(t)\), \(y=x_3-h\), the normalized
periodic bridge representation is

\[
 F^+(t,Q(t)+z,h+y)
 =R^3K_T(y)\mathbb E_{t,y}^{\rm br}
 \partial K_T(z+\mathfrak S_t^y).
\]

Jensen therefore gives the correctly normalized square bound

\[
 |F^+|^2\le
 R^6K_T(y)^2\mathbb E_{t,y}^{\rm br}
 |\partial K_T(z+\mathfrak S_t^y)|^2.
\tag{A.4}
\]

Partitioning both real variables into \(2\pi\)-cells turns \(D^-\) into
its full two-variable periodization \(\overline D^-\). The heat kernels
and bridge laws are periodic, so this is an equality before Jensen and
does not select a central copy. For each path, the torus translation

\[
 u=z+\mathfrak S_t^y
\]

preserves Haar measure and changes the horizontal chord argument to

\[
 Q(t)-\mathfrak S_t^y+u.
\]

The integrated bridge-reversal identity then maps

\[
 \mathfrak S_t^y
 \longmapsto
 \mathfrak S_t^\leftarrow[X]
 =B\int_0^t
 [\theta(s,h)-\theta(s,h+X_s)]\,ds,
\]

and changes \(K_T(y)^2d y\,d\mathbb P^{\rm br}_{t,y}\) into the common
forward expectation with the single endpoint weight \(K_T(X_t)\). Thus

\[
\begin{aligned}
 \mathcal I^+(\tau)
 \le{}&R^6\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb T}|\partial K_T(u)|^2\\
 &\quad\times\mathbb E^{\rm fw}
 [K_T(X_t)\overline D^-
 (t,q_\omega(t)+u,h+X_t)]\,du\,dt,
\end{aligned}
\tag{A.5}
\]

with

\[
 q_\omega(t)=Q(t)-\mathfrak S_t^\leftarrow[X].
\]

The sign, one remaining \(K_T\), \(R^6\), and every winding in (A.5) are
all correct.

### A3. Chord size and endpoint support

For the complete \(k=j-1\) derivative, the padded outer radius is

\[
 r_-=\left(\frac{32}{63}L+\frac18\right)R.
\]

Since \(|\partial_2\psi_{j-1}^R|\le C/R\) and an \(x_1\)-chord has length
at most \(2r_-=O(LR)\),

\[
 0\le\overline D^-\le CL.
\tag{A.6}
\]

For large \(j\), \(r_-<1\), so a supported torus point has a unique small
vertical lift and

\[
 |h+X_t|_{\rm lift}\le r_-.
\tag{A.7}
\]

No estimate here discards the other periodic field copies: uniqueness is
only a consequence of the compact Euclidean collar having radius below
one.

### A4. Lower caloric defect

Write \(A(s,x)=1-\theta(s,x)\). On
\(\xi\in[-64R,-32R]\), the initial shear equals \(-1\). Retaining only
the central positive Gaussian copy gives, whenever
\(|x|_{\rm lift}\le3LR/5\) and
\((61-1/64)R^2\le s\le65R^2\),

\[
 A(s,x)\ge
 \frac{32}{\sqrt{65\pi}}
 \exp\!\left[-\frac{16}{3903}
 \left(\frac35L+64\right)^2\right].
\tag{A.8}
\]

The prefactor exceeds one. The exact exponent margin is

\[
\begin{aligned}
 \frac{L^2}{640}
 -\frac{16}{3903}\left(\frac35L+64\right)^2
 ={}&\frac{361}{4163200}L^2\\
 &-\frac{2048}{6505}L-\frac{65536}{3903}.
\end{aligned}
\tag{A.9}
\]

At \(L=9216\), (A.9) equals

\[
 \frac{433872896}{97575}>0,
\]

and its derivative is

\[
 \frac{41744}{32525}>0.
\]

It follows that \(A(s,x)\ge e^{-L^2/640}\). The inherited plateau error
at \(h\) has exponent \(a=49/14625\), and

\[
 a-\frac1{640}=\frac{3347}{1872000}>0.
\tag{A.10}
\]

Thus, after increasing the index,

\[
 \theta(s,h)-\theta(s,x)
 \ge\frac12e^{-L^2/640}.
\tag{A.11}
\]

### A5. Final Brownian segment and support-conditioned lag

For a real lift of the common forward Brownian path, let

\[
 \mathcal H_t=
 \left\{\sup_{t-R^2/64\le s\le t}
 |\widetilde X_s-\widetilde X_t|\le\frac1{16}LR\right\}.
\]

The reversed increments have the law of Brownian motion with generator
\(\partial_x^2\). Reflection and the Gaussian tail bound give

\[
 \mathbb P(\mathcal H_t^c)
 \le4\exp\!\left[
 -\frac{(LR/16)^2}{4(R^2/64)}\right]
 =4e^{-L^2/16}.
\tag{A.12}
\]

On chord support and \(\mathcal H_t\), use the endpoint lift from (A.7)
throughout the final segment. Then

\[
 |h+X_s|_{\rm lift}
 \le\left(\frac{32}{63}+\frac1{16}\right)LR+\frac R8
 \le\frac35LR,
\]

with exact positive margin

\[
 \frac35-\frac{32}{63}-\frac1{16}
 =\frac{149}{5040}.
\tag{A.13}
\]

Before the final segment, the integrand in
\(\mathfrak S_t^\leftarrow\) is at least
\(-4e^{-aL^2}\). On the final segment, (A.11) applies. Splitting the
integral at \(t-R^2/64\) gives

\[
\begin{aligned}
 \mathfrak S_t^\leftarrow
 &\ge-4Bte^{-aL^2}
 +\frac12B\frac{R^2}{64}e^{-L^2/640}\\
 &\ge-\frac{65}{16}e^{-aL^2}
 +\frac1{16384}e^{-L^2/640}\\
 &\ge\Sigma_L,
\end{aligned}
\tag{A.14}
\]

where

\[
 \Sigma_L=\frac1{32768}e^{-L^2/640}.
\]

This is explicitly a support-conditioned statement. It is used only
where \(\overline D^-\ne0\) and on \(\mathcal H_t\); it is not asserted
for every Brownian path with the same endpoint.

Finally,

\[
 \frac{\Sigma_L}{LR}
 =\frac{1}{32768L}e^{L^2/640}\longrightarrow\infty.
\tag{A.15}
\]

### A6. Torus geometry and absence of a hidden winding

For the relevant times,

\[
 \mathfrak S_t^\leftarrow\le2Bt\le\frac{65}{32},
 \qquad -\frac12\le Q(t)\le q.
\]

On good supported paths,

\[
 -\frac{81}{32}\le q_\omega(t)
 \le q-\Sigma_L\le-\frac34\Sigma_L.
\tag{A.16}
\]

Since \(81/32<\pi\), this places \(q_\omega\) in the central interval
\((-\pi,0)\), hence
\(\operatorname{dist}_{\mathbb T}(q_\omega,0)=|q_\omega|\). The chord
support itself says

\[
 \operatorname{dist}_{\mathbb T}(q_\omega+u,0)\le r_-.
\]

The torus triangle inequality therefore yields, without choosing a
horizontal winding,

\[
\begin{aligned}
 \operatorname{dist}_{\mathbb T}(u,0)
 &\ge\operatorname{dist}_{\mathbb T}(q_\omega,0)
 -\operatorname{dist}_{\mathbb T}(q_\omega+u,0)\\
 &\ge\frac34\Sigma_L-r_-
 \ge\frac12\Sigma_L.
\end{aligned}
\tag{A.17}
\]

The proof also imposes \(2R\le\Sigma_L<1\), so
\(d=\Sigma_L/2\) lies in the declared heat-tail range \(R\le d\le1\).

### A7. Bad-path power and exponent ledger

On \(\mathcal H_t^c\), use the pointwise chord bound, the endpoint heat
kernel bound, and the full derivative-kernel \(L^2\) bound. Before the
exceptional probability is inserted, the exact scale is

\[
 R^6\cdot R^2\cdot R^{-1}\cdot L\cdot R^{-3}
 =LR^4.
\tag{A.18}
\]

The target has one additional \(R\) and the annular weight gap. The
Brownian exponent has the exact reserve

\[
 \frac1{16}-\frac1{320}-\frac2{1323}
 =\frac{24497}{423360}>0.
\tag{A.19}
\]

Consequently,

\[
 \mathcal P^-_{\rm bad}
 \le C e^{-G_1L^2}LR^5.
\tag{A.20}
\]

No independence between \(X_t\), chord support, and
\(\mathcal H_t^c\) is needed: the proof takes the pointwise suprema of
\(K_T\) and \(\overline D^-\) before using
\(\mathbb P(\mathcal H_t^c)\).

### A8. Good-path power and super-Gaussian ledger

On good supported paths, (A.17) restricts the horizontal integral to
\(\operatorname{dist}_{\mathbb T}(u,0)\ge\Sigma_L/2\). The raw scale is

\[
 R^6\cdot R^2\cdot R^{-1}\cdot L\cdot R^{-4}
 =LR^3.
\tag{A.21}
\]

The periodic Gaussian series, including noncentral copies, supplies

\[
 \exp\!\left[-\frac{\Sigma_L^2}{1056R^2}\right],
\]

and

\[
 \frac{\Sigma_L^2}{1056R^2}
 =\frac{1}{1056\cdot32768^2}
 \exp\!\left(\frac{L^2}{320}\right).
\tag{A.22}
\]

This grows faster than every multiple of \(L^2\), so eventually

\[
 \exp\!\left[-\frac{\Sigma_L^2}{1056R^2}\right]
 \le R^2e^{-G_1L^2}.
\]

Hence

\[
 \mathcal P^-_{\rm good}
 \le C e^{-G_1L^2}LR^5.
\tag{A.23}
\]

Combining (A.20), (A.23), and the factor-four reduction (A.2), and using

\[
 \Gamma_{j-1}e^{-G_1L^2}=\Gamma_j,
\]

proves (A.1).

## 3. Error found during the audit and its correction

The first audited draft stated

\[
 -\frac12\le Q(t)\le q
 \qquad(0\le t\le65R^2).
\]

This was false on \(0\le t<R^2\). By the exact entrance calibration,

\[
 Q(R^2)=-\frac12,
\]

and \(Q(t)<-1/2\) before that entrance time. The source proof now states
the correct interval

\[
 -\frac12\le Q(t)\le q
 \qquad(R^2\le t\le65R^2).
\tag{A.24}
\]

Every use of the lower bound in the R0.74M proof occurs for
\(t\in I_{2R}=(61R^2,65R^2)\). Therefore the original overstatement did
not invalidate the final-segment argument, and (A.24) repairs the statement
without changing the theorem.

The proof's no-wrap paragraph was also rebound in the current source to
the torus triangle inequality shown in (A.17). This is not an additional
assumption; it makes the all-winding conclusion direct and avoids a
representative-dependent argument.

## 4. Independent arithmetic check

I separately recomputed the decisive rational comparisons using Ruby
Rational, independently of the Python certificate. The following values
were recovered exactly:

\[
\begin{array}{c|c}
\text{item}&\text{independent value}\\ \hline
\text{geometry gap}&149/5040\\
\text{heat margin at }L=9216&433872896/97575\\
\text{heat-margin derivative at }L=9216&41744/32525\\
\text{plateau exponent gap}&3347/1872000\\
\text{expulsion exponent gap}&1/640\\
\text{bad-event reserve}&24497/423360\\
\text{raw bad-path power}&LR^4\\
\text{raw good-path power}&LR^3
\end{array}
\]

All comparisons were positive where required. This finite recomputation
supports, but does not replace, the analytic reconstruction in Section 2.

## 5. Final boundary

This audit passes exactly the complete nearest-inward \(k=j-1\) row for
the frozen smooth periodic family. It also verifies that both packet
signs, their cross term, the full cutoff derivative, the fixed time cutoff,
and all periodic windings are covered.

It does **not** prove any of the following:

1. the remaining shell rows or their synthesis;
2. the complete R0.74K signed condition;
3. a matching bound for every \(\mathfrak C_j\) or \(X_j\);
4. a universal square-root-log endpoint inequality;
5. a theorem for arbitrary three-dimensional Navier--Stokes solutions;
6. global regularity or finite-time singularity; or
7. novelty or priority.

The final status is therefore:

\[
 \boxed{\text{R0.74M NEAREST-INWARD ROW: PASS; NOT CLAY.}}
\]
