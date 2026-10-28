from pathlib import Path
import sympy as s
import json
results=[]
x,c,p,m=s.symbols('x c p m');k=x*x-1;delta=k*k-x*x
for A in [c,c*x,c*x*x,c*x**3]:
 u=k-A*x;v=-x+A*k;h=s.expand(u**3-3*u*v*v-x*v**3)
 print('A=',A,'h=',s.factor(h),flush=True)
 for e in range(1,17):
  # coefficient equations h*P+v+m*x^e*delta=0
  dh=s.degree(h,x);N=e+4-dh
  if N<0 or N>6:continue
  ps=s.symbols('p0:'+str(N+1));P=sum(ps[i]*x**i for i in range(N+1))
  eq=s.Poly(h*P+v+m*x**e*delta,x)
  gb=s.groebner(eq.all_coeffs(),*ps,m,c)
  result={'A':str(A),'e':e,'degree_P_bound':int(N),'basis':[str(g) for g in gb]}
  results.append(result)
  print(result,flush=True)
with open(str(Path(__file__).resolve().with_name('quadratic_ansatz.json')),'w') as f:json.dump(results,f,indent=2)
print('COMPLETE:',len(results),'systems; unit ideals:',sum(r['basis']==['1'] for r in results))
