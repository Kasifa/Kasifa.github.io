# R0.73V exact signed-third-order heat-lift certificate

This package checks the finite Fourier algebra used by R0.73V.  It uses
normalized Haar probability measure on
\(\mathbb T^3=[0,2\pi]^3\), Fourier convention

\[
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,d\mu(x),
 \qquad q=e^{-s},
\]

and heat multiplier \(q^{|k|^2}\).  Every coefficient is computed as a
finite polynomial in \(q\) over exact Gaussian rationals.  The scripts use
only `fractions.Fraction` and the Python standard library.  Floating point,
third-party packages, network access, GPU, and DGX are not used.

## Two independent producers

`compute_exact_certificate.py` uses sparse exponent-to-coefficient
dictionaries and writes `results.json`.  `independent_recompute.py` does not
import the primary producer; it uses dense trimmed polynomial tuples and
writes `independent-results.json`.  Both rebuild the full sparse
\(\kappa,Q,\Xi=2R\) tables and the locked target rows.  `seal_package.py`
requires their complete `commonCore` objects to be byte-identical and binds
the canonical complete-table digest.

`audit-checklist.json` fixes 66 public expectations.  `contract.json` fixes
the mathematical interface independently of the generated output.  Both JSON
parsers used for the seal reject duplicate keys.

## Four-site Germano rows

For

\[
 u=(2\sin(x+y),\ 2\sin x-2\sin(x+y),\ 0)
\]

and \(h_*=(1,2,0)\), the package constructs the complete generalized heat
cumulants

\[
 \kappa_{ijk}=\tau_s(u_i,u_j,u_k),\quad
 Q_i=\tau_s(p,u_i),\quad
 \Xi_{ij}=2\tau_s(p,S_{ij}).
\]

It then certifies, component by component,

\[
 -i h_{*,k}\widehat\kappa_{ijk}(h_*)
 =q^3(1-q^2)^2(q^2+2)
 \begin{pmatrix}2&-3&0\\-3&4&0\\0&0&0\end{pmatrix},
\]

\[
 -i h_{*,i}\widehat Q_j(h_*)-i h_{*,j}\widehat Q_i(h_*)
 =q^3(1-q^2)
 \begin{pmatrix}4&2&0\\2&-8&0\\0&0&0\end{pmatrix},
\]

\[
 \widehat\Xi(h_*)=q^3(1-q^2)
 \begin{pmatrix}-4&0&0\\0&4&0\\0&0&0\end{pmatrix}.
\]

Thus the local \(\kappa\)-flux vanishes to order \(s^2\), while the two
pressure rows generally vanish only to order \(s\).  `results.json` preserves
every nonzero coefficient of the full \(\kappa,Q,\Xi\) tables, not only these
contracted target rows.

## Compressed lift is a separate object

Let \(N=\mathbb P\nabla\!\cdot(u\otimes u)\),
\(\mathcal C_s=P_s(u\odot N)\), and

\[
 \chi_s=\mathcal C_s-v_s\odot N_s.
\]

This `chi` is not the Germano signed-stress source.  With

\[
 K=\begin{pmatrix}-2&1&0\\1&0&0\\0&0&0\end{pmatrix},
\]

the exact target coefficients are

\[
 \widehat{\mathcal C_s}(h_*)=-q^5K,\qquad
 \widehat{v_s\odot N_s}(h_*)=-q^3K,\qquad
 \widehat\chi_s(h_*)=(q^3-q^5)K.
\]

The sign-pair difference is twice the last coefficient.  Under
\(u_L(x)=u(Lx)\) and \(s=\theta L^{-2}\), its Frobenius norm is

\[
 2\sqrt6\,L(e^{-3\theta}-e^{-5\theta}).
\]

## Six-site zero-mode pressure witness

For the R0.73T field

\[
 u=(6\sin y-4\sin(x+y),\ 4\sin x+4\sin(x+y),\ 0),
\]

the zero-mode contractions of the \(\kappa\)-flux and \(Q\)-divergence
vanish.  The pressure-strain row does not:

\[
 \widehat\Xi(0)=(1-q^4)\operatorname{diag}(-48,48,0).
\]

The independent mode grouping checks that the \(|m|^2=1\) contributions
cancel exactly and that the complete coefficient comes from \(|m|^2=2\).
This is a same-output-coefficient witness.  It is not an equality-state or
whole-field information-theoretic non-recovery theorem.

## Selected fourth-order ascent

Differentiate \(\kappa_{112}\) in the inviscid Navier--Stokes direction
\(\dot u=-N\).  For the four-site field, the selected coefficient at
\(h=(0,2,0)\) is

\[
 2i q^2(1-q^2)^2.
\]

At \(q=1/2\), the scripts also form the exact finite perturbations
\(u-\varepsilon N\) for \(\varepsilon=0,1,2,3\) and extract the linear
coefficient with the exact cubic interpolation formula.  The result is
\(9i/32\), independently confirming the selected polynomial value.

## Reproduction and seal

From the repository root, execute the first six commands in `command.txt`.
The expected primary and independent lines begin with
`R073V_EXACT_CERTIFICATE=PASS` and
`R073V_INDEPENDENT_RECOMPUTE=PASS`.  The first seal is intentionally
`hash-bound-uncommitted`.  After all eight source files are committed, use
the two final commands with the full immutable source commit.  The final seal
uses `git cat-file blob` and fails if any committed source byte differs.

## Claim boundary

The package certifies finite Fourier \(q\)-polynomials, parity and dilation
flags, one coefficientwise pressure witness, and one selected fourth-order
tangent.  It does not prove componentwise or information-theoretic minimality,
finite-order PDE closure, control of the pressure-strain row, generic
Navier--Stokes integration, singularity, arbitrary-data global regularity, or
the Clay Millennium conclusion.  `NOT CLAY`.
