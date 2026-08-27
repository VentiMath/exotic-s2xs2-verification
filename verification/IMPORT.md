# Import provenance

This directory is a curated import of the working verification repository at
its commit `1bc4caf` ("Record the run 45 freeze in STATUS, PROVENANCE, and
the outreach draft", 2026-08-26). Everything here — the engine under
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

## Environment note

GAP, KBMAG, and ACE run through the documented docker shim `bin/gap`
(image `gapsystem/gap-docker`), invoked from `luttinger/` with
`PATH=../bin`. The shim bind-mounts the working directory, so the clone
must live on a path the docker VM shares with the host (on a VM-backed
docker such as colima, a system temp directory typically is not shared and
GAP will report it cannot read its input file). The certificate *verifiers*
(the derivation-DAG checker, the proof-producing Tietze replay, and the
analytic checks) are plain Python and need no GAP installation.
