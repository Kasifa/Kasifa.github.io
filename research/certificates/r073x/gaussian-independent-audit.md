# R0.73X Gaussian velocity-tail independent audit

**Audit date:** 2026-09-01

**Role:** independent analytic and certificate audit; no source theorem or
certificate file was edited

**Initial verdict:** `ANALYTIC PASS / CERTIFICATE COVERAGE FAIL`;
superseded by the dated re-audit in Section 5

The displayed Gaussian velocity-tail estimate is mathematically valid with
the constants and normalizations currently stated. The translated packet
also gives the claimed functional obstruction, with the quantifier boundary
recorded below. The initially audited Python program ran successfully and its scalar
rows are numerically consistent, but it does **not** independently check all
the items its header claims: annular geometry is absent and the packet powers
were entered as literals. It therefore could not yet serve as the complete
second producer for those rows.

NOT CLAY.

## 1. Audited inputs and reproduction

The audit was performed against these exact input digests:

```text
904bd5618fb780d14a4ddfe491f4910cd47bb45b0b6575e9207049dc48b61682  research/r073x_gaussian_velocity_tail_proof.md
3dbfa0e712b740cccb4891dfa84255342f798ad8b331e6d20433df426aec7c6d  scripts/r073x_gaussian_tail_certificate.py
bdb09c09c11a26bfa44901ef3fc53782e56905ad085d06d38a83df1977e5b6fb  research/r073x_exterior_tail_counterexample_audit.md
```

Both the bundled and system Python runtimes returned the same result from

```bash
python3 scripts/r073x_gaussian_tail_certificate.py --check-only
```

namely

```text
R073X_GAUSSIAN_KERNEL=PASS
R073X_SCALE_INTEGRAL=PASS
R073X_SCALING=PASS
R073X_PACKET_L2_TAIL=REFUTED_FUNCTIONALLY
R073X_PDE_REGULARITY=OPEN
R073X_CLAY=OPEN
R073X_PAYLOAD_SHA256=13e75c5777c6b686f12fd9c375abc6855d25d09db50d9aee964ae651a2b994f5
```

Removing the `payload_sha256` field from the stored JSON and hashing its
canonical serialization reproduces that payload digest exactly. The largest
reported relative quadrature error is
\(3.066793995953942\times10^{-14}\).

## 2. PASS/FAIL ledger

| Row | Verdict | Independent check |
|---|---|---|
| Factor \(1/(4s)\) and cubic split | **PASS** | From \(|a-b|^3\le4(|a|^3+|b|^3)\), the factor \(4\) exactly cancels the denominator \(4\); there is no missing factor. |
| Gaussian kernel ratio | **PASS** | \(\big((|y|/s)g_s\big)/(s^{-1/2}g_{2s})=2^{3/2}q e^{-q^2/8}\). Its derivative has the sign of \(1-q^2/4\), so the global maximum is at \(q=2\) and equals \(2^{5/2}e^{-1/2}\). |
| Centering/Jensen constant | **PASS** | \(\int|y|g_s=4\sqrt{s}/\sqrt\pi\), \(|P_su|^3\le P_s|u|^3\), and \(g_s\le2^{3/2}g_{2s}\). Thus the second constant is \(2^{7/2}/\sqrt\pi\), and \(C_0=9.8141320262657512<10\). |
| Annular distance | **PASS** | For \(x\in B_R\), \(z\in A_m\), \(m\ge1\), \(|x-z|\ge(2^m-1)R\ge2^{m-1}R\), since \(2^m-1-2^{m-1}=2^{m-1}-1\ge0\). |
| Heat-ball coefficient | **PASS** | Multiplying \(\sup_{B_R}g_{2s}(x-z)\) by \(|B_R|=4\pi R^3/3\) gives \((4\pi/3)(8\pi)^{-3/2}=1/(12\sqrt{2\pi})\), exactly (3.2). |
| Scale integral | **PASS** | With \(a=4^mR^2/32\), \(r=a/s\) gives \(\int_0^{\theta R^2}s^{-2}e^{-a/s}ds=a^{-1}e^{-a/(\theta R^2)}\), hence \(32(4^mR^2)^{-1}e^{-4^m/(32\theta)}\). |
| Assembly of (1.7) | **PASS** | The core coefficient is \(2C_0\sqrt\theta R^{-2}=8C_0\sqrt\theta(2R)^{-2}\). The annular coefficient is \(32/(12\sqrt{2\pi})=8/(3\sqrt{2\pi})\), and \(4^{-m}R^{-2}=(2^mR)^{-2}\). |
| Navier--Stokes scaling | **PASS** | Under \(u_\lambda=\lambda u(\lambda^2t,\lambda x)\), \(s\mapsto\lambda^{-2}s\), \(R\mapsto\lambda^{-1}R\), and \(\mathscr S\mapsto\lambda^4\mathscr S\). Both sides of (1.7), every core/annular row, and \(\mathcal E\) have degree zero; \(\nu\) is unchanged. On a torus this is local/dimensional rescaling or rescaling between periods, not an arbitrary symmetry of one fixed-period torus. |
| Energy interpolation and viscosity exponent | **PASS** | If \(E=\mathcal E(z_0,2R)\), then \(M_0:=\operatorname*{ess\,sup}\int_{B_{2R}}|u|^2\le2RE\) and \(M_1:=\int_{I_R\times B_{2R}}|\nabla u|^2\le2R\nu^{-1}E\). Local Sobolev and time Hölder give \(CR^2\nu^{-3/4}E^{3/2}\) plus \(CR^2E^{3/2}\). Division by \((2R)^2\) yields \(C(1+\nu^{-1})^{3/4}E^{3/2}\), up to a universal constant. |
| Periodic-lift tail finiteness | **PASS** | A radius-\(2^{m+1}R\) ball meets at most \(C[1+(2^mR)^3]\) fundamental cells. Its normalized lifted annular row grows only polynomially (at worst \(C(2^m+4^{-m}R^{-2})\|u\|_{L^3(I_R\times\mathbb T^3)}^3\)); the factor \(e^{-4^m/(32\theta)}\) makes the series summable. |
| Existence of packet moment | **PASS** | For \(w=(fg'h,-f'gh,0)\), the cross term in the first component of \(\int w|w|^2\) vanishes because \(\int g'g^2=0\). The remaining term is \((\int f^3)(\int(g')^3)(\int h^3)\ne0\). |
| Nonzero remote leakage coefficient | **PASS** | \(B_s=-2s\nabla G_s\). If \(B_s(z)\cdot M_3(w)\) vanished on every admissible separation, analyticity would make this directional derivative of \(G_s\) vanish identically, contradicting its Fourier series for nonzero \(M_3(w)\). Since \(\int w=0\), \(P_su_{A,\delta}=O(A\delta^4)\), while the leading cubic term is \(cA^3\delta^3\); centering corrections are higher order. |
| Packet concentration powers | **PASS** | Change of variables gives \(\int W|u_{A,\delta}|^3\asymp A^3\delta^3\), \((\int W|u_{A,\delta}|^2)^{3/2}\asymp A^3\delta^{9/2}\), ratio \(\delta^{-3/2}\), and \(\int|\nabla u_{A,\delta}|^2\asymp A^2\delta\). |
| Remote-packet quantifier | **PASS, conditional** | The witness refutes an unconstrained arbitrary-data or velocity-only functional inequality for which \(p=\mu=0\) is admissible. It does not refute an estimate restricted to unforced Navier--Stokes trajectories, nor one requiring \(p\) to be the pressure associated with \(u\). The source states the first limitation; the associated-pressure exclusion should be added verbatim to its summary. |
| Certificate execution and payload integrity | **PASS** | Two Python runtimes pass, `--check-only` performs no writes, the stored payload hash reproduces, and quadrature agrees with the closed form on the declared 48-case grid. |
| Certificate verification of annular geometry | **FAIL** | The program inserts \(a=4^m/32\) but never checks the distance inequality, ball-volume coefficient, or final \(8/(3\sqrt{2\pi})\) assembly. The header's claim that annular geometry is checked is unsupported by executable evidence. |
| Certificate verification of packet powers | **FAIL** | The values \(3,9/2,-3/2,1\) are literals. The only assertion subtracts two literals; it does not derive them from dimension, a change of variables, or an independently sampled packet. This is bookkeeping, not an independent producer. |
| Certificate coverage of interpolation and lifted summability | **FAIL** | No executable row checks the \(\nu^{-3/4}\) interpolation exponent or polynomial-versus-super-exponential lifted-tail argument. These rows are analytically valid, but the current certificate does not certify them. |

## 3. Exact corrections required before complete certification

1. Add \(u\in L^3(I_R\times\mathbb T^3)\) to the theorem statement, or state
   explicitly that (1.7) is extended-valued and becomes finite under this
   hypothesis. The paragraph after (1.7) contains the fact but not the formal
   hypothesis.
2. Add exact certificate rows for

   \[
   2^m-1\ge2^{m-1},\qquad
   {4\pi/3\over(8\pi)^{3/2}}={1\over12\sqrt{2\pi}},\qquad
   {32\over12\sqrt{2\pi}}={8\over3\sqrt{2\pi}},
   \]

   and for \(2R^{-2}=8(2R)^{-2}\). If these stay analytic-only, narrow the
   script header/report instead of claiming executable annular geometry.
3. Derive packet powers from a declared dimension \(d=3\): \(d\), \(3d/2\),
   \(-d/2\), and \(d-2\). For genuine second-producer evidence, also evaluate
   an explicit compactly supported divergence-free packet for several
   high-precision \(\delta\) values and independently recover the four slopes.
4. Add certificate rows for energy interpolation and lifted-tail summability,
   or leave them outside its advertised scope. A finite partial sum does not
   prove summability; record the analytic comparison
   \(2^me^{-c4^m}\le e^{-c4^m/2}\) beyond an explicit finite index, and check
   the prefix separately.
5. Sharpen the counterexample summary to say “unconstrained triples with
   \(p=\mu=0\), or a velocity-only intermediate inequality,” and explicitly
   say that no associated-pressure inequality is refuted.

## 4. Release decision

The Gaussian velocity-tail lemma may be retained as an internally proved
functional lemma. It should not yet be labeled “two-producer certified” or
released on the strength of the current Python certificate alone. After the
coverage corrections, rerun an independent audit against new input digests.
No pressure/cutoff closure, suitable-weak endpoint, epsilon regularity, or
Clay conclusion follows from this audit.

## 5. Re-audit of the revised certificate

**Re-audit date:** 2026-09-01

**Final verdict:** `PASS WITH THE ORIGINAL CLAIM BOUNDARY`

This re-audit supersedes the three certificate-coverage FAIL rows in Section
2. It does not enlarge the mathematical claim: the result remains a
functional Gaussian velocity-tail lemma, not a PDE regularity theorem.

### 5.1 Revised inputs

```text
d2708a1cc267fb61dcbd1ecb4c00be46b9746175c0b5a77dab044e8138590925  scripts/r073x_gaussian_tail_certificate.py
136b40fb6d30d4fd671e5dc3049817266986f595da46e9a6b6a31a409fe3f836  research/r073x_gaussian_tail_certificate.json
e678ee897e2e574fd3cc3b5bb674fc82524c7897a7546786c4958704c03ab248  research/r073x_gaussian_tail_certificate_report.md
3a867a6c70941318ee3cfd1c088470a2c915987c7b648da63955011df724512a  research/r073x_gaussian_velocity_tail_proof.md
6a54aeee49a01fe0953ca472573ae7bb918678b7501ca38ee03427d79e74ac28  research/r073x_exterior_tail_counterexample_audit.md
```

A final metadata-only change set the proof status to `INDEPENDENT AUDIT PASS` and changed its SHA-256 to `71ad083661ecbe3f420f75affccfb21fae3a92a73074bfa5f29a11edd30af7c9`; restoring only that line in memory reproduces the previously audited digest `3a867a6c70941318ee3cfd1c088470a2c915987c7b648da63955011df724512a`, so the final verdict remains PASS.

The proof now includes \(u\in L^3(I_R\times\mathbb T^3)\) in the theorem
hypotheses. The counterexample summary now explicitly restricts the witness
to unconstrained velocity-only triples with \(p=\mu=0\), and says that it
does not refute either an unforced-trajectory estimate or an
associated-pressure estimate.

### 5.2 Revised PASS/FAIL ledger

| Revised row | Verdict | Re-audit evidence |
|---|---|---|
| Annular distance and constants | **PASS** | The program evaluates \((2^m-1)\ge2^{m-1}\), derives \((4\pi/3)(8\pi)^{-3/2}=1/(12\sqrt{2\pi})\), derives the final \(32\)-multiple \(8/(3\sqrt{2\pi})\), and checks the core identity exactly with `Fraction`. The executable distance table stops at \(m=64\), but the universal continuation is independently exact: the gap is \(2^{m-1}-1\ge0\) for every \(m\ge1\). Thus no finite-\(m\) assumption enters the theorem. |
| Dimension-derived packet exponents | **PASS** | From the declared \(d=3\), the code derives \(d=3\), \(3d/2=9/2\), \(-d/2=-3/2\), and \(d-2=1\); these values are no longer separately inserted literals. |
| Independent packet quadrature | **PASS** | For each \(\delta\), the program rebuilds the physical cube, cell volume, packet, derivatives, and positive nonconstant weight. Its final consecutive slopes are \(2.999857066\), \(4.499782070\), \(-1.499925004\), and \(0.999799421\). A separate re-audit with node counts \(20,28,40\) and deltas \(0.2,\ldots,0.0125\) recovered final slopes within \(1.3\times10^{-4}\) of \(3,9/2,-3/2,1\), with a stable nonzero sign for the cubic moment. |
| Energy interpolation | **PASS** | The executable row derives \(\alpha=3(1/2-1/3)=1/2\), gradient-norm power \(3/2\), gradient-energy and mass-energy powers \(3/4\), time-length power \(1/4\), viscosity power \(-3/4\), and total radius power \(2\). This reproduces the analytic calculation rather than merely asserting the final exponent. |
| Lifted-tail summability | **PASS** | The worst permitted decay is \(c=1/32\), since \(0<\theta\le1\). At \(m_0=4\), \((c/2)4^{m_0}-m_0\log2=1.2274112777>0\); the next gap increment is \(11.3068528194>0\) and then strictly increases. Hence \(2^me^{-c4^m}\le e^{-(c/2)4^m}\) for every \(m\ge4\). The majorant ratios are at most \(e^{-12}=6.1442123533\times10^{-6}<1\), so the infinite tail is geometrically summable after the finite prefix. |
| Generated JSON versus current code | **PASS** | Direct import gives `generate()==stored_json`. Removing `payload_sha256` and canonically hashing the stored payload gives `fcac97440dde87d00103f3a09b346bdd918c9fbb7360ee792edc2c8d0357e3b7`, exactly the value returned by both Python runtimes. |
| Generated report versus current code | **PASS** | Direct import gives `render_report(generate())==stored_report`. |
| `--check-only` zero-write contract | **PASS** | SHA-256, modification time, and size of the script, JSON, report, proof, and counterexample audit were captured before and after a system-Python run and were identical. The bundled runtime returned the same PASS rows and payload hash. |
| Claim boundary | **PASS** | The certificate still declares no NSE time step, no PDE regularization, and Clay status OPEN. The functional packet obstruction remains explicitly separated from associated-pressure and NSE-only quantifiers. |

### 5.3 Final decision

The revised scalar certificate is now a genuine second producer for the
annular coefficient assembly, concentration exponents and numerical slopes,
the viscosity/radius interpolation powers, and lifted-tail summability. In
combination with the analytic proof and this independent re-audit, the
Gaussian velocity-tail functional lemma passes its internal certificate
gate.

This PASS does **not** certify pressure/cutoff closure, smallness of the tail
from a local hypothesis, a suitable-weak endpoint, epsilon regularity, or
three-dimensional Navier--Stokes global regularity. NOT CLAY.
