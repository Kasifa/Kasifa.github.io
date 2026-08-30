**Figure R0.73I — finite selected-gain action and correction diagnostic.**
**A,** Finite Fourier--Galerkin average actions
`A_N(D)/D` at `N=24,48,96` and 64-point Gauss--Legendre quadrature.  The
visible axis break separates the rigorous continuum numerical-abscissa upper
bound `c_H(0)=sqrt(19/180)` from the magnified band containing the finite
values and the `r=0.17035` reference.  The three windows are
`D=10^-4` (explicit pilot),
`D_ub=sqrt(19/180)/392` (a strict analytic upper bound for the existential
`d0`, not `d0`), and `D=1/450` (a legacy comparison, not the inherited
theorem endpoint).
**B,** The finite correction remainder
`R_{Lambda,48}(D)-C_48(D)` versus `Lambda`, where
`R_{Lambda,N}=log G_{Lambda,N}-Lambda A_N` and
`C_N=-integral Re(<ell,h_d>+<ell,Lh>) dd` is the computed finite
Berry-plus-viscous correction.  The dashed `Lambda^-1` segment is only a
visual slope guide.  Every colored mark and curve is a binary64 finite
Fourier--Galerkin diagnostic.  Ordinary cutoff/step agreement and the
observed approach to `C_N` are not a tail enclosure, continuum action
theorem, or adiabatic proof.
