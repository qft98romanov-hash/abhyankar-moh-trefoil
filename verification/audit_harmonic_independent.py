"""Literal appendix audit: recursive-descent TeX parser + independent SymPy parser.
Run: python -u audit_harmonic_independent.py --repository /path/to/repository [--expect-correct]
No original files are modified. All arithmetic is exact.
"""
import os
os.environ['SYMPY_GROUND_TYPES']='python'
import ast, re, json, hashlib, time, argparse, sys
from functools import lru_cache
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
def require(condition, message="Validation failed"):
    """Keep validation and parser token consumption active under python -O."""
    if not condition:
        raise AssertionError(message)

cli=argparse.ArgumentParser(description=__doc__)
cli.add_argument('--repository',type=Path,required=True,help='Directory containing verify.py and paper/')
cli.add_argument('--tex',type=Path,help='Alternate harmonic_explicit.tex')
cli.add_argument('--expect-correct',action='store_true',help='Exit 1 if any printed component differs from compact formulas')
cli.add_argument('--json',type=Path,help='Optional JSON results path')
args=cli.parse_args()
SRC=args.repository.resolve()
TEX=args.tex.resolve() if args.tex else SRC/'paper/harmonic_explicit.tex'
start=time.perf_counter()
print('SymPy',sp.__version__)
for path in [SRC/'verify.py',TEX]:
    print('SHA256',path.name,hashlib.sha256(path.read_bytes()).hexdigest())
# Load setup and both compact constructions; omit top-level checks.
module=ast.parse((SRC/'verify.py').read_text())
kept=[]
for node in module.body:
    if isinstance(node,ast.Expr): continue
    kept.append(node)
ns={}
exec(compile(ast.Module(body=kept,type_ignores=[]),'verify.py [checks omitted]','exec'),ns)
ring,a,x,y,z,t=(ns[v] for v in ['ring','a','x','y','z','t'])
red,at=ns['red'],ns['at']
zero,one=ring(0),ring(1)
print('Both compact constructions loaded in',round(time.perf_counter()-start,3),'seconds')
# The parser reads actual TeX, erasing only presentation commands.
COMMANDS={'bigl','bigr','Bigl','Bigr','Biggl','Biggr','left','right','qquad','quad','times'}
class TexParser:
    def __init__(self,source):
        self.tokens=[]
        p=0
        while p<len(source):
            c=source[p]
            if c.isspace() or c=='&': p+=1; continue
            if source[p:p+2]=='\\\\': p+=2; continue
            if source[p:p+2]=='{}': p+=2; continue
            if source[p:p+2] in ('\\{','\\}'):
                self.tokens.append(source[p+1]);p+=2;continue
            if c=='\\':
                m=re.match(r'\\([A-Za-z]+)',source[p:])
                if not m or m.group(1) not in COMMANDS: raise ValueError(('Unknown TeX command',source[p:p+40]))
                p+=len(m.group()); continue
            if c.isdigit():
                m=re.match(r'\d+',source[p:]);self.tokens.append(m.group());p+=len(m.group());continue
            if c in 'axyzXYZ+-^()[]{}': self.tokens.append(c);p+=1;continue
            if c=='.' and not source[p+1:].strip(): p+=1;continue
            raise ValueError(('Unknown character',c,source[p:p+30]))
        self.tokens.append('EOF'); self.pos=0
    def peek(self): return self.tokens[self.pos]
    def consume(self): tok=self.peek();self.pos+=1;return tok
    def expr(self):
        result=self.product()
        while self.peek() in ('+','-'):
            op=self.consume();q=self.product();result=result+q if op=='+' else result-q
        return result
    def product(self):
        sign=1
        while self.peek() in ('+','-'):
            if self.consume()=='-': sign=-sign
        result=self.power()*sign
        while self.peek().isdigit() or self.peek() in 'axyzXYZ' or self.peek() in ('(','[','{'):
            result=red(result*self.power())
        return result
    def power(self):
        result=self.atom()
        if self.peek()=='^':
            self.consume()
            if self.peek()=='{':
                self.consume(); exponent=int(self.consume()); require(self.consume()=='}', 'Validation failed')
            else: exponent=int(self.consume())
            result=red(result**exponent)
        return result
    def atom(self):
        token=self.consume()
        if token.isdigit(): return ring(int(token))
        if token in {'a','x','y','z','X','Y','Z'}: return {'a':a,'x':x,'y':y,'z':z,'X':x,'Y':y,'Z':z}[token]
        if token in ('(','[','{'):
            close={'(':')','[':']','{':'}'}[token]
            result=self.expr()
            require(self.consume()==close, 'Validation failed')
            return result
        raise ValueError(('Bad atom',token,self.pos))
    def parse(self):
        result=red(self.expr());require(self.peek()=='EOF', 'Validation failed');return result

tex=TEX.read_text()
blocks=re.findall(r'\\begin\{(?:align\*|gather\*)\}(.*?)\\end\{(?:align\*|gather\*)\}',tex,re.S)
require(len(blocks)==6, len(blocks))
bodies=[block.split('=',1)[1] for block in blocks]
Utex='(X^3-3X+Y)'; Vtex=r'\bigl(Z+(1-a)(42X^3-49X)\bigr)'
bodies=bodies[:3]+[b.replace(Utex,'y').replace(Vtex,'z') for b in bodies[3:]]
actual=[]
A,xx,yy,zz=sp.symbols('a x y z')
# Independent backend: pairs of QQ[x,y,z] polynomials representing p+a*q.
# This never calls ring.red or uses polynomial division by a^2-a+1.
Pzero=sp.Poly(0,xx,yy,zz,domain=sp.QQ)
Pone=sp.Poly(1,xx,yy,zz,domain=sp.QQ)
def pair_mul(p,q):
    b,c=p;d,e=q
    return b*d-c*e,b*e+c*d+c*e
@lru_cache(None)
def pair_eval(expr):
    if expr==A: return Pzero,Pone
    if expr.is_Number: return sp.Poly(expr,xx,yy,zz,domain=sp.QQ),Pzero
    if expr.is_Symbol: return sp.Poly(expr,xx,yy,zz,domain=sp.QQ),Pzero
    if expr.is_Add:
        parts=[pair_eval(q) for q in expr.args]
        return sum((p[0] for p in parts),Pzero),sum((p[1] for p in parts),Pzero)
    if expr.is_Mul:
        result=(Pone,Pzero)
        for q in expr.args: result=pair_mul(result,pair_eval(q))
        return result
    if expr.is_Pow:
        base,exponent=expr.args
        require(exponent.is_Integer and exponent>=0, 'Validation failed')
        result=(Pone,Pzero); b=pair_eval(base); n=int(exponent)
        while n:
            if n&1: result=pair_mul(result,b)
            n//=2
            if n: b=pair_mul(b,b)
        return result
    raise ValueError(('Unsupported symbolic node',expr))
for i,body in enumerate(bodies):
    actual.append(TexParser(body).parse())
    normalized=re.sub(r'\\[A-Za-z]+','',body).replace('\\\\','').replace('&','').replace('{}','')
    normalized=normalized.replace('\\{','(').replace('\\}',')')
    normalized=normalized.replace('{','(').replace('}',')').replace('[','(').replace(']',')').rstrip().rstrip('.')
    normalized=normalized.translate(str.maketrans('XYZ','xyz')).replace('\n',' ')
    expr=parse_expr(normalized,local_dict={'a':A,'x':xx,'y':yy,'z':zz},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
    coefficient_pair=pair_eval(expr)
    independent=zero
    for ea,coefficient in enumerate(coefficient_pair):
        for (ex,ey,ez),q in coefficient.terms():
            independent+=a**ea*ring(q)*x**ex*y**ey*z**ez
    require(independent==actual[i], ('Parser disagreement',i))
    print('PASS independent parsing component',i+1,';',len(actual[i]),'QQ monomials',flush=True)
expected=list(ns['phi_h'])+[x**3-3*x+y,at(ns['inverse_y'],xx=y,yy=x,zz=z),at(ns['inverse_z'],xx=y,yy=x,zz=z)]
labels=['forward1','forward2','forward3','inverse1','inverse2','inverse3']
differences=[red(p-q) for p,q in zip(actual,expected)]
for label,d in zip(labels,differences):
    print(label,'difference (inverse x,y,z = X,U,V):',d,flush=True)
print('Inverse axis point X=1,Y=0,Z=0 => X=1,U=-2,V=7(a-1)')
for name,polys in [('printed',actual[3:]),('compact',expected[3:])]:
    print(name,(str(at(polys[0],xx=one,yy=zero,zz=zero)),)+tuple(str(at(p,xx=one,yy=ring(-2),zz=7*(a-1))) for p in polys[1:]))
print('Elapsed',round(time.perf_counter()-start,3),'seconds')
if args.json:
    args.json.write_text(json.dumps({'labels':labels,'differences':[str(d) for d in differences]},indent=2))
if args.expect_correct and any(differences):
    print('FAIL: printed formulas differ from the compact construction.')
    sys.exit(1)
