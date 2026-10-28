# Consolidated verification copy, 28 October 2026.
# Purpose: Check finite lengths of the successive quadratic-modification filtration.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact checks for the recurrence and all leading-coefficient ideals.

The proof for arbitrary indices is in PROOF.md. No numerical arithmetic.
"""
from pathlib import Path
import json
import sympy as s

x,y,z,p,w=s.symbols('x y z p w')
root=Path(__file__).resolve().parent
checks=[]
for ell in range(1,4):
    r={-1:z,0:y}
    for j in range(1,ell+1):
        r[j]=s.expand(x*r[j-2]-r[j-1]**2)
    P,W=r[ell],r[ell-1]
    jac=s.expand(s.diff(P,y)*s.diff(W,z)-s.diff(P,z)*s.diff(W,y))
    assert jac==(-x)**ell
    assert s.expand(P.subs(x,0)+y**(2**ell))==0
    assert s.gcd(s.Poly(s.diff(P,y),x,y,z),s.Poly(s.diff(P,z),x,y,z)).total_degree()==0
    back={-1:p,0:w}
    for j in range(ell):
        back[j+1]=s.cancel((back[j]**2+back[j-1])/x)
    py,pz=back[ell-1],back[ell]
    assert s.cancel(P.subs({y:py,z:pz}, simultaneous=True)-p)==0
    assert s.cancel(W.subs({y:py,z:pz}, simultaneous=True)-w)==0
    image_exponents=[]
    for n in range(17):
        q,rem=divmod(n,2**ell)
        sn=back[ell]**q
        for j in range(ell):
            sn*=back[j]**((rem>>j)&1)
        poly=s.Poly(s.expand(sn),w)
        e=sum(n//2**j for j in range(1,ell+1))
        a=ell*n-e
        assert poly.degree()==n
        assert s.cancel(poly.LC()-x**(-e))==0
        result=s.cancel(x**(ell*n)*s.diff(poly.as_expr(),w,n))
        assert result==s.factorial(n)*x**a
        assert s.diff(poly.as_expr(),w,n+1)==0
        image_exponents.append(a)
    checks.append({'l':ell,'p':str(P),'w':str(W),'jacobian':str(jac),
                   'plinth_generator':str(x**ell),'exponents_n_0_to_16':image_exponents,
                   'checks':'PASS'})
out={'arithmetic':'exact rational','status':'PASS','cases':checks}
(root/'verification.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
