# R0.74Q relaxed dominance and payment — independent analytic audit

## Verdict and frozen binding

\[
 \boxed{\text{FINAL PASS within the audited scope}.}
\]

This is a read-only, formula-by-formula analytic audit of the stochastic
packet tails, the amplitude-weighted all-\(N\) sums, the periodic remainder,
the outer-lobe velocity-cubic payment, the normalized divergence, and the
signed-flux / square-function boundary in
`research/r074q_relaxed_multipacket_cubic_obstruction.md`.

The final source after the small audit-driven edits is frozen at

    ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d

The audited formulas are (Q.138)--(Q.180), restricted to the topics named
above.  The common-shear NSE construction, relaxed calibration, primary
bridge-survival proof, annular-placement proof, and inherited shell-balance
theorem are inputs, not independently re-proved in this audit.

## 1. Stochastic tail ledger

Conditioning on the vertical Brownian path in the common-shear equation
convolves the horizontal derivative kernel to time \(R^2+t\).  Therefore

\[
 R^3\|\partial K_{R^2+t}^{\rm per}\|_\infty
 \le CR,
\]

uniformly in the shear magnitude, packet index, and number of packets.  The
remaining vertical expectation is exactly the periodic heat kernel at time
\(R^2+t\).

| Formula | Result | Independent check |
|---|---|---|
| (Q.138) | **PASS** | The preceding conditioning gives \(|G_m^\pm|\le CRK_{R^2+t}^{\rm per}(x_3\mp h_m)\).  The constant is independent of \(m,N,B\). |
| (Q.139) | **PASS** | Since \(c_h-\alpha=1/240\) and every distinct dyadic pair has \(|L_m-L_\ell|\ge L\), the displayed inequality holds once \(L\ge240\). |
| (Q.140) | **PASS** | On the positive \(\ell\)-lobe, the direct central lift is at distance at least \(\alpha|L_m-L_\ell|R\); division by \(4(R^2+t)\le264R^2\) gives \(a_\times=\alpha^2/264\). |
| (Q.141) | **PASS** | The inversion partner is separated by at least \(\alpha(L_m+L_\ell)R\), so its central Gaussian has the stated stronger exponent. |
| (Q.142) | **PASS** | For the target packet's own inversion partner, \(2c_hL_\ell-1\ge2\alpha L_\ell\); hence the exponent is \(4a_\times L_\ell^2\). |
| (Q.143) | **PASS** | The inherited direct-packet lower bound is \(2c_0\), while (Q.142) tends to zero uniformly.  Thus the full paired target satisfies \(|G_\ell|\ge c_0\).  Inversion parity transfers the statement to the negative lobe. |

The small final edit makes the winding constant explicit.  Once
\(L_NR\le5/144\) and \(R\le1/32\),

\[
 2h_N+R
 \le2c_h\frac5{144}+\frac1{32}
 =\frac{37}{384}<\frac1{10}.
\]

Every nonzero vertical lift is consequently at distance at least \(6|n|\).
Together with \(4(R^2+t)\le264R^2\), this gives the summable winding factor

\[
 \sum_{n\ne0}e^{-36n^2/(264R^2)}
 \le C e^{-3/(22R^2)}.
\]

Horizontal periodic copies are already included in the uniform periodic
derivative-kernel norm used in (Q.138).

## 2. Amplitude-weighted all-\(N\) sums

Write

\[
 q=\frac4{3969},\qquad
 a_\times=\frac{49}{14850},\qquad
 \mathfrak a_\ell=A_*L_\ell^{-1/2}e^{qL_\ell^2}.
\]

The common factor \(A_*\) cancels from every ratio.

### 2.1 Outer packets on an inner target

| Formula | Result | Independent check |
|---|---|---|
| (Q.144) | **PASS** | For \(L_m=rL_\ell\), the amplitude ratio is \(r^{-1/2}e^{q(r^2-1)L_\ell^2}\); multiplying by the direct Gaussian tail gives the displayed identity. |
| (Q.145) | **PASS** | The net decay exponent is exactly \(a_\times(r-1)^2-q(r^2-1)\). |
| (Q.146) | **PASS** | At the adjacent value \(r=2\), \(a_\times-3q=67/242550>0\). |
| (Q.147) | **PASS** | Direct expansion gives \(\Phi(r)-(a_\times-3q)(r-1)^2=2q(r-1)(r-2)\ge0\). |
| (Q.148) | **PASS** | Since \(r=2^d\), the direct tails are dominated by a summable series beginning with \(e^{-\delta_\times L_\ell^2}\).  Negative partners have larger separation; winding terms are deferred to the common periodic ledger. |

Thus the potentially dangerous exponential growth of the adjacent outer
amplitude is strictly beaten by the vertical Gaussian tail.  The exact
remaining margin is \(67/242550\); no zero-margin step is hidden in the
summation.

### 2.2 Inner packets on an outer target

| Formula | Result | Independent check |
|---|---|---|
| (Q.149) | **PASS** | With \(L_m=2^{-d}L_\ell\), the polynomial ratio is \(2^{d/2}\), while amplitude decay and spatial separation add in the exponent. |
| (Q.150) | **PASS** | The two exponent contributions are exactly \(a_\times(1-2^{-d})^2\) and \(q(1-4^{-d})\). |
| (Q.151) | **PASS** | At \(d=1\), \(a_\times/4+3q/4=4601/2910600>0\). |
| (Q.152) | **PASS** | Setting \(s=2^{-d}\), the exact difference is \(a_\times(s-3s^2/4)+3qs^2/4\), which is at least \((5a_\times/8)s\) for \(s\le1/2\). |
| (Q.153) | **PASS** | Since \(sL_\ell=L_m\ge L\), successive terms have ratio at most \(\sqrt2e^{-(5a_\times/8)L_\ell L}<1/2\) for large \(L\).  The adjacent term therefore controls the full inner sum uniformly. |

### 2.3 Periodic remainder and full dominance

The final source now records the exact identity

\[
 \frac{\mathfrak a_m}{\mathfrak a_\ell}
 =\sqrt{\frac{L_\ell}{L_m}}
   e^{q(L_m^2-L_\ell^2)}.
\]

For \(m>\ell\), this is at most \(e^{qL_N^2}\).  For \(m<\ell\), the
function \(x^{-1/2}e^{qx^2}\) is increasing throughout the asymptotic
parameter range, so the ratio is at most one.

| Formula | Result | Independent check |
|---|---|---|
| (Q.154) | **PASS** | Summing at most \(N\) amplitude ratios against the winding tail gives \(CN\exp(qL_N^2-3/(22R^2))\). |
| (Q.155) | **PASS** | From \(L_N=(16/63)L^2\), \(qL_N^2=1024L^4/15752961\); from \(R=e^{-L^2/320}\), \(R^{-2}=e^{L^2/160}\). |
| (Q.156) | **PASS** | The negative double-exponential term \(-(3/22)e^{L^2/160}\) dominates \(O(L^4)+\log N\), so the remainder tends to zero. |
| (Q.157) | **PASS** | Combining the two central-tail sums, the common winding sum, and \(|G_\ell|\ge c_0\) yields a bound uniform in \(A_*,N,\ell,t,x\). |
| (Q.158) | **PASS** | Both rational central exponents and the exact winding majorant are copied correctly into the explicit \(\varepsilon_L\). |
| (Q.159) | **PASS** | Since \(\varepsilon_L\to0\), it is eventually at most \(1/2\), uniformly over all target lobes. |
| (Q.160) | **PASS** | The reverse triangle inequality gives \(|U_N|\ge\frac12|\mathfrak a_\ell G_\ell|\ge(c_0/2)\mathfrak a_\ell\). |

This proves the absolute no-cancellation statement on every target lobe,
not merely on the outermost one.

## 3. Outermost lobe and velocity-cubic payment

The relevant target-lobe volume and time length are

\[
 |\Omega_{N,+}(t)|=\frac1{16}L_NR^3,
 \qquad |J|=R^3.
\]

Moreover,

\[
 A_{k_N}(R)=A_{k_N-1}(2R),
 \qquad
 \gamma_{k_N-1}=\Gamma_N^{1/4}.
\]

| Formula | Result | Independent check |
|---|---|---|
| (Q.162) | **PASS** | The three side lengths are \(L_NR/8\), \(R/4\), and \(2R\), whose product is \(L_NR^3/16\). |
| (Q.165) | **PASS** | This is the nonnegative exterior velocity-cubic row at radius \(2R\); it may be retained alone for a payment lower bound. |
| (Q.166) | **PASS** | Doubling the radius lowers the dyadic annulus index by one exactly. |
| (Q.167) | **PASS** | The frozen weight satisfies \(\gamma_{k_N-1}=e^{-(c_\gamma/4)L_N^2}=\Gamma_N^{1/4}\). |
| (Q.168) | **PASS** | The spacetime normalization is \((2R)^{-2}R^3(L_NR^3/16)=L_NR^4/64\).  Inserting (Q.160) and \(\mathfrak a_N=A_*\Gamma_N^{-1/2}L_N^{-1/2}\) gives \(cA_*^3R^4\Gamma_N^{-5/4}L_N^{-1/2}\). |

No cancellation assumption remains in this lower bound: it is supplied by
the proved all-lobe dominance (Q.157)--(Q.160).

## 4. Normalized divergence

Recall \(T=A_*^2R^2\).  Taking the \(2/3\) power of (Q.168) cancels
\(A_*^2\) exactly after division by \(NT\).

| Formula | Result | Independent check |
|---|---|---|
| (Q.169) | **PASS** | The remaining factors are \(N^{-1}R^{2/3}L_N^{-1/3}\Gamma_N^{-5/6}\), and \(\Gamma_N^{-5/6}=e^{(5/6)c_\gamma L_N^2}\). |
| (Q.170) | **PASS** | Taking logarithms gives the first line.  The coarse bound \(L_N^2\ge L^4/16\), together with \(L_N\le L^2/2\), produces the second line in the correct lower-bound direction. |
| (Q.171) | **PASS** | \(5c_\gamma/96=5/47628>0\). |
| (Q.172) | **PASS** | The independent survival reserve remains valid because \(a_S-\rho=23/112640>0\). |
| (Q.173) | **PASS with explicit scope** | The rational identity \(5c_\gamma-a_S=603445/89413632>0\) is correct and is now explicitly labelled as the inherited adjacent-two-shell comparison, not the stronger present outermost exponent. |

The exact outermost leading coefficient is

\[
 \frac{5c_\gamma}{6}\left(\frac{16}{63}\right)^2
 =\frac{5120}{47258883}>0.
\]

Consequently

\[
 \frac{(P_R^{M,(N)})^{2/3}}{NT}\longrightarrow\infty
\]

for every positive common amplitude \(A_*(L)\); the normalized conclusion
does not depend on how that common amplitude varies with \(L\).

## 5. Square-function and signed-flux boundary

The lobe dominance also gives a legitimate endpoint-clock lower bound, but
only a lower bound.

| Formula | Result | Independent check and boundary |
|---|---|---|
| (Q.161) | **PASS** | On the target lobe, \(\eta_R=\Psi_{k_\ell}^R=1\), dissipation is nonnegative, and (Q.160) plus (Q.162) gives \(K_{k_\ell,R}(\tau)\gtrsim\Gamma_\ell\mathfrak a_\ell^2L_\ell R^2\). |
| (Q.163) | **PASS** | Equal-target normalization converts the preceding expression to \(c_KT\), uniformly in all target indices. |
| (Q.164) | **PASS as a lower bound only** | The \(N\) distinct target components give \(Y_{2,R}^{\rm sf}\ge c_K\sqrt N\,T\).  No matching upper bound follows because off-target clocks, cross terms, and earlier positive variation are uncontrolled. |
| (Q.174) | **PASS** | Summing the simultaneous target-clock lower bounds gives \(c_KNT\). |
| (Q.175) | **PASS as inherited identity** | The exact balance is \(K=Q+F\); terminal clock size alone is not signed flux. |
| (Q.176) | **PASS as inherited absolute ledger** | The available control is on \(\sum_k\operatorname{TV}Q_{k,R}\), with size \(C(P_R^{M,(N)})^{2/3}\). |
| (Q.177) | **PASS** | Nonnegative off-target clocks and the absolute source ledger yield only \(\sum_kF_{k,R}(\tau)\ge c_KNT-C(P_R^{M,(N)})^{2/3}\). |
| (Q.178) | **PASS as OPEN** | Since (Q.100) makes the error larger than \(NT\), no conclusion \(\mathfrak C_R^{M,(N)}\asymp NT\) can be drawn. |
| (Q.179) | **PASS as conditional only** | The displayed divergence relative to \(\mathfrak C_R^{M,(N)}\) follows only if a separate signed-flux analysis first proves (Q.178). |
| (Q.180) | **PASS** | The proved normalized payment divergence rules out the desired low-payment relation \((P_R^{M,(N)})^{2/3}=o(NT)\) for this explicit equal-target architecture. |

The correct final boundary is therefore

\[
 \boxed{Y_{2,R}^{\rm sf}\gtrsim\sqrt N\,T\quad\text{PROVED},}
\]

while

\[
 \boxed{Y_{2,R}^{\rm sf}\lesssim\sqrt N\,T\quad\text{OPEN},}
 \qquad
 \boxed{\mathfrak C_R^{M,(N)}\asymp NT\quad\text{OPEN}.}
\]

The audit proves neither a signed-flux lower bound of order \(NT\), an
all-shell square-function upper bound, the fixed-scale inequality (Q.1),
regularity, singularity, nor any Clay conclusion.  **NOT CLAY.**
