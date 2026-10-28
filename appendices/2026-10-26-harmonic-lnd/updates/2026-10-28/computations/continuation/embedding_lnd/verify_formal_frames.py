#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check explicit normal frames; the general formal-triviality assertion requires the written proof.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Standard-library certificates for the explicit normal frames in §10.

Checks a=grad(P)∘γ, aγ'=1, l_iγ'=0 and det(l_1,l_2,a)=1.
Together with the stated universal Taylor calculation these certify the
initial coordinate map used in all infinitesimal trivializations.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from verify_jet_certificates import cn, plus, times, trim, retraction

HERE=Path(__file__).resolve().parent
def neg(a):return [-x for x in a]
def derivative(a):return trim([i*a[i] for i in range(1,len(a))] or [0])
def scale(a,c):return trim([x*c for x in a])
def divide(a,b):
    a=list(map(Q,a));b=list(map(Q,b));q=[Q(0)]*max(1,len(a)-len(b)+1)
    while a!=[0] and len(a)>=len(b):
        j=len(a)-len(b);c=a[-1]/b[-1];q[j]+=c
        a=plus(a,[Q(0)]*j+scale(b,-c))
    return trim(q),trim(a)
def xgcd(f,g):
    r0,r1=list(map(Q,f)),list(map(Q,g))
    a0,a1=[Q(1)],[Q(0)];b0,b1=[Q(0)],[Q(1)]
    while r1!=[0]:
        q,r=divide(r0,r1)
        r0,r1=r1,r
        a0,a1=a1,plus(a0,neg(times(q,a1)))
        b0,b1=b1,plus(b0,neg(times(q,b1)))
    assert len(r0)==1 and r0[0]
    return scale(a0,1/r0[0]),scale(b0,1/r0[0])
def evaluate(P,cs):
    total=[Q(0)]
    for beta,c in P.items():
        q=[c]
        for f,n in zip(cs,beta):
            for _ in range(n):q=times(q,f)
        total=plus(total,q)
    return total
def pder(P,i):
    out={}
    for a,c in P.items():
        if a[i]:
            b=list(a);b[i]-=1;out[tuple(b)]=c*a[i]
    return out
def dot(a,b):
    out=[Q(0)]
    for x,y in zip(a,b):out=plus(out,times(x,y))
    return out
def determinant(rows):
    p=rows
    return plus(plus(times(p[0][0],plus(times(p[1][1],p[2][2]),neg(times(p[1][2],p[2][1])))),
                     neg(times(p[0][1],plus(times(p[1][0],p[2][2]),neg(times(p[1][2],p[2][0])))))),
                times(p[0][2],plus(times(p[1][0],p[2][1]),neg(times(p[1][1],p[2][0])))))

results=[]
for triple in [(3,4,5),(3,5,7),(4,5,7),(3,7,8),(3,10,11),(3,13,14),(5,7,8),(7,10,11)]:
    cs=[cn(n) for n in triple];v=[derivative(f) for f in cs];P=retraction(triple)
    a=[evaluate(pder(P,i),cs) for i in range(3)]
    A,B=xgcd(v[0],v[1])
    l1=[v[1],neg(v[0]),[0]]
    l2=[times(A,v[2]),times(B,v[2]),[-1]]
    assert dot(a,v)==[1]
    assert dot(l1,v)==[0] and dot(l2,v)==[0]
    assert determinant([l1,l2,a])==[1]
    encode=lambda row:[[str(c) for c in p] for p in row]
    results.append({'triple':list(triple),'bezout_A':[str(c) for c in A],'bezout_B':[str(c) for c in B],'gradient_parameter':encode(a),'normal_row_1':encode(l1),'normal_row_2':encode(l2),'determinant':'1'})
    print('FORMAL FRAME CERTIFIED',triple,'determinant 1',flush=True)
(HERE/'formal_frames.json').write_text(json.dumps({'coefficient_order':'ascending powers of u','arithmetic':'fractions.Fraction; exact','results':results},indent=2)+'\n')
print('ALL 8 NORMAL FRAMES PASSED')
