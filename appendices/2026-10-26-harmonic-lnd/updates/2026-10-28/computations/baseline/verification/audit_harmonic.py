#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Audit the audit harmonic identities by exact symbolic arithmetic.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Strict TeX-expression audit of all six harmonic components.

Reads only the source appendix and compact verify.py; changes neither.
Arithmetic is exact in QQ[a,x,y,z,t]/(a^2-a+1).
"""
from pathlib import Path
import re
import runpy
import json
import sys
import time
import argparse

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def require(condition, message="Validation failed"):
    """Keep validation and parser token consumption active under python -O."""
    if not condition:
        raise AssertionError(message)

def normalize(s):
    s = s.replace(r'\\', '').replace('&', '').replace('{}', '')
    s = s.replace(r'\times', '*')
    s = re.sub(r'\\(?:Biggl|Biggr|Bigl|Bigr|bigl|bigr|left|right|qquad)\b', '', s)
    s = s.replace(r'\{', '(').replace(r'\}', ')')
    s = s.replace('[', '(').replace(']', ')')
    s = re.sub(r'\s+', '', s)
    if not re.fullmatch(r'[axyzXYZ0-9+*^(){}.-]+', s):
        raise ValueError('Unhandled TeX token: ' + s)
    return s.removesuffix('.')


class Parser:
    """Recursive descent: no eval, all characters consumed, implicit multiplication."""
    def __init__(self, s, names, ring, red):
        self.s, self.names, self.ring, self.red = s, names, ring, red
        self.tokens = re.findall(r'\d+|[a-zA-Z]|[+*^(){}-]', s)
        require(''.join(self.tokens) == s, 'Validation failed')
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def pop(self):
        token = self.peek()
        self.i += 1
        return token

    def expression(self):
        v = self.product()
        while self.peek() in ('+', '-'):
            op, w = self.pop(), self.product()
            v = v + w if op == '+' else v - w
        return self.red(v)

    def product(self):
        v = self.unary()
        while self.peek() is not None and self.peek() not in ('+', '-', ')', '}'):
            if self.peek() == '*': self.pop()
            v = self.red(v*self.unary())
        return v

    def unary(self):
        if self.peek() == '+': self.pop(); return self.unary()
        if self.peek() == '-': self.pop(); return -self.unary()
        return self.power()

    def power(self):
        v = self.atom()
        if self.peek() == '^':
            self.pop()
            if self.peek() == '{':
                self.pop()
                exponent = self.pop()
                require(self.pop() == '}', 'Validation failed')
            else:
                exponent = self.pop()
                require(exponent is not None and len(exponent) == 1,
                        'Unbraced TeX exponent must be a single digit')
            require(exponent.isdigit(), 'Validation failed')
            v = self.red(v**int(exponent))
        return v

    def atom(self):
        token = self.pop()
        if token in ('(', '{'):
            v = self.expression()
            require(self.pop() == (')' if token == '(' else '}'), 'Validation failed')
            return v
        if token and token.isdigit(): return self.ring(int(token))
        if token in self.names: return self.names[token]
        raise ValueError((token, self.i, self.s))

    def parse(self):
        v = self.expression()
        require(self.i == len(self.tokens), (self.i, len(self.tokens)))
        return self.red(v)


def main():
    global ROOT, OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT,
                        help='Repository containing verify.py and paper/harmonic_explicit.tex')
    parser.add_argument('--output',type=Path,default=OUT,
                        help='Directory for report and difference files')
    args=parser.parse_args()
    ROOT,OUT=args.repo.resolve(),args.output.resolve()
    OUT.mkdir(parents=True,exist_ok=True)
    start = time.perf_counter()
    c = runpy.run_path(str(ROOT/'verify.py'))
    ring, red = c['ring'], c['red']
    a,x,y,z,t = (c[s] for s in 'axyzt')
    def parse(s, names=None):
        return Parser(normalize(s), names or dict(zip('axyzXYZ', (a,x,y,z,x,y,z))), ring, red).parse()

    tests = [
        (r'-x^2', -x*x), (r'ax(xz-y^2+2)', a*x*(x*z-y*y+2)),
        (r'\Biggl\{-x+2a\Biggr\}^{3}', red((-x+2*a)**3)),
        (r'X^{2}\left(126 a-126\right)', red(x*x*(126*a-126))),
        (r'-(a+1)^2+\{2x\}\times[-3y]', red(-(a+1)**2-6*x*y)),
    ]
    for s, expected in tests: require(parse(s) == red(expected), s)
    print('Parser self-tests passed', len(tests), flush=True)
    text = (ROOT/'paper'/'harmonic_explicit.tex').read_text()
    blocks = re.findall(r'\\begin\{(align\*|gather\*)\}(.*?)\\end\{\1\}', text, re.S)
    require(len(blocks) == 6, 'Validation failed')
    results = []
    printed_inverse = []
    for i, (_, block) in enumerate(blocks):
        label, rhs = block.split('=', 1)
        signature = (rf'(\Phi_H)_{i+1}(x,y,z)' if i < 3 else
                     rf'(\Phi_H^{{-1}})_{i-2}(X,Y,Z)')
        require(re.sub(r'\s+', '', label) == signature,
                ('Unexpected component label or argument order', label, signature))
        require(len(re.findall('=', block)) == 1, 'Validation failed')
        if i < 3:
            printed = parse(rhs)
            compact = c['phi_h'][i]
            coordinates = 'original x,y,z'
        else:
            # Invertible polynomial coordinate substitution:
            # X=y, Y=x-y^3+3y, Z=z-(1-a)(42y^3-49y).
            # It sends the two repeatedly displayed expressions to x,z.
            names = dict(zip('aXYZ', (a,y,x-y**3+3*y,z-(1-a)*(42*y**3-49*y))))
            printed = parse(rhs,names)
            compact = (x,c['inverse_y'],c['inverse_z'])[i-3]
            coordinates = 'X=y, Y=x-y^3+3y, Z=z-(1-a)(42y^3-49y)'
            printed_inverse.append(printed)
        difference = red(printed-compact)
        coefficients = {}
        for mon, coefficient in difference.to_dict().items():
            key = str(mon[1:])
            coefficients[key] = coefficients.get(key, ring(0)) + ring(coefficient)*a**mon[0]
        row = dict(component=i+1, label=label.strip(), equal=difference==0,
                   printed_terms=len(printed), compact_terms=len(compact),
                   differing_QQ_a_coefficients=len(coefficients),
                   difference=str(difference), coordinate_system=coordinates)
        results.append(row)
        (OUT/f'component_{i+1}_difference.txt').write_text(str(difference)+'\n')
        print(json.dumps({k:v for k,v in row.items() if k!='difference'}), flush=True)
        if difference:
            print('First discrepancies',list(coefficients.items())[:20],flush=True)
    (OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    point=tuple(c['at'](p,xx=ring(-2),yy=ring(1),zz=-7*(1-a)) for p in printed_inverse)
    expected=(ring(-2),ring(1),ring(1))
    print('Printed harmonic_inverse(1,0,0):',tuple(map(str,point)))
    print('Expected gamma_H(1):',tuple(map(str,expected)))
    print('TOTAL', sum(not row['equal'] for row in results), 'unequal of 6; seconds',time.perf_counter()-start)
    if any(not row['equal'] for row in results):
        raise SystemExit(1)


if __name__ == '__main__': main()
