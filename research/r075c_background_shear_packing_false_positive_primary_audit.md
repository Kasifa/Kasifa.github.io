# Independent primary audit of R0.75C

## 0. Frozen object and verdict

Candidate SHA-256:
`1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89`.

**Verdict: PASS. Mathematical blockers: 0. Release blockers: 0.**

The two formerly malformed tokens are repaired: C.19 now has
\(p_m^{\rm sh}\le\), and C.25 has the matched
\(\left|\left\{\cdots\right\}\right|\). All requested scales continue to
recompute correctly.

## 1. Exact shear, geometry, and packing

For \(u^{\rm sh}=(0,b,0)\), \(b=b(t,x_3)\), incompressibility is exact,
\((u\cdot\nabla)u=0\), and the heat equation for \(b\) gives smooth
unforced NSE with zero pressure. Heat flow preserves oddness, so an even
mollifier gives the zero Version-M path \(X_R=a_R=0\).

The outer collar has radius \(r=pLR\), thickness \(O(R)\), and volume
\(O(r^2R)=O(L^2R^3)\). Its fixed inward cap retains volume
\(\gtrsim L^2R^3\). On \(r/4\le x_3\le r/2\), distance to the saturation
transitions is \(\gtrsim LR\); the periodic heat tail is
\(O(e^{-cL^2})\) uniformly for \(61R^2\le t\le65R^2\). Hence
\(\theta_R\ge1/2\) and \(|b|\ge B/2\) on the cap.

Each enlarged block has duration \(\asymp R^3\). Since
\(B\asymp R^{-2}\),
\[
 p_m^{\rm sh}
 \asymp R^{-2}\omega B^3(L^2R^3)R^3
 \asymp\omega L^2R^{-2}.
\]
There are \(N\asymp R^{-1}\) comparable terms, so C.21 gives
\(N_{\rm eff}^{\rm sh}\asymp N\asymp R^{-1}\). The exact threshold excess
is
\[
 \frac9{40000}-\frac{4279}{79380000}
 =\frac{27163}{158760000}>0.
\]
This rejects only a claim that B.44 must hold universally. B.44 remains a
valid sufficient condition when it does hold.

## 2. BV heat estimate and shear dissipation

Every \(x_3\)-slice of the spherical collar has area
\(O(rR)=O(LR^2)\). The saturation datum has uniformly bounded BV norm.
Young's inequality and
\(\|K_t^{\rm per}\|_2^2\le Ct^{-1/2}\) give
\[
 \int_{61R^2}^{65R^2}
 \|\partial_3\theta_R(t)\|_2^2dt\le CR.
\]
Therefore
\[
 D_{k,R}^{{\rm out},b}
 \le C\frac\omega R(LR^2)B^2(R)
 =C\omega LR^2B^2.
\]

## 3. Version-M payment normalization

C.31 uses the legal time interval \(I_{2R}=(61R^2,65R^2)\), payment
radius \(2R\), and the conservative collar weight \(W_{2R}\ge\omega\).
Restricting the nonnegative exterior velocity row to the cap gives
\[
 P_R^M\ge
 cR^{-2}\omega(R^2)(L^2R^3)B^3
 =c\omega B^3L^2R^3.
\]
Consequently
\[
 (P_R^M)^{2/3}\gtrsim
 \omega^{2/3}B^2L^{4/3}R^2,
\qquad
 \frac{D_{k,R}^{{\rm out},b}}{(P_R^M)^{2/3}}
 \lesssim\omega^{1/3}L^{-1/3}\to0.
\]
All \(R,L,\omega,B\) powers pass.

The candidate now explicitly states after C.31 that the same bound holds
for every \(u=(F,b,0)\) with the frozen shear, since
\(|u|^3=(F^2+b^2)^{3/2}\ge|b|^3\). Thus Section 5's use of the paid shear
row for general passive \(F\) is mathematically and textually closed.

## 4. Claim boundary

The candidate correctly states that:

- total-cubic \(N_{\rm eff}\) is a false positive for the persistent paid
  background shear;
- the universal B.44 proposal is rejected, but the direct B.45 estimate is
  neither proved nor disproved;
- only \(D_{k,R}^{{\rm out},F}\) remains OPEN after the shear row is paid;
- no complete-clock counterexample, fixed-deletion theorem, suitable-weak
  extension, or regularity conclusion is obtained.

Final status: **PASS; remaining blockers: 0.** The revision changes no
exponent or conclusion. This audit makes no novelty or priority claim.
\(\mathbf{NOT\ CLAY}\).
