# R0.71P gap matrix -- positive-entry spatial batching versus temporal packing

**Date:** 2026-08-26

| Claim or gate | Status | Evidence | Remaining boundary |
|---|---|---|---|
| Fixed multiplier, cutoff, and partition | closed scope | R0.71P setup | no moving cutoff or refresh theorem |
| Half-open observation window \(K=[a,b)\) | **PASS** | left zero boundary included; right boundary excluded | adjacent windows require the same convention |
| Finite-order right entry atom \(A_+\) | inherited exact theorem | R0.71O finite-order face theorem | flat and accumulating zeros require a different analysis |
| Positive-entry target uses only \(A_+\) | closed scope | equation (0.2) | total-Jordan \(A_++A_-\) is stronger and deferred |
| Segmented positive variation adds every internal entry \(A_+\) | **PASS** | zero-padded component identity (2.1) | an initial trace is separately declared when \(d(a)>0\) |
| Subtracting interior variation and initial trace recovers the entry target | **PASS** | corrected identity (2.2), constant-branch exact check | none under the stated traces and half-open convention |
| Ordinary hard BV atom is \((A_+-A_-)^+\) | **PASS** | direct internal-jump calculation | ordinary BV can miss an even-order touch |
| Segmented-minus-hard positive atom is \(\min(A_+,A_-)\) | **PASS** | scalar identity (2.4) | none under finite traces |
| Entry layer-cake formula | **PASS** | Tonelli formula (2.5), exact rational audit | represents an existing mass; gives no NSE estimate by itself |
| Positive-entry target is the positive Jordan part of the signed aggregate | **REJECTED** | even touch: separate soft positive and negative limits survive while the signed limit vanishes | use componentwise relaxed positive parts, not aggregate Jordan notation |
| Componentwise relaxed positive-entry measure admits internal signed cancellation | **REJECTED** | every weight and \(A_+\) is nonnegative | a signed precursor may help only through a new domination estimate |
| Countable truncation passage for positive atoms | exact extended-measure statement | fixed counting measure plus Tonelli/monotone convergence | the limit and the counting measure may fail to be locally finite |
| Cellwise trace projection \(A_+\le \lVert\mathbf1_{\operatorname{supp}\chi_Q}F_j\rVert_2^2/Y\) | **PASS, sharp** | Cauchy--Schwarz, exact Gram audit | no universal cellwise coefficient below one |
| Leading direction remains in cutoff support | exact | fixed support is a closed \(L^2\) subspace containing every observable value | moving cutoffs add new terms |
| Same-shell cell sum loses no cell-count factor | **PASS** | bounded support overlap \(M_\chi\) | requires the declared fixed overlap constant |
| All-shell time-slice sum reaches the \(\dot H^{-1}\) Lamb budget | **PASS** | Littlewood--Paley square-function upper bound | depends on the declared annular frame constant \(C_T\) |
| Physical estimate \(\lVert L\rVert_{\dot H^{-1}}^2/Y\lesssim\lVert u\rVert_2Y^{1/2}\) | **PASS** | Sobolev duality, Hölder, interpolation | grows with enstrophy and is not a continuation bound |
| Simultaneous entry batch estimate | **PASS** | Theorem 4.1 | same-time only; it does not sharpen the full factor \(M_\chi C_T\) |
| Distinct entry-time counting measure \(\mathfrak n_\Lambda\) | exact definition | equation (5.1) | no current uniform packing bound |
| Full target equals batch mass integrated against \(\mathfrak n_\Lambda\) | **PASS** | nonnegative regrouping identity (5.3) | cannot replace \(d\mathfrak n\) by \(dt\) without new input |
| Fixed finite truncation with \(\overline K\Subset I_{\mathrm{strong}}\) is finite | **PASS** | Hilbert-valued time analyticity and isolated zeros | no uniform count in truncation or near a singular endpoint |
| Identically zero observable | closed convention | no positive-denominator component, hence no entry | does not create a count |
| Qualitative analyticity controls zero number uniformly | **REJECTED** | analytic functions can have arbitrarily many isolated zeros across a family | needs quantitative radius, growth, and anchor data |
| Jensen disk count | conditional exact formula | equation (7.2) for distinct vector zeros | analytic radius, complex norm, lower anchor, and covering are unproved at energy level |
| Masuda unique continuation rules out filtered-cell zeros | **REJECTED** | theorem concerns the complete velocity on a spatial open set | operator-kernel zero is a different event |
| Spatial Gevrey decay pays temporal entries | **REJECTED as stated** | Fourier decay is a per-time amplitude estimate | repeated temporal sampling remains |
| Denominator mass pays entry count | **REJECTED abstractly** | \(C_N=N^{-1}\sin(Nt)e\): mass \(\pi/N^2\), entries \(N\) | family is not a coupled NSE path |
| Ordinary first-time square budgets pay entry count | **REJECTED abstractly** | same path has bounded \(C_t\) and \(F\) square masses | no genuine NSE multiple-face counterexample |
| Soft positive variation recovers hard entry count | **PASS** | soft/hard ratio \((1+N^{-2})^{-1}\to1\) | limit order must resolve the faces |
| Genuine smooth NSE initial entry | **PASS** | exact Fourier and independent \(32^3\) FFT | one-sided initial jet only |
| NSE initial entry saturates cellwise projection | **PASS** | \(A_+=\lVert F\rVert_2^2/Y=1/4\) | does not saturate a temporal-packing or full-frame constant |
| Exact producer | **PASS** | symbolic Gram, overlap, boundary, layer-cake, oscillatory, and Fourier checks | computational checks support but do not replace proofs |
| Independent checker | **PASS** | 64 random overlap trials, half-open root detection, quadrature, FFT | floating point, not interval arithmetic |
| Uniform all-shell/all-cell positive-entry sum | open | no payment of \(d\mathfrak n_\Lambda\) | R0.71Q quantitative analytic-window gate |
| Infinite-frame and Leray passage | open | no uniform tightness of face-counting measures | requires new estimates |
| Continuation, singularity, or global regularity | not claimed | outside finite theorem | Millennium problem remains open |

## Finite route verdict

R0.71P removes the spatial cell multiplicity at each common entry time.  It
does not remove the multiplicity of distinct entry times.  The remaining
quantity is explicit:

\[
 \int_K
 M_\chi C_T\frac{\lVert L(t)\rVert_{\dot H^{-1}}^2}{Y(t)}
 \,d\mathfrak n_\Lambda(t).
\]

R0.71Q must test whether a quantitative complex-time radius/growth/anchor
ledger yields a parabolic-window packing estimate without assuming a known
continuation norm, inverse denominator, target BV, or transversality bound.
