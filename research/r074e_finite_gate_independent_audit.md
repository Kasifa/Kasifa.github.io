# R0.74E finite-gate independent audit

## Result and scope

I independently recomputed the claims in Sections 7--9 of the current
R0.74E note and the accompanying exact-arithmetic certificate.  The result
is **PASS** for the claims that the note labels as proved: the single-mode
perturbative rejection, the midpoint sufficient-window rejection, the
outer-annulus finite rational gate, the odd-symmetry cancellation, and the
exact contrast calibration.

This result is deliberately narrower than a positive endpoint theorem.  It
does not prove passive-packet survival, close the complete
\(E/G_u/G_p/H_u\) payment ledger, or produce an amplitude that makes the
Version-M/F ratio diverge.

## Audited snapshot

The audit used these files as authority.  Their SHA-256 digests were
recomputed immediately before the audit record was written.

| File | SHA-256 |
|---|---|
| `research/r074e_local_mollified_frame_gate.md` | `3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7` |
| `scripts/r074e_outer_annulus_exponent_certificate.py` | `eece8145a024b7d6b22829f9c197f4f74e20e697b9ae74d8721325d1ee07b59b` |
| `research/r074e_outer_annulus_exponent_certificate.json` | `c6b7f0b9d11a58568c588dd3116e66fbdb9d7d5b5383493c9b492bf6cdba4372` |
| `research/r074e_outer_annulus_exponent_certificate_report.md` | `3bb32d68d879682199c3b7673ce6ee403ef7421faf2015744dc4a11ccc565c6e` |

The main-note digest includes the contemporaneous Section 4 support
bookkeeping, the non-strict support inclusion in (4.12c), and the clarified
quantifier on nonautomatic cancellation after (4.10).  The mathematical
scope checked here remains Sections 7--9.

## Independent method

The rational identities below were recomputed directly with integer
numerators and denominators, without importing values from the certificate
program.  I then ran the certificate producer and compared its complete
standard output byte-for-byte with the frozen JSON.  Finally, I checked the
signs in the passive equation by direct differentiation and checked the
terminal ODE by uniqueness, rather than inferring either fact from the
certificate.

The reproduction commands were:

```bash
shasum -a 256 \
  research/r074e_local_mollified_frame_gate.md \
  scripts/r074e_outer_annulus_exponent_certificate.py \
  research/r074e_outer_annulus_exponent_certificate.json \
  research/r074e_outer_annulus_exponent_certificate_report.md

python3 scripts/r074e_outer_annulus_exponent_certificate.py \
  | cmp - research/r074e_outer_annulus_exponent_certificate.json

git diff --check -- research/r074e_finite_gate_independent_audit.md
```

The byte comparison and `git diff --check` both returned exit status zero.
The generated object and the frozen JSON are therefore identical, not merely
numerically equivalent.  The JSON reports `passed = 13`, `total = 13`, and
`status = PASS`.

## Section 7: exact Fourier sequence and limited rejection

For integer \(k_m\to\infty\), the definitions

\[
 R_m=\frac{4}{M_mk_m},\qquad
 h_m=\frac{2}{k_m}=\frac{M_mR_m}{2},\qquad
 k_mR_m=\frac{4}{M_m}
\]

are mutually consistent.  With

\[
 k_m=\left\lceil\frac{4e^{M_m^2/96}}{M_m}\right\rceil,
\]

the quantity inside the ceiling tends to infinity, so

\[
 \frac{R_m}{e^{-M_m^2/96}}
 =\frac{4e^{M_m^2/96}/M_m}{k_m}\longrightarrow1.
\]

Thus the construction uses an exact integer torus mode while retaining the
stated exponential scale.

For \(B\asymp R^{-2}\) and \(kh=2\), the packet-scale linear shear is

\[
 |B|kR^2|\sin(kh)|\asymp k
 =\frac{4}{M_mR_m}\longrightarrow\infty.
\]

A transverse Brownian displacement of size \(R\) consequently creates a
horizontal displacement

\[
 |B|kR^3\asymp kR=\frac4{M_m},
\]

which is much larger than both \(R_m\) and \(M_mR_m\) on this sequence.  At
the negative extremum, \(kh=\pi\) and
\(R=2\pi/(M_mk_m)\).  The first nonzero coefficient is then

\[
 |B|k^2R^3\asymp k^2R
 =4\pi^2\frac1{M_m^2R_m}\longrightarrow\infty.
\]

These calculations reject treatment of this particular Fourier shear as a
uniformly controlled scale-\(R\) perturbation.  They do not reject every
possible nonperturbative single-mode construction.

## Section 8: exact plateau family and midpoint no-window

The two translated bump terms in

\[
 g_{R,m}(x_3)
 =\eta(x_3/\delta)-\eta((x_3-h)/\delta),\qquad
 h=\frac{M_mR}{2},\quad \delta=\frac{M_mR}{16},
\]

have equal integrals and disjoint supports.  The prescribed periodization is
smooth, and equality of the integrals makes its mean zero.  Since the plateau half-width is
\(\delta/2=M_mR/32\ge2R\) for \(M_m\ge64\), while the fixed mollifier is
supported at scale \(R\), the two convolution values at time zero are
exactly \(+1\) at \(0\) and \(-1\) at \(h\).

For the formal target
\(A^2M_mR^2e^{-M_m^2/288}\) and the packet cubic row
\(A^3R^4/M_m^2\), taking the latter to the \(2/3\) power leaves the
exponential comparison

\[
 e^{-M_m^2/288}R^{-2/3}
 =\exp\!\left[
   \left(\frac{2c_R}{3}-\frac1{288}\right)M_m^2
 \right].
\]

Therefore target dominance by this route requires

\[
 c_R>\frac{3}{2}\frac1{288}=\frac1{192}.
\]

The nearest plateau edge is only
\(d=M_mR/32\) away.  Over \(65R^2\), the direct heat-kernel exponent is

\[
 \frac{d^2}{4(65R^2)}
 =\frac{M_m^2}{266240}.
\]

Requiring the resulting order-\(B\) displacement to be smaller than one
packet width \(R=e^{-c_RM_m^2}\) gives the opposite sufficient condition

\[
 c_R<\frac1{266240}.
\]

Because \(1/192>1/266240\), this direct midpoint perturbative window is
empty.  This is a rejection of that sufficient mechanism only.  The exact
2D3C family itself remains valid, and the calculation is not a universal
no-go for signed caloric cancellation or other plateau geometries.

## Section 9: independent finite rational calculation

The frozen values are

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta^2=\frac{31}{256},\qquad
 c_R=\frac1{320},\qquad
 \kappa=16.
\]

First,

\[
 1<\lambda<2,
 \qquad
 c_h^2+\beta^2=\frac{225+31}{256}=1.
\]

Thus \(r_j=L_jR_j\), with \(L_j=\lambda2^j\), lies strictly inside the
selected dyadic annulus, and \(|(q_j,h_j)|=r_j\).  The annular exponent is

\[
 c_\gamma=\frac1{128\lambda^2}
 =\frac1{128(3969/1024)}=\frac8{3969}.
\]

The formal packet-\(G_u\) lower threshold is

\[
 \frac32c_\gamma=\frac4{1323}.
\]

Indeed, the exponential part of the target-to-\(G_u^{2/3}\) comparison is
\(\gamma_jR_j^{-2/3}\), so its coefficient is positive precisely when
\(c_R>(3/2)c_\gamma\).  Direct caloric isolation at distance
\(\alpha r_j\) requires \(c_R<\alpha^2/260\).  The chosen value has the
strict exact window

\[
 \frac4{1323}<\frac1{320}<\frac{49}{14625},
\]

with margins

\[
 \frac1{320}-\frac4{1323}=\frac{43}{423360}>0,
\qquad
 \frac{49}{14625}-\frac1{320}=\frac{211}{936000}>0.
\]

The buffered local-leakage exponent beats both the inverse-\(R_j\)
prefactor and the annular weight:

\[
 \frac{c_h^2}{264}-c_R
 =\frac{75}{22528}-\frac1{320}
 =\frac{23}{112640}>0,
\]

\[
 \frac{c_h^2}{264}-c_\gamma
 =\frac{75}{22528}-\frac8{3969}
 =\frac{117451}{89413632}>0.
\]

The transition-window equivalence and its margin are

\[
 \alpha^2-\frac{780}{256\lambda^2}
 =\frac{196}{225}-\frac{1040}{1323}
 =\frac{2812}{33075}>0.
\]

Finally,

\[
 c_h-\alpha=\frac1{240},\qquad
 7680(c_h-\alpha)=32=2\kappa.
\]

This last identity binds the text's \(\kappa=16\) to the certified finite
separation reserve.  The checked right-hand side is computed as \(2\kappa\),
rather than supplied as an independent numeric constant.

### The thirteen exact checks

| Check | Independent recomputation | Result |
|---|---|---|
| Lower annulus edge | \(63/32-1=31/32\) | PASS |
| Outer annulus edge | \(2-63/32=1/32\) | PASS |
| Radial split | \(225/256+31/256=1\) | PASS |
| Annular coefficient | \((128\lambda^2)^{-1}=8/3969\) | PASS |
| Packet-\(G_u\) threshold | \((3/2)(8/3969)=4/1323\) | PASS |
| Window lower margin | \(1/320-4/1323=43/423360\) | PASS |
| Window upper margin | \(49/14625-1/320=211/936000\) | PASS |
| Leakage versus inverse \(R_j\) | \(75/22528-1/320=23/112640\) | PASS |
| Local-leakage margin | \(75/22528-8/3969=117451/89413632\) | PASS |
| Transition-window margin | \(196/225-1040/1323=2812/33075\) | PASS |
| Buffer gap | \(15/16-14/15=1/240\) | PASS |
| Finite separation | \(7680/240=32=2(16)\) | PASS |
| Midpoint incompatibility | \(1/192-1/266240=4157/798720>0\) | PASS |

The independently recomputed values agree with all thirteen JSON checks.  In
addition, the producer output is byte-identical to that JSON.  The report's
displayed window, strict margins, separation reserve, and stated analytic
boundary agree with the producer and JSON.

## Exact 2D3C reduction and mean-zero conditions

Write \(x=x_2\), \(z=x_3\), and let

\[
 b_t=b_{zz},\qquad
 F_t+bF_x=F_{xx}+F_{zz}.
\]

For any constant amplitude \(\mathfrak a\), set

\[
 u=(\mathfrak a F,b,0),\qquad p=0.
\]

Then \(\nabla\cdot u=0\), because \(F\) is independent of \(x_1\) and
\(b\) is independent of \(x_2\).  Direct substitution gives

\[
 \partial_tu-\Delta u+(u\cdot\nabla)u+\nabla p
 =\bigl(
   \mathfrak a(F_t-\Delta_{23}F+bF_x),
   b_t-b_{zz},0
  \bigr)=0.
\]

The odd shear has zero mean.  Each initial passive packet contains a
periodic heat-kernel derivative in \(x_2\), so its global integral is zero;
the divergence-free passive equation preserves this integral.  Thus the
field in (9.13) is exact smooth periodic unforced mean-zero NSE.

## Odd inversion symmetry and terminal ODE cancellation

The saturation profile is odd because both \(\sigma\) and \(\sin x_3\)
are odd.  Periodic heat evolution preserves oddness, so

\[
 b_j(t,-z)=-b_j(t,z).
\]

The periodic heat kernel is even and its derivative is odd.  Under
\((x,z)\mapsto(-x,-z)\), the two terms in the paired initial datum exchange
and each acquires a minus sign.  Hence

\[
 F_j(0,-x,-z)=-F_j(0,x,z).
\]

This symmetry has the correct PDE sign.  Define

\[
 H(t,x,z)=-F_j(t,-x,-z).
\]

Then

\[
 H_t=-F_t(-x,-z),\quad
 H_x=F_x(-x,-z),\quad
 \Delta H=-\Delta F(-x,-z).
\]

Using \(b_j(z)=-b_j(-z)\),

\[
 H_t+b_j(z)H_x-\Delta H
 =-\bigl(F_t+b_j(-z)F_x-\Delta F\bigr)(-x,-z)=0.
\]

Uniqueness for the smooth linear parabolic equation therefore preserves the
paired oddness.  An even radial periodic mollifier is invariant under
\((y_2,y_3)\mapsto(-y_2,-y_3)\), so the paired integrands cancel exactly:

\[
 (\varphi_{R_j}^{\rm per}*F_j)(t,0)=0,
 \qquad
 (\varphi_{R_j}^{\rm per}*b_j)(t,0)=0.
\]

Consequently \(u_{j,R_j}(t,0)=0\).  The constant curve \(X(t)=0\) solves
the terminal problem

\[
 \dot X(t)=u_{j,R_j}(t,X(t)),\qquad X(t_{0,j})=0.
\]

The mollified field is smooth and hence locally Lipschitz.  Uniqueness of
the terminal ODE, equivalently uniqueness after reversing time, gives

\[
 X_{R_j}(t)\equiv0,
 \qquad a_{R_j}(t)=a_{R_j}'(t)=0.
\]

Thus Versions M and F coincide for this family and all acceleration rows
vanish exactly.  This cancellation does not estimate any of the remaining
packet or exterior rows.

## Exact contrast calibration

For sufficiently large \(j\),

\[
 \arcsin(\kappa R_j)\le2\kappa R_j=32R_j.
\]

Since \(h_j=c_hL_jR_j\), \(r_j=L_jR_j\), and
\(c_h-\alpha=1/240\), the condition \(L_j\ge7680\) gives

\[
 \operatorname{dist}_{\mathbb T}
   (h_j,\{g_j\ne1\})
 \ge(c_hL_j-32)R_j
 \ge\alpha r_j.
\]

The transition at the torus seam is farther away.  At \(t=0\),
\(\theta_j(0,h_j)=1\).  For \(0<t\le65R_j^2\), the periodic heat-kernel
tail and \(-1\le g_j\le1\) give

\[
 0\le1-\theta_j(t,h_j)
 \le C\exp\!\left[-\frac{\alpha^2r_j^2}{4t}\right]
 \le Ce^{-\alpha^2L_j^2/260}.
\]

It follows that

\[
 64R_j^2(1-o(1))\le
 \mathfrak D_j
 =\int_{R_j^2}^{65R_j^2}\theta_j(t,h_j)\,dt
 \le64R_j^2.
\]

Since \(q_j\to0\) and \(q_*=1/2\),

\[
 B_j=\frac{q_j+q_*}{\mathfrak D_j}>0,
 \qquad B_j\asymp R_j^{-2}.
\]

The signs and endpoints follow by direct substitution.  With

\[
 q_{{\rm pre},j}
 =-q_*-B_j\int_0^{R_j^2}\theta_j(t,h_j)\,dt,
\]

the positive-layer reference path satisfies

\[
 Q_j(R_j^2)=-q_*,
\]

and

\[
 Q_j(65R_j^2)
 =-q_*+B_j\mathfrak D_j
 =-q_*+(q_j+q_*)=q_j.
\]

At the inverted layer, oddness gives
\(\theta_j(t,-h_j)=-\theta_j(t,h_j)\), while the paired entrance point is
\(-q_{{\rm pre},j}\).  Its reference path is therefore exactly
\(-Q_j(t)\).  In particular, the positive layer travels from \(-q_*\) to
\(+q_j\); the inverted layer travels from \(+q_*\) to \(-q_j\).  There is
no hidden sign reversal in the calibration.

## What this audit does not prove

The following gates remain **OPEN**:

1. a two-packet Feynman--Kac survival lemma uniform in \(j\);
2. buffered local leakage from the strict finite exponent margin;
3. all transition, packet, mixed-pressure, and periodic-copy contributions
   in the complete \(E/G_u/G_p/H_u\) ledger;
4. a choice of \(\mathfrak a_j\) that closes the simultaneous Version-M/F
   ratio;
5. any endpoint divergence or positive absorption theorem.

The midpoint calculation rejects one direct perturbative sufficient
mechanism.  The outer-annulus calculation proves one finite compatibility
gate.  Neither calculation is a packet-survival theorem or a universal
transport obstruction.  No epsilon-regularity criterion, continuation
theorem, global regularity theorem, or Navier--Stokes Millennium Prize
solution follows.  **NOT CLAY.**
