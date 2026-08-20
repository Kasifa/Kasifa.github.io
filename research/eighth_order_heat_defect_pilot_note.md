# R0.68B-2c pilot — Degree ten moves the defect bound into range

## 1. Status

The degree-eight heat jet from R0.68B-2b is numerically stable, but its first
same-shift defect bound is too large.  I therefore raised the centred spatial
jet from degree eight to degree ten and derived a new exact combinatorial
compression of the six-dimensional affine shifts.

The new calculation is promising but is **not yet a theorem**.  It proves an
exact carry-weight identity and an exact signature-reduction formula, then
uses binary64 dominant moments inside that formula.  A second audit now
covers all \(4368\) pure and mixed eleventh-derivative multiindices; outward
rounding is still missing.

## 2. Why the degree-eight remainder is not enough

For the degree-eight centred jet, same-shift aggregation over all
\(16^6\) free shifts gives the observable defect

\[
 b_{\mathrm{obs}}^{(8)}\approx 750.0499837058.
\]

After division by the dominant root
\(\mu\approx6438.806869529992\), the leading resolvent term is already about
\(0.11649\).  A global ninth-derivative bound would then have to be below
about \(1.28\times10^{-7}\).  The centre value of the largest pure ninth
derivative is only \(1.86\times10^{-9}\), but the available global
majorants are not yet tight enough to justify that threshold.

This is a failure of the current *bound*, not evidence that the heat
projection vanishes.

## 3. Four-bit signature compression

Write the six free carrier shifts as

\[
 e=(e_1,\ldots,e_6)\in\{0,\ldots,15\}^6.
\]

Once \(e\) is fixed, only the sixteen four-bit strings of the dependent
seventh carrier remain.  The carry recursion for the word \(0100\), read from
least to most significant bit, is explicit.  After admissibility and Fourier
signs are imposed, those sixteen branches aggregate into fourteen integers:

\[
 2\ \hbox{dependent least-significant bits}
 \ \times\ 7\ \hbox{input carries}.
\]

The distance from the centred branch point depends only on

\[
 h(e)=\sum_{j=1}^6|2e_j-15|,
 \qquad
 \left\|\frac{e+(1/2,\ldots,1/2)}{16}
 -(1/2,\ldots,1/2)\right\|_1=\frac{h(e)}{32}.
\]

For each of the \(64\) free least-significant-bit patterns, the remaining
\(8^6=262144\) upper-bit combinations collapse to roughly seven hundred
distinct pairs

\[
 \bigl(h(e),\ \hbox{fourteen-component signature}\bigr).
\]

The full \(16^6=16777216\) shift grid therefore collapses to \(44514\)
signature classes.  Every aggregated signature entry is \(0\), \(1\), or
\(-1\).  Six independent spot checks agree with entries of the original
1792-state sparse cycle.

## 4. Exact absolute carry weight

After the Fourier signs are discarded, the seven-carry cycle has the exact
positive right eigenvector

\[
\begin{aligned}
w={}&(64,\ 24137121,\ 904780185,\ 3769909270,\\
&\qquad 3049493910,\ 448102641,\ 4826809),
\end{aligned}
\]

with exact eigenvalue

\[
 16^6=16777216.
\]

Consequently a zero-degree-ten-jet remainder contracts over one four-bit
block by

\[
 \frac{16^6}{16^{11}}=\frac1{16^5}
 =\frac1{1048576}.
\]

## 5. Degree-ten pilot

The six-variable degree-ten lift has

\[
 {10+6\choose6}=8008
\]

channels per state.  Its complete 35-shuffle heat pairing is

\[
 B_{10,\mathrm{pilot}}
 =-1.4923824318477604\times10^{-8}.
\]

The difference from the degree-eight pilot is only
\(1.92\times10^{-18}\).

The signature-compressed degree-ten observable defect is

\[
 b_{\mathrm{obs}}^{(10)}
 \approx30.23448650536.
\]

The deliberately coarse no-cancellation weighted bound is

\[
 \|b^{(10)}\|_w
 \le 1.2824960745\times10^{-6}.
\]

Combining the statewise zeroth resolvent term with the exact weighted tail
gives the pilot upper value

\[
 Z_{\mathrm{obs}}^{(10)}
 \approx0.00469566611239.
\]

Thus a global eleventh-derivative bound below

\[
 \boxed{3.1782124\times10^{-6}}
\]

would protect the negative heat-jet signal.

## 6. All eleventh derivatives

For every shuffle and spatial coordinate I bounded the affine first
derivative of each quadratic heat rate on all \(2^6\) cube vertices.  The
pure second derivatives are constant.  The Hermite pairing formula then
reduces every pure eleventh derivative to positive time polynomials, whose
monomials are integrated exactly over the seven-simplex.

The six complete pure bounds are approximately

\[
\begin{array}{c|rrrrrr}
i&1&2&3&4&5&6\\ \hline
\|\partial_i^{11}K\|_\infty
&1.1605&1.6582&2.1436&2.5663&0.2813&0.0961
\end{array}
\times10^{-6}.
\]

The largest is

\[
 \boxed{2.5663266368\times10^{-6}},
\]

which is below the required \(3.1782124\times10^{-6}\) threshold.  Even the
sum of the per-shuffle pure maxima is only
\(2.8100085712\times10^{-6}\).

The seven simplex variables can in fact be eliminated before the spatial
scan.  If

\[
 F_j(z)=L_j\cdot z+\frac12z^\mathsf TQ_jz,
\]

then exact simplex integration gives

\[
 \sum_{k=0}^{11}\frac{T^{k+7}}{(k+7)!}
 h_k(F_1,\ldots,F_7).
\]

Expanding this six-variable polynomial through total degree eleven evaluates
all \(4368\) multiindices for every one of the \(35\) shuffles.  The global
maximum is still the pure fourth-coordinate derivative:

\[
 \boxed{
 \max_{|\alpha|=11}\|\partial^\alpha K\|_\infty
 =2.56632663673508\times10^{-6},
 \qquad
 \alpha=(0,0,0,11,0,0).}
\]

Representative mixed values are

\[
\begin{aligned}
(0,1,10,0,0,0)&:\ 1.7139603\times10^{-6},\\
(0,0,10,1,0,0)&:\ 1.7027259\times10^{-6},\\
(0,5,6,0,0,0)&:\ 1.1632264\times10^{-6}.
\end{aligned}
\]

Thus the mixed-derivative gate is closed at the binary64 majorant level.

## 7. The remaining finite gate

The remaining task is now narrower: replace the binary64 moment, defect and
all-derivative values by outward-rounded guarded enclosures.  Only after those
guards are independently checked can the degree-ten heat projection be
stated with a strict sign.

This calculation concerns one fixed eighth-order coefficient in a globally
smooth parallel-shear invariant class.  It does not control general
three-dimensional perturbations, singularity formation, or global
regularity, and it does not solve the Navier--Stokes Millennium problem.
