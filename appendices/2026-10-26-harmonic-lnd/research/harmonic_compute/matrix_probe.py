import sympy as s
from math import gcd
x,t=s.symbols('x t')
def C(n,u=t): return s.expand(2*s.chebyshevt(n,u/2))
def coeff(n):
 p=s.Poly(s.rem(C(n),t**3-3*t-x,t),t)
 assert s.expand(p.coeff_monomial(1)+2*p.coeff_monomial(t*t))==0
 return [p.coeff_monomial(t),p.coeff_monomial(t*t)]
for b,c in [(4,5),(5,7),(7,8),(7,11),(8,13),(10,11),(10,17),(11,13),(11,19),(13,14),(13,17),(13,20),(13,23)]:
 M=s.Matrix([coeff(b),coeff(c)])
 print((3,b,c),'det=',s.factor(M.det()))
