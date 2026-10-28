# Consolidated verification copy, 28 October 2026.
# Purpose: Check bounded parameter-space and transfer-obstruction identities, without asserting rectifiability.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
from pathlib import Path
"""Exact certificates for finite claims in results.tex; not a rectification certificate."""
import sympy as s
import json,sys,platform
from itertools import product
x,y,z,t,r,alpha,beta=s.symbols('x y z t r alpha beta')
C=lambda n,u=t:s.expand(2*s.chebyshevt(n,u/2))
checks=[]
def verify(label,condition):
 if not condition:raise AssertionError(label)
 print('PASS:',label,flush=True);checks.append(label)
verify('Chebyshev product for H378 transfer',s.expand(C(2,C(3))*C(8)-C(7)**2+2-C(2))==0)
verify('target H(3,2,7) parameter',s.expand(C(3)*(C(2)**2-2)-C(7)-t)==0)
red=lambda p:s.rem(s.rem(s.expand(p),t**3-3*t-r,t),r*r-2,r).expand()
verify('C7 on x^2=2 fibres',red(C(7)-(t-r*(t*t-2)))==0)
verify('centre relation on same fibres',red(2-C(7)**2-C(2))==0)
rem=s.Poly(red(t-alpha*C(7)-beta),t)
verify('linear centre would force alpha=1 and alpha*r=0',rem.coeff_monomial(t)==1-alpha and rem.coeff_monomial(t*t)==alpha*r)
F=(x*x-2)*z-y**3+3*y
verify('parameter F for H457',s.expand(F.subs({x:C(4),y:C(5),z:C(7)},simultaneous=True)-t)==0)
for d in (1,2,3):
 mons=[(i,j,k) for i in range(d+1) for j in range(d-i+1) for k in range(d-i-j+1)]
 vals=[s.Poly(C(4)**i*C(5)**j*C(7)**k,t) for i,j,k in mons]
 md=max(p.degree() for p in vals)
 mat=s.Matrix([[p.nth(n) for p in vals] for n in range(md+1)])
 rhs=s.Matrix([int(n==1) for n in range(md+1)])
 ra,rb=mat.rank(),mat.row_join(rhs).rank()
 print('H457 degree',d,'columns',len(mons),'rank',ra,'augmented',rb,flush=True)
 verify('H457 parameter degree '+str(d),ra<rb if d<3 else ra==rb==len(mons))
verify('F457 has critical points',all(s.rem(s.rem(s.diff(F,v).subs(z,0),x*x-2,x),y*y-1,y)==0 for v in (x,y,z)))
# All degree <= 4 parameter polynomials for H378, and a relative obstruction.
d=4; mons=[(i,j,k) for i in range(d+1) for j in range(d-i+1) for k in range(d-i-j+1)]
vals=[s.Poly(C(3)**i*C(7)**j*C(8)**k,t) for i,j,k in mons]
md=max(p.degree() for p in vals)
mat=s.Matrix([[p.nth(n) for p in vals] for n in range(md+1)])
rhs=s.Matrix([int(n==1) for n in range(md+1)])
sol,free=mat.gauss_jordan_solve(rhs)
H=s.expand(sum(co*x**i*y**j*z**k for co,(i,j,k) in zip(sol,mons)))
verify('H378 degree <=4 solution space has dimension 2',len(free)==2)
verify('H378 every degree <=4 parameter has relative critical point (0,0,1)',all(s.diff(H,w).subs({x:0,y:0,z:1})==0 for w in (y,z)))
verify('relative obstruction is not a full gradient obstruction',s.diff(H,x).subs({x:0,y:0,z:1})==-3)
# Exact polynomial identities for the cubic-projection matrix.
for n in range(1,41):
 if n%3==0:continue
 q=n//3;U=lambda j:0 if j<0 else s.chebyshevu(j,x/2)
 A,B=(U(q),-U(q-1)) if n%3==1 else (-U(q-1),U(q))
 verify('matrix representation n='+str(n),s.rem(C(n)-A*t-B*(t*t-2),t**3-3*t-x,t).expand()==0)
with open(str(Path(__file__).resolve().with_name('verification.json')),'w') as f:
 json.dump({'python':sys.version,'sympy':s.__version__,'checks':checks,'count':len(checks),'scope':'Exact finite identities; no claim of H378/H457 rectification'},f,indent=2)
print('ALL',len(checks),'CHECKS PASSED')
