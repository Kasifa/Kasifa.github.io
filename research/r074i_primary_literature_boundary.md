# R0.74I primary-literature boundary

**Date:** 2026-09-02
**Status:** **PASS for the bounded source-comparison boundary only**

This note records the post-audit literature boundary. It does not audit the
new estimates in R0.74I and does not establish novelty or priority.

## Direct conclusion

The suitable-weak local energy framework, fixed-cylinder interpolation, and a
velocity-only cubic one-scale epsilon gate are established. Mollified,
reference-time-anchored trajectories and skewed cylinders are also established.
In particular, Vasseur--Yang prescribe

\[
 \dot X(s)=u_\varepsilon(s,X(s)),\qquad X(t)=x,
\]

and use a one-sided backward skewed cylinder. Therefore terminal/reference-time
anchoring and backward skewness are prior art, not novelty-bearing features.

## Collision

The bounded primary-source screen found direct collisions at the component
level:

- [Caffarelli--Kohn--Nirenberg](https://doi.org/10.1002/cpa.3160350604) and
  [Lin](https://doi.org/10.1002/(SICI)1097-0312(199803)51:3%3C241::AID-CPA2%3E3.0.CO;2-A):
  suitable weak solutions, local energy inequality, and CKN compactness;
- [Guevara--Phuc](https://doi.org/10.1007/s00526-017-1151-7):
  fixed-cylinder kinetic/dissipation-to-cubic interpolation;
- [Wang--Wu--Zhou](https://doi.org/10.1016/j.jde.2019.05.003): Theorem 1.1
  with \(\delta=1/2\), giving the pressure-free cubic one-scale gate; and
- [Yang](https://doi.org/10.4171/AIHPC/20) and
  [Vasseur--Yang](https://doi.org/10.1007/s00205-021-01661-4): spatially
  mollified anchored flows, tubular/skewed cylinders, and a one-sided backward
  skewed-cylinder application to suitable solutions.

## Non-collision within the bounded screen

No checked primary source states the full R0.74I combination: the exact
solution-generated moving test and weak passage, frozen Version-M payment,
positive collar-flux estimate, moving-to-fixed containment with its constants,
and the resulting small-payment epsilon implication.

The logarithmic precedents also act on different observables:

- [Chan--Vasseur](https://doi.org/10.4310/maa.2007.v14.n2.a5) and
  [Montgomery-Smith](https://doi.org/10.1007/s10492-005-0032-0) weaken
  global-in-space regularity hypotheses by logarithmic denominators on a
  finite time interval;
- [Chemin](https://doi.org/10.3934/cam.2025038) places
  \(\sqrt{\log}\) in a comparison between
  \(N_T(u)\) and \(\|u\|_{L_t^\infty\dot B^{1/2}_{2,\infty}}\);
- [Ogawa--Taniuchi](https://doi.org/10.2748/tmj/1113246381) obtain exponent
  \(1/\nu-1/\rho\), equal to \(1/2\) for \((\nu,\rho)=(1,2)\), in a
  global Besov/Orlicz vorticity uniqueness mechanism;
- [Lei--Ren](https://doi.org/10.1016/j.aim.2024.109654) use a logarithmic
  multiscale singular-set gauge; and
- [Tao](https://doi.org/10.1090/pspum/104/01874) uses iterated logarithms in
  quantitative critical-norm and possible-blow-up estimates.

None supplies the local scalar-payment estimate

\[
 Y_R\lesssim P_R^{2/3}\sqrt{1+\log_+P_R},
 \qquad Y_R\in\{X_R,\mathfrak C_R\}.
\]

## Finite non-hit

The search covered suitable-weak local energy, fixed-cylinder epsilon
regularity, mollified-flow skewed cylinders, logarithmically improved Serrin
criteria, critical Besov/Orlicz interpolation, quantitative critical
\(L_t^\infty L_x^3\) bounds, and logarithmic CKN gauge refinements. It stopped
when these mechanisms repeated without producing the same observable-level
theorem.

This is a **finite non-hit only**. It is not evidence of novelty, priority, an
endpoint upper estimate, smallness at a possible singular point, or global
regularity.

The full source ledger is in `r074i_report-source.md`. The independent audit is
preserved as the immutable pre-repair snapshot
`r074i_primary_literature_independent_audit.md`.

**NOT CLAY.**
