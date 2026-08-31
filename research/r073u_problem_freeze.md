# R0.73U problem freeze: full-tensor heat hierarchy and the signed-flux boundary

**Frozen date:** 2026-09-01

**Domain:** the normalized periodic torus \(\mathbb T^3=[0,2\pi]^3\),
with normalized Haar measure \(d\mu=(2\pi)^{-3}dx\), viscosity \(\nu>0\),
and a smooth real mean-zero divergence-free Navier--Stokes solution on its
smooth lifespan

**Dependencies:** the R0.73Q periodic \(L_t^4L_x^6\) Stokes--HLS estimate,
the R0.73R caloric/LP critical-space audit, and the R0.73T scalar
autocorrelation non-closure result

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Frozen question

R0.73T showed that the scalar product field
\(\widehat{|u|^2}\) loses both tensor polarization and a signed cubic flux.
R0.73U replaces that scalar object by the complete local-product tensor at
every heat scale.  With \(P_s=e^{s\Delta}\), define

\[
 v_s=P_su,\qquad
 \Theta_s=P_s(u\otimes u),\qquad
 \tau_s=\Theta_s-v_s\otimes v_s,\qquad
 p_s=P_sp.
 \tag{1.1}
\]

The bounded questions are:

1. Does \(\Theta_s\) retain enough tensor information to reconstruct pressure
   at the same heat scale?
2. Is \(\tau_s\) positive, and does it satisfy an exact evolution in the
   scale variable \(s\)?
3. Do \(\Theta_s\), \(\tau_s\), and \(p_s\) remain in the critical product
   space paired with \(E=L_t^4L_x^6\)?
4. Can the complete quadratic tensor heat hierarchy evolve autonomously, or
   does a signed third-order flux remain missing?
5. If autonomy fails, what is the smallest exact finite Fourier witness, and
   what derivative cost remains at a parabolic heat slice \(s\asymp L^{-2}\)?

The target is an exact positive hierarchy and a narrow, auditable no-go
statement.  The target is not a finite turbulence closure model and not an
arbitrary-data global regularity theorem.

## 2. Objects that must not be conflated

The local product tensor used here is

\[
 T^{\rm loc}_{ij}(h)=\widehat{u_i u_j}(h)
 =\sum_k\widehat u_i(k)\widehat u_j(h-k).
 \tag{2.1}
\]

It differs from the classical two-point K\'arm\'an--Howarth tensor

\[
 R_{ij}(r)=\int_{\mathbb T^3}u_i(x)u_j(x+r)\,d\mu(x),
 \qquad
 \widehat R_{ij}(k)=\widehat u_j(k)\overline{\widehat u_i(k)}.
 \tag{2.2}
\]

The first object retains cross-wave-number convolutions and reconstructs the
instantaneous pressure.  The second retains same-wave-number covariance and
leads to the classical KHM hierarchy.  A result for one is not to be stated as
a result for the other.

## 3. Frozen positive claim slots

The analytic gate must prove, with all tensor norms and signs specified:

- pointwise symmetry and positive semidefiniteness of \(\Theta_s\) and
  \(\tau_s\);
- the heat covariance identity
  \[
   \partial_s\tau_s
   =\Delta\tau_s+2\sum_\ell
     (\partial_\ell v_s)\otimes(\partial_\ell v_s),
   \qquad \tau_0=0;
  \tag{3.1}
  \]
- same-scale pressure reconstruction and the exact filtered equation;
- contraction estimates in \(L_t^2L_x^3\), followed by the R0.73Q causal
  Stokes map back to \(L_t^4L_x^6\);
- the exact tensor heat-plane identity, including the cubic and
  pressure--velocity terms.

These claims may be called exact identities, classical filtering
reconstructions, or internal corollaries as appropriate.  None is a novelty
or priority claim.

## 4. Frozen no-go claim

The no-go is restricted to a state made only from even quadratic data:

\[
 \mathcal H(u)=\{\Theta_s(u),\tau_s(u),p_s(u):s\ge0\}.
 \tag{4.1}
\]

Since \(\mathcal H(-u)=\mathcal H(u)\), a single-valued autonomous law for
the signed tensor time tangent would have to give the same tangent to \(u\)
and \(-u\).  The finite certificate must exhibit a smooth divergence-free
trigonometric polynomial for which the nonlinear tensor tangent is nonzero
and changes sign.  This proves non-autonomy of the quadratic hierarchy alone.

The result does **not** say that a state containing the signed resolved
velocity \(v_s\) is non-autonomous.  Including all of \(u\), or the \(s=0\)
signed velocity, restores the original Navier--Stokes state and therefore
falls outside the no-go.

## 5. Frozen parabolic-scale boundary

For integer dilations of the exact witness, the coefficient-level tangent
separation must be evaluated at \(h_L=(L,2L,0)\).  At a fixed heat scale it is
exponentially suppressed.  At a parabolic slice \(s=\theta L^{-2}\), it must
be shown to retain a factor proportional to

\[
 L e^{-5\theta}
 =\sqrt{\theta}\,e^{-5\theta}s^{-1/2}.
 \tag{5.1}
\]

The permitted conclusion is: this witness forces a one-derivative
\(s^{-1/2}\) cost for recovery of its signed tensor tangent at a fixed
parabolic heat slice.  It does not prove that every time-integrated estimate,
every augmented hierarchy, or every cancellation mechanism must fail.

## 6. Release boundary

R0.73U may be marked complete only after:

1. the analytic derivation and an independent sign/index audit agree;
2. an exact rational sparse-Fourier certificate reproduces the witness;
3. a formal figure package passes data, vector, raster, print-size, and
   grayscale checks;
4. the claim--source ledger distinguishes classical KHM/filtering results
   from local calculations and open claims;
5. Chinese and English HTML/PDF copies are synchronized;
6. the cumulative recap, homepage counters, route inventory, and GitHub Pages
   deployment are verified live.

Ordinary Chinese--English translation is performed directly on the local
workstation.  DGX is not used for translation.  No Navier--Stokes simulation
is required by this analytic/finite release.
