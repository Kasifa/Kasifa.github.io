**Figure R0.73F — Fixed-window finite propagation diagnostics and two exact cautionary examples.**
(A) For the declared finite Fourier compression (N=96) and the diagnostic
endpoint (d_{\rm diag}=0.01), the full propagator norm and the conorm of the
finite transported top block are reported as
\((\varepsilon/d_{\rm diag})\log\|U_\varepsilon\|\) and
\((\varepsilon/d_{\rm diag})\log m(U_\varepsilon|_{E_{\rm top}})\).  The
horizontal line (0.17035) is an analytic reference entering the frozen
(d=0) argument, not a numerical fit and not a certified moving rate.
(B) Finest-pair step-halving discrepancies, adjacent-cutoff (48/96)
discrepancies, and an independently coded explicit-Fourier reconstruction are
shown in the same normalized-rate units; values below (10^{-17}) are plotted
at that display floor.  Adjacent-cutoff agreement is not a tail bound.
(C) The exact matrices (D_n=[[-n,n^2],[0,-n]]) satisfy
\(\exp(D_n/n)=e^{-1}[[1,n],[0,1]]\) and hence
\(\|\exp(D_n/n)\|\ge n/e\), despite spectrum \(\{-n\}\).
(D) Three exact rotating branches have pointwise maximum at least (1/4),
while every branch integrates to (-1/4) over one cycle.  This shows that
pointwise eigenvalue selection does not determine a transported growth
direction.

All quantities in A--B are finite, sampled, IEEE-754 binary64 diagnostics.
The choice (d_{\rm diag}=0.01) is explicitly **not** the analytic (d_0).
The figure proves no continuum spectral/resolvent/evolution estimate, no
nonlinear Navier--Stokes result, and no Clay Millennium statement.  The exact
examples in C--D are abstract counterexamples and do not describe the exact
Fourier row.
