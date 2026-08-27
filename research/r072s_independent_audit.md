# R0.72S independent mathematical audit

**Date:** 2026-08-28
**Status:** analytic PASS and dual-route exact-contract PASS; the canonical
certificate directory and release manifest are the authority for formal
publication status

## 0. Scope and verdict

This audit independently checks the finite-harmonic family

\[
 f(\phi;z_2,z_3)=\cos\phi+
 \operatorname{Re}\!\left(z_2e^{2i\phi}+z_3e^{3i\phi}\right),
 \qquad (z_2,z_3)\in\mathbb C^2,
 \tag{0.1}
\]

and the two heat paths declared in `r072s_report-source.md`.

The following analytic claims pass.

1. The incidence preimages split exactly into types
   \(A_2,A_3,A_4,A_5\), and no higher type occurs in this family.
2. The coefficient-to-derivative jet of orders one through four has
   determinant \(5400\).  This proves restricted miniversality modulo an
   additive constant and the local marked-branch codimensions \(1,2,3,4\).
3. The pure-second-harmonic heat path has exactly one degenerate event for
   finite \(y\ge0\), with distinct critical-point count \(4/3/2\).
4. The real-even heat path has distinct critical-point count \(4/2/2\), and
   its collision is an \(A_3\) function germ.
5. The two local square-root laws have leading squared coefficients \(-2\)
   and \(-6\), respectively.

These statements concern a marked incidence preimage or one explicitly
counted path.  They do not classify the complete image of the incidence map
in \(\mathbb R^4\), its self-intersections, or all complement chambers.

The two exact implementations independently return `passed`, produce
identical canonical payloads, and pass the aligned comparator in a temporary
unsealed run.  This verifies the schema and finite algebra before source
freeze.  The formal certificate must still be rerun from committed, clean,
tracked sources and hashed without the temporary-unsealed flag.

---

## 1. Incidence preimages and the exact \(A_k\) partition

At a declared degenerate critical point write

\[
 z_3e^{3i\phi}=A+iB,
 \qquad c=\cos\phi,
 \qquad s=\sin\phi.
 \tag{1.1}
\]

If \(z_2e^{2i\phi}=p+iq\), the equations \(f'=f''=0\) are

\[
 -s-2q-3B=0,
 \qquad
 -c-4p-9A=0.
 \tag{1.2}
\]

Hence

\[
 p=-\frac{c+9A}{4},
 \qquad
 q=-\frac{s+3B}{2},
 \tag{1.3}
\]

which gives the declared incidence parameterization

\[
 z_3=(A+iB)e^{-3i\phi},
 \qquad
 z_2=e^{-2i\phi}\left[-\frac{c+9A}{4}
 -\frac{i(s+3B)}2\right].
 \tag{1.4}
\]

Direct differentiation and substitution give

\[
\begin{aligned}
 f'''&=15B-3s=3(5B-s),\\
 f''''&=45A-3c=3(15A-c),\\
 f'''''&=15s-195B=15(s-13B),\\
 f''''''&=15c-585A=15(c-39A).
\end{aligned}
\tag{1.5}
\]

Therefore the marked critical germ is

\[
\begin{array}{c|l}
 A_2 & B\ne s/5,\\
 A_3 & B=s/5,\quad A\ne c/15,\\
 A_4 & B=s/5,\quad A=c/15,\quad s\ne0,\\
 A_5 & B=s/5,\quad A=c/15,\quad s=0.
\end{array}
\tag{1.6}
\]

On the closure of the \(A_4\) locus,

\[
 f'''''=-24s.
 \tag{1.7}
\]

If this also vanishes, then \(s=0\), \(c=\pm1\), and

\[
 f''''''=-24c\ne0.
 \tag{1.8}
\]

Thus no \(A_k\) with \(k\ge6\) occurs.  The two \(A_5\) coefficient pairs
are

\[
 (z_2,z_3)=\left(-\frac25,\frac1{15}\right)
 \quad(\phi=0),
 \qquad
 (z_2,z_3)=\left(\frac25,\frac1{15}\right)
 \quad(\phi=\pi).
 \tag{1.9}
\]

This is a complete classification of **incidence preimages by vanishing
order**.  It is not a proof that the projected caustic is embedded.  A
coefficient pair could, in principle, have several marked preimages of the
same or different types.

---

## 2. The coefficient-derivative jet and restricted miniversality

Use coefficient coordinates

\[
 (x_2,y_2,x_3,y_3)
 =\left(\operatorname{Re}z_2,\operatorname{Im}z_2,
 \operatorname{Re}z_3,\operatorname{Im}z_3\right).
 \tag{2.1}
\]

Their four variations of \(f\) are

\[
 \cos2\phi,\quad-\sin2\phi,\quad
 \cos3\phi,\quad-\sin3\phi.
 \tag{2.2}
\]

At \(\phi=0\), the matrix of derivative orders one through four is

\[
 W_0=
 \begin{pmatrix}
 0&-2&0&-3\\
 -4&0&-9&0\\
 0&8&0&27\\
 16&0&81&0
 \end{pmatrix}.
 \tag{2.3}
\]

After grouping the odd rows and sine columns, and the even rows and cosine
columns, the two block determinants are \(-30\) and \(-180\).  The row and
column permutation signs cancel, so

\[
 \boxed{\det W_0=(-30)(-180)=5400.}
 \tag{2.4}
\]

Changing \(\phi\) only rotates the real-imaginary coordinate pair in each
frequency block by determinant-one rotations.  Hence

\[
 \det W(\phi)\equiv5400.
 \tag{2.5}
\]

This proves that the four coefficient directions control the derivative
jets of orders one through four.  It is the appropriate restricted
miniversal, or \(R^+\)-versal, statement for critical-point geometry modulo
an additive constant.  If the function value is also part of the unfolding,
a fifth constant parameter is required at \(A_5\).

For a type \(A_k\) preimage, impose

\[
 f'=f''=\cdots=f^{(k)}=0,
 \qquad f^{(k+1)}\ne0,
 \qquad 2\le k\le5,
 \tag{2.6}
\]

in the five-dimensional joint space
\(\mathbb T\times\mathbb R^4\).  The coefficient columns supply the first
\(k-1\) independent jet rows, while the \(\phi\)-column supplies
\(f^{(k+1)}\) in the final row.  The constraint map has rank \(k\).
Projection to coefficient space is locally immersive on the marked
\(A_k\) locus, so a single local branch has

\[
 \operatorname{codim}_{\mathbb R^4}A_k=k-1.
 \tag{2.7}
\]

Equation (2.7) is a local marked-branch statement.  It does not turn the
entire caustic image into one globally embedded stratified hypersurface.

---

## 3. Heat identity

For the declared decay exponents \(3=2^2-1\) and \(8=3^2-1\), both heat
paths satisfy

\[
 \partial_yF=F_{\phi\phi}+F.
 \tag{3.1}
\]

Consequently

\[
 \partial_yF'=F'''+F',
 \qquad
 \partial_yF''=F''''+F''.
 \tag{3.2}
\]

At a degenerate critical point this reduces to

\[
 \partial_yF'=F''',
 \qquad
 \partial_yF''=F''''.
 \tag{3.3}
\]

This independently checks the equal jet and time-derivative constants in
both collision models.

---

## 4. Pure-second \(A_2\) path: unique event and \(4/3/2\)

Take

\[
 z_{20}=4i,
 \qquad z_{30}=0,
 \qquad
 F_y(\phi)=\cos\phi-4e^{-3y}\sin2\phi.
 \tag{4.1}
\]

Put \(k=8e^{-3y}>0\) and \(s=\sin\phi\).  Then

\[
 F_y'=2ks^2-s-k,
 \qquad
 s_\pm(k)=\frac{1\pm\sqrt{1+8k^2}}{4k}.
 \tag{4.2}
\]

The negative root satisfies \(-1<s_-<0\) for every \(k>0\).  For the
positive root, after the necessary sign guard \(4k-1\ge0\), squaring gives

\[
 s_+(k)\le1\quad\Longleftrightarrow\quad k\ge1.
 \tag{4.3}
\]

The Hessian is

\[
 F_y''=\cos\phi\,(-1+4k\sin\phi).
 \tag{4.4}
\]

If \(\cos\phi\ne0\), degeneracy would require \(s=1/(4k)\); substitution
into (4.2) gives

\[
 -k-\frac1{8k}<0,
 \tag{4.5}
\]

so no such point exists.  If \(\cos\phi=0\), the case \(s=1\) gives
\(k=1\), while \(s=-1\) would require \(k=-1\).  Hence the unique
degenerate event for finite \(y\ge0\) is

\[
 y_*=\log2,
 \qquad \phi_*=\frac\pi2,
 \qquad z_2(y_*)=\frac i2.
 \tag{4.6}
\]

At this point

\[
 F'''=-3,
 \qquad \partial_yF'=-3.
 \tag{4.7}
\]

Thus the marked germ is \(A_2\), and the path crosses its smooth local
codimension-one caustic branch transversely in the full four-real-dimensional
coefficient slice.  All other critical points are simple.

The exact number of **distinct** critical points is

\[
 \boxed{
 \#\operatorname{Crit}(F_y)=
 \begin{cases}
 4,&0\le y<\log2,\\
 3,&y=\log2,\\
 2,&y>\log2.
 \end{cases}}
 \tag{4.8}
\]

At equality, the other sine root is \(s_-=-1/2\), producing two Morse
critical points in addition to the \(A_2\) point.  The \(A_2\) zero of
\(F'\) has multiplicity two.  Thus the real critical zeros counted with
multiplicity total four at the crossing, although there are only three
distinct points.  The phrase “\(4\to2\)” is valid as a before/after summary,
not as the literal equality-time count.

Let

\[
 \delta=y-y_*,
 \qquad \xi=\phi-\phi_*.
 \tag{4.9}
\]

Then

\[
 F_y'=-\cos\xi+e^{-3\delta}\cos2\xi
 =-3\delta-\frac32\xi^2
 +O(\delta^2+|\delta|\xi^2+\xi^4).
 \tag{4.10}
\]

For \(\delta<0\), the colliding branches are

\[
 \xi_\pm=\pm\sqrt{-2\delta}+O(|\delta|^{3/2}).
 \tag{4.11}
\]

The remainder is sharper than \(O(|\delta|)\) because the local equation is
even in \(\xi\).  For \(\delta>0\), these two local roots are absent.

---

## 5. Real-even \(A_3\) path: \(4/2/2\)

Let

\[
 a_0=-\frac{2563}{1280},
 \qquad b_0=\frac1{30},
 \qquad t=e^{-y},
 \tag{5.1}
\]

and

\[
 H_y(\phi)=\cos\phi+a_0t^3\cos2\phi+b_0t^8\cos3\phi.
 \tag{5.2}
\]

With \(x=\cos\phi\),

\[
 H_y'=-\sin\phi\,q_t(x),
 \tag{5.3}
\]

where

\[
 q_t(x)=12b_0t^8x^2+4a_0t^3x+1-3b_0t^8.
 \tag{5.4}
\]

For \(x\in[-1,1]\) and \(0<t\le1\),

\[
 \partial_xq_t(x)
 \le4t^3(a_0+6b_0t^5)
 \le-\frac{2307}{320}t^3<0.
 \tag{5.5}
\]

Also

\[
 q_t(-1)=1-4a_0t^3+9b_0t^8>0.
 \tag{5.6}
\]

At the other endpoint define

\[
 h(t)=q_t(1)=1+4a_0t^3+9b_0t^8.
 \tag{5.7}
\]

Then \(h'(t)<0\) on \((0,1]\), and

\[
 h(1/2)=0.
 \tag{5.8}
\]

Strict monotonicity of \(q_t\) now gives the complete real count:

\[
 \boxed{
 \#\operatorname{Crit}(H_y)=
 \begin{cases}
 4,&0\le y<\log2,\\
 2,&y=\log2,\\
 2,&y>\log2.
 \end{cases}}
 \tag{5.9}
\]

Before the crossing, the unique root of \(q_t\) in \((-1,1)\) produces two
off-axis simple critical points, in addition to \(0\) and \(\pi\).  At and
after the crossing there is no internal root.  At equality, \(\phi=0\) is
degenerate and \(\phi=\pi\) is simple.

At \(t_*=1/2\),

\[
 a_*=-\frac{2563}{10240},
 \qquad b_*=\frac1{7680},
 \tag{5.10}
\]

and

\[
 \partial_xq_{1/2}(1)=-\frac{511}{512},
 \qquad
 H''''(0,y_*)=-\frac{1533}{512},
 \qquad
 \partial_yH''(0,y_*)=-\frac{1533}{512}.
 \tag{5.11}
\]

Thus \(\phi=0\) is an \(A_3\) function germ.  It is a triple zero of
\(H'\); together with the simple zero at \(\pi\), the equality-time critical
zeros have total multiplicity four but only two distinct locations.

With \(\delta=y-y_*\) and \(K=-1533/512\), evenness in \(\phi\) gives

\[
 H_y'(\phi)=K\delta\phi+\frac K6\phi^3
 +O(\delta^2|\phi|+|\delta||\phi|^3+|\phi|^5).
 \tag{5.12}
\]

The two off-axis branches therefore satisfy

\[
 \phi_\pm=\pm\sqrt{-6\delta}+O(|\delta|^{3/2}),
 \qquad \delta<0.
 \tag{5.13}
\]

The coefficient germ belongs to the ambient \(A_3\) stratum, and the full
four-parameter coefficient family is restricted miniversal there.  The
specific one-parameter heat path, however, stays in the real-even plane.
It crosses the endpoint \(A_3\) wall transversely **only inside that
two-dimensional slice**, since

\[
 \left.\partial_y\bigl[h(e^{-y})\bigr]\right|_{y=y_*}
 =\frac{1533}{512}\ne0.
 \tag{5.14}
\]

It is not transverse to the codimension-two \(A_3\) stratum in the full
four-dimensional coefficient space.  A one-dimensional path cannot be
transverse to a codimension-two submanifold in that ambient space.  In
local unfolding coordinates, the path is the symmetry axis of
\(x^3+ux+v\), with \(v=0\), rather than a generic two-parameter traversal.

---

## 6. Distinct points, multiplicity, and projected geometry

The two count ledgers use distinct points:

| path | before | at the wall | after | equality-time multiplicity |
|---|---:|---:|---:|---:|
| pure-second \(A_2\) | 4 | 3 | 2 | \(2+1+1=4\) |
| real-even \(A_3\) | 4 | 2 | 2 | \(3+1=4\) |

Neither multiplicity statement should be substituted for the number of
distinct critical locations.  Conversely, the distinct count at the wall
must not be used to erase the vanishing order that distinguishes \(A_2\)
from \(A_3\).

Likewise, the following objects must remain separate.

1. The incidence preimage is a marked tuple \((\phi,A,B)\) satisfying
   \(f'=f''=0\).
2. Its projection is a coefficient pair \((z_2,z_3)\).
3. A local marked \(A_k\) branch has codimension \(k-1\).
4. The global projected caustic can have several branches or
   self-intersections and is not classified here.

---

## 7. Exact certificate boundary and source-stage status

The exact source contract uses two independent arithmetic routes:

1. `r072s_exact_audit.py`: Python `Fraction` arithmetic and a direct exact
   determinant;
2. `r072s_independent_audit.mjs`: JavaScript `BigInt` rationals and a Bareiss
   determinant.

In a temporary unsealed run performed after the schema alignment, both routes
returned `passed`, their canonical payloads were identical, and every
decisive comparator check passed.  The programs machine-check finite
crossing-power identities, representative endpoint evaluations, nonzero
jets, both sign/monotonicity-guard ledgers, and the normalized heat-equation
identity.  Their count and transversality ledger fields are computed from
those inputs rather than inserted as conclusion literals.  The comparator
checks that derivation contract and exact cross-route agreement; the hash
builder rejects a stale payload lacking it.

This is a source-stage check, not a formal seal.  At this point
`formalSourceReady=false` is expected because the new sources have not yet
been frozen in a clean commit.  The formal run must record one full source
commit in both implementations, set `temporaryUnsealedSourceAllowed=false`,
pass the comparator with every check true, and then close the exact directory
with its flat `SHA256SUMS` ledger.

Even after that mechanical repair, the exact certificate has a deliberately
narrow role.  It checks:

1. rational incidence-jet coefficients and the \(A_k\) ledger;
2. the determinant \(5400\);
3. rational crossing coefficients and powers, representative-regime
   endpoint values, nonzero jets, sign/monotonicity guards, and leading split
   coefficients \(-2\) and \(-6\);
4. exact agreement of the two canonical finite payloads.

Those are finite machine checks.  The continuous inequalities and
monotonicity arguments in Sections 4--5—not the finite programs—deduce the
unique event, global critical counts, simplicity away from collision, and
the geometric transversality statements.  The certificate does **not**
replace:

1. the continuum monotonicity and root-count arguments in Sections 4--5;
2. a classification of all global caustic self-intersections or chambers;
3. a full real \(A_{2j+1}^{\pm}\) sign refinement;
4. a nonautonomous enhanced-dissipation estimate through either collision;
5. any nonlinear three-dimensional Navier--Stokes stability or regularity
   theorem.

---

## 8. Final publication boundary

The strongest defensible R0.72S statement is the following.

> The fixed-first-harmonic \(1{:}2{:}3\) coefficient family has an exact
> marked-incidence partition through \(A_5\) and is restricted miniversal
> modulo constants at those germs.  One explicit pure-second heat path has a
> unique ambient-generic \(A_2\) fold with distinct count \(4/3/2\), while
> one explicit real-even path has a symmetry-restricted \(A_3\) collision
> with distinct count \(4/2/2\).  The latter path is transverse only to the
> endpoint wall inside the real-even slice.  These results do not classify
> the global caustic image and do not prove enhanced dissipation through a
> collision.

Analytically and at the temporary source-stage comparison, this statement
passes.  A formally sealed publication additionally requires a clean
committed-source certificate rerun, flat hash ledger, formal figure package,
and release gate; those artifacts are tracked outside this prose audit.
