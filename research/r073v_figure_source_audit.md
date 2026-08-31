# R0.73V independent figure-source and claim-boundary audit

**Audit date:** 2026-09-01

**Figure ID:** fig-r073v-signed-third-order-interface

**Scope:** independent read-only verification of the immutable figure source,
certificate pins, two-path common core, 158 source-data rows, Panel A--D
mathematics, small-\(s\) orders, selected-coefficient scope, and public claim
boundary

**Ordinary translation path:** LOCAL_DIRECT_NO_DGX

**Verdict:** PASS. The current figure package is byte-identical to its final
package-seal commit, all 147 reconstructed checks pass, the generic formal
figure validator reports no error or warning, and the displayed Panel A--D
formulas agree with the sealed two-path exact certificate. No mathematical
source or claim-boundary blocker remains.

## 1. Immutable source chain

The figure has two consecutive immutable commits:

| Layer | Commit | Independent check |
|---|---|---|
| figure source and 11 raw artifacts | 680fde5a24834b8e1c877f651eb20b119c671f49 | resolves and contains the 10 declared source files plus 11 raw artifacts |
| final figure-package seal | b413586aa7a7389f8943acb2469eb28cdbbf31f3 | resolves; its parent is exactly the figure-source commit and it adds four metadata files |

The scoped working-tree package has no byte difference from
b413586aa7a7389f8943acb2469eb28cdbbf31f3. The manifest records

    figureSourceCommit=680fde5a24834b8e1c877f651eb20b119c671f49
    figureSourceCommitAssigned=TRUE
    sealState=formal-figure-source-seal
    requiresParentFigureSourceCommitFinalReseal=FALSE

All 24 entries in the package SHA256SUMS file verify. The four metadata files
are correctly outside the earlier 21-file figure-source commit and inside the
later package-seal commit.

## 2. Certificate pins and two independent paths

The figure contract pins the exact R0.73V certificate as follows:

    certificateSourceCommit=7c445c522a241bdc8b867b6fce0f0fed9b82e97d
    certificatePackageCommit=b34d91ea96c257b943f11d134e8024138e5f3cb0
    primarySha256=e024ea767ff146ee2e53455522e6c0ab2c59608e74038673cc8a6fca0271b0c4
    independentSha256=0c40808136b532b536a871184a9937b7a29c436e04ef0235e607964b0ebec1d0
    commonCoreSha256=24519dec8a70d0ebe1e0ba3ea1899569ca3dbfabc1b11691990387c628731fa2
    completeTableDigest=a7494d44f45b1249a513ac4d44476b7ce5af622b0d59928f4e4631d9715c22f7

The primary producer uses sparse exponent maps. The independent producer uses
dense trimmed polynomial tuples and does not import the primary producer.
Read-only reruns returned

    primaryCertificate=PASS
    primaryChecks=66/66
    independentRecompute=PASS
    primaryAndIndependentTableDigestEqual=TRUE
    certificateStatus=sealed
    twoPathCommonCoreByteIdentical=TRUE

The figure validator refuses to reconstruct source-data.csv before the two
complete commonCore objects agree. This is stronger than checking only the
few coefficients printed in the figure.

## 3. Read-only reproduction

I ran the figure validator in verify-only mode with the exact dependency
versions recorded by the package. I also ran the generic figure-package
validator, both certificate producers in check-only mode, the certificate
sealer in check-only mode, and the package checksum verification.

The outputs were:

    figureValidation=PASS
    figureValidationChecks=147/147
    genericFigurePackageErrors=0
    genericFigurePackageWarnings=0
    certificateChecks=66/66
    independentCertificate=PASS
    certificateFinalSeal=TRUE
    packageChecksums=24/24

The pinned dependency versions are Matplotlib 3.10.6, NumPy 2.5.2, Pillow
12.3.0, pypdf 6.10.0, and pypdfium2 5.13.0. Verification mode did not rewrite
the figure package.

## 4. Source-data inventory

source-data.csv has one header plus 158 data rows. Its declared partition sums
exactly:

| Source-data group | Rows |
|---|---:|
| metadata and definitions | 5 |
| Panel A compressed interface | 16 |
| Panel B four-site entries | 16 |
| Panel C six-site entries | 12 |
| Panel D exact and finite-\(\varepsilon\) rows | 6 |
| dilation rows | 2 |
| Panel D deterministic renderer samples | 101 |
| **Total** | **158** |

Every data row carries the primary and independent JSON source paths, both
producer hashes, evidence class, and normalization. The 101 Panel D samples
are explicitly typed as analytic renderer samples from the closed exact
formula. They are not observations, fitted data, or evidence used to infer
the formula.

## 5. Panel A: pressure-aware compressed interface

The panel uses

\[
 N=\mathbb P\nabla\!\cdot(u\otimes u),\qquad
 \mathcal C_s=P_s(u\odot N),\qquad
 \chi_s=\mathcal C_s-v_s\odot N_s.
\]

For the smooth four-site witness, \(h_*=(1,2,0)\), \(q=e^{-s}\), and

\[
 K=\begin{pmatrix}-2&1&0\\1&0&0\\0&0&0\end{pmatrix},
\]

the certificate gives

\[
 \widehat{\mathcal C_s}(h_*)=-q^5K,\qquad
 \widehat{v_s\odot N_s}(h_*)=-q^3K,\qquad
 \widehat\chi_s(h_*)=(q^3-q^5)K.
\]

These identities agree componentwise with both certificate coefficient maps
and all 16 Panel A rows. Since \(\chi_s\) is odd under the sign pair,

\[
 \widehat\chi_s(u;h_*)-\widehat\chi_s(-u;h_*)
 =2(q^3-q^5)K.
\]

Under \(u_L(x)=u(Lx)\) and \(s=\theta L^{-2}\), the displayed Frobenius
magnitude

\[
 2\sqrt6\,L(e^{-3\theta}-e^{-5\theta})
\]

also matches the certificate. The notation
\(\Delta\widehat\chi\) in the bottom figure line refers to this sign-pair
difference, as defined in Panel A; it is not a Laplacian.

**Panel A verdict:** PASS. It shows a selected exact coefficient of the
equation-slot-compressed lift. It does not establish unique or
information-theoretic minimality.

## 6. Panel B: four-site order separation

At the same output mode, the active \(2\times2\) blocks are

\[
 -\widehat{\partial_k\kappa_{kij}}(h_*)
 =q^3(1-q^2)^2(q^2+2)
 \begin{pmatrix}2&-3\\-3&4\end{pmatrix},
\]

\[
 -\widehat{\partial_iQ_j+\partial_jQ_i}(h_*)
 =q^3(1-q^2)
 \begin{pmatrix}4&2\\2&-8\end{pmatrix},
\]

\[
 \widehat\Xi(h_*)
 =q^3(1-q^2)
 \begin{pmatrix}-4&0\\0&4\end{pmatrix}.
\]

The two pressure rows sum to

\[
 q^3(1-q^2)
 \begin{pmatrix}0&2\\2&-4\end{pmatrix}.
\]

The omitted third row and third column are exactly zero in both complete
certificate tables. They are not values hidden by plotting or thresholding.

Because

\[
 1-q^2=2s+O(s^2),
\]

the prefactors have bottom-scale expansions

\[
 q^3(1-q^2)^2(q^2+2)=12s^2+O(s^3),
\qquad
 q^3(1-q^2)=2s+O(s^2).
\]

For example, the off-diagonal cumulant-flux coefficient is
\(-36s^2+O(s^3)\), while the combined pressure coefficient is
\(4s+O(s^2)\). Their ratio has magnitude

\[
 {1\over9s}+O(1).
\]

Thus the displayed statement that absorption costs at least \(s^{-1}\) is
correct for the selected coefficient. The figure writes “coefficientwise” in
the panel and footer, so it does not promote this ratio to a whole-field norm
inequality or universal closure lower bound.

**Panel B verdict:** PASS.

## 7. Panel C: six-site same-output witness

For

\[
 u=(6\sin y-4\sin(x+y),\;4\sin x+4\sin(x+y),\;0)
\]

at output mode \(h=0\), both complete contracted arrays

\[
 -\widehat{\partial_k\kappa_{kij}}(0),\qquad
 -\widehat{\partial_iQ_j+\partial_jQ_i}(0)
\]

vanish, while

\[
 \widehat\Xi(0)
 =(1-q^4)\operatorname{diag}(-48,48,0).
\]

This is nonzero for \(0<s<\infty\). The certificate also confirms that the
\(\lvert m\rvert^2=1\) input group cancels and the
\(\lvert m\rvert^2=2\) group supplies the displayed pressure--strain
coefficient.

This is a same-output coefficient witness. It is not a pair of distinct
inputs with identical complete \(\kappa_s\) fields and different pressure
sources.

**Panel C verdict:** PASS.

## 8. Panel D: selected quartic remainder

For the four-site field, the selected nonlinear physical-time coefficient is

\[
 \left.\partial_t\widehat\kappa_{112,s}(0,2,0)\right|_{\rm nonlinear}
 =2iq^2(1-q^2)^2.
\]

It is nonzero for every \(0<s<\infty\). At \(q=1/2\), direct substitution
gives

\[
 2i\left({1\over2}\right)^2
 \left(1-\left({1\over2}\right)^2\right)^2
 ={9i\over32},
\]

matching the independent finite-\(\varepsilon\) extraction.

Under parabolic dilation, the coefficient becomes

\[
 2iL e^{-2\theta}(1-e^{-2\theta})^2.
\]

The plotted ordinate is its absolute magnitude divided by \(L\):

\[
 g(\theta)=2e^{-2\theta}(1-e^{-2\theta})^2.
\]

This curve is positive for \(\theta>0\), has its maximum at
\(\theta=\tfrac12\log3\), and has peak \(8/27\). The rendered curve has that
shape and scale. The 101 plotted points are deterministic samples of this
closed formula, not a fit.

The figure and caption consistently call this a selected quartic remainder.
They do not claim a general centered-\(\kappa\) fourth-order ledger,
fourth-order non-closure, or failure of every finite hierarchy.

**Panel D verdict:** PASS.

## 9. Claim-boundary audit

The caption, README, chart contract, JSON contract, footer, and QA report
consistently permit only:

1. exact finite Fourier coefficients from two independent producers;
2. a coefficientwise four-site order separation;
3. a same-output six-site pressure witness;
4. one selected nonzero quartic next-level remainder;
5. deterministic plotting of an already certified closed formula.

They consistently reject:

    informationTheoreticMinimalityEstablished=FALSE
    wholeFieldNonRecoveryEstablished=FALSE
    finiteHierarchyNoGoEstablished=FALSE
    fourthOrderNonClosureEstablished=FALSE
    pdeClosureEstablished=FALSE
    navierStokesSimulation=FALSE
    fittedScalingLaw=FALSE
    singularSolution=FALSE
    regularityCriterionImproved=FALSE
    globalRegularityEstablished=FALSE
    clayProblemSolved=FALSE

The title and panel labels do not use unqualified “minimal,” “closure,”
“simulation,” “blow-up,” or novelty/priority wording. “Exact” modifies the
finite coefficient or source interface, not an arbitrary-data regularity
result.

The environment, manifest, contract, README, and QA report agree on

    ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
    dgxUsed=FALSE
    gpu=not used
    network=not used
    navierStokesSimulation=FALSE
    NOT CLAY

## 10. Final audit decision

The mathematical sources, immutable commit chain, certificate pins, two-path
common core, 158 source rows, Panel A--D formulas, bottom-scale orders, and
selected-coefficient boundaries all pass.

    figureSourceCommit=680fde5a24834b8e1c877f651eb20b119c671f49
    figurePackageSealCommit=b413586aa7a7389f8943acb2469eb28cdbbf31f3
    certificatePins=PASS
    twoPathCommonCore=PASS_BYTE_IDENTICAL
    panelACompressedInterface=PASS
    panelBFourSiteOrderSeparation=PASS_COEFFICIENTWISE
    panelCSixSitePressureWitness=PASS_SAME_OUTPUT_COEFFICIENT
    panelDSelectedQuarticRemainder=PASS_SELECTED_COEFFICIENT
    sourceDataRows=158
    formalFigureChecks=147/147
    genericFigurePackageErrors=0
    genericFigurePackageWarnings=0
    ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
    dgxUsed=FALSE
    clayConclusion=OPEN
    figureSourceAudit=PASS
    releaseBlockers=NONE
    NOT CLAY
