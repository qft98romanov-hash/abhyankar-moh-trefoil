#!/usr/bin/env python3
"""Verify source provenance and documentation-only changes without trusting logs.

Python programs are compared by their abstract syntax trees after removing
documentation strings. GAP and Macaulay2 programs may differ only by the
documented English comment prefix. The archived inputs are byte-checked first.
Generated JSON files are deliberately not compared with historical outputs:
fresh mathematical checks are allowed to regenerate those outputs.
"""
import ast
import hashlib
import io
import json
from pathlib import Path
import re
import tokenize
import zipfile

ROOT = Path(__file__).resolve().parent


class StripDocumentation(ast.NodeTransformer):
    """Remove only the leading documentation string of each lexical scope."""

    def visit(self, node):
        node = super().visit(node)
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body = node.body[1:]
        return node


def canonical_tree(source):
    """Ignore locations and docstrings, while retaining all executable nodes."""
    return ast.dump(StripDocumentation().visit(ast.parse(source)), include_attributes=False)


def main():
    mapping = json.loads((ROOT / 'provenance/source_mapping.json').read_text())
    checked = []
    with zipfile.ZipFile(ROOT / 'provenance/original_bundle_inputs.zip') as archive:
        for entry in mapping['files']:
            rel = entry['path']
            original = archive.read(rel)
            if hashlib.sha256(original).hexdigest() != entry['original_sha256']:
                raise AssertionError('Historical input hash mismatch: ' + rel)
            path = ROOT / rel
            if path.suffix not in ('.py', '.g', '.m2'):
                continue
            current = path.read_bytes()
            if hashlib.sha256(current).hexdigest() != entry['prepared_sha256']:
                raise AssertionError('Prepared source hash mismatch: ' + rel)
            if path.suffix == '.py':
                before, after = original.decode('utf-8'), current.decode('utf-8')
                if canonical_tree(before) != canonical_tree(after):
                    raise AssertionError('Executable AST changed: ' + rel)
                for token in tokenize.generate_tokens(io.StringIO(after).readline):
                    if token.type == tokenize.COMMENT and re.search('[\u0400-\u04ff]', token.string):
                        raise AssertionError('Untranslated Python comment: ' + rel)
                for node in ast.walk(ast.parse(after)):
                    if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        if re.search('[\u0400-\u04ff]', ast.get_docstring(node) or ''):
                            raise AssertionError('Untranslated Python docstring: ' + rel)
                method = 'AST_EQUAL_WITHOUT_DOCSTRINGS'
            else:
                leader = '#' if path.suffix == '.g' else '--'
                prefix = (leader + ' Consolidated verification copy, 28 October 2026.\n'
                          + leader + ' Exact source statements are unchanged; original logs are historical evidence.\n'
                          + leader + ' This interpreter is optional and is not required by the Python certificate suite.\n')
                if current != prefix.encode('utf-8') + original:
                    raise AssertionError('Non-comment change in optional interpreter source: ' + rel)
                method = 'COMMENT_PREFIX_ONLY'
            checked.append({'path': rel, 'method': method, 'status': 'PASS'})
    report = {'status': 'PASS', 'date': '2026-10-28', 'checked_code_files': len(checked),
              'python_files': mapping['python_files'], 'other_code_files': mapping['other_code_files'],
              'historical_input_files': len(mapping['files']), 'checks': checked}
    (ROOT / 'provenance/comment_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: documentation-only changes in', len(checked), 'code files; archived input hashes verified.')


if __name__ == '__main__':
    main()
