# R0.76H primary analytic audit

## Verdict and audited scope

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Scope: the full physical plateau mass and complete-clock signed flux for
  the one explicit shifted-binomial packet frozen in R0.76G.

This audit does not authorize publication.  It separates the analytic proof
from the finite ledger and from the later independent reread.

## 1. Geometry and scaling audit

At fixed \(z=x_2/(aR)\), the physical \((x_1,x_3)\)-area is
\(R^2\mathcal A_a(z)\), where H.11 subtracts the inner disk from the outer
disk.  Multiplying this by \(dx_2=aR\,dz\) and \(dt=R^2\,ds\) gives the
exact factor \(aR^5\) in H.12.

On \(J_{a,p}\), one has \(|z|\le1-\delta_0/a\), so both radial boundaries
are active and \(\mathcal A_a=4\pi a\delta_0\).  The strip has
\(z\)-width \(\delta_0/a\).  This yields
\(4\pi\delta_0a^2R^5P_L\), with no missing power of \(a\) or \(R\).

## 2. Uniform Gaussian-moment audit

The exact even moment is

\[
 \mathcal M_{m,s}(w)=
 \sum_{\ell=0}^m
 \frac{(2m)!}{(2m-2\ell)!\ell!}
 \left(\frac{s}{a^2}\right)^\ell w^{2m-2\ell}.
\]

Every coefficient is nonnegative.  The heat representation in H.14 is
therefore compared with this moment without cancellation.  On
\(7/5\le w\le8/5\), the sine and carrier errors are controlled by
\(m\varepsilon^2\to0\) and \(m\varepsilon\to0\).  After division by
\((7/5)^{2m}\), the omitted-tail logarithm is at most

\[
 2m\log(9/7)-49a^2/800+O(1)\longrightarrow-\infty,
\]

because \(2m\le a^2/512\) and \(\log(9/7)<2/7\).  Thus H.18 is a relative
moment comparison, not merely a lower bound relative to \(w^{2m}\).

Differentiation, Hölder, and Jensen give
\(|\partial_w\log\mathcal M_{m,s}(w)|\le2m/w\).  On the retained compact
range this is at most \(10m/7\), proving H.20.

## 3. Adjacent-strip payment audit

For a cap point and any point of \(J_{a,p}\), the corresponding \(w\)-values
differ by at most \(D/a\).  Combining H.18 and H.20 costs at most
\(2\exp(10Dm/(7a))\).  Cubing, integrating over the strip of width
\(\delta_0/a\), and solving for \(Q_L\) gives exactly the exponent
\(20Dm/(7a)\) and the factor \(a^{2/3}\) in H.27.

The positive cap is favourable because \(W_a<0\) there and the scaled drift
is \(-\beta\).  The negative cap can only lower the signed flux, so it is
legitimate to use the positive cap alone for the upper estimate in H.25.
Hölder is applied only in time on an interval of length four.

The physical prefactor satisfies

\[
 \frac{a^2R^3}{(a^2R^5)^{2/3}}
 =a^{2/3}R^{-1/3}.
\]

Together with H.27 this gives the \(a^{4/3}R^{-1/3}\) factor in H.6.

## 4. Terminal boxes and matching bounds

On both terminal boxes, \(s\ge s_0\) and \(w\ge w_0\).  Positivity of every
coefficient in the exact moment expansion gives
\(\mathcal M_{m,s}(w)\ge K_0\).  For the mass box, the outer factor \(a\),
the area \(4\pi a\delta_0\), and the two widths \(1/a\) and
\(\delta_0/a\) cancel to a constant.  This verifies the lower scale in
H.34.

On the full plateau, \(s\le4\) and
\(|w|\le w_*+\delta_0/a\).  Termwise comparison with \((s_0,w_0)\) costs
\(\exp(Cm/a)\), hence at most \(\exp(Ca)\).  The outer factor and maximal
cross-section account for the upper \(a^2\) in H.34.

On the positive-cap box, \(-W_a\asymp a\), while each box width is
\(1/a\).  The favourable contribution is therefore of order
\(\beta a^{-1}A^2\varepsilon^{4m}K_0^2\).  Since
\(K_0\ge w_0^{2m}\), the full adverse-to-favourable ratio is bounded by

\[
 Ca\left(\frac{2}{3w_0}\right)^{4m}=o(1).
\]

This proves eventual strict positivity of the complete signed flux.

## 5. Exponent and claim-boundary audit

H.34 and H.37 give the two-sided quotient in H.38.  All factors except
\(R^{-1/3}\) have logarithm \(o(L^2)\), so the raw rate is exactly
\(3/40000\).  Multiplication by \(R^{1/3}\omega^{1/3}\) cancels the
\(R\)-rate and leaves exactly \(-2/11907\).

The proof kills only the explicit shifted-binomial candidate.  It does not
replace the uniform \(\exp(Cq)\) estimate in R0.76E, cover arbitrary
packets, establish Version-M extraction, or address regularity or
singularity.  No simulation, formal scientific figure, novelty claim, or
priority claim is made.  **NOT CLAY.**
