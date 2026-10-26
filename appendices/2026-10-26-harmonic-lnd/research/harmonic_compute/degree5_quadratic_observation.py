"""Finite observation for H378. Scope: total degree<=5 and relative (y,z) degree<=2.
Not a claim concerning all degree 5 coordinates or arbitrary rectification.
"""
import sympy as s
x,y,z,t,a,b=s.symbols('x y z t a b')
C=lambda n,u=t:s.Poly(2*s.chebyshevt(n,u/2),u).as_expr()
F=y*z-C(5,x)
G=y*y-z*z+C(3,x)*y-C(2,x)*z
assert s.expand(F.subs({x:C(3),y:C(7),z:C(8)}, simultaneous=True)-t)==0
assert s.expand(G.subs({x:C(3),y:C(7),z:C(8)}, simultaneous=True))==0
mons=[(i,j,k) for i in range(6) for j in range(min(2,5-i)+1) for k in range(min(2-j,5-i-j)+1)]
polys=[s.Poly(C(3)**i*C(7)**j*C(8)**k,t) for i,j,k in mons]
md=max(p.degree() for p in polys)
M=s.Matrix([[p.nth(n) for p in polys] for n in range(md+1)])
rhs=s.Matrix([int(n==1) for n in range(md+1)])
sol,free=M.gauss_jordan_solve(rhs)
H=s.expand(sum(c*x**i*y**j*z**k for c,(i,j,k) in zip(sol,mons)))
assert len(free)==2
assert s.expand(H-(F+(free[0]+x*free[1])*G))==0
print('PASS: all parameters in the specified finite space are F+(a+b*x)G')
q=a+b*x
D=s.expand(-4*q*q-1)
print('Rank-one condition on homogeneous quadratic part:',D,'=0')
# Over C this forces b=0, a=+/-i/2. At those values, a quadratic plane
# coordinate can occur only if its linear component is independent of its
# quadratic direction on every x-fibre.
for sign in (1,-1):
 aa=sign*s.I/2
 H=s.expand(F+aa*G)
 L=y-sign*s.I*z
 assert s.expand(H-aa*L**2-aa*C(3,x)*y+aa*C(2,x)*z+C(5,x))==0
 J=s.expand(-aa*C(2,x)+sign*s.I*aa*C(3,x))
 assert s.degree(J,x)==3
 print('Candidate a=',aa,'has determinant',J,'of degree 3; thus exceptional roots over C')
print('FINITE OBSERVATION VERIFIED; no relative coordinate in this restricted space.')
