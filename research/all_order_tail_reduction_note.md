# R0.68A — The all-order target tail reduces to one eighth-order obstruction

## 1. Result

The R0.67 calculation settled the complete sixth-order heat coefficient for
the periodic target family, but it deliberately left the sum of all Picard
orders open.  R0.68A closes the genuinely infinite part of that problem.

Let

\[
 M_r=16^r,\qquad
 q_r=\frac{2(16^r-1)}{15},\qquad
 m_r=q_r+1=\frac{2M_r+13}{15},
\tag{1.1}
\]

take \(L=1\), \(H_r=4M_r\), and choose the quartic-critical amplitude

\[
 \varepsilon_r^2=\left(\frac{16}{\lambda}\right)^r,
 \qquad A_r=\varepsilon_r\sqrt{H_r},
\tag{1.2}
\]

where \(\lambda>25\) is the certified R0.66 dominant quartic root.  If

\[
 \mathcal R_{\ge10,r}
 =\sum_{n=10}^{\infty}A_r^n
   \widehat G_n(0,m_r,t_{H_r}),
\tag{1.3}
\]

then

\[
 \boxed{
 \frac{|\mathcal R_{\ge10,r}|}
 {|A_r^2\widehat G_2(0,m_r,t_{H_r})|}
 <\frac1{30000}\left(\frac{43}{64}\right)^r.}
\tag{1.4}
\]

Thus the complete infinite tail after order eight is strictly summable and
vanishes relative to the quadratic target.  Together with the R0.60 support
theorem and the completed fourth- and sixth-order calculations, this reduces
the all-order target asymptotic to one finite question:

\[
 \boxed{\text{the complete eighth-order target coefficient.}}
\tag{1.5}
\]

This is a reduction theorem inside a globally smooth invariant shear class.
It is not a theorem about singularity formation or global regularity for
general three-dimensional Navier--Stokes solutions.

## 2. Sectorwise Dyson majorant

For a fixed positive second frequency \(m\), the invariant-shear equation is

\[
 \partial_tG_m-\partial_1^2G_m+m^2G_m+imAF_1G_m=0.
\tag{2.1}
\]

The amplitude-free initial sector contains \(L\) coefficients of modulus
one, hence its normalized \(L^2(\mathbb T)\) norm is \(\sqrt L\).  Heat is
an \(L^2\) contraction, and multiplication by \(F_1\) has operator norm
\(\|F_1\|_\infty\).  The time-ordered simplex therefore gives, for
\(p=n-1\),

\[
 \|A^{p+1}G_{p+1,m}(t)\|_2
 \le
 A e^{-m^2t}\sqrt L\,\frac{\Theta_m(t)^p}{p!},
\tag{2.2}
\]

where

\[
 \Theta_m(t)=A|m|\int_0^t\|F_1(s)\|_\infty\,ds.
\tag{2.3}
\]

This also proves absolute convergence of the full amplitude series in every
fixed sector.  No finite truncation or numerical time stepping enters (2.2).

## 3. The dimensionless interaction parameter

R0.58 proved the tensor Rudin--Shapiro heat envelope

\[
 \|F_1(s)\|_\infty
 \le2C_T\sqrt{LM}\,e^{-H^2s},
 \qquad C_T=4+3\sqrt2.
\tag{3.1}
\]

At

\[
 t_H=\frac{T}{H^2},\qquad T=\frac{\log2}{2},
\tag{3.2}
\]

and \(A=\varepsilon\sqrt H\), \(H=4LM\), \(m\le M\), equations
(2.3) and (3.1) give

\[
 \begin{aligned}
 \Theta_m(t_H)
 &\le
 \frac{2C_TA|m|\sqrt{LM}}{H^2}(1-e^{-T})\\
 &\le \frac{C_T(1-2^{-1/2})}{4}\frac{\varepsilon}{L}
 =\boxed{\frac{1+\sqrt2}{4}\frac{\varepsilon}{L}}.
 \end{aligned}
\tag{3.3}
\]

Put

\[
 \kappa=\frac{1+\sqrt2}{4}<\frac58.
\tag{3.4}
\]

The important point is that \(\Theta_m\) is uniform in \(M\).  The amplitude
\(A\sim\sqrt H\) is exactly offset by the short time, the tensor square-root
cancellation, and \(m\le M\).

## 4. Why the tail starts with nine interactions

R0.60 proved

\[
 \widehat G_n(0,m,t_H)=0
 \qquad(n=3,5,7,9).
\tag{4.1}
\]

For \(n=9\), a hypothetical zero first frequency would split nine shell
frequencies into groups of four and five.  With \(H=4N\) and \(D=N-1\),
their strict gap is

\[
 H-4D=4.
\tag{4.2}
\]

Hence, after retaining every term through order eight, the next possible
target contribution is \(n=10\), corresponding to \(p=9\) shear
interactions.  From (2.2),

\[
 |\mathcal R_{\ge10,m}|
 \le
 A e^{-m^2t_H}\sqrt L
 \sum_{p=9}^{\infty}\frac{\Theta_m^p}{p!}
 \le
 A e^{-m^2t_H}\sqrt L\,
 e^{\Theta_m}\frac{\Theta_m^9}{9!}.
\tag{4.3}
\]

## 5. Comparison with the exact quadratic target

R0.61 gives

\[
 |A^2\widehat G_2(0,m,t_H)|
 =A^2e^{-m^2t_H}\frac{m}{H^2}S_{2,m}.
\tag{5.1}
\]

Every one of the \(L\) positive summands in \(S_{2,m}\) is larger than
\(4/25\), so

\[
 S_{2,m}>\frac{4L}{25}.
\tag{5.2}
\]

The common factor \(e^{-m^2t_H}\) cancels between (4.3) and (5.1).  For the
periodic target (1.1), \(m_r\ge2M_r/15\), and therefore

\[
 \frac{|\mathcal R_{\ge10,r}|}
 {|A_r^2\widehat G_2(0,m_r,t_{H_r})|}
 \le
 \frac{375}{9!}\,e^{\kappa\varepsilon_r}
 \kappa^9\sqrt{M_r}\,\varepsilon_r^8.
\tag{5.3}
\]

Since \(\varepsilon_r\le1\), \(\kappa<5/8\), and
\(e^\kappa<e^{2/3}<2\),

\[
 \frac{375}{9!}e^{\kappa\varepsilon_r}\kappa^9
 <\frac{750}{9!}\left(\frac58\right)^9
 <\frac1{30000}.
\tag{5.4}
\]

Finally,

\[
 \sqrt{M_r}\,\varepsilon_r^8
 =\left(\frac{2^{18}}{\lambda^4}\right)^r
 <\left(\frac{2^{18}}{25^4}\right)^r
 <\left(\frac{43}{64}\right)^r.
\tag{5.5}
\]

Equations (5.3)--(5.5) prove (1.4).

## 6. What is now closed, and what is not

R0.68A proves four points.

1. The invariant-shear amplitude series is absolutely convergent in each
   fixed \(m\)-sector, with an explicit factorial majorant.
2. At quartic-critical amplitude, all target terms of order at least ten are
   jointly negligible; they do not have to be computed one by one.
3. The completed sixth-order term is not followed by an uncontrolled
   infinite hierarchy.  The only missing term before the certified tail is
   order eight.
4. The next calculation is finite and falsifiable: determine the complete
   heat-weighted eighth-order coefficient on the same periodic target.

The theorem does **not** determine the eighth-order sign or dominant heat
projection.  It does not transfer from the invariant shear class to arbitrary
three-dimensional data.  It does not prove norm inflation, blow-up, or global
regularity for the Clay problem.

## 7. Next step

The eighth-order zero-time central-charge transfer has

\[
 2\times2^7\times7=1792
\tag{7.1}
\]

states.  A direct sparse probe gives the candidate dominant block root

\[
 256\lambda=6438.806869529\ldots,
\tag{7.2}
\]

and the same probe reproduces \(\lambda\), \(16\lambda\), and
\(4096\lambda\) at orders four, six, and ten.  This is strong structural
evidence, not yet an eighth-order heat theorem.  R0.68B must:

1. prove the exact eighth-order image spectrum and reachability;
2. include every heat ordering and every target-charge sector allowed at
   order eight;
3. certify an upper asymptotic below the threshold needed by (1.4), or prove
   the expected \(256\lambda\) dominant projection directly.

Once that finite calculation is complete, the target asymptotic of the full
Picard series will be decided for this packet.
