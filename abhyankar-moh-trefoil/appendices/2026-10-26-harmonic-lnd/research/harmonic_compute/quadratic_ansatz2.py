from pathlib import Path
import sympy as s
import json
results=[]
x=s.symbols('x');k=x*x-1;delta=k*k-x*x
for da in (1,3,5):
 aa=s.symbols('a0:'+str((da+1)//2));A=sum(c*x**(2*i+1) for i,c in enumerate(aa))
 u=k-A*x;v=-x+A*k;h=s.expand(u**3-3*u*v*v-x*v**3)
 for dp in (1,3,5):
  if da==5 and dp==5:continue  # Excluded: this system was not completed.
  pp=s.symbols('p0:'+str((dp+1)//2));P=sum(c*x**(2*i+1) for i,c in enumerate(pp));m=s.symbols('m')
  e=3*da+7+dp-4
  eq=s.Poly(h*P+v+m*x**e*delta,x)
  print('START',da,dp,e,flush=True)
  gb=s.groebner(eq.all_coeffs(),*pp,m,*aa)
  print('END',da,dp,'basis',list(gb),flush=True)
  results.append({'degree_A_bound':da,'degree_P_bound':dp,'e':e,'basis':[str(g) for g in gb]})
  with open(str(Path(__file__).resolve().with_name('quadratic_ansatz2.json')),'w') as f:json.dump(results,f,indent=2)
print('COMPLETE:',len(results),'systems; unit ideals:',sum(r['basis']==['1'] for r in results))
