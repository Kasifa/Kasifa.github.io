# R0.29 canonical transport reduction and the infinite charge ladder

## Status

R0.28 rewrote the negative edge in terms of three rational arrays
\(a,u,v\), with

\[
 (\mathcal L-1)u=\{a,u\},
 \qquad
 (\mathcal L-1)v=\{a,v\}.
\tag{1.1}
\]

The proposed next step was a parity-twisted invariant cone involving the
zero-charge slice and nearby charge sectors.  Two exact facts change the form
of that task.

First, no fixed finite collection of charge sectors is closed: the equation
for charge \(q\) contains a nonzero term from charge \(q+1\).  Second, the two
transport arrays are not independent.  After normalization they form a
log-canonical coordinate system and admit an exact exponential factorization.

These statements hold to all orders as formal identities.  They do not prove
the eventual endpoint sign, a coefficient-ratio limit, or a Navier--Stokes
regularity statement.

## Algebraic setting

Let

\[
 X=Z\partial_Z,
 \qquad
 Y=W\partial_W,
 \qquad
 \mathcal L=X+Y,
\]

and use the log-canonical bracket

\[
 \{f,g\}=(Xf)(Yg)-(Yf)(Xg).
\tag{2.1}
\]

The rational R0.28 initial data are

\[
 a_1=Z+W,
 \qquad
 u_1=-\frac Z{12},
 \qquad
 v_1=-\frac W3.
\tag{2.2}
\]

If \(F\) begins in total degree \(m\), then the formal equation

\[
 (\mathcal L-m)F=\{a,F\}
\tag{2.3}
\]

has a unique solution after its degree-\(m\) term is specified.  Indeed, at
degree \(n>m\), the left side is \((n-m)F_n\), while the right side only uses
lower-degree components of \(F\).

## The normalized transport coordinates

Define

\[
 U=-12u,
 \qquad
 V=-3v.
\tag{3.1}
\]

Then \(U_1=Z\), \(V_1=W\), and both satisfy

\[
 (\mathcal L-1)U=\{a,U\},
 \qquad
 (\mathcal L-1)V=\{a,V\}.
\tag{3.2}
\]

### Theorem 1: log-canonical identity

The full formal series obey

\[
 \boxed{\{U,V\}=UV.}
\tag{3.3}
\]

To prove this, apply \(\mathcal L\) to the bracket and use the Jacobi identity:

\[
 (\mathcal L-2)\{U,V\}=\{a,\{U,V\}\}.
\]

The product rule gives the same equation for \(UV\):

\[
 (\mathcal L-2)(UV)=\{a,UV\}.
\]

Their degree-two terms agree because

\[
 \{Z,W\}=ZW.
\]

Formal uniqueness in (2.3) proves (3.3).  Equivalently,

\[
 \left\{\log U,\log V\right\}=1,
\tag{3.4}
\]

after the leading monomials \(Z,W\) are factored before taking logarithms.
Thus \((Z,W)\mapsto(U,V)\) is a near-identity log-symplectic formal change of
coordinates.

### Theorem 2: exact ratio identity

The two transport coordinates also satisfy

\[
 \boxed{\frac UV=\frac ZW e^{-a}.}
\tag{3.5}
\]

Let \(B=\log Z-\log W\).  The bracket (2.1) gives

\[
 \{B,F\}=\mathcal L F.
\tag{3.6}
\]

Dividing (3.2) by \(U,V\) shows

\[
 \{B-a,\log U\}=1,
 \qquad
 \{B-a,\log V\}=1.
\tag{3.7}
\]

Equation (3.4) implies that \(\log U,\log V\) are formal canonical
coordinates.  Both \(B-a\) and \(\log U-\log V\) have bracket one with each
coordinate.  Their difference is therefore constant.  The leading terms are
both \(\log Z-\log W\), so the constant is zero.  This proves (3.5).

In polynomial-exponential form, the same identity is

\[
 \boxed{4Wu=Zv e^{-a}.}
\tag{3.8}
\]

## Complete factorization of the sharp field

Since \(d=pu+qv\), (3.8) gives

\[
 \boxed{
 d=v\left(q+\frac{pZ}{4W}e^{-a}\right).
 }
\tag{4.1}
\]

There is a symmetric version.  Define the zero-constant stretch series

\[
 \phi=\frac12\log\frac{UV}{ZW}.
\tag{4.2}
\]

Combining the product in (4.2) with the ratio (3.5) yields

\[
 U=Z e^{\phi-a/2},
 \qquad
 V=W e^{\phi+a/2},
\tag{4.3}
\]

and hence

\[
 \boxed{
 d=-e^\phi\left(
 \frac{pZ}{12}e^{-a/2}
 +\frac{qW}{3}e^{a/2}
 \right).
 }
\tag{4.4}
\]

The stretch is not another independent nonlinear unknown.  Substitution of
(4.3) into (3.2) gives the linear equation

\[
 \boxed{
 \mathcal L\phi-\{a,\phi\}=\frac12(X-Y)a,
 \qquad \phi_0=0.
 }
\tag{4.5}
\]

Thus the sharp transport sector is determined by the active scalar \(a\) and
one zero-initial linear response \(\phi\).  The original arrays \(u,v\) are
recovered by exponentiation.

More generally, every monomial in the canonical coordinates satisfies

\[
 (\mathcal L-m-n)(U^mV^n)=\{a,U^mV^n\}.
\tag{4.6}
\]

Consequently, if a transported field starts from a homogeneous polynomial
\(P_m(Z,W)\), its unique solution is \(P_m(U,V)\).  This explicitly integrates
the entire linear transport hierarchy once the canonical map is known.

## Why finitely many charge sectors cannot close

Use the R0.28 charge coordinates

\[
 R=Z^2W,
 \qquad
 \Xi=Z^{-1},
 \qquad
 Z^nW^k=R^k\Xi^q,
 \qquad
 q=3k-(n+k).
\]

Write \(f_{k,q}=[R^k\Xi^q]f\).  The transport recurrence is

\[
 (3k-q-1)f_{k,q}
 =\sum_{\substack{i+j=k\\r+s=q}}(is-rj)a_{i,r}f_{j,s}.
\tag{5.1}
\]

The active series has the exact lower support bound

\[
 a_{k,q}=0\quad(q<-1),
 \qquad
 a_{0,-1}=1.
\tag{5.2}
\]

For (5.2), induction leaves only the possible charge \(-2=(-1)+(-1)\);
the two ordered terms cancel because their determinant factors are opposite.

Now isolate the \((i,r)=(0,-1)\) leaf in (5.1).  It contributes

\[
 (0\cdot(q+1)-(-1)k)a_{0,-1}f_{k,q+1}
 =k f_{k,q+1}.
\]

Therefore

\[
 \boxed{
 (3k-q-1)f_{k,q}
 =k f_{k,q+1}+\text{lower-degree convolution terms}.
 }
\tag{5.3}
\]

For every fixed upper charge cutoff \(Q\), the equation at \(q=Q\) requires
the omitted sector \(Q+1\) once \(k\) is large enough.  A finite band around
zero charge is therefore not an invariant subsystem.  Any coefficientwise
cone proof must control an infinite charge ladder, with weights strong enough
to absorb the upward shift in (5.3).

## Exact finite regression

The formal proof above is all-order.  The companion GMP audit independently
constructs \(e^{-a}\) from

\[
 \mathcal L(e^{-a})=-(\mathcal L a)e^{-a}
\]

and checks (3.3) and (3.8) coefficient by coefficient.  The finite regression
is an implementation check, not the source of the theorem.

## Consequence for the next theorem

The raw proposal “add the zero-charge slice and a few adjacent sectors” is not
closed.  There are now two mathematically viable next routes:

1. construct an infinite charge cone with explicit exponential or factorial
   weights and prove that (5.3), including all nonlinear convolution terms,
   preserves it; or
2. use (4.3)--(4.5) to study the analytic singularities of \(a\) and the
   stretch \(\phi\), then transfer them through the explicit exponentials.

The second formulation eliminates an independent sharp transport array and
exposes the canonical Jacobian.  R0.30 should compare these two routes by
proving the first nontrivial weighted estimate, rather than extending another
finite coefficient table.
