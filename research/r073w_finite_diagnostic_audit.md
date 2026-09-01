# R0.73W finite diagnostic audit

**Audit date:** 2026-09-01

**Status:** two independent exact producers agree; the final manifest is
commit-bound to the immutable source commit

**Package:** `research/certificates/r073w/`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## 1. Question certified

The finite gate tests two universal statements about

\[
 \Pi_s=-\tau_s:\nabla v_s,\qquad
 D_{ii,s}=P_s(|\nabla u|^2)-|\nabla v_s|^2.
\]

1. Does \(\Pi_s\) have a universal pointwise or spatial-mean one-sided sign
   for all smooth divergence-free data?
2. Can a constant independent of field amplitude satisfy
   \[
   |\langle\Pi_s\rangle|
   \le C\nu\langle D_{ii,s}\rangle
   \tag{1.1}
   \]
   for every smooth divergence-free datum at a fixed positive heat scale?

An exact finite counterexample is sufficient to answer either universal
question negatively.  It is not sufficient to infer generic turbulent
behavior, a singularity, or a regularity theorem.

## 2. Independent producer architecture

The primary producer, `compute_fourier_certificate.py`, uses sparse complex
Fourier maps.  Coefficients lie in the Gaussian rationals, and heat dependence
is stored as exact sparse Laurent polynomials in \(q=e^{-s}\).  Stress and
production are rebuilt through exact Fourier convolution.

The second producer, `independent_trig_certificate.py`, does not import the
primary path.  It starts from real sine/cosine fields, applies independent
product-to-sum rules, and stores rational \(q\)-polynomials as dense tuples.
It reconstructs the same physical objects in a different basis and data
structure.

Both producers:

- rebuild \(v_s,\tau_s,\Pi_s\), unfiltered/filtered gradient energy, and
  \(D_{ii,s}\) from the declared fields;
- recompute the negative field rather than only asserting parity;
- compute Fourier-support rank by exact rational elimination;
- use the Python standard library only, with no floating point or network;
- emit complete `commonCore` objects for bytewise comparison.

## 3. Rank-three primary witness

The public witness is

\[
 \begin{aligned}
 R(x,y,z)=\big(&\cos(y+z)-\sin(x+y+z)+\cos(2z),\\
 &\cos x+\sin(x+y+z),0\big).
 \end{aligned}
\tag{3.1}
\]

Both producers verify that it is real, mean-zero, divergence-free, and has
Fourier-support rank three.  For \(u_A=AR\), they agree exactly on

\[
 {\langle\Pi_s(u_A)\rangle\over A^3}
 ={1\over4}q^2(1-q^2),
\tag{3.2}
\]

\[
 \langle|\nabla R|^2\rangle={13\over2},
\qquad
 {\langle|\nabla v_s|^2\rangle\over A^2}
 ={1\over2}q^2+q^4+3q^6+2q^8,
\tag{3.3}
\]

and

\[
 {\langle D_{ii,s}\rangle\over A^2}
 ={1\over2}(1-q^2)+(1-q^4)+3(1-q^6)+2(1-q^8).
\tag{3.4}
\]

The factored form is

\[
 {\langle D_{ii,s}\rangle\over A^2}
 ={1\over2}(1-q^2)(13+12q^2+10q^4+4q^6).
\tag{3.5}
\]

For \(-R\), stress and gradient defect are unchanged while production is
the negative of (3.2).  Thus a one-sided sign law cannot hold for all smooth
divergence-free fields.

For \(A>0\), \(\nu>0\), and \(0<q<1\), exact cancellation gives

\[
 { |\langle\Pi_s(u_A)\rangle|
  \over \nu\langle D_{ii,s}(u_A)\rangle}
 ={Aq^2\over2\nu(13+12q^2+10q^4+4q^6)}.
\tag{3.6}
\]

The ratio is linear in \(A\) and therefore unbounded as
\(A\to\infty\).  As \(q\to1\), its coefficient tends to
\(1/(78\nu)\).  This disproves (1.1) with an amplitude-independent constant.

## 4. Diagnostic cross-checks

The package retains two additional fields.

The three-coordinate triad

\[
 W=(\cos(y+z)-\sin(x+y+z),\ \cos x+\sin(x+y+z),0)
\tag{4.1}
\]

has frequency rank two, because the three positive wavevectors satisfy one
exact triad relation and the field is invariant under
\(\partial_y-\partial_z\).  Both producers correctly report rank two rather
than inferring rank from the displayed coordinates.  They verify

\[
 \langle\Pi_s(AW)\rangle/A^3={1\over4}q^2(1-q^2)
\tag{4.2}
\]

and the small-scale ratio coefficient \(1/(46\nu)\).

The 2D3C field

\[
 U=(0,-2,-1)\cos x+(-2,0,-1)\cos y
 +(-2,2,-1)\sin(x+y)
\tag{4.3}
\]

gives

\[
 \langle\Pi_s(AU)\rangle/A^3=-q^2(1-q^2),
\qquad
 \langle D_{ii,s}(AU)\rangle/A^2
 =(1-q^2)(14+9q^2).
\tag{4.4}
\]

The opposite sign in (4.4) is an independent diagnostic of convention and
parity.  The public conclusion remains bound to the rank-three field (3.1).

## 5. Final computation and source seal

After rerunning both producers from the immutable source:

```text
primaryProducerChecks=56/56 PASS
independentProducerChecks=56/56 PASS
commonCoreAgreement=TRUE
commonCoreSha256=4c72251bde4bf12bb5cfe8c3c6b15c0e049dc440a2c41daa751eb0a5da9460f2
arithmetic=EXACT_NO_FLOATING_POINT
standardLibraryOnly=TRUE
networkUsed=FALSE
dgxUsed=false
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
manifestStatus=SEALED_COMMIT_BOUND
sourceCommit=b9f3b3943df1e2abf6abc2f51c1fb25d1f1e8440
gitPinApplied=true
```

The seal reads all nine source blobs from the full 40-character commit and
requires byte identity with the current sources.  `SHA256SUMS` binds those
nine files, the two generated results, and `manifest.json`.

## 6. Exact conclusion boundary

The immutable source-bound package licenses exactly these statements:

- no universal pointwise one-sided sign rule can hold for every smooth
  divergence-free field;
- no universal spatial-mean one-sided sign rule can hold;
- no amplitude-independent constant can make the specific same-time mean
  absorption (1.1) hold for all amplitudes;
- the public witness has rank-three Fourier support.

It does not license any of the following:

- that one fixed witness changes sign from point to point;
- that rank three means generic three-dimensional turbulence;
- that every possible viscous, nonlinear, localized, or time-integrated
  payment fails;
- that the field is a Navier--Stokes time trajectory or blow-up candidate;
- arbitrary-data global regularity or a Clay conclusion.

```text
universalPointwiseOneSidedSignRule=FALSE
universalMeanOneSidedSignRule=FALSE
amplitudeIndependentSameTimeMeanQuadraticAbsorption=FALSE
formalFiniteCertificate=SEALED_COMMIT_BOUND
primaryWitnessFrequencyRank=3
genericityClaim=FORBIDDEN
navierStokesSimulation=NOT_RUN
singularityClaim=FORBIDDEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
NOT CLAY
```
