# Consolidated verification copy, 28 October 2026.
# Purpose: Check bounded mixed-projection multiplicity cases and exceptional-parameter identities.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent checks of H378 uniform and constant mixed-projection claims."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'python_deps'))
import sympy as s
x,t,r,aa=s.symbols('x t r aa')
K=s.QQ.frac_field(r)
a=r/(r*r-1)
k=x*x-1
u=k-a*x
v=a*k-x
h=s.Poly(u**3-3*u*v*v-x*v**3,x,domain=K)
d=s.Poly(x**4-3*x*x+1,x,domain=K)
vp=s.Poly(v,x,domain=K)
left=s.Poly(x-r,x,domain=K)
right=s.Poly(x+1/r,x,domain=K)
left_powers=[s.Poly(1,x,domain=K)]
right_powers=[s.Poly(1,x,domain=K)]
for j in range(10):
    left_powers.append((left_powers[-1]*left).rem(h))
    right_powers.append((right_powers[-1]*right).rem(h))
allowed_den=s.Poly(r*(r*r-1),r)
records=[]
for n in range(4,11):
 for e in range(n+1):
    f=n-e
    rem=(d*left_powers[e]*right_powers[f]).rem(h)
    equations=[rem.nth(j) for j in range(3,7)]
    equations += [rem.nth(j)*vp.nth(2)-rem.nth(2)*vp.nth(j) for j in (0,1)]
    polys=[]
    for eq in equations:
        num,den=s.cancel(eq).as_numer_denom()
        pol=s.Poly(num,r)
        if not pol.is_zero:polys.append(pol)
        den=s.Poly(den,r).monic()
        while den.degree()>0:
            g=s.gcd(den,allowed_den)
            assert g.degree()>0,(e,f,den)
            den=den.exquo(g).monic()
    g=polys[0]
    for p in polys[1:]:g=s.gcd(g,p)
    assert g.degree()==0,(e,f,g)
    # In particular r=+/-i, corresponding to repeated roots of v, is
    # regular in every denominator and cannot be a simultaneous zero.
    remainders=[p.rem(s.Poly(r*r+1,r)) for p in polys]
    repeat_gcd=s.Poly(r*r+1,r)
    for p in remainders:repeat_gcd=s.gcd(repeat_gcd,p)
    assert repeat_gcd.degree()==0
    records.append({'e':e,'f':f,'gcd':'1','denominators_supported_at':'r=0,+1,-1 only','repeated_root_case':'excluded'})
    print(e,f,'PASS',flush=True)

# Check the mixed-projection identity before any specialization or division.
u0=k-aa*x;v0=aa*k-x
L=u0*t+v0*(t*t-2)
z0=-x*t+k*(t*t-2)
P,B,C,M=s.symbols('P B C M')
expr=s.rem(P*L**2+B*L+C+M*z0-t,t**3-3*t-x,t)
coef_t=s.Poly(expr,t).nth(1);coef_t2=s.Poly(expr,t).nth(2)
hh=u0**3-3*u0*v0*v0-x*v0**3
assert s.expand(v0*coef_t-u0*coef_t2+P*hh+M*(x**4-3*x*x+1)+v0)==0
assert s.Poly(hh,x).LC()==-aa**3

# Special a=+/-1 has L=0 on the indicated nonzero roots.
for sign in (1,-1):
    qx=x*x-sign*x-1
    assert s.rem(u0.subs(aa,sign),qx,x)==0
    assert s.rem(v0.subs(aa,sign),qx,x)==0
    assert s.rem(k-sign*x,qx,x)==0
    assert s.rem(s.Integer(1),qx,x)==1

out={'status':'PASS','cases_checked':len(records),'mixed_identity':'verified before specializing a',
     'leading_coefficient_h':'-a^3','a_zero':'covered by uniform theorem',
     'a_plus_minus_one':'L vanishes on roots x^2-a*x-1, C8 has nonzero t^2 coefficient',
     'M_zero':'degree(h)=7 > degree(v)=2 for a != 0',
     'cases':records}
Path(__file__).with_name('review_h378_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('ALL PASS')
