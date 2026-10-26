"""Точное вычисление примера переноса с кратным корнем m=x**2."""
import sympy as s

x, y, z, T, Q = s.symbols("x y z T Q")
h = y + x*y**2 + x**2*z
# Обратный центра y+x*y**2 по модулю x**2: f(T)=T-x*T**2.
q = s.cancel((y - h + x*h**2) / x**2).expand()
assert s.denom(q) == 1

def D(poly):
    return s.expand(x**2*s.diff(poly, y) - (1+2*x*y)*s.diff(poly, z))

yi = T - x*T**2 + x**2*Q
zi = s.cancel((T - yi - x*yi**2)/x**2).expand()
assert s.denom(zi) == 1
assert D(h) == 0 and D(q) == 1
assert s.expand(h.subs({y: yi, z: zi}, simultaneous=True)) == T
assert s.expand(q.subs({y: yi, z: zi}, simultaneous=True)) == Q
assert s.expand(yi.subs({T: h, Q: q}, simultaneous=True)) == y
assert s.expand(zi.subs({T: h, Q: q}, simultaneous=True)) == z
assert s.det(s.Matrix([h, q]).jacobian([y, z])).expand() == -1
assert D(D(D(z))) == 0
print("h =", h)
print("q =", q)
print("inverse y =", yi)
print("inverse z =", zi)
print("D(h)=0; D(q)=1; det=-1; both inverse compositions: VERIFIED")
