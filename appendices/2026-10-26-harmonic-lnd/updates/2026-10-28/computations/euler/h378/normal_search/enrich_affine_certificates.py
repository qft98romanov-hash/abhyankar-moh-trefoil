#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Regenerate exact homogeneous directions completing the supplied affine-family certificates.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Save exact homogeneous bases for the two feasible bounded systems."""
from pathlib import Path
import json,time
import sympy as s
from search_normal_fields import system_from_basis, V
from verify_normal_certificates import decode, modular_rank

ROOT=Path(__file__).resolve().parent
for name in ('normal_degree_8.json','normal_only_degree_7.json'):
    begin=time.monotonic();path=ROOT/name;data=json.loads(path.read_text())
    basis=[decode(p) for p in data['basis']]
    keys,A,b=system_from_basis(basis,data['degree_bound'])
    if 'divergence_two' not in data.get('constraints',['divergence_two']):
        sel=[i for i,key in enumerate(keys) if key[0]=='normal']
        A=A.extract(sel,list(range(A.cols)));b=b.extract(sel,[0])
    print(name,'matrix built',A.shape,round(time.monotonic()-begin,3),flush=True)
    N=A.to_DM().nullspace().to_Matrix().T
    # Primitive integral vectors keep the certificate compact.
    for j in range(N.cols):
        den=s.ilcm(*[v.q for v in N[:,j]])
        values=[int(v*den) for v in N[:,j]]
        g=s.igcd(*values)
        for i,v in enumerate(values):N[i,j]=v//g
    assert (A.to_DM()*N.to_DM()).is_zero_matrix
    assert modular_rank(N)==N.cols
    rank_mod=modular_rank(A)
    assert rank_mod+N.cols==A.cols
    data['homogeneous_basis_coefficients']=[
        [{'index':i,'coefficient':str(v)} for i,v in enumerate(N[:,j]) if v]
        for j in range(N.cols)]
    data['dimension_certificate']={'prime':1000003,'matrix_rank_mod_prime':rank_mod,
       'exact_nullvectors':N.cols,'nullvectors_rank_mod_prime':N.cols,
       'status':'EXACT_DIMENSION_CERTIFICATE_GENERATED'}
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(name,'EXACT AFFINE DIMENSION',N.cols,'seconds',round(time.monotonic()-begin,3),flush=True)
