# R0.73Q endpoint no-go: why the bare Kato supremum does not close

**Status:** exact proof-route obstruction; independently checked

**Scope:** this note disproves one proposed estimate from the sole reference
action \(u\in L^4_tL^6_x\).  It does **not** disprove stability in a full
Koch--Tataru or \(BMO^{-1}\) space.

## 1. Candidate endpoint estimate

For a time-dependent field, consider the bare Kato quantity

\[
 \|w\|_{\mathcal K_6}
 :=\sup_{t>0}t^{1/4}\|w(t)\|_6.
 \tag{1.1}
\]

The periodic Stokes heat estimate gives a cross term of the form

\[
 t^{1/4}\int_0^t(t-s)^{-3/4}
 \|u(s)\|_6\|w(s)\|_6\,ds.
 \tag{1.2}
\]

Using (1.1) on \(w\), closure from only
\(\|u\|_{L^4_tL^6_x}<\infty\) would require an estimate comparable to

\[
 \sup_{t>0}t^{1/4}
 \int_0^t(t-s)^{-3/4}s^{-1/4}g(s)\,ds
 \le C\|g\|_{L^4(0,\infty)}.
 \tag{1.3}
\]

Near a fixed positive time, the harmless factors \(t^{1/4}\) and
\(s^{-1/4}\) do not change the endpoint.  Thus (1.3) would imply the false
one-dimensional map

\[
 I_{1/4}:L^4\to L^\infty.
 \tag{1.4}
\]

## 2. Exact counterexample to the required time map

For \(n\ge2\), define on \((0,1)\)

\[
 g_n(s)
 :=n^{-1/4}(1-s)^{-1/4}
 {\bf1}_{\{e^{-n}<1-s<1/2\}}.
 \tag{2.1}
\]

Then

\[
 \begin{aligned}
 \|g_n\|_4^4
 &=n^{-1}\int_{e^{-n}}^{1/2}{dr\over r}\\
 &=1-\frac{\log2}{n},
 \end{aligned}
 \tag{2.2}
\]

so \(\|g_n\|_4\to1\).  At \(t=1\), however,

\[
 \begin{aligned}
 \int_0^1(1-s)^{-3/4}g_n(s)\,ds
 &=n^{-1/4}\int_{e^{-n}}^{1/2}{dr\over r}\\
 &=n^{3/4}-n^{-1/4}\log2\longrightarrow\infty.
 \end{aligned}
 \tag{2.3}
\]

Therefore no constant in (1.3) can depend only on the \(L^4\) norm of the
reference coefficient.

## 3. Exact interpretation

The failed implication is

\[
 \boxed{
 u\in L^4_tL^6_x
 \quad\not\Longrightarrow\quad
 \text{closure of the cross term in the bare }
 \sup_t t^{1/4}L^6_x\text{ norm}.}
 \tag{3.1}
\]

The obstruction is the logarithmic endpoint at the upper integration limit.
It is avoided in the successful R0.73Q space because

\[
 I_{1/4}:L^2_t\to L^4_t
 \tag{3.2}
\]

is a strong Hardy--Littlewood--Sobolev map, and the product of two
\(L^4_tL^6_x\) fields belongs to \(L^2_tL^3_x\).

## 4. Why this says nothing negative about full \(BMO^{-1}\)

The Koch--Tataru path norm contains both

\[
 \sup_t\sqrt t\|w(t)\|_\infty
 \tag{4.1}
\]

and a local parabolic-cylinder Carleson \(L^2\) term.  Its tent-space
bilinear estimate does not reduce to (1.3).  Auscher--Dubois--Tchamitchian
also established whole-space \(BMO^{-1}\)-topology stability around global
\(VMO^{-1}\) solutions in that class.

Conversely, Coiculescu--Palasek now show that nonperturbative
\(BMO^{-1}(\mathbb T^3)\) data can have two distinct global finite-\(X_{KT}\)
solutions.  This makes the endpoint solution class and perturbative branch
indispensable; “nonperturbative” is not a quantitative norm lower bound.

The safe labels are therefore

```text
bareKatoSupFromL4L6Action=BLOCKED_BY_EXACT_ENDPOINT_COUNTEREXAMPLE
fullKochTataruBilinearTheory=NOT_REFUTED
smallBMOInverseUniqueness=KNOWN
nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL
periodicRelativeBMOInverseTube=NOT_CLAIMED
```
