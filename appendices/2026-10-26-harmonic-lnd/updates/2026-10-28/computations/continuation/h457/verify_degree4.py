# Consolidated verification copy, 28 October 2026.
# Purpose: Check degree-four parameter and relative-coordinate obstructions for H(4,5,7).
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact degree <= 4 obstruction for H(4,5,7), all three fixed projections.

Run: python verify_degree4.py
Only exact rational arithmetic is used.  The proof also uses the classical
degree-reduction theorem for plane polynomial automorphisms; see PROOF.md.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'python_deps'))
import json
import sympy as s

x,y,z,t,r,w,a,b,v,q,L,u=s.symbols('x y z t r w a b v q L u')
C=lambda n:s.Poly(2*s.chebyshevt(n,t/2),t,domain=s.QQ)
gamma=[C(n) for n in (4,5,7)]
F0=(x*x-2)*z-y**3+3*y
K=[
 x*x*z*z-x*x-x*y*y+2*x-y**3*z+3*y*z-z*z,
 x*x*y+x*y**3-x*y*y*z-2*x*y+x*z-y*z*z+z**3-2*z,
 x*x*y*z-x*y*y+x-y**4+3*y*y-2*y*z+z*z-2,
 x**3+x*x*y*y-2*x*x-x*z*z-x-y*y-y*z+2,
 x**3*z-x*x*z+x*y-3*x*z+y**3-y*z*z-2*y+2*z,
 x**3*y+x*x*z-x*y**3-x*y+x*z-y**3-y*y*z+y*z*z+y-z,
 x**4+x*x*y*y-5*x*x+x*y*y-x*y*z-x*z*z-y*y-z*z+4,
]
checks=[]
def zero(expr,label):
    assert s.cancel(s.expand(expr))==0,(label,s.expand(expr))
    checks.append(label)
def coeff(expr,gens,mon):
    return s.Poly(s.expand(expr),*gens).coeff_monomial(mon)

sub={c:p.as_expr() for c,p in zip((x,y,z),gamma)}
zero(F0.subs(sub, simultaneous=True)-t,'F0(gamma)=t')
for i,k in enumerate(K):zero(k.subs(sub, simultaneous=True),'K%d(gamma)=0'%i)
mons=[x**i*y**j*z**k for i in range(5) for j in range(5-i) for k in range(5-i-j)]
ps=[s.Poly(m.subs(sub,simultaneous=True),t) for m in mons]
A=s.Matrix([[p.nth(j) for p in ps] for j in range(29)])
N=s.Matrix([[s.Poly(k,x,y,z).coeff_monomial(m) for k in K] for m in mons])
assert A.rank()==28 and N.rank()==7 and A*N==s.zeros(29,7)
checks.append('complete affine family: 35 monomials, rank 28, kernel dimension 7')
cs=s.symbols('c0:7'); F=s.expand(F0+sum(c*k for c,k in zip(cs,K)))

# Fixed x, quartic branch c2=w != 0.
fx=s.expand(F.subs({cs[0]:0,cs[1]:0,cs[2]:w,cs[3]:v,cs[4]:u,cs[5]:u,cs[6]:q}))
Ax=coeff(fx,(y,z),z*z); Bx=coeff(fx,(z,),z); Cx=coeff(fx,(z,),1)
zero(Ax-(w-x*(v+q)-q),'x quartic z2 coefficient')
zero(coeff(Bx,(y,),y*y)+u,'x quartic y2z coefficient')
fx2=s.expand(fx.subs(q,-v)); Ax2=w+v
Bx2=s.expand(Bx.subs(q,-v)); Cx2=s.expand(Cx.subs(q,-v))
N4x=s.expand(4*Ax2*coeff(Cx2,(y,),y**4)-coeff(Bx2,(y,),y*y)**2)
zero(N4x-(-4*w*(w+v)-u*u),'x quartic fourth coefficient relation')
N3x=s.expand(4*Ax2*coeff(Cx2,(y,),y**3)-2*coeff(Bx2,(y,),y*y)*coeff(Bx2,(y,),y))
zero(coeff(N3x,(x,),x*x)-2*u*w,'x quartic cubic residual has x2 coefficient 2uw')
zero(coeff(Bx.subs({q:w,v:-w,u:0}),(y,),y)-w*(x*x-x-1),'x quartic linear-z branch cannot be coordinate')
# Fixed x, cubic branch: pure-cube condition forces all but c3,c6 zero.
fx3=s.expand(F0+v*K[3]+q*K[6])
zero(coeff(fx3,(y,z),z*z)-(-x*(v+q)-q),'x cubic z2 coefficient')
zero(coeff(fx3,(y,z),y*z)-(-v-q*x),'x cubic yz coefficient')
# A=0 forces q=v=0 by constant and x coefficients; F0 is a generic coordinate.
zero(s.diff(F0,y).subs(y,1),'F0 derivative y at critical locus')
zero(s.rem(s.diff(F0,z),x*x-2,x),'F0 derivative z at critical locus')
zero(s.diff(F0,x).subs(z,0),'F0 derivative x at critical locus')

# Fixed y, quartic branch c6=w != 0.
fy=s.expand(F.subs({cs[0]:0,cs[1]:0,cs[2]:a,cs[3]:-w,cs[4]:0,cs[5]:b,cs[6]:w}))
Ay=coeff(fy,(x,z),z*z); By=coeff(fy,(z,),z); Cy=coeff(fy,(z,),1)
zero(Ay-(a+b*y-w),'y quartic z2 coefficient')
zero(coeff(By,(x,),x*x)-(1+a*y+b),'y quartic x2z coefficient')
N4y=s.expand(4*Ay*w-coeff(By,(x,),x*x)**2)
zero(coeff(N4y,(y,),y*y)+a*a,'y quartic forces a=0')
zero(coeff(N4y.subs(a,0),(y,),y)-4*w*b,'y quartic forces b=0')
zero(N4y.subs({a:0,b:0})+4*w*w+1,'y quartic forces 4w2+1=0')
N3y=s.expand(4*Ay*coeff(Cy,(x,),x**3)-2*coeff(By,(x,),x*x)*coeff(By,(x,),x))
zero(N3y.subs({a:0,b:0})-(4*w*w+2*w*y),'y quartic cubic residual contradicts w!=0')
# Fixed y, cubic branches.
fy30=s.expand(F0-K[5]); zero(coeff(fy30,(x,z),z*z)+y,'y cubic c1=0 branch has z2=-y')
fy31=s.expand((F0-s.Rational(1,9)*K[1]+v*K[3]).subs(z,L-3*v*x))
fy31=s.Poly(fy31,v).rem(s.Poly(3*v*v+1,v)).as_expr()
zero(coeff(fy31,(x,),x*x)-(2*v*y*y/3-5*v/3-4*y/9),'y cubic c1!=0 branch has nonzero x2 coefficient')

# Fixed z, quartic branch with leading term -w(y+r*x)^4, w != 0.
cz=[a,-4*w*(r+r**3),w,w*(r**4-6*r*r),b,-4*w*r**3,-w*r**4]
fz=s.expand((F0+sum(c*k for c,k in zip(cz,K))).subs(y,L-r*x))
E30=coeff(fz,(x,L),x**3); E21=coeff(fz,(x,L),x*x*L)
zero(coeff(E21.subs(r,0),(z,),z)-w,'z quartic r=0 impossible')
aa=w*(1-8*r*r-8*r**4)/(3*r*r)
bb=w*(2*r-4*r**3-4*r**5)/3
E30s=s.factor(E30.subs({a:aa,b:bb}));E21s=s.factor(E21.subs({a:aa,b:bb}))
P=3*r**6-41*r**4+25*r*r+1
zero(-3*r*E21s-9*E30s-w*P,'z quartic necessary P(r2)=0')
Az=coeff(fz,(x,L),x*x).subs({a:aa,b:bb})
B2z=coeff(fz,(x,L),x*L*L).subs({a:aa,b:bb})
N4z=s.expand(-4*w*Az-B2z*B2z)
Q=48*r**8+96*r**6-8*r**4-56*r*r+7
zero(coeff(N4z,(z,),z*z)+w*w*Q/(3*r*r),'z quartic necessary Q(r2)=0')
Pu=3*u**3-41*u*u+25*u+1
Qu=48*u**4+96*u**3-8*u*u-56*u+7
BA=98443392*u**3+361976832*u*u+422233904*u+148292464
BB=-6152712*u*u+73768936*u+82963001
zero(BA*Pu+BB*Qu-729033471,'integer Bezout P,Q certificate')
# Fixed z, quartic leading pure x4 branch.
fz40=s.expand(F0+a*K[0]+b*K[4]+w*(K[6]-K[3]))
zero(coeff(fz40,(x,y),y**3)-(b-1-a*z),'z quartic pure-x4 y3 coefficient')
zero(coeff(fz40,(x,y),x*y*y)-(w-a),'z quartic pure-x4 xy2 coefficient')
# Fixed z, cubic branches: (a,b)=(0,0),(0,1).
zero(coeff(F0,(x,y),x*x)-z,'z cubic F0 has x2=z')
zero(coeff(F0+K[4],(x,y),x*y)-1,'z cubic F0+K4 has xy=1')

result={
 'status':'proved conditional only on classical plane automorphism degree-reduction theorem',
 'field':'any field of characteristic zero; contradictions remain valid after algebraic closure',
 'model':[str(p.as_expr()) for p in gamma],
 'F0':str(F0),'kernel_degree4_basis':[str(k) for k in K],
 'rank_evaluation_degree4':28,'number_monomials_degree4':35,'kernel_dimension_degree4':7,
 'conclusions':{
  'over_k(x)':'only F0 is a coordinate among parameter polynomials of total degree <=4',
  'over_k(y)':'no coordinate among parameter polynomials of total degree <=4',
  'over_k(z)':'no coordinate among parameter polynomials of total degree <=4',
  'over_k[x],k[y],k[z]':'no relative coordinate parameter of total degree <=4',
  'absolute_rectifiability':'NOT decided; no claim about absolute coordinates of degree4 or higher'},
 'bezout':{'variable':'u=r^2','P':str(Pu),'Q':str(Qu),'A':str(BA),'B':str(BB),'constant':729033471},
 'checks_passed':checks,'checks_count':len(checks),
 'source_classical_lemma':'https://arxiv.org/pdf/math/0408077; Division Lemma and degree reduction in sections 2 and 4'
}
target=Path(__file__).with_name('degree4_certificate.json')
target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'checks_passed':len(checks),'rank':28,'kernel_dimension':7,'certificate':str(target)},ensure_ascii=False))
