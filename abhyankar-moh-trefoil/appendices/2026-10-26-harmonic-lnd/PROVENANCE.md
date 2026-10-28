# Provenance and verification scope

Date: 26 October 2026. Status: preliminary appendix, under verification.

The mathematical text, programs, rational certificates and exploratory outputs
were prepared in an AI-assisted research session. “Independent” in the original
working notes means a separate implementation or argument within that process;
it does not mean external human peer review. All claims remain open to checking.

## Exact source identity

`research/source_manifest.json` binds 11 upstream files to commit
`3cf41be3fb3b1108e1ec91dd23dff7bfcf59569e` using Git blob SHA-1 and byte lengths.
`research/repo_audit/exact_source_sha256.txt` additionally lists SHA-256 hashes
of these exact bytes. The bootstrap validates the pinned source before use.

## Historical source extraction

The initial tool extraction appended one final newline to some text sources.
The files were subsequently normalized to the exact Git bytes. This changes
byte hashes but not the Python or mathematical content. The following retained
records describe that earlier extraction and have not been silently rewritten:

- `research/repo_audit/input_sha256.txt`;
- source-hash lines in `research/repo_audit/verify_printed_current.log`;
- `source_sha256` in `research/lnd_certificate/certificate_results.json`.

In particular, the recorded verify.py SHA-256
`352f33e3a79c51ecf8b92fa457cf22298b6085f717cb8b5dd5d37dd8b0882d20`
is the hash of the exact pinned verify.py bytes followed by one additional
newline. The pinned Git manifest and `exact_source_sha256.txt` are the current
source identity records. Historical machine paths and execution times in the
audit notes are provenance, not commands to copy. Use README instructions.

The rational witness hashes and upper-slice hashes in the minimum-degree
certificates match the supplied witness files. Computational checks establish
their stated algebraic identities or finite search results. They do not replace
review of the general mathematical arguments or establish literature priority.

This appendix has its own SHA256SUMS.txt. The root repository manifest and all
other pre-existing repository files are intentionally left unchanged.
