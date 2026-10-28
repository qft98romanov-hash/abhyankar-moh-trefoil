#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check exact divergence obstructions to the naive normal Euler construction.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact controls for the uniform divergence obstruction to naive Euler lifts.

The universal exclusion is proved in PROOF.md.  This program does not infer
non-nilpotence from a finite list of nonzero iterates.
"""
from pathlib import Path
import json
import sympy as s

x, y, z, u, v = s.symbols('x y z u v')
Y = (x, y, z)

def C(n, q):
    a, b = s.Integer(2), q
    if n == 0:
        return a
    for _ in range(1, n):
        a, b = b, s.expand(q*b-a)
    return b

def check(triple, P):
    gamma = tuple(C(n,u) for n in triple)
    subst = dict(zip(Y,gamma))
    assert s.expand(P.subs(subst, simultaneous=True)-u) == 0
    grad = s.Matrix([s.diff(P,q) for q in Y])
    grad_curve = grad.subs(subst, simultaneous=True).applyfunc(s.expand)
    tangent = s.Matrix([s.diff(f,u) for f in gamma])
    assert s.expand((grad_curve.T*tangent)[0]-1) == 0
    J = s.eye(3)-tangent*grad_curve.T
    assert (J*J-J).applyfunc(s.expand) == s.zeros(3)
    assert s.expand(s.trace(J)-2) == 0
    assert (J*tangent).applyfunc(s.expand) == s.zeros(3,1)

    div = s.expand(3-sum(s.diff(C(n,v),v).subs(v,P)*s.diff(P,q)
                        for n,q in zip(triple,Y)))
    r = s.Poly(P,*Y).total_degree()
    active = [i for i,q in enumerate(Y) if s.diff(P,q) != 0]
    lead_i = max(active, key=lambda i: triple[i])
    term_degrees = {i:r*(triple[i]-1)+s.Poly(s.diff(P,Y[i]),*Y).total_degree()
                    for i in active}
    expected_degree = term_degrees[lead_i]
    assert all(expected_degree > d for i,d in term_degrees.items() if i != lead_i)
    assert s.Poly(div,*Y).total_degree() == expected_degree

    def top(f,d):
        return s.Add(*(coef*x**mon[0]*y**mon[1]*z**mon[2]
                       for mon,coef in s.Poly(f,*Y).terms() if sum(mon)==d))
    lead_P=top(P,r)
    dgrad=s.Poly(s.diff(P,Y[lead_i]),*Y).total_degree()
    expected_top=-triple[lead_i]*lead_P**(triple[lead_i]-1)*top(s.diff(P,Y[lead_i]),dgrad)
    assert s.expand(top(div,expected_degree)-expected_top)==0

    # Restrict divergence before substituting into the large composed polynomial.
    div_curve=3-sum(s.diff(f,u)*g for f,g in zip(gamma,grad_curve))
    assert s.expand(div_curve-2)==0

    # h=2-div lies in I; first-order divergence correction is (1+h/3)delta.
    # Its divergence minus 2 is (delta h-h-h^2)/3, in I^2.
    # Verify the exact first-jet identity without expanding delta(h) globally.
    h=2-div
    h_grad_curve=s.Matrix([s.diff(h,q).subs(subst,simultaneous=True) for q in Y]).applyfunc(s.expand)
    assert s.expand((h_grad_curve.T*tangent)[0])==0
    assert (J.T*h_grad_curve-h_grad_curve).applyfunc(s.expand)==s.zeros(3,1)
    return {
        'triple':list(triple), 'parameter':str(P), 'parameter_degree':int(r),
        'divergence_degree':int(expected_degree),
        'divergence_leading_form':str(s.factor(expected_top)),
        'divergence_on_curve':2,
        'normal_projector_check':'PASS',
        'first_order_divergence_correction_check':'PASS',
        'status':'NAIVE_E_NOT_LND_BY_THEOREM'
    }

def main():
    records=[
        check((3,4,5),y*z-x**3+3*x),
        check((3,5,7),(x*x-1)*z-x*y*y+2*x),
        check((4,5,7),(x*x-2)*z-y**3+3*y),
    ]
    result={'date':'2026-10-28', 'arithmetic':'exact rational',
            'scope':'Three exact controls; the all-P theorem is proved in prose',
            'cases':records,'status':'PASS'}
    path=Path(__file__).resolve().with_name('euler_obstruction_certificate.json')
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for record in records:
        print(record['triple'], 'divergence degree',record['divergence_degree'],'PASS')
    print('ALL EXACT EULER OBSTRUCTION CONTROLS PASSED')

if __name__=='__main__':
    main()
