"""Independent low-degree proof certificates for the base coordinate.
Run with SymPy 1.14.0. Exact arithmetic, no numerical evaluation.
"""
import json
from pathlib import Path
from sympy import QQ
from sympy.polys.rings import ring

R,a,x,y,z,v,T=ring('a,x,y,z,v,T',QQ)
rel=a*a-a+1
def red(p): return p%rel
def sub(p, **values):
    images=[values.get(str(g),g) for g in R.gens]
    out=R.zero
    for powers,c in p.to_dict().items():
        t=R(c)
        for image,n in zip(images,powers): t=red(t*image**n)
        out+=t
    return red(out)
def eq(name,p):
    if red(p)!=0: raise AssertionError(name)
    print('PASS:',name)
    results.append(name)
def trunc(p,n):
    return R.from_dict({mon:c for mon,c in red(p).to_dict().items() if mon[1]<n})
results=[]
b=1-a
A=-1+a*x**2-a*x**4
q=-2*x**5+(6-2*a)*x**3-2*b*x
h0=b*x*v**2+A*v+q
H=a*x**3*y**2+2*x**2*y*z+b*x*z**2+((a-1)*x**3-a*x)*y+A*z+q
eq('H = h0(x,z+a*x*y) - (1-a)*x^5*y', H-sub(h0,v=z+a*x*y)+b*x**5*y)
f=(-T+x*(b*T**2+2*a-2)+x**2*(2*a*T**3-5*a*T)
   +x**3*(-5*T**4+15*T**2-2*a)
   +x**4*(14*b*T**5-50*b*T**3+(29-24*a)*T))
eq('f(h0(v)) = v modulo x^5',trunc(sub(f,T=h0)-v,5))
eq('h0(f(T)) = T modulo x^5',trunc(sub(h0,v=f)-T,5))
def D(p): return red(H.diff(z)*p.diff(y)-H.diff(y)*p.diff(z))
eq('D(x)=0',D(x))
eq('D(H)=0',D(H))
eq('D(v)=(1-a)*x^5',D(z+a*x*y)-b*x**5)
eq('D(y)=2*(1-a)*x*v+A',D(y)-sub(2*b*x*v+A,v=z+a*x*y))
eq('D^3(y)=0',D(D(D(y))))
eq('D^3(z)=0',D(D(D(z))))
N=red(a*(a*x*y+z-sub(f,T=H)))
eq('slice numerator derivative is x^5',D(N)-x**5)
eq('slice numerator vanishes modulo x^5',trunc(N,5))
# Harmonic transfer gives another globally nilpotent Jacobian derivation.
hH=sub(H,y=x*z-y*y+2,z=y)
def DH(p): return red(hH.diff(z)*p.diff(y)-hH.diff(y)*p.diff(z))
eq('harmonic DH(x)=0',DH(x))
eq('harmonic DH(hH)=0',DH(hH))
eq('harmonic DH^3(y)=0',DH(DH(DH(y))))
eq('harmonic DH^5(z)=0',DH(DH(DH(DH(DH(z))))))
if not DH(DH(y)) or not DH(DH(DH(DH(z)))):
    raise AssertionError('Expected exact harmonic nilpotency orders 3 and 5')
print('PASS: harmonic nilpotency orders for y and z are exactly 3 and 5')
results.append('harmonic nilpotency orders for y and z are exactly 3 and 5')
# W=N/x^5 is polynomial, hence D(W)=1. Since D(x)=D(H)=0,
# H,h0,f identities give the polynomial inverse by the explicit formula below:
# v=f(T)+(1-a)*x^5*W,
# y=(h0(v)-T)/((1-a)*x^5), z=v-a*x*y.
# The second division is polynomial by h0(f(T))=T mod x^5.
Path(__file__).with_suffix('.json').write_text(json.dumps({'passed':results,'count':len(results)},indent=2))
print('ALL INDEPENDENT BASE AND LND CERTIFICATES PASSED')
