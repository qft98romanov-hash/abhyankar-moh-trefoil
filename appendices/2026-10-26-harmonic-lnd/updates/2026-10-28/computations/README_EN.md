# Reproducible computations for the research appendix

**28 October 2026. Research material under verification.**

This directory consolidates the computations used in this research branch.
It is self-contained after installing Python and SymPy: no source download,
GitHub authentication, repository checkout, GAP or Macaulay2 is required for
the default Python certificate suite. The mathematical arguments and their
limitations remain in the accompanying paper and proof notes. A successful
finite computation is not a proof of an unrestricted search claim.

## Directory map

| Directory | Contents and role |
| --- | --- |
| `baseline/` | Exact source formulas, printed LaTeX components and the core Python verifiers; optional GAP/Macaulay2 implementations and their historical logs. |
| `legacy_appendix/` | The earlier harmonic/LND appendix, including its degree-seven and degree-eleven slice certificates, periodic shears and bounded reductions. Its `repo/` dependency is already supplied offline. |
| `continuation/` | The eight-model slice study, multiplicity certificates, formal frames, transfer filtrations, relative-ML controls and restricted-ansatz obstructions. |
| `euler/` | The normal locally-finite-field criterion, naive-field controls, exact degree obstructions, complete 24- and 19-dimensional affine families and invariant-axis certificates. |
| `audit_checks/` | Exact identification of the original Shastri parameter and van den Essen--van Rossum slice, with the audit of named conjectures. |
| `provenance/` | Unchanged original inputs, source mapping and the audit proving that the prepared computational programs differ only in documentation. |
| `verification_logs/` | Fresh logs produced by the consolidated runner. These are distinct from historical logs inside the source directories. |

The upstream repository was read at commit
`b954f3609e900761fddc9c8ff03d8301e9604cab`.
The historical appendix pins its eleven dependencies to
`3cf41be3fb3b1108e1ec91dd23dff7bfcf59569e`; the eleven relevant Git blobs are
unchanged between these baselines. Those exact original bytes are retained in
the provenance archive.

## Quick reproduction

Tested environment: **Python 3.12 and SymPy 1.14.0**. From this directory:

```sh
python -m pip install -r requirements.txt
python run_all_checks.py
```

The same command works from another current directory if the full path to
`run_all_checks.py` is supplied. Paths to inputs are determined relative to
the runner and each checked script. Existing research scripts contain
assertions, so **do not use `python -O` or `python -OO`**. The consolidated
runner rejects optimized mode and explicitly enables assertions in children.

The default suite runs **35 verification programs** and can take several
minutes. It checks supplied certificates instead of repeating their costly
discovery. Every child runs from its own directory; exact failures and
timeouts are reported separately. Later checks still run if an earlier one
fails. The process exits with a nonzero status unless every selected program
passes.

```sh
python run_all_checks.py --list
python run_all_checks.py --only euler_h457_family euler_h378_family
python run_all_checks.py --timeout 1800
```

The last command raises the per-program timeout on a slower machine. A timeout
is an incomplete computation, not a mathematical obstruction.

## What is checked by default

1. Source provenance and documentation-only changes in 56 Python programs and
   seven GAP/Macaulay2 files.
2. The two compact rectifiers and the twelve printed components.
3. The exact original parameter/slice identities identifying the candidate in
   Conjectures 5.1--5.3. Kernel polynomiality additionally uses the complete
   rectifier and inverse, not merely the parameter polynomial.
4. The Shastri and harmonic minimum-slice certificates, including separate
   implementations of their lower bounds.
5. The factored LND/kernel-coordinate certificate, base LND, repeated-factor
   transfer example, periodic shears and the prescribed harmonic reduction
   scan up to index 100.
6. All fourteen final continuation verifiers: jet lower/upper certificates,
   formal frames, multiplicities, restricted-coordinate obstructions,
   relative-ML controls, transfer image ideals and iterated modifications.
7. All seven Euler verifiers: control examples, exact degree bounds and complete
   affine families, plus the proof certificates excluding the two selected
   representatives from local finiteness.

The numbers of programs, named assertions and finite model cases are **not
numbers of independent theorems**. Several verifiers intentionally overlap.
In particular, finite examples do not establish the general LF criterion,
the all-parameter naive-field obstruction or the all-iteration growth claims
without the written arguments.

## Exact arithmetic and completeness

The programs use rational arithmetic and, for the base rectifiers, the exact
quadratic relation `a*a - a + 1 = 0`. They do not replace identities by random
point evaluation or floating-point comparisons.

Some rank certificates use a prime modulus. Such ranks provide **lower bounds**
on rational rank. Matching upper bounds come from supplied exact rational null
vectors. Infeasibility is certified by rational row functionals with
`lambda^T A = 0` and `lambda^T b = 1`; it is not inferred just from failure over
a finite field. This is why those exclusions survive every characteristic-zero
field extension.

The Euler families satisfy the normal conditions and global divergence two.
They are **families of candidates, not families of locally nilpotent
derivations**. One particular point of each family is excluded by an invariant
axis. Other points do not all preserve that axis, so the certificate must not
be promoted to an exclusion of the whole family.

## Historical inputs, English comments and hashes

`provenance/original_bundle_inputs.zip` retains all 292 supplied inputs before
documentation edits and fresh runs. It preserves the original files, including
historical result JSON and logs. They were not silently replaced by the new
execution history.

`provenance/source_mapping.json` records the SHA-256 hashes of both original
and prepared files. English audit comments were added to runnable programs;
the two Russian Python documentation fragments were translated. For all
56 Python programs, the abstract syntax trees are identical after removing
documentation strings. The seven other source files differ only by a known
English comment prefix. Run the independent audit with:

```sh
python verify_comment_only_edits.py
```

This audit validates the historical input archive and every prepared code
hash; it then compares the actual source trees. It does not trust a pre-existing
`PASS` marker. The new runner and provenance-audit program are additional
infrastructure and do not purport to be old programs.

The historical bootstrap and old manifests are preserved for provenance.
**Do not run `legacy_appendix/bootstrap_source.py` for this consolidated
package:** its original Git-byte manifest describes the unannotated files,
whereas the supplied runnable copies have additional comments. The source
dependency is already present. Use `run_all_checks.py` and the new provenance
audit instead. Hash differences caused by the documented annotations are not
changes to polynomial formulas or executable Python statements.

Fresh checking may regenerate JSON results beside the corresponding programs.
The immutable archive still preserves their previous versions. The outer
delivery manifest describes the delivered snapshot; its generated-file hashes
can change after another run.

## Fresh results and historical evidence

`verification_summary.json` identifies the current run, exact program hashes,
versions, selected scope and per-program statuses. `verification_logs/` contains
its individual logs. A partial `--only` run is explicitly labelled as selected
certificates and must not be described as a full-suite run.

Older `aggregate_checks.json`, `verification.log` and similar files inside
the source trees are historical evidence unless a particular local runner
regenerates them. They may record older paths, hashes or execution times.
They are not instructions to reproduce those machine paths.

The word "independent" in the research notes means a separate implementation
or argument within this AI-assisted process. It does not mean independent
external human peer review. All claims remain submitted for further checking.

## Optional discovery and other interpreters

```sh
python run_all_checks.py --full
```

Full mode first runs all 35 certificates and then repeats three bounded
discovery tasks: the listed low-degree parameter searches and the first
normal-field systems for both difficult models. Each discovery task runs in
an isolated copy under `full_search_runs/`, so the supplied complete family
certificates are not overwritten. The field-search outputs are necessary-
condition candidates and do not establish local finiteness.

Other exploratory programs are retained alongside their original notes and
logs, including quadratic/divisor ansatz searches, the mixed-projection search,
jet-system discovery and affine-family enrichment. Their search spaces and
default bounds can be read directly in the English-commented source. They are
not all run by `--full`; some Groebner searches can be expensive.

Optional GAP and Macaulay2 implementations are provided in `baseline/gap/` and
`baseline/macaulay2/`. Their recorded upstream logs are retained. These
interpreters were not available in the consolidation runtime, so **no fresh
GAP or Macaulay2 execution is claimed here**. From the respective directory,
follow its supplied README. Its deliberate negative controls are expected to
fail; that failure confirms the checker is detecting the corrupted identity.

Nothing in this package claims a new rectifier for H(3,7,8) or H(4,5,7), a
classification of all harmonic embeddings, general cancellation, or the
general spatial embedding problem.
