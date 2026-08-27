# Independent second verifier for the filled-group certificates

## Scope

Run 57 independently verifies the eight `luttinger-kbmag-proof-v1`
derivation DAGs that prove the paper's eight filled groups trivial. The new
checker is `luttinger/verify_certificates.rb`. It is written from scratch in
Ruby and uses only the Ruby standard library.

It does not import or invoke the Python checker, the certificate compiler,
the triangulation code, GAP, KBMAG, or any project group library. The Python
and Ruby programs share only the documented JSON certificate and original
presentation files that they are meant to check.

## Checks performed

For each of the eight certificates the Ruby verifier:

1. hashes the exact bytes of `r_presentations.json` and checks the certificate
   binding;
2. reconstructs the selected filling and verifies its case name, relators,
   generator count, and formal-inverse table;
3. checks every input equation up to free reduction, cyclic conjugacy, and
   inversion of the claimed input relator;
4. checks every formal-inverse axiom;
5. reconstructs every critical overlap from two earlier proved rules and
   literally replays both recorded rewrite branches;
6. literally replays both sides of every equation-tidying change and checks
   preservation of the group equation; and
7. requires a proved `[letter]=[]` root for all eight monoid letters—the four
   generators and their four formal inverses.

The eight DAGs contain 14,115 retained records. Both implementations accept
exactly the same cases with exactly the same per-case record counts.

## Negative controls

`--negative-controls` makes four independent corruptions of a real
certificate. The checker must and does reject:

* a final identity root changed away from the empty word;
* a claimed input-relator equation changed by one letter;
* a word position changed inside a nonempty internal rewrite trace; and
* a false SHA-256 digest for the source presentation.

These controls test distinct layers rather than merely damaging the gzip or
JSON syntax.

## Trust consequence

The eight simple-connectivity conclusions no longer depend on one custom
checker or one language runtime. The remaining computational trust is the
ordinary possibility of a shared conceptual error between two short
implementations of the same elementary equational logic, plus the Ruby and
Python language runtimes themselves.

This run does not claim a second-language replay of
`r_tietze_certificate.json.gz`. That preliminary certificate is replayed when
`r_run.py` reconstructs its 99,863-generator input, but the committed package
does not serialize that large input. Packaging a deterministic sealed input
is separate future work; it does not affect Run 57, whose eight proofs start
from the exact committed four-generator presentations.
