# R0.73N symmetry audit: why the background family cannot be one trajectory

**Status:** direct transformation proof; independent analytic and
adversarial audits PASS

**Question:** can an exact Navier--Stokes symmetry, time shift, or compactness
argument turn the R0.73M family
\(\{\overline U_\Lambda\}_{\Lambda\to\infty}\) into perturbations of one
fixed background while preserving viscosity one, the standard torus,
the \(H^3\) input topology, and the \(L^2\) output distance?

**Decision:** no.  Each candidate either leaves \(\Lambda\) unchanged or
changes the equation, domain, Fourier rows, observation time, or endpoint
distance.

## 1. General amplitude--space scaling ledger

Write Navier--Stokes on \(\mathbb T_L^d\) as

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p
 =\nu\Delta u,
 \qquad \nabla\cdot u=0.
 \tag{1.1}
\]

For \(A,C>0\), define

\[
 v(t,x)=A\,u(ACt,Cx),
 \qquad
 q(t,x)=A^2p(ACt,Cx).
 \tag{1.2}
\]

Direct substitution gives

\[
 \nu'=\frac AC\nu,
 \qquad
 L'=\frac LC,
 \qquad
 T'=\frac{T}{AC}.
 \tag{1.3}
\]

Thus fixed viscosity requires \(A=C\), the standard parabolic scaling

\[
 S_Cu(t,x)=C\,u(C^2t,Cx).
 \tag{1.4}
\]

If the torus period and an invertible dynamical conjugacy are also fixed,
\(C=1\).  An integer \(C=m>1\) produces a shorter-period solution that can
be viewed on the original torus, but \(x\mapsto mx\) is a covering map,
not an invertible torus automorphism.  It also changes every Fourier row.

With unnormalized volume measure,

\[
 \|Aw(C\cdot)\|_{H^3(\mathbb T_{L/C}^d)}^2
 =A^2C^{-d}\sum_{|\alpha|\le3}C^{2|\alpha|}
 \|\partial^\alpha w\|_2^2.
 \tag{1.5}
\]

For fixed-viscosity scaling \(A=C\),

\[
 \|S_Cw\|_{\dot H^s}
 =C^{s+1-d/2}\|w\|_{\dot H^s}.
 \tag{1.6}
\]

In particular, \(H^3\) is not scaling invariant.  Under normalized measure
on a fixed torus and an integer covering, the Jacobian factor is replaced
by the covering multiplicity and the highest derivative still scales as
\(C^4\).

## 2. Candidate transformation table

| Candidate | Exact effect | R0.73M verdict |
|---|---|---|
| spatial translation | preserves \(\nu,L,T,H^3,L^2\); changes only Fourier phase | cannot change amplitude \(\Lambda\) |
| time translation | moves the initial state along one trajectory | the two heat modes have incompatible decay rates |
| Galilean transform | \(u(t,x-ct)+c\); preserves paired difference norms | adds a zero mode and moving phases, not amplitude |
| pure amplitude | \(u\mapsto Au\) | not a symmetry of the nonlinear neighborhood |
| amplitude plus time | \(u(t,x)\mapsto Au(At,x)\) | changes viscosity to \(A\nu\) |
| standard scaling | \(u\mapsto Cu(C^2t,Cx)\) | changes frequencies, period representation, time, and \(H^3\) |
| integer torus covering | \(m u(m^2t,mx)\) | maps \(K_z=\pm1\) to \(K_z=\pm m\) and is not invertible |
| divide by \(\Lambda\) | fixes the background profile | leaves a \(\Lambda\)-dependent nonlinear coefficient |
| fast-time normalization | fixes nonlinear coefficient after amplitude division | changes viscosity, observation time, and endpoint distance |

## 3. Pure amplitude is accidental only on the base shear

In Leray form,

\[
 \partial_t(Au)+\mathbb P[(Au\cdot\nabla)(Au)]-\nu\Delta(Au)
 =A(A-1)\mathbb P[(u\cdot\nabla)u].
 \tag{3.1}
\]

The background is a unidirectional shear, so
\((\overline U\cdot\nabla)\overline U=0\) and
\(\overline U_\Lambda=\Lambda\overline U_1\) is again an exact solution.
Once a non-shear perturbation is added, the right side of (3.1) generally
does not vanish.  Amplitude division therefore does not conjugate the
neighborhood dynamics.

For example, setting \(V_\Lambda=U_\Lambda/\Lambda\) gives

\[
 \partial_tV_\Lambda
 +\Lambda(V_\Lambda\cdot\nabla)V_\Lambda+\nabla P_\Lambda
 =\Delta V_\Lambda.
 \tag{3.2}
\]

The background is fixed, but the equation is not.

Alternatively, with fast time

\[
 V_\Lambda(s,x)=\Lambda^{-1}U_\Lambda(s/\Lambda,x),
 \tag{3.3}
\]

one obtains

\[
 \partial_sV_\Lambda+(V_\Lambda\cdot\nabla)V_\Lambda+\nabla P_\Lambda
 =\Lambda^{-1}\Delta V_\Lambda.
 \tag{3.4}
\]

The background becomes \(2W(4s/\Lambda,2y)\), the observation time becomes
\(s_*=\Lambda T_*\), and the R0.73M endpoint lower bound becomes
\(c_*\rho/\Lambda\to0\).  Equation, time, background, and distance have all
changed.

## 4. Time translation cannot identify two family members

The explicit background is

\[
 \overline U_\Lambda(t,y)
 =e_z\left[-\Lambda e^{-4t}\sin2y
 +\frac{\Lambda}{2}e^{-16t}\sin4y\right].
 \tag{4.1}
\]

If a time translate of \(\overline U_{\Lambda_0}\) equals
\(\overline U_\Lambda\) on a nontrivial interval, equality of its two
orthogonal Fourier coefficients requires

\[
 \Lambda=\Lambda_0e^{-4\tau}
 =\Lambda_0e^{-16\tau}.
 \tag{4.2}
\]

Hence \(\tau=0\) and \(\Lambda=\Lambda_0\).  Spatial translation or a
Galilean change can only multiply nonzero Fourier coefficients by
unit-modulus phases and cannot repair (4.2).

## 5. Parabolic scaling cannot preserve the selected geometry

Applying (1.4) to one member gives

\[
 S_C\overline U_{\Lambda_0}
 =e_z\left[
 -C\Lambda_0e^{-4C^2t}\sin(2Cy)
 +\frac{C\Lambda_0}{2}e^{-16C^2t}\sin(4Cy)
 \right].
 \tag{5.1}
\]

Equality with a member of the original family requires preservation of the
Fourier support \(\{2,4\}\), the two heat rates \(\{4,16\}\), and the
selected \(K_z=\pm1\) perturbation row.  These conditions force \(C=1\),
after which \(\Lambda\) is unchanged.

## 6. Compactness at the original initial time fails

Orthogonality of the two background modes gives the exact normalized
energy

\[
 \|\overline U_\Lambda(0)\|_2^2
 =\Lambda^2\left(\frac12+\frac18\right)
 =\frac58\Lambda^2.
 \tag{6.1}
\]

The family is unbounded in every fixed Sobolev space.  It has no
weakly compact subsequence in those spaces.  Dividing by \(\Lambda\) makes
the backgrounds converge but changes the perturbation equation as in
(3.2).

## 7. Time-shift compactness loses the two-harmonic mechanism

For a shift \(\tau_\Lambda\), put

\[
 a_\Lambda=\Lambda e^{-4\tau_\Lambda},
 \qquad
 b_\Lambda=\Lambda e^{-16\tau_\Lambda}.
 \tag{7.1}
\]

They satisfy the exact relation

\[
 b_\Lambda=\frac{a_\Lambda^4}{\Lambda^3}.
 \tag{7.2}
\]

Any shifted sequence bounded in \(H^3\) has \(a_\Lambda,b_\Lambda\)
bounded.  Consequently \(b_\Lambda\to0\).  Every strong limit is either
zero or a single first-harmonic heat shear; it cannot retain two nonzero
harmonics.

The representative choice

\[
 \tau_\Lambda=\frac14\log\Lambda
 \tag{7.3}
\]

gives

\[
 \overline U_\Lambda(t+\tau_\Lambda)
 \longrightarrow-e^{-4t}\sin2y\,e_z,
 \tag{7.4}
\]

while the second-harmonic coefficient is
\(\frac12\Lambda^{-3}e^{-16t}\).

R0.73M contains no theorem for the interval
\([\tau_\Lambda,\tau_\Lambda+T]\): it does not prove a small shifted
perturbation, a new selected action after the second harmonic disappears,
or a fixed endpoint distance there.  If all three properties and strong
background convergence held at one fixed \(T>0\), the fixed-time
relative-energy continuity theorem would contradict them.

## 8. Infinite-block embedding does not rescue this route

A superposition of mean-zero heat shears is still an exact unforced
background because shear self-advection vanishes.  This observation does
not embed the R0.73M nonlinear neighborhoods:

1. a fixed smooth periodic shear has decaying Fourier coefficients and a
   finite \(\int_0^\infty\|U(t)\|_{H^4}\,dt\);
2. the \(H^3\) tube proof in the companion no-go theorem then gives it a
   positive fixed-background stability radius;
3. interactions of a perturbation with all background blocks are not the
   isolated two-harmonic selected-row problem certified in R0.73M.

Thus an infinite superposition would require a new spectral and nonlinear
theorem, and any smooth heat-shear candidate remains inside the same
finite-total-strain stability class.

## 9. Exact boundary

~~~text
amplitudeOnlyIdentificationIsNSSymmetry=FALSE
timeTranslationIdentifiesLambdaFamily=FALSE
parabolicScalingIdentifiesLambdaFamilyOnFixedTorus=FALSE
originalTimeCompactness=FALSE
boundedTimeShiftRetainsTwoHarmonics=FALSE
infiniteSmoothHeatShearEvadesFiniteStrainTube=FALSE
differentForcedOrNondecayingBackgroundRoute=OPEN
transverseCriticalNormGrowth=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
~~~

The audit closes only the claim that the already certified family can be
relabelled as one fixed background.  It does not classify every possible
fixed non-autonomous Navier--Stokes trajectory.
