#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Verify sample kernel, plinth and image-ideal identities for the transfer construction.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact certificates for kernels/plinth ideals/filtration of coordinate transfers.

The theorem is proved in PROOF.md; these examples only test its constructive
steps. No floating-point arithmetic and no inference from unsuccessful search.
Run: python verify_transfer_filtration.py
"""
from pathlib import Path
import json
from math import factorial
import sympy as s

x, y, z, Y, Z, T, V = s.symbols('x y z Y Z T V')
OUT = Path(__file__).resolve().parent

def exact_div(a, b, gens=(x,y,z)):
    q, rem = s.div(s.Poly(s.expand(a), *gens, domain=s.QQ),
                   s.Poly(s.expand(b), *gens, domain=s.QQ))
    assert rem.is_zero, (a, b, rem)
    return q.as_expr()

def mod_x(f, modulus, *other):
    f = s.Poly(s.expand(f), *other, domain=s.QQ[x])
    result = 0
    for powers, coefficient in f.terms():
        c = s.rem(coefficient, modulus, x)
        result += c * s.prod(v**i for v,i in zip(other,powers))
    return s.expand(result)

def content_nonconstant(f):
    terms = s.Poly(f, y,z).terms()
    coeffs = [c for p,c in terms if p != (0,0)]
    g = s.Poly(coeffs[0],x)
    for c in coeffs[1:]:
        g = s.gcd(g,s.Poly(c,x))
    return g.monic().as_expr()

def inverse_mod(G, modulus):
    """Inverse of a one-variable coordinate over Q[x]/(modulus)."""
    a0 = G.subs(y,0)
    a1 = s.expand(G).coeff(y,1)
    inva1 = s.invert(a1,modulus,x)
    base = mod_x(inva1*(T-a0),modulus,T)
    nonlinear = s.expand(G-a0-a1*y)
    F = base
    # Nilradical nilpotency index is at most deg(modulus).
    for _ in range(s.degree(modulus,x)):
        F = mod_x(base-inva1*nonlinear.subs(y,F),modulus,T)
    assert mod_x(G.subs(y,F)-T,modulus,T)==0
    assert mod_x(F.subs(T,G)-y,modulus,y)==0
    return F

def monic_relation(G,J,pi,E):
    """Characteristic polynomial of J over B[G], B=Q[x]/pi**E.

    B[y] has basis 1,y,...,y**(e-1), where e=deg(G mod pi).
    Reduction is finite because the terms above degree e are nilpotent.
    """
    modulus = s.expand(pi**E)
    e = int(s.degree(mod_x(G,pi,y),y))
    ae = s.expand(G).coeff(y,e)
    ae_inv = s.invert(ae,modulus,x)
    equation = mod_x(ae_inv*(G-T),modulus,T,y)
    low = s.Add(*[c*y**k[0] for k,c in s.Poly(equation,y).terms() if k[0]<=e])
    tail = s.expand(equation-low)
    assert s.Poly(low,y).LC()==1
    def reduce_y(f):
        f=mod_x(f,modulus,T,y)
        total=0
        for _ in range(E):
            q,rem=s.div(f,low,y)
            total=mod_x(total+rem,modulus,T,y)
            f=mod_x(-q*tail,modulus,T,y)
        assert f==0
        assert s.degree(total,y)<e or total==0
        return total
    cols=[]
    for i in range(e):
        f=reduce_y(J*y**i)
        cols.append([s.expand(f).coeff(y,j) for j in range(e)])
    matrix=s.Matrix(e,e,lambda i,j:cols[j][i])
    P=mod_x(matrix.charpoly(V).as_expr(),modulus,T,V)
    assert s.Poly(P,V).degree()==e and s.Poly(P,V).LC()==1
    assert mod_x(P.subs({T:G,V:J},simultaneous=True),modulus,y)==0
    return P,e

cases = [
    ('quadratic_bad',Y,Z,y**2,x),
    ('nilpotent_good',Y,Z,y+x*y**2,x**2),
    ('scaled_bad',Y,Z,x*y**2,x**2),
    ('scaled_good',Y,Z,x*y,x**2),
    ('fully_scaled',Y,Z,x**2*y**2,x**2),
    ('mixed_good_bad',Y,Z,y+x*y**2,x**2*(x-1)**2),
    ('nonlinear_H_scaled_good',Y+Z**2,Z,-y**2+x*y+x**2*y**3,x**3),
    ('nonlinear_H_bad',Y+Z**2,Z,0,x**2),
    ('two_shears_bad',Y+(Z+Y**2)**2,Z+Y**2,0,x**2),
    ('nonlinear_W_bad',Y+Z**2,Z+(Y+Z**2)**2,0,x**2),
    ('swapped_good',Z,-Y,y**2,x**2),
    ('scaled_mixed',Y,Z,x*(y+x*y**2),x**3*(x-1)**2),
    ('irreducible_good',Y,Z,y+(x**2+1)*y**2,(x**2+1)**2),
    ('variable_residue_degree',Y,Z,y**2+x*y**3,x**2*(x-1)),
    ('harmonic_457_parameter',Y,Z,-y**3+3*y,x**2-2),
    ('mixed_cubic_linear',Y,Z,-x*y**3-(1-x)*y,x*(x-1)),
]

records=[]
for name,H,W,p,m in cases:
    print(name,flush=True)
    d=s.expand(s.diff(H,Y)*s.diff(W,Z)-s.diff(H,Z)*s.diff(W,Y))
    assert d in (1,-1)
    subst={Y:p+m*z,Z:y}
    h=s.expand(H.subs(subst,simultaneous=True))
    w=s.expand(W.subs(subst,simultaneous=True))
    c=h.subs({y:0,z:0})
    g=content_nonconstant(h)
    h0=exact_div(h-c,g)
    m1=exact_div(m,g)
    G=h0.subs(z,0)
    J=w.subs(z,0)
    D=lambda f:s.expand(s.diff(h,z)*s.diff(f,y)-s.diff(h,y)*s.diff(f,z))
    D0=lambda f:s.expand(s.diff(h0,z)*s.diff(f,y)-s.diff(h0,y)*s.diff(f,z))
    assert D(h0)==0 and s.expand(D(w)-d*m)==0
    assert s.expand(D0(w)-d*m1)==0
    assert exact_div(s.diff(h0,z),m1)==s.expand(s.diff(H,Y).subs(subst,simultaneous=True))
    factorization=s.factor_list(m1,x)
    factorization=(factorization[0],[(pi,int(E)) for pi,E in factorization[1]])
    good=1
    boundary=[]
    for pi,E in factorization[1]:
        Gpi=mod_x(G,pi,y)
        e=int(s.degree(Gpi,y))
        assert e>=1
        boundary.append({'prime':str(pi),'multiplicity':E,'degree':e,'G':str(Gpi)})
        if e==1:
            good*=pi**E
    r=s.expand(good)
    q0=exact_div(m1,r)
    if r==1:
        inverse=None
        phi=0
    else:
        inverse=inverse_mod(G,r)
        phi=mod_x(J.subs(y,inverse),r,T)
    S=exact_div(w-phi.subs(T,h0) if hasattr(phi,'subs') else w,r)
    assert s.expand(D(S)-d*g*q0)==0
    assert D(D(S))==0
    relations=[]
    # Verify finite local normal forms, including nilpotent higher terms.
    # The two-shear test is moderately larger, so n<=3 there.
    for item,(pi,E) in zip(boundary,factorization[1]):
        P,e=monic_relation(G,J,pi,E)
        numerator=s.expand(P.subs({T:h0,V:w},simultaneous=True))
        v=exact_div(numerator,pi**E)
        tested=[]
        for n in range(1,4 if name=='two_shears_bad' else 6):
            j,i=divmod(n,e)
            B=s.expand(w**i*v**j)
            derivative=B
            for _ in range(n):
                derivative=D0(derivative)
            expected=s.expand(factorial(n)*d**n*exact_div(m1**n,pi**(E*j)))
            assert s.expand(derivative-expected)==0,(name,pi,n)
            tested.append({'n':n,'i':i,'j':j,'D0_n_basis':str(expected),
                           'valuation_predicted':E*(n-n//e)})
        relations.append({'prime':str(pi),'exponent':E,'P':str(P),
                          'v':str(v),'tests':tested})
    records.append({'name':name,'H':str(H),'W':str(W),'p':str(p),'m':str(m),
                    'h':str(h),'w':str(w),'c':str(c),'g':str(g),'h0':str(h0),
                    'm1':str(m1),'boundary':boundary,'plinth_generator':str(s.expand(g*q0)),
                    'minimal_preslice':str(S),'D_preslice':str(s.expand(d*g*q0)),
                    'good_part':str(r),'inverse_mod_good_part':str(inverse),
                    'local_relations':relations,'verified':True})

result={'coefficient_field':'QQ','sympy_version':s.__version__,
        'case_count':len(records),'all_verified':all(r['verified'] for r in records),
        'scope':'Exact examples; general proof in PROOF.md. No novelty claim.',
        'cases':records}
(OUT/'certificates.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'cases':len(records),'all_verified':result['all_verified']}))
