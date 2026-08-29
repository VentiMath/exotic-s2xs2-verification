# Import provenance

This directory is a curated import of the working verification repository at
its commit `3c01e24` ("Clarify the 100-case framing-scan count",
2026-08-28), superseding the earlier `1bc4caf`, `58b4fa8`, and `a9b6cb8`
imports. Replaying the second checker (`luttinger/verify_certificates.rb`,
run 57) and the case-100 transfer verifier
(`luttinger/case100_transfer/verify_transfer_certificate.rb`, run 63) needs
only a stock Ruby 3 interpreter. Everything here — the engine under
`luttinger/`, the certificates, the run transcripts under `runs/`, the
referee-packet notes under `notes/`, and the provenance ledger — is the
committed state of that repository, imported without modification except for
the removals listed below and the lint pass recorded in this repository's
own history. Relative paths referenced by `STATUS.md`, the notes, and the
run transcripts resolve within this directory. Run 58 and its
`luttinger/j_certificates/` artifacts originate in this repository rather
than the working one; runs 59–63 independently reproduce and extend them.
Run 64 — the downstream proof chain (`luttinger/downstream_chain.py`, its
certificate, `luttinger/verify_downstream_chain.rb`, the extension of
`luttinger/proof_ledger.py`, and `notes/downstream_proof_chain_2026-08-28.md`)
— also originates in this repository.
So does run 65, the batch inventory checks in `luttinger/verify_kbmag_certificate.py`,
`luttinger/verify_certificates.rb`, and `luttinger/make_proof_manifest.py`, with the
regenerated proof manifest and downstream-chain certificate.

## Removed from the import

* `luttinger/paper_2608.17267.txt` and the paper PDFs — the author's
  copyrighted text. The paper is arXiv:2608.17267.
* `luttinger/author_scripts/` and `luttinger/walkthrough.txt` — the author's
  own MIT-licensed scripts. Rather than vendoring them, we reference his
  repository directly: github.com/bwuebben/exotic-s2xs2 at commit
  `ea1fc13d1f641678a228a8c7fdf8cce18da350a4` (2026-08-17). Where our runs
  invoked those scripts, the transcripts record the invocation and output.
* `luttinger.tar.gz` — the inherited starting tarball (contains the above).
* Three files under `notes/` recording private correspondence drafts,
  user-relayed community reactions, and a work-packet handoff for an
  unrelated formalization project. They contain no mathematics of this
  verification; the provenance ledger's references to them describe what
  they were.
* `academy-curriculum/` — teaching material derived from the verification
  for VentiMath's academy, not part of the verification itself.
* `luttinger/hello.g`, `luttinger/pkgtest.g`, `luttinger/bk_out.txt` —
  environment smoke tests and a scratch transcript.
* The large KBMAG ancestry `.history` streams and `kbprog` sidecars behind
  the run 59–63 certificates — reproducible build products (the working
  repository ignores them too); the compact `.json.gz` certificates and their
  exact input rewriting systems ship.

`luttinger/paper_data.md` ships: a per-line review (2026-08-27) confirmed
every line is mathematical construction data in our own notation with
citations to the paper's numbered propositions, sections, and Table 1 — not
reproduced exposition.

## Replaying run 53 (the interpretation dictionary)

`luttinger/interpretation_dictionary.py` parses two of the author's scripts
that this import deliberately does not vendor. To replay it, fetch
`scripts/develop.py` and `scripts/decide.g` from
github.com/bwuebben/exotic-s2xs2 at commit `ea1fc13d` into
`luttinger/author_scripts/`. The certificate pins their SHA-256
(`1a4a67d5…` and `302725da…`), and the run transcript records that the
locally parsed copies are byte-identical to that upstream commit, so any
fetched copy either matches and replays or visibly differs.

## Replaying run 54 (the raw-paper extraction)

`luttinger/paper_coordinate_extractor.py` reads only `paper_2608.17267.txt`,
a plain-text extraction of the paper, which this import does not vendor (the
text is the author's copyright). To replay the extraction step, produce the
text from the paper's arXiv source for 2608.17267 and place it at
`luttinger/paper_2608.17267.txt`. The frozen extraction certificate
(`paper_coordinate_certificate.json`) ships, so the second, separate step —
`paper_model_dictionary_compare.py --check`, which compares the frozen
extraction with the model certificates — replays from this directory alone,
as does the run-55 checker `lemma71_normal_form_check.py --check`.

## Replaying run 56 (the Lidman–Piccirillo source-figure audit)

`luttinger/lp_source_figure_audit.py` reads only the original `main.tex`
and `morecurves.pdf` from the immutable arXiv:2505.14387v1 source archive,
which this import does not vendor (the files are Lidman–Piccirillo's
copyright). To replay, fetch and extract the v1 e-print and pass
`--source-dir`; the checker refuses to run unless the two input hashes
match the pinned values, and it needs poppler (`pdftocairo`) and
ImageMagick for the vector separation. Every other checker replays from
this directory alone.

## Environment note

GAP, KBMAG, and ACE run through the documented docker shim `bin/gap`
(image `gapsystem/gap-docker`), invoked from `luttinger/` with
`PATH=../bin`. The shim bind-mounts the working directory, so the clone
must live on a path the docker VM shares with the host (on a VM-backed
docker such as colima, a system temp directory typically is not shared and
GAP will report it cannot read its input file). The certificate *verifiers*
(the derivation-DAG checker, the proof-producing Tietze replay, and the
analytic checks) are plain Python and need no GAP installation.
