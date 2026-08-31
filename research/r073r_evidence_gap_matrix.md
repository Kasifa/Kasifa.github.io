# R0.73R evidence gap matrix

**Status:** bounded discovery and targeted follow-up complete; certificate and
release audit still pending

| Claim slot | Current evidence | Confidence | Main risk or contradiction | Next targeted check |
|---|---|---:|---|---|
| Periodic heat-flow norm is equivalent to the dyadic \(\ell^4\) critical Besov budget | Direct proof plus Chemin--Gallagher (2006), Definitions 1.1 and 2.2, on mean-zero \(\mathbb T^3\) | high | None at the level claimed; it is a classical collision, not a novelty slot | Retain the direct normalization proof and label `VERIFIED_CLASSICAL` |
| Sextic shell concentration has the autocorrelation formula and the component-safe \(|f|^2f\) convolution identity | Independent Fourier expansion and Parseval derivation | high | Fourier-sign convention could shift indices without changing the norm | Independent finite-lattice reconstruction with exact rational arithmetic |
| Modal count gives \(\|f_j\|_6\lesssim m_j^{1/3}\|f_j\|_2\) | Hausdorff--Young plus finite-support \(\ell^{6/5}\)-to-\(\ell^2\) comparison; independent component-safe readback | high | Definition of an active site must include vector coefficients | Test equality-scale examples and retain a fixed three-component constant |
| Triple-sum additive multiplicity gives \(\|f_j\|_6\lesssim R_j^{1/6}\|f_j\|_2\) | Independent Plancherel and Cauchy--Schwarz derivation | high | Real/vector support conventions and sharpness not yet tested | Exact convolution enumeration on the matched families |
| Dirichlet and Rudin--Shapiro fields have identical support and coefficient magnitudes | Explicit polynomial definitions and carrier construction | high | Real-field encoding may change multiplicities at conjugate sites | Enumerate the full vector Fourier table for finite \(m\) |
| Exact carrier moments are \(1/2\) and \(5/16\) | Even-power expansion with \(N>6(m-1)\); exact rational convolution checks for \(m=1,2,4,8\) | high | General proof still needs to state the envelope support bound | Independent Laurent-polynomial coefficient extraction |
| \(\|D_m\|_6^6=(11m^5+5m^3+4m)/20\) | Direct triple-sum count; exact integer checks for \(m=1,2,4,8\) | high | Closed-form combinatorial derivation not yet written | Derive the piecewise quadratic triple-count formula and sum its square |
| Rudin--Shapiro normalized matched field has uniformly bounded \(L^6\) | \(|P_m|\le\sqrt{2m}\), \(L^2(P_m)^2=m\) | high | Bound constant in the two-dimensional real carrier field | Recompute the sixth moment inequality exactly |
| One-annulus \(\mathfrak X\) norm is equivalent to \(N^{-1/2}L^6\) | Uniform smooth annular heat multiplier and inverse-multiplier proof; independent reconstruction agrees | high | Must say fixed-ratio annulus, not “exactly one arbitrary LP block” | Preserve the width ratio \(\sqrt{82}/8\) and audit the implementation constants |
| Matched scaled fields have \(L^2\to0\), coherent \(\mathfrak X\asymp1\), incoherent \(\mathfrak X\to0\) | Algebraic combination of exact moments and the two-sided annular bound; independent power audit agrees | high | An \(\asymp1\) statement alone does not order an unknown threshold | Use a fixed extra amplitude only when comparing with a prescribed threshold; seal a finite formula certificate |
| The formulation is not already a named theorem with the same Navier--Stokes consequence | Targeted primary search found complete collisions for heat/Besov, sparse-frequency \(\Lambda(p)\), randomization, refined Sobolev, spectral clusters, and oscillatory large data; no exact matched divergence-free pair was located | medium-high | Absence from a bounded search is not a novelty proof | Publish only a local synthesis claim and keep novelty/priority forbidden |
| Failure of the heat-flow entrance does not imply unsafe dynamics | Exact identity \((e_3g(x_1,x_2)\cdot\nabla)e_3g=0\) | high | None if the fields are independent of \(x_3\) | Include this exclusion in every public summary and figure caption |
| Exact phase-sensitive convolution is a genuinely cheaper proxy | It exactly reconstructs \(\|f_j\|_6\) | high | It is an evaluation identity and becomes circular if advertised as an independent a priori improvement | Label it an exact finite diagnostic; reserve “proxy” for \(R_j\), \(M_j\), or a future cheaper phase statistic |

## Discovery stop rule

The broad-search stop rule has fired.  The heat/Besov characterization,
finite-support inequalities, Rudin--Shapiro flatness, randomization, refined
Sobolev, spectral-cluster, and oscillatory-data neighborhoods have been
checked.  Further searching is now limited to a concrete theorem-number,
domain, or priority-risk question raised during source readback.
