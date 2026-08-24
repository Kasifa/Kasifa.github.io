# R0.70R exact certificate

This directory locks the finite exact payload for the near-rank diffusion
jet gate.

The curvature convention is the canonical report convention

\[
 \mathcal K_Q=
 \sum_{k,b>1}
 \frac{|v_b^{\mathsf T}(\partial_kQ)v_1|^2}
      {\lambda_1-\lambda_b}.
\]

Thus \(\mathcal K_Q\) is the half-curvature, not the variable
\(K=2\mathcal K_Q\) used inside the R0.70Q exact certificate.

At a point, put

\[
 a_\alpha=v_1\cdot\Omega_\alpha,
 \quad b_\alpha=P\Omega_\alpha,
 \quad c_{\alpha k}=v_1\cdot\partial_k\Omega_\alpha,
 \quad h_{\alpha k}=P\partial_k\Omega_\alpha,
\]

and

\[
 D=\sum_{\alpha,k}|h_{\alpha k}|^2,
 \qquad C=\sum_{\alpha,k}|c_{\alpha k}|^2.
\]

The producer verifies four groups.

1. The exact off-diagonal identity

   \[
   y_k:=P(\partial_kQ)v_1
   =\sum_\alpha(a_\alpha h_{\alpha k}
                    +c_{\alpha k}b_\alpha)
   \]

   is combined with finite-dimensional Cauchy, the operator norm
   \(\|\{d_\alpha\}\mapsto\sum b_\alpha d_\alpha\|=\sqrt{\lambda_2}\),
   direct-sum Minkowski, and the reduced-resolvent norm. Under
   \(\lambda_1>\lambda_2\ge\lambda_3\ge0\), this gives

   \[
   \boxed{
   \mathcal K_Q\le
   \frac{(\sqrt{\lambda_1}\sqrt D+
           \sqrt{\lambda_2}\sqrt C)^2}
        {\lambda_1-\lambda_2}.}
   \]

   The finite producer records the Cauchy, synthesis-operator, Gram
   sum-of-squares, and denominator slacks separately.
2. For \(\rho=\lambda_2/\lambda_1\) and

   \[
   c(\rho)=\frac{\sqrt\rho}{1-\sqrt\rho},
   \]

   setting \(A=\sqrt{\lambda_1}\),
   \(B=\sqrt{\lambda_2}\), \(p=\sqrt D\), and \(q=\sqrt C\) gives the exact
   square slack

   \[
   D+c(\rho)(D+C)
   -\frac{(Ap+Bq)^2}{A^2-B^2}
   =\frac{AB(p-q)^2}{A^2-B^2}\ge0.
   \]

   Consequently

   \[
   \boxed{D-\mathcal K_Q\ge-c(\rho)(D+C).}
   \]
3. The two-block, one-derivative jet

   \[
   \Omega_1=3e_1,\qquad \Omega_2=e_2,\\
   \partial\Omega_1=2e_2,\qquad \partial\Omega_2=2e_1
   \]

   has \(Q=\operatorname{diag}(9,1,0)\), \(D=C=4\),
   \(\mathcal K_Q=8\), \(\rho=1/9\), and \(c(\rho)=1/2\). Hence

   \[
   D-\mathcal K_Q=-4=-c(\rho)(D+C),
   \]

   so the coefficient is attained in covariance-jet algebra.
4. The same jet is realized at \(x_1=0\) by the smooth periodic vorticity

   \[
   \omega_0=A\cos(kx_1)v+\frac pk\sin(kx_1)w
   +B\cos(\ell x_1)w+\frac q\ell\sin(\ell x_1)v,
   \]

   with \(v=e_2\), \(w=e_3\). The producer constructs an explicit smooth
   divergence-free velocity whose curl is \(\omega_0\). It also checks two
   disjoint active scalar tight-frame index groups, each with coefficient
   square sum one. For \(p=q\), the exact deficit ratio is sharp. The rational
   instance uses \((A,B,p,q,k,\ell)=(3,1,2,2,2,32)\).

Run the command in `command.txt` from the repository root. The regenerated
file must be byte-identical to `result.json` before checking `SHA256SUMS`.

## Scope boundary

This is a finite pointwise covariance-jet certificate. The displayed torus
field is a smooth divergence-free vorticity and is the curl of a smooth
divergence-free velocity, so it is a valid smooth Navier--Stokes initial
datum. The tight-frame ledger is conditional on the two Fourier pairs having
disjoint active scalar LP index sets.

The certificate does not prove that a single Navier--Stokes/LP evolution
preserves the sharp jet relation, does not close the covariance PDE, and does
not prove a continuation criterion, finite-time blow-up, global smoothness,
or the Millennium problem.
