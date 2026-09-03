# R0.75F finite certificate report

- Verdict: **PASS**
- Assertions: 16/16
- Main SHA-256: f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440
- Fixture SHA-256: 0ce9b3bf060f4b38fe497be7bcdad3d1bdbd51ea27ff9aab146c8b10f5a0aced
- Expected SHA-256: 3946cb2cc992f4d1e55b88a7be9b7ecd8529e76a437093af6583f8fdacf2ddc9
- Failed checks: none

The rational complex fixture verifies both modal equations, the product rule, ell=m-n, and F.8 without division by b or ell. The closed two-mode solution is then integrated independently in Q[p], p=pi^-2: transport comes directly from i*ell*b*g, both integration-by-parts identities are checked separately, and F.12, F.17, and F.18 have zero residual. The additional arbitrary moment fixture checks pi/2pi row normalization.

For N=3,5,7 the producer enumerates every ordered difference pair, recomputes the fourth moment and normalized means, and obtains ratios 19/9, 17/5, and 33/7. This rules out only the positivity-only uniform diagonal comparison. It is not a frozen-collar counterexample. E.24, complete clock, fixed deletion, suitable-weak transfer, and regularity remain OPEN. **NOT CLAY.**
