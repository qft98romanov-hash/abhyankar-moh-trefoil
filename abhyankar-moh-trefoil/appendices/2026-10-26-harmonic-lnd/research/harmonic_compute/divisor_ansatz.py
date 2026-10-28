import sympy as s
from itertools import product
x,r=s.symbols('x r');k=x*x-1;de=k*k-x*x
A=r;B=r*r-1;u=B*k-A*x;v=A*k-B*x
h=s.Poly(u**3-3*u*v*v-x*v**3,x,domain=s.QQ.frac_field(r))
vpoly=s.Poly(v,x,domain=s.QQ.frac_field(r))
for total in range(1,13):
 for e in range(total+1):
  f=total-e
  if e==f==0:continue
  R=s.Poly((x-r)**e*(r*x+1)**f*de,x,domain=s.QQ.frac_field(r)).rem(h)
  constraints=[]
  for i in range(3,7):
   q=s.cancel(R.nth(i));n=q.as_numer_denom()[0]
   if n!=0:constraints.append(s.Poly(n,r))
  for i,j in ((0,1),(0,2),(1,2)):
   q=s.cancel(R.nth(i)*vpoly.nth(j)-R.nth(j)*vpoly.nth(i));n=q.as_numer_denom()[0]
   if n!=0:constraints.append(s.Poly(n,r))
  if not constraints:print('IDENTITY',e,f,flush=True);continue
  g=constraints[0]
  for q in constraints[1:]:g=s.gcd(g,q)
  # exclude degenerate parameter roots r=0,+-1; special poles require independent analysis
  fac=s.factor_list(g.as_expr())[1]
  rem=[(p,n) for p,n in fac if s.degree(p,r)>1 or p not in (r,r-1,r+1)]
  if rem:print('CANDIDATE',e,f,rem,flush=True)
 print('TOTAL',total,'complete',flush=True)
