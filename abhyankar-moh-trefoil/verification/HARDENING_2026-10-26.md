# Combined audit corrections — 26 October 2026

The audits examined published commit `088f4aa760566ad67f6594b853ab18f700f94913`.
They found no error in the current two rectification formulas or their
polynomial inverse proofs, but found reproducible gaps in the checkers and
verification evidence. This update fixes those gaps. The construction
formulas and twelve printed RHS retain their corrected 25 October coefficients.

## Supplementary harmonic reader: inverse-coordinate collision

The old reader replaced `X^3-3*X+Y` by `y`, then also interpreted original `Y`
as `y`. Both parsing routes shared this non-injective transformation.
Replacing `+(X^3-3X+Y)\Bigl[X^{2} - 2\Bigr]` by
`+Y\Bigl[X^{2} - 2\Bigr]` corrupts inverse component 2 by
`-(X^3-3*X)*(X^2-2)`, yet the supplementary reader accepted it.
The main strict reader rejected it. A corresponding collision between the
compressed third coordinate and original `Z` was also reproduced.
Neither corruption occurs in the published formulas.

Both parsing routes now evaluate the original inverse RHS by the invertible
coordinate substitution

```text
X = x,
Y = y - x^3 + 3*x,
Z = z - (1-a)*(42*x^3-49*x).
```

Here `(x,y,z)` are independent `(X,U,V)` coordinates. The first inverse
component becomes `y`; original `Y` and `Z` retain their distinct meanings.
Equivalent reordered expressions pass, whereas `U -> Y` and `V -> Z`
corruptions fail. The maintained runner tests `U -> Y` with both the
independent and strict readers and requires its exact nonzero residual.

## Actual inverse callables

Adding `+Y` to a component of `harmonic_inverse` vanishes on the tested axis
and previously passed the core checks. Both published callables are correct;
two new symbolic checks now bind them to their proved factorizations:

```text
trefoil_inverse(y, x-y^3+3*y, z-8+14*y^2) = (x, R-2, S+5*x),
harmonic_inverse(y, x-y^3+3*y, z-(1-a)*(42*y^3-49*y))
    = (x, inverse_y, inverse_z).
```

These are identities in independent variables, not point tests. The core
prints 19 PASS messages instead of 17. The runner requires the deliberately
changed callable to fail at the new harmonic binding.

## Other safeguards

- Check component names, numbers and argument order on each LHS.
- Reject unbraced multidigit exponents: TeX `x^10` is not `x^{10}`.
- Preserve `\times` in both supplementary parsing routes, including unary signs.
- Match the opening and closing formula environment names.
- Pass the wrapper's optimization setting to both child interpreters.
- Resolve the three Macaulay2 wrappers' core file relative to their own script.

The readers check the repository's explicit syntax, not arbitrary TeX macros
or rendering semantics. Separate compilation checks the paper.

## Evidence and attribution

`VERIFICATION.md` links the complete `printed_rerun.log` rather than an
incomplete historical capture. The control-results path now names the actual
`negative_control_logs/results.json`. Historical input hashes are identified
as historical; `current_verification.json` records revised inputs and fresh
complete outputs. The runner has five positive cases and fourteen deliberate
rejections, checking both exit code and expected diagnostic; old sign controls
are retained.

The stale opening comment in the trefoil appendix is corrected. The known
Chebyshev affine normalization is attributed to Gene and Jenna Freudenburg,
*Curves defined by Chebyshev polynomials*, arXiv:0902.3440, Introduction, p. 3.
The existing Bhatwadekar–Dutta citation now identifies Theorem 3.2.
These are attribution and locator improvements, not new priority claims.

The scope remains the two stated constructions over `Q[a]/(a^2-a+1)`, their
affine Chebyshev normalization and the conditional transfer theorem. No full
Lean formalization or general spatial embedding theorem is asserted.
