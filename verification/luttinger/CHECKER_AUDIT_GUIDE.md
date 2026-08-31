# External conformance-audit guide for the filled-group checkers

This guide turns the remaining software trust statement in the manuscript
into a bounded review task.  It is **not** an independent audit and must not
be cited as one.  An external reviewer can audit either checker against the
normative specification without reading KBMAG, the certificate compiler, the
search code, or any topology program.

## Normative objects

The mathematical specification is `CERTIFICATE_SPEC.md`.  The two candidate
implementations are:

- `verify_kbmag_certificate.py` (Python, standard library only);
- `verify_certificates.rb` (Ruby, standard library only).

For this working revision their SHA-256 digests are:

```text
ed2661526a0c8236ccc519a08f03752d4bb6307b3454f50bebb02d07e10a9ca1  CERTIFICATE_SPEC.md
d8c7bd3486387e6e81e0ff3c77aafd108ed7a201cdee6eac2fef4ea67f02846e  verify_kbmag_certificate.py
0b4c1e314f48863c7117af708627f366be1c5c3d29e7eb5941f3488fbe57f105  verify_certificates.rb
```

These are working-tree identifiers, not release identifiers.  The next
release must regenerate this block and bind all three files in its manifest.

## Clause-to-code map

Line numbers below refer to the files with the preceding digests.  Function
names, rather than line numbers, are the durable identifiers.

| Specification obligation | Python implementation | Ruby implementation | What the reviewer must establish |
|---|---|---|---|
| §1 signed words, inverse, free and cyclic reduction, cyclic key | `inverse`, `free_reduce`, `cyclic_reduce`, `cyclic_key`, lines 25–57 | same names, lines 31–64 | Each operation is literal and the lexicographic minimum ranges over every cyclic rotation of a word and its inverse. |
| §1 word alphabets | `check_word`, `check_signed_word`, lines 64–76 | same names, lines 65–87 | Source words use nonzero signed integers of absolute value at most `ngens`; certificate words use integers in `1..2*ngens`; booleans and out-of-range letters are rejected. |
| §2 source binding and selected filling | `verify_certificate`, lines 237–289 | `verify_filled_certificate`, lines 115–157 | Format, source-byte digest, plain-integer case index, signs, slug, positive generator count, two filling relators, exact relator list, and exact inverse table are checked before records are accepted. |
| §3 literal rewrite traces | `apply_trace`, lines 78–95 | `apply_trace`, lines 89–107 | Every rule index is earlier than the current record, the offset is a valid boundary, the left side occurs literally, and replacement uses the stored right side. |
| §4.1 inverse axiom | record branch beginning line 295 | branch beginning line 158 | The right side is empty and the two-letter left side is an inverse-table pair. |
| §4.2 input relator | branch beginning line 300 | branch beginning line 161 | The indexed source relator exists and has the same equation key as the record. |
| §4.3 overlap | branch beginning line 306 | branch beginning line 167 | Parent indices are earlier plain integers; the overlap is nonempty and literal; both branches come from the same union word; both traces replay; the resulting equation key equals the recorded key. |
| §4.4 change | branch beginning line 335 | branch beginning line 199 | The old record is an earlier plain integer; both sides replay independently; replay outputs equal the stored reduced sides; equation keys agree. |
| §5 identity roots | lines 354–365 | lines 217–229 | There are exactly `2*ngens` roots and root `l` literally has `[l] -> []`. |
| §6 batch inventory | `check_inventory`, lines 102–131 | `check_inventory`, lines 243–262 | Indices and slugs are unique; full mode has every source filling exactly once, exact filenames, two filling relators per case, and the requested dimensions. |

The soundness proof is §7 of the specification and Theorem 3.5 of the main
paper.  The code review should not substitute a claim that KBMAG is sound:
KBMAG is only a certificate generator and is outside this trust boundary.

## Required replay

From `verification/luttinger/`, run:

```sh
python3 verify_kbmag_certificate.py \
  --input sealed_transport/r_presentations.json \
  --full-inventory --expect-generators 3 --expect-relators 78 \
  --negative-controls sealed_transport/proof_certificates/*.json.gz

ruby verify_certificates.rb \
  --root sealed_transport --full-inventory \
  --expect-generators 3 --expect-relators 78 --negative-controls
```

Both runs must accept all eight certificates and reject:

1. a duplicated batch;
2. a corrupted identity root;
3. a corrupted input-relator equation;
4. a corrupted literal rewrite trace;
5. a JSON boolean substituted for an integer word letter;
6. a JSON boolean substituted for the integer case index; and
7. a wrong presentation digest.

The two boolean controls are especially important in Python, where `bool`
subclasses `int` even though booleans are not integers in the certificate
grammar.

The two programs must report the same eight slugs and the same total of
39,163 proof records.  The corruption controls are necessary tests of the
failure paths, not a proof of conformance.

## Suggested external audit record

An audit can be reported in one page containing:

1. reviewer name, date, operating system, Python/Ruby versions, and commit;
2. the three SHA-256 values above as independently recomputed;
3. a yes/no disposition for every row of the clause-to-code map;
4. the complete terminal output of the two commands;
5. any discrepancy, ambiguity, or unreviewed branch; and
6. one of the conclusions `conforms`, `does not conform`, or `incomplete`.

Only a report produced by a person or group outside the project can retire
the manuscript's independent-audit caveat.
