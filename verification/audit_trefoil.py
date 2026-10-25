"""Literal appendix audit: recursive-descent TeX parser + independent SymPy parser.
Run: python -u audit_trefoil.py --repository /path/to/repository [--expect-correct]
No original files are modified. All arithmetic is exact.
"""
import os
os.environ['SYMPY_GROUND_TYPES']='python'
import ast, re, json, hashlib, time, argparse, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
def require(condition, message="Validation failed"):
    """Keep validation and parser token consumption active under python -O."""
    if not condition:
        raise AssertionError(message)

cli=argparse.ArgumentParser(description=__doc__)
cli.add_argument('--repository',type=Path,required=True,help='Directory containing verify.py and paper/')
cli.add_argument('--tex',type=Path,help='Alternate trefoil_explicit.tex; default: repository/paper/trefoil_explicit.tex')
cli.add_argument('--expect-correct',action='store_true',help='Exit 1 if any printed component differs from compact formulas')
cli.add_argument('--json',type=Path,help='Optional JSON results path')
args=cli.parse_args()
SRC=args.repository.resolve()
TEX=args.tex.resolve() if args.tex else SRC/'paper/trefoil_explicit.tex'
start=time.perf_counter()
print('SymPy',sp.__version__)
for path in [SRC/'verify.py',TEX]:
    print('SHA256',path.name,hashlib.sha256(path.read_bytes()).hexdigest())
# Load only setup, helper definitions and trefoil construction; omit all checks.
module=ast.parse((SRC/'verify.py').read_text())
kept=[]
for node in module.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='correction' for t in node.targets): break
    if isinstance(node,ast.Expr): continue
    kept.append(node)
ns={}
exec(compile(ast.Module(body=kept,type_ignores=[]),'verify.py [checks omitted]','exec'),ns)
ring,a,x,y,z,t=(ns[v] for v in ['ring','a','x','y','z','t'])
red,at=ns['red'],ns['at']
zero,one=ring(0),ring(1)
print('Compact trefoil constructed in',round(time.perf_counter()-start,3),'seconds')
# The parser reads actual TeX, erasing only presentation commands.
COMMANDS={'bigl','bigr','Bigl','Bigr','left','right','qquad','quad'}
class TexParser:
    def __init__(self,source):
        self.tokens=[]
        p=0
        while p<len(source):
            c=source[p]
            if c.isspace() or c=='&': p+=1; continue
            if source[p:p+2]=='\\\\': p+=2; continue
            if source[p:p+2]=='{}': p+=2; continue
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
            else:
                exponent=self.consume()
                require(len(exponent)==1 and exponent.isdigit(),
                        'Unbraced TeX exponent must be a single digit')
                exponent=int(exponent)
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
blocks=[body for _,body in re.findall(r'\\begin\{(align\*|gather\*)\}(.*?)\\end\{\1\}',tex,re.S)]
require(len(blocks)==6, 'Validation failed')
signatures = [rf'(\Phi_T)_{i}(x,y,z)' for i in range(1,4)] + [
    rf'(\Phi_T^{{-1}})_{i}(X,Y,Z)' for i in range(1,4)]
for block,signature in zip(blocks,signatures):
    require(block.count('=')==1, 'Expected exactly one equation per component')
    require(re.sub(r'\s+', '', block.split('=',1)[0])==signature,
            ('Unexpected component label or argument order', signature))
bodies=[block.split('=',1)[1] for block in blocks]
actual=[TexParser(body).parse() for body in bodies]
# Second independent parse: symbolic expression with a separate normalization
# pipeline and SymPy's implicit-multiplication expression parser.
A,xx,yy,zz=sp.symbols('a x y z')
for i,body in enumerate(bodies):
    normalized=re.sub(r'\\[A-Za-z]+','',body).replace('\\\\','').replace('&','').replace('{}','')
    normalized=normalized.replace('{','(').replace('}',')').replace('[','(').replace(']',')').rstrip().rstrip('.')
    normalized=normalized.translate(str.maketrans('XYZ','xyz')).replace('\n',' ')
    expr=parse_expr(normalized,local_dict={'a':A,'x':xx,'y':yy,'z':zz},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
    expr=sp.Poly(expr,A,xx,yy,zz,domain=sp.QQ)
    independent=zero
    # Reduce powers of a via a distinct 2x2 recurrence, no polynomial remainder.
    coeffs=[(1,0),(0,1)]
    for k in range(2,expr.degree(A)+1):
        c,d=coeffs[-1];coeffs.append((-d,c+d))
    for (ea,ex,ey,ez),q in expr.terms():
        c,d=coeffs[ea]
        independent+=(c+d*a)*ring(q)*x**ex*y**ey*z**ez
    require(independent==actual[i], ('Parser disagreement',i))
    print('PASS independent parsing component',i+1,';',len(actual[i]),'QQ monomials')

expected=list(ns['phi_t'])+list(ns['trefoil_inverse'](x,y,z))
labels=['forward 1','forward 2','forward 3','inverse 1','inverse 2','inverse 3']
def grouped(p):
    ans={}
    for (ea,ex,ey,ez,et),q in p.to_dict().items():
        require(et==0, 'Validation failed')
        ans.setdefault((ex,ey,ez),[0,0])[ea]+=q
    return ans

def fmt(pair): return str(sp.expand(pair[0]+pair[1]*A))
differences=[]
for label,pa,pe in zip(labels,actual,expected):
    delta=red(pa-pe);differences.append(delta)
    print('\nCOMPONENT',label,'delta = printed - compact:',delta)
    if delta==0: print('PASS literal equality')
    else:
        ga,ge=grouped(pa),grouped(pe)
        for mon,pair in sorted(grouped(delta).items()):
            print('  exponent',mon,'printed',fmt(ga.get(mon,[0,0])),'correct',fmt(ge.get(mon,[0,0])),'difference',fmt(pair))
print('\nCounterexample (x,y,z)=(1,0,0):')
for label,p in zip(labels,differences): print(label,at(p,xx=one,yy=zero,zz=zero))
# Preserve all literal bodies, parser-normalized expressions, and exact errors.
if args.json:
    args.json.write_text(json.dumps({'labels':labels,'differences':[str(d) for d in differences]},indent=2))
print('Elapsed',round(time.perf_counter()-start,3),'seconds')
print('\nINVERSE CHECK IN INDEPENDENT COORDINATES (X,U,V):')
Utex='(X^3-3X+Y)'; Vtex='(Z+8-14X^2)'
compressed=[TexParser(body.replace(Utex,'y').replace(Vtex,'z')).parse() for body in bodies[4:]]
compact_expected=[red(at(ns['R'],xx=y,yy=x,zz=z)-2),red(at(ns['S'],xx=y,yy=x,zz=z)+5*y)]
compressed_differences=[red(p-q) for p,q in zip(compressed,compact_expected)]
# Compressed differences are separately checked against full substitutions.
for full,short in zip(differences[4:],compressed_differences):
    require(full==at(short,xx=x,yy=x**3-3*x+y,zz=z+8-14*x**2), 'Validation failed')
for label,p,q in zip(['inverse 2','inverse 3'],compressed,compact_expected):
    print(label,'(x,y,z denote X,U,V) delta:',red(p-q))
    ga,ge=grouped(p),grouped(q)
    for mon,pair in sorted(grouped(red(p-q)).items()):
        print('  (X,U,V) exponent',mon,'printed',fmt(ga.get(mon,[0,0])),'correct',fmt(ge.get(mon,[0,0])))

# Exactly eight literal sign substitutions, followed by re-parsing all six RHS.
patches=[
    ('- 30180 a - 20159','- 30180 a + 20159'),
    ('- 15005311 a - 544778','- 15005311 a + 544778'),
    ('- 57839390 a + 42459540','- 57839390 a - 42459540'),
    ('- 5332390 a + 1292060','- 5332390 a - 1292060'),
    ('- 21350 a + 1302','- 21350 a - 1302'),
    ('- a + 4\\Bigr]','- a - 4\\Bigr]'),
    ('- 8 a - 3\\Bigr]','- 8 a + 3\\Bigr]'),
    ('- 5 a - 5\\Bigr]','- 5 a + 5\\Bigr]'),
]
fixed=tex
print('\nEIGHT LITERAL SIGN CORRECTIONS:')
patch_count=0
for old,new in patches:
    require(tex.count(old)<=1, (old,tex.count(old)))
    if old in tex:
        line=tex[:tex.index(old)].count('\n')+1
        print('line',line,repr(old),'->',repr(new))
        fixed=fixed.replace(old,new)
        patch_count+=1
    else:
        require(tex.count(new)==1, ('Neither original nor corrected token occurs exactly once',old,new))
        print('Already corrected:',repr(new))
fixed_blocks=[body for _,body in re.findall(r'\\begin\{(align\*|gather\*)\}(.*?)\\end\{\1\}',fixed,re.S)]
for label,block,q in zip(labels,fixed_blocks,expected):
    require(TexParser(block.split('=',1)[1]).parse()==q, label)
print('PASS all six literal components equal compact formulas after',patch_count,'in-memory changes')
print('\nEXACT CONTROL POINTS (a remains symbolic, with a^2-a+1=0):')
for label,ps,qs,point in [
    ('forward at (1,0,0)',actual[:3],expected[:3],(one,zero,zero)),
    ('forward at trefoil point (-2,-3,-9)',actual[:3],expected[:3],(ring(-2),ring(-3),ring(-9))),
    ('inverse at axis point (1,0,0)',actual[3:],expected[3:],(one,zero,zero)),
    ('inverse at (0,1,-8)',actual[3:],expected[3:],(zero,one,ring(-8))),
    ('inverse at (0,1,-7)',actual[3:],expected[3:],(zero,one,ring(-7))),
]:
    print(label)
    print('  printed:',tuple(str(at(p,xx=point[0],yy=point[1],zz=point[2])) for p in ps))
    print('  compact:',tuple(str(at(p,xx=point[0],yy=point[1],zz=point[2])) for p in qs))
print('Total elapsed',round(time.perf_counter()-start,3),'seconds')

if args.expect_correct and any(differences):
    print('FAIL: printed formulas differ from the compact construction.')
    sys.exit(1)
