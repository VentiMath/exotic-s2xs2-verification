# Import provenance

This directory is a curated import of the working verification repository at
its commit `a9b6cb8` ("Add an independent Ruby proof verifier",
2026-08-27), superseding the earlier `1bc4caf` and `58b4fa8` imports.
Replaying the second checker (`luttinger/verify_certificates.rb`, run 57)
needs only a stock Ruby 3 interpreter. Everything here — the engine under
`luttinger/`, the certificates, the run transcripts under `runs/`, the
referee-packet notes under `notes/`, and the provenance ledger — is the
committed state of that repository, imported without modification except for
the removals listed below. Relative paths referenced by `STATUS.md`, the
notes, and the run transcripts resolve within this directory.

## Removed from the import

* `luttinger/paper_2608.17267.txt` and the paper PDFs — the author's
  copyrighted text. The paper is arXiv:2608.17267.
* `luttinger/author_scripts/` and `luttinger/walkthrough.txt` — the author's
  own MIT-licensed scripts. Rather than vendoring them, we reference his
  repository directly: github.com/bwuebben/exotic-s2xs2 at commit
  `ea1fc13d1f641678a228a8c7fdf8cce18da350a4` (2026-08-17). Where our runs
  invoked those scripts, the transcripts record the invocation and output.
* `luttinger.tar.gz` — the inherited starting tarball (contains the above).
* Two files under `notes/` recording private correspondence drafts and
  user-relayed community reactions. They contain no mathematics; the
  provenance ledger's references to them describe what they were.

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
