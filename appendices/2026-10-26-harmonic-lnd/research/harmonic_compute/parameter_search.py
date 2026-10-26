import sympy as s
from itertools import product
x,y,z,t=s.symbols('x y z t')
C=lambda n:s.Poly(2*s.chebyshevt(n,t/2),t,domain=s.QQ)
def search(triple,maxdeg):
 vals=[C(n) for n in triple]
 for d in range(1,maxdeg+1):
  mons=[(i,j,k) for i in range(d+1) for j in range(d-i+1) for k in range(d-i-j+1)]
  ps=[vals[0]**i*vals[1]**j*vals[2]**k for i,j,k in mons]
  md=max(p.degree() for p in ps); A=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix([[p.nth(q) for p in ps] for q in range(md+1)]))
  mat=A.to_Matrix(); rhs=s.Matrix([int(q==1) for q in range(md+1)])
  try:
   sol,free=mat.gauss_jordan_solve(rhs)
  except ValueError:continue
  sol=sol.subs({v:0 for v in free})
  H=s.expand(sum(co*x**i*y**j*z**k for co,(i,j,k) in zip(sol,mons)))
  assert s.expand(H.subs({x:vals[0].as_expr(),y:vals[1].as_expr(),z:vals[2].as_expr()}, simultaneous=True)-t)==0
  print(triple,'mindeg',d,'freedim',len(free),'H=',H,flush=True)
  return H
for tr in ((3,4,5),(3,5,7),(3,7,8),(3,7,11),(4,5,7),(5,6,7)):
 search(tr,8)
