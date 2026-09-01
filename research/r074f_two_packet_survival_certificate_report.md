# R0.74F two-packet survival finite compatibility certificate report

## Result

The exact-arithmetic certificate returns **PASS: 30/30**.

This is a finite compatibility result, not a packet-survival theorem.  It
checks rational identities, strict exponent margins, the first admissible
discrete scale, and a conditional terminal-lobe annulus inclusion.  All
Brownian, heat-kernel, Feynman--Kac, and PDE statements remain outside the
certificate.

## Frozen inputs

The R0.74E constants are

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta^2=\frac{31}{256},
\]

\[
 c_R=\frac1{320},\qquad
 \kappa=16,\qquad
 c_\gamma=\frac8{3969}.
\]

The new finite bookkeeping constants are

\[
 L_{\rm surv}=9216,\qquad
 s=\frac{255}{256},\qquad
 b_{\rm tr}=2\kappa+1=33.
\]

Here \(2\kappa R=32R\) is the reserved transition width and the final
\(R\) is the terminal vertical-error allowance.  The certificate does not
prove that an analytic transition or stochastic path obeys these bounds.

## Buffer gate

The earlier contrast threshold is retained with exact room

\[
 9216-7680=1536.
\]

At the new threshold,

\[
 \frac{c_hL_{\rm surv}}{256}
 =\frac{135}{4}
 >33,
 \qquad \text{margin}=\frac34.
\]

The exact continuous threshold for this inequality is

\[
 L\ge \frac{256\cdot33}{c_h}=\frac{45056}{5},
\]

so the transparent integer choice \(9216\) has margin \(1024/5\) above the
minimum.  The resulting conservative separation coefficient is

\[
 sc_h=\frac{3825}{4096}
 >\frac{14}{15}=\alpha,
 \qquad \text{margin}=\frac{31}{61440}.
\]

## Exponent gate

The denominator change has the exact positive margin

\[
 \frac{s^2}{260}-\frac1{264}
 =\frac{3181}{112459776}>0.
\]

Define the two conditional exponents

\[
 c_{\rm surv}
 =\frac{(sc_h)^2}{260}
 =\frac{2926125}{872415232},
 \qquad
 c_{\rm leak}
 =\frac{c_h^2}{264}
 =\frac{75}{22528}.
\]

Their strict hierarchy is certified by

\[
 c_{\rm surv}-c_{\rm leak}
 =\frac{238575}{9596567552}>0,
\]

\[
 c_{\rm surv}-c_R
 =\frac{999137}{4362076160}>0,
 \qquad
 c_{\rm leak}-c_R
 =\frac{23}{112640}>0.
\]

Thus both proposed exponential decays have finite arithmetic room after an
inverse-\(R\) prefactor, **conditional on separately proving the analytic
estimates that produce those exponents**.  The inherited ordering also has

\[
 c_R-c_\gamma=\frac{1409}{1270080}>0.
\]

## Discrete scale gate

For \(L_j=\lambda2^j\),

\[
 L_{12}=8064<9216<16128=L_{13}.
\]

The exact margins are \(1152\) and \(6912\), respectively.  Therefore the
condition \(L_j\ge L_{\rm surv}\) means exactly \(j\ge13\) on this sequence.
The value \(9216\) is a threshold and is not itself attained by \(L_j\).

## Conditional terminal-lobe annulus gate

For either lobe sign, assume on a chosen Euclidean lift that

\[
 x=(x_1,\ \pm q_j+\varepsilon_2,\ \pm h_j+\varepsilon_3),
 \qquad q_j^2+h_j^2=r_j^2,
 \qquad r_j=L_jR_j,
\]

and assume the deterministic bounds

\[
 |x_1|\le\frac{r_j}{16},\qquad
 |\varepsilon_2|\le\frac{65}{32}R_j,
 \qquad |\varepsilon_3|\le R_j.
\]

The horizontal allowance \(65/32=2+1/32\) is interpreted as a two-packet
unit plus a separately proved \(Q\)-error bound.  The combined transverse
\(\ell^1\) allowance is \(97/32\).

At \(L=L_{\rm surv}\), the normalized inner-radius margin is

\[
 1-\frac1\lambda-\frac{97}{32L_{\rm surv}}
 =\frac{1015129}{2064384}>0.
\]

For the outer radius, exact componentwise estimation gives

\[
 \frac{|x|^2}{r_j^2}
 \le
 1+\frac1{256}
 +\frac{97}{16L_j}
 +\frac{5249}{1024L_j^2}.
\]

At the threshold, the right side equals

\[
 \frac{87370044545}{86973087744},
\]

and its exact margin below \((2/\lambda)^2\) is

\[
 \left(\frac2\lambda\right)^2
 -\frac{87370044545}{86973087744}
 =\frac{116914328399}{4261681299456}>0.
\]

The positive \(L^{-1}\) and \(L^{-2}\) error terms in the upper bound
decrease as \(L\) increases.  Consequently, under the displayed
deterministic hypotheses,
both terminal lobes lie strictly in

\[
 2^jR_j<|x|<2^{j+1}R_j
 \qquad(L_j\ge9216).
\]

This is a conditional geometry implication.  The certificate does not
establish any of its deterministic hypotheses or the validity of the chosen
torus chart.

## Scope boundary

The certificate proves only exact rational identities, strict finite
compatibility, and conditional annular inclusion under the displayed input
bounds.  In particular, it does **not** prove:

1. the transition-width or \(Q\)-error hypotheses;
2. torus-chart validity, periodic-copy bounds, or heat-kernel estimates;
3. Brownian confinement or a Brownian-bridge estimate;
4. Feynman--Kac time ordering, packet survival, or sign preservation;
5. pressure, leakage, exterior-payment, or endpoint rows;
6. Navier--Stokes regularity, singularity, or the Clay problem.

## Reproduction

From the repository root, run

```bash
python3 scripts/r074f_two_packet_survival_certificate.py
```

The standard output must be byte-for-byte identical to
`research/r074f_two_packet_survival_certificate.json`.
