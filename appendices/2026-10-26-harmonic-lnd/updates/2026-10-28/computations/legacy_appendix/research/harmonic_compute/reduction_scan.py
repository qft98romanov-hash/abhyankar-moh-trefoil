# Consolidated verification copy, 28 October 2026.
# Purpose: Enumerate only the specified strictly decreasing Chebyshev moves within finite index bounds.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
from pathlib import Path
"""Exact finite scan of ONLY strictly decreasing Chebyshev involutions.
All indices positive; sorted triples; pairwise coprime.  C_r(C_a)C_s(C_b)-C_c=C_|ra-sb|
when c=ra+sb.  No claim that failure detects nonrectifiability.
"""
from math import gcd
from functools import lru_cache
from itertools import combinations
import json
BASES={(3,4,5),(3,5,7)}
@lru_cache(None)
def children(v):
 a,b,c=v; out=[]
 for r in range(1,c//a+1):
  n=c-r*a
  if n>0 and n%b==0:
   s=n//b;d=abs(r*a-s*b)
   if d:
    w=tuple(sorted((a,b,d)))
    if w!=v: out.append((w,r,s))
 return tuple(sorted(out))
@lru_cache(None)
def cores(v):
 if v[0]==1:return frozenset({(1,1,1)})
 nxt=children(v)
 if not nxt:return frozenset({v})
 return frozenset().union(*(cores(w) for w,_,_ in nxt))
@lru_cache(None)
def known(v):
 cs=cores(v)
 if (1,1,1) in cs:return 'Q'
 if cs&BASES:return 'Q(sqrt(-3))'
 return 'unresolved_by_this_algorithm'
summary={}
for bound in (20,50,100):
 vs=[v for v in combinations(range(2,bound+1),3) if all(gcd(v[i],v[j])==1 for i,j in ((0,1),(0,2),(1,2))) ]
 counts={k:sum(known(v)==k for v in vs) for k in ('Q','Q(sqrt(-3))','unresolved_by_this_algorithm')}
 uns=sorted(set().union(*(cores(v) for v in vs if known(v).startswith('unresolved'))))
 summary[str(bound)]={'total':len(vs),**counts,'distinct_unresolved_cores':len(uns),'first_30_unresolved_cores':uns[:30]}
 print(bound,summary[str(bound)],flush=True)
with open(str(Path(__file__).resolve().with_name('reduction_scan.json')),'w') as f:json.dump(summary,f,indent=2)
