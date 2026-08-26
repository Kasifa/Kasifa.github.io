# R0.71U bounded primary-source audit: temporal jets, recurrence, and zero-level occupation

**Search date:** 2026-08-26

**Question:** do established NSE, analytic-zero, coarea, variation, or
Carleson theorems already sum the normalized derivative mass at all positive
zeros of a global shell; and what established framework contains the exact
2D3C recurrence construction?

## 1. Bounded answer

The checked literature does not supply the complete R0.71U result.

Established time analyticity makes a fixed finite-dimensional shell curve
analytic on a classical interval.  It gives trajectory-wise finiteness of
nontrivial shell zeros on compact subintervals, but no energy-uniform number,
minimum separation, or derivative-mass sum.  Jensen gives a conditional count
only after paying a complex radius, a complex upper norm, and a nonzero lower
anchor.  Carleson and tent-space results provide upper parabolic mass, not a
reverse lower mass at every zero.  Coarea and Banach-indicatrix results
integrate crossings over the level; a distinguished zero level can remain an
exceptional boundary trace.

The exact 2D3C reduction of three-dimensional NSE to a two-dimensional
in-plane NSE plus a passively advected out-of-plane velocity component is
standard.  The narrower triangular shear used in R0.71U is obtained by direct
substitution.  The bounded search did not locate a theorem prescribing an
arbitrary finite set of Fourier-mode zero times inside that class.  This is a
search boundary, not an originality or priority statement.

The search used two focused waves: first temporal analyticity, zero counting,
and Carleson/occupation; then 2D3C invariant dynamics, parameter
transversality, and weak trace regularity.  Further repeated searches were
stopped when they returned the same source families without a fixed-level
normalized-jet theorem.

## 2. Claim-to-source ledger

| Source | Verified scope | Why it does not close R0.71U |
|---|---|---|
| Kyuya Masuda, *On the Analyticity and the Unique Continuation Theorem for Solutions of the Navier--Stokes Equation* (1967), [DOI](https://doi.org/10.3792/pja/1195521421) | Time analyticity for classical NSE and a unique-continuation statement for the complete field. | A filtered shell vanishing at one time is not the complete field vanishing on a spatial open set; no count, separation, or jet mass is supplied. |
| Roger Temam, *Navier--Stokes Equations and Nonlinear Functional Analysis*, 2nd ed., [open monograph](https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf) | Complex-time analyticity on strong intervals, with bounds depending on strong norms. | The radius and complex upper norm are trajectory dependent and not controlled uniformly by Leray energy near an unknown endpoint. |
| Giga--Jo--Mahalov--Yoneda, *On time analyticity of the Navier--Stokes equations with spatially almost periodic data* (2008), [DOI](https://doi.org/10.1016/j.physd.2008.03.007), [author PDF](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/69669/re860.pdf) | Holomorphic time sectors and no sudden creation for suitable Fourier data. | Isolated repeated zeros remain possible; no quantitative derivative mass at all zeros is bounded. |
| Foias--Temam, *Gevrey class regularity for the solutions of the Navier--Stokes equations* (1989), [DOI](https://doi.org/10.1016/0022-1236(89)90015-3) | Spatial Gevrey regularity and Fourier decay for periodic regular solutions. | Spatial decay at each time does not control temporal recurrence of one projection. |
| Linkmann--Buzzicotti--Biferale, *Non-universal behaviour of helical two-dimensional three-component turbulence* (2018), [DOI](https://doi.org/10.1140/epje/i2018-11612-1), [postprint](https://www.pure.ed.ac.uk/ws/portalfiles/portal/148197815/1801.06091.pdf) | Equations (1) record 2D3C NSE as in-plane 2D NSE plus passive evolution of the third component. | It supplies the invariant-class context, not arbitrary prescribed target-zero times. |
| Biferale--Buzzicotti--Linkmann, *From two-dimensional to three-dimensional turbulence through two-dimensional three-component flows* (2017), [DOI](https://doi.org/10.1063/1.4990082), [arXiv](https://arxiv.org/abs/1706.02371) | Further records the standard 2D3C framework and its dynamical context. | It does not prescribe temporal zeros of a fixed Fourier projection by selecting unforced initial data. |
| Karlin--Studden, *Tchebycheff Systems* (1966), [catalogue record](https://books.google.com/books?id=P7Y-AAAAIAAJ) | Standard source for Chebyshev systems, sign-regular evaluation matrices, and interpolation. | It supplies the finite interpolation tool, not the NSE invariant-class construction. |
| Agrachev--Sarychev, *Navier--Stokes equations: controllability by means of low modes forcing* (2005), [DOI](https://doi.org/10.1007/s00021-004-0110-1) | Projection and solid controllability using finite-dimensional external forcing. | R0.71U selects initial data and then evolves the unforced equation; it also prescribes several zero times rather than one controlled terminal projection. |
| Shirikyan, *Exact controllability in projections for three-dimensional Navier--Stokes equations* (2007), [DOI](https://doi.org/10.1016/J.ANIHPC.2006.04.002), [journal page](https://ems.press/journals/aihpc/articles/4076970) | Exact controllability of finite-dimensional projections with time-dependent external control. | It is an important neighboring theorem but has different control, forcing, and temporal quantifiers. |
| Singh--Sridhar, *Plane shearing waves of arbitrary form: exact solutions of the Navier--Stokes equations* (2011), [arXiv](https://arxiv.org/abs/1101.5507) | Exact plane shearing waves and Kelvin-mode superposition in a background linear shear. | Different domain/background geometry and no normalized shell-zero packing theorem. |
| Koch--Tataru, *Well-Posedness for the Navier--Stokes Equations* (2001), [author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf), [DOI](https://doi.org/10.1006/aima.2000.1937) | Critical \(BMO^{-1}\) data and an upper parabolic square-Carleson norm. | No reverse lower mass for every smooth zero and no derivative sample at a distinguished level. |
| Stanislaw Banach, *Sur les lignes rectifiables et les surfaces dont l'aire est finie* (1925), [DOI](https://doi.org/10.4064/fm-7-1-225-236) | Indicatrix identity relating variation to crossing number integrated over the level. | It does not control one fixed exceptional level. |
| Rafal M. Lochowski, *On a generalisation of the Banach indicatrix theorem* (2017), [DOI](https://doi.org/10.4064/cm6583-3-2017), [arXiv](https://arxiv.org/abs/1503.01746) | Upward/downward and truncated variation as level-integrated crossing quantities. | Positive-height excursions are controlled, but raw zero-height entries with collapsing amplitudes are not. |
| Bertoin--Yor, *Local times for functions with finite variation* (2014), [DOI](https://doi.org/10.1112/blms/bdu014) | Local-time/occupation formulas for finite-variation paths, with level statements in the appropriate a.e. sense. | A zero-level boundary density still requires an endpoint trace theorem. |
| Lennart Carleson, *An interpolation problem for bounded analytic functions* (1958), [DOI](https://doi.org/10.2307/2372840) | Interpolating analytic zero sequences under quantitative separation. | Bounded analyticity alone gives Blaschke-type summability, not the separation or lower anchors needed here. |
| Morris Hirsch, *Differential Topology* (1976), [DOI](https://doi.org/10.1007/978-1-4684-9449-5) | Finite-dimensional transversality and parameter transversality. | A one-dimensional time curve cannot be transverse to a point in a shell space of dimension greater than one. \(C_t\ne0\) should be called a first-order vector zero. |
| Stephen Smale, *An infinite dimensional version of Sard's theorem* (1965), [DOI](https://doi.org/10.2307/2373250) | Sard--Smale framework for Fredholm maps. | It does not provide a slope lower bound or recurrence packing; the R0.71U construction uses an explicit finite IFT instead. |
| Caffarelli--Kohn--Nirenberg, *Partial regularity of suitable weak solutions of the Navier--Stokes equations* (1982), [DOI](https://doi.org/10.1002/cpa.3160350604) | Local energy framework and parabolic size of the singular set. | It does not define \(C_t(t_\beta)\) and \(Y(t_\beta)\) at an arbitrary weak zero time or show that spectral zeros avoid singular times. |

## 3. Conditional analytic theorem that is already available

Let a finite-dimensional shell curve \(C\) be holomorphic in
\(D_R(s_0)\), and suppose

\[
 M=\sup_{D_R(s_0)}\|C\|,
 \qquad m=\|C(s_0)\|>0.
\]

Choose a norm-one functional \(\ell\) with
\(|\ell(C(s_0))|=m\).  Every vector zero of \(C\) is a zero of the scalar
function \(\ell\circ C\).  Jensen therefore gives, for \(0<r<R\),

\[
 N_C(D_r)
 \le\frac{\log(M/m)}{\log(R/r)}.
\]

Cauchy's estimate gives

\[
 \sup_{D_r}\|C'\|\le\frac{M}{R-r}.
\]

If the real slice has \(Y\ge y_*>0\), then

\[
 \sum_{t_\beta\in D_r\cap\mathbb R}
 \kappa^{-6}\frac{\|C'(t_\beta)\|^2}{Y(t_\beta)}
 \le
 \frac{\kappa^{-6}M^2}{(R-r)^2y_*}
 \frac{\log(M/m)}{\log(R/r)}.
\]

This is a valid conditional summed-jet theorem.  Its radius, complex norm,
anchor, and enstrophy floor are not a Leray ledger and are not known to sum
over all shells.  R0.71U's real-variable second-jet theorem replaces the
complex anchor by an explicit time-derivative recurrence tax.

## 4. Exact method tests

The entire function

\[
 f_N(t)=N^{-1}\sin(Nt)
\]

has bounded variation and bounded \(L^2\) first derivative on a fixed
interval, but has \(O(N)\) zeros with \(|f_N'|=1\).  Its complex-strip norm
grows like \(e^{N\rho}/N\), exactly restoring the missing factor in Jensen.

The function

\[
 h(t)=t^{7/2}\sin(t^{-2}),\qquad h(0)=0,
\]

lies in \(C^1\cap W^{1,2}(0,1)\), has simple zeros
\(t_n=(n\pi)^{-1/2}\), and its squared slopes have a divergent sum.  This
shows why energy-class time regularity alone cannot define a uniform raw-zero
trace.  Neither scalar path is an NSE counterexample.

## 5. Weak-solution trace boundary

For a fixed smooth divergence-free packet \(\psi\), the weak equation gives
a Lipschitz or absolutely continuous coefficient \(\langle u,\psi\rangle\)
under the usual energy bounds, and positive-height excursions can be charged
to its variation.  The derivative exists only almost everywhere.  An
adaptively selected zero need not be a Lebesgue point of that derivative, and
the enstrophy denominator is also only an almost-everywhere quantity for a
general Leray--Hopf solution.  The normalized jet in R0.71U is therefore a
classical-event object.  Any weak-limit extension needs a separately defined
relaxed measure or canonical representative.

## 6. Search and stopping record

The focused queries covered:

- NSE temporal analyticity, Fourier-mode zeros, and no-sudden-creation;
- analytic zero counts, Jensen, Blaschke, and Carleson separation;
- Hilbert-valued curve zeros and parameter transversality;
- coarea, local time, Banach indicatrix, truncated variation, and upward
  crossings;
- 2D3C NSE, passive velocity components, exact shear classes, and Kelvin
  waves;
- Leray--Hopf packet traces and suitable-solution singular sets.

The search stopped after the second wave because new queries returned the
same four interfaces: conditional complex growth, level-averaged crossing,
upper Carleson mass, or probabilistic expected crossings.  No checked source
gave the deterministic normalized fixed-zero summed theorem or the arbitrary
prescribed-time 2D3C construction.  This conclusion is deliberately bounded.

The recurrence quantifier is finite and solution dependent: for each finite
prescribed time set and each (N), the construction may choose a new initial
datum and hence a new trajectory.  It does not produce one fixed trajectory
realizing an arbitrary infinite time set.  Uniformly bounded initial energy
and enstrophy show that raw counts are unbounded on that bounded class;
because the actual energy--enstrophy pair varies with (N), the construction
does not rule out every nonuniform function of that exact pair.
