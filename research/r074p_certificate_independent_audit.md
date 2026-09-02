# R0.74P finite certificate — independent reconstruction audit

## Verdict

**PASS.**  The independent Ruby implementation reconstructed all 52 finite
checks, and the Python producer reproduced the frozen JSON byte for byte.

This audit is finite only.  It does not certify the local-energy identity,
the BV ledgers, any infinite-shell passage, regularity, novelty, or a Clay
conclusion.

## Execution evidence

- Frozen JSON SHA-256:
  `c65b38def48b5439f112ab145360c1abb211de5bf6f004eca103271d8d9a204b`.
- Python producer versus frozen JSON: byte-identical.
- Independent Ruby result: `PASS (52/52 checks)`.
- JSON structure: 52 checks with 52 unique identifiers, all `pass=true`;
  four scale rows, seven sampled Carleson rows, and six finite
  \(\ell^1/\ell^2\) rows.

## Independent exact arithmetic

The reserve exponent was recomputed as

\[
 m=\frac1{320}-\frac32\frac8{3969}
  =\frac{43}{423360}>0.
\]

Hence

\[
 \frac m3=\frac{43}{1270080},
 \qquad
 \frac{2m}{3}=\frac{43}{635040},
\]

and

\[
 K_*=L^{7/3}\exp\!\left(\frac{43}{635040}L^2\right).
\]

The target weight was independently checked:

\[
 c_\gamma L_j^2
 =\frac8{3969}\frac{3969}{1024}4^j
 =\frac{4^{j-1}}{32},
\]

so \(\Gamma=e^{-c_\gamma L^2}\) and

\[
 \Gamma^{-1/2}=\exp\!\left(\frac4{3969}L^2\right).
\]

The normalized strong-clock penalty is therefore

\[
 \frac{4/3969}{43/635040}=\frac{640}{43}.
\]

The seven sampled window rows agree with
\(\beta(\sigma)=\min\{\sigma,1\}\).  The finite equal-entry rows at
\(N=4,16,64,256,1024,4096\) agree with

\[
 \|v\|_1=N,
 \qquad
 \|v\|_2=\sqrt N,
 \qquad
\frac{\|v\|_1}{\|v\|_2}=\sqrt N.
\]

For the three sampled orders \(\sigma>1\), the branch is frozen as
`right-endpoint-supremum`: because \(J\Subset I_R\), one has (x<1), and
the value (K_*^{-1}) is approached as \(x\uparrow1\) rather than attained
at a permitted endpoint.

## Boundary

The sampled \(\sigma\) values are reproducibility checks, not a proof of
the continuum maximization; that proof is analytic in Theorem 4.2.  The
finite equal-entry sequences expose the abstract sequence obstruction but
do not prove or disprove a Navier--Stokes effective-shell theorem.

**FINITE ONLY. NOT CLAY.**
