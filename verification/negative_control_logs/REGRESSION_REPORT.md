# Expanded Python regression controls

Only `verification/run_negative_controls.py` was edited for this task. The completed runner passed **5 positive and 14 negative controls (19 subprocess cases)** in 281.973 seconds; its outer driver exited 0 in 282.017 seconds. Every negative case returned exactly 1 and contained its expected diagnostic; every positive returned exactly 0 and contained its required success marker(s).

The existing seven cases were retained. New coverage includes the harmonic U→Y collision through both harmonic auditors, unbraced multi-digit exponents and corrupted component argument order through every applicable appendix parser, and the harmonic inverse callable +Y mutation. Added positives exercise the patched 19-check core, the standalone harmonic auditor, and three explicit-multiplication unit cases using the actual independent parser extracted by AST. The unit case distinguishes `x\times-y` from subtraction and also checks grouped and numeric multiplication.

All mutations use isolated temporary repository copies and uniquely matched fragments. The runner checks exact exit codes and required markers, including both the exact U→Y residual `-x**5 + 5*x**3 - 6*x` and the semantic failure marker. It records each completed result immediately, preserves the command and expected markers, and writes final positive/negative counts and elapsed time in `summary.json`. It uses only the Python standard library and the repository's existing SymPy dependency.

Every direct child check is invoked with `-O`; existing wrapper controls retain their original behavior (the wrapper's own child auditor commands do not inherit `-O`). Neither source formulas nor other source files were edited by this task. The core source, harmonic appendix, and regression runner hashes were unchanged through the run. A concurrent provenance-comment change in the trefoil appendix was detected by the final hash guard; every noncomment line is identical to the published snapshot, so it has no parser or arithmetic effect. Before/after hashes and the comment-only distinction are preserved in `input_hashes.json`, `post_run_hashes.json`, and `input_changes.json`.

Fresh logs, `results.json`, `summary.json`, the runner patch, hash evidence, and driver metadata are in `cross_audit/regression_results` and mirrored in `working/rectification_repository/verification/negative_control_logs`.

| Case | Expected / actual exit | Seconds |
| --- | ---: | ---: |
| `false_identity_optimized` | 1 / 1 | 0.431 |
| `nondivisible_numerator_optimized` | 1 / 1 | 0.420 |
| `positive_explicit_times_optimized` | 0 / 0 | 0.429 |
| `positive_core_optimized` | 0 / 0 | 31.373 |
| `positive_trefoil_optimized` | 0 / 0 | 1.694 |
| `positive_harmonic_optimized` | 0 / 0 | 4.110 |
| `positive_harmonic_standalone_optimized` | 0 / 0 | 33.597 |
| `negative_trefoil_wrapper` | 1 / 1 | 2.131 |
| `negative_harmonic_wrapper` | 1 / 1 | 34.234 |
| `negative_harmonic_standalone_optimized` | 1 / 1 | 32.277 |
| `negative_trefoil_unbraced_exponent_optimized` | 1 / 1 | 0.749 |
| `negative_trefoil_component_label_optimized` | 1 / 1 | 0.678 |
| `negative_harmonic_unbraced_exponent_optimized` | 1 / 1 | 1.644 |
| `negative_harmonic_unbraced_exponent_standalone_optimized` | 1 / 1 | 31.947 |
| `negative_harmonic_component_label_optimized` | 1 / 1 | 1.552 |
| `negative_harmonic_component_label_standalone_optimized` | 1 / 1 | 33.097 |
| `negative_harmonic_u_to_y_independent_optimized` | 1 / 1 | 4.478 |
| `negative_harmonic_u_to_y_standalone_optimized` | 1 / 1 | 38.455 |
| `negative_harmonic_inverse_callable_optimized` | 1 / 1 | 28.649 |

Environment: Python 3.12.14, SymPy 1.14.0. Each subprocess case can contain multiple checks; counts above are subprocess control counts.
