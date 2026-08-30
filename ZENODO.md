# Archival deposit (Zenodo)

The versioned GitHub release is the reproducibility target today. A journal
submission additionally needs a DOI-bearing archival copy that does not depend
on GitHub remaining available. This file records how that deposit is made and
which decision has to be taken first.

`.zenodo.json` and `CITATION.cff` in the repository root carry the deposit
metadata. Zenodo reads `.zenodo.json` automatically; GitHub renders
`CITATION.cff` as a "Cite this repository" panel.

## The ordering trap

**Zenodo only archives releases created after its webhook is switched on.**
Enabling the integration does not retroactively archive `v1.5.8` or any earlier
tag. So the switch must be flipped *before* `v2.0.0` is cut, not after. If
`v2.0.0` is tagged first, it will not be deposited and a throwaway `v2.0.1`
would be needed to trigger one.

## Which route

The two routes differ only in whether the DOI can be printed inside the paper.

**Route A — GitHub integration (recommended).** The DOI is minted when the
release is published, so it cannot appear in that release's own PDF. The paper
cites the versioned release; the DOI is added to the repository README, and to
the manuscript at its next revision.

1. Sign in at zenodo.org with GitHub.
2. Zenodo -> profile menu -> GitHub, find
   `VentiMath/exotic-s2xs2-verification`, toggle it **On**.
3. Cut release `v2.0.0` on GitHub.
4. Zenodo archives the source tree and mints two DOIs: a *version* DOI for
   `v2.0.0` and a *concept* DOI that always resolves to the newest version.
   Cite the concept DOI in prose; cite the version DOI for an exact replay.
5. Attach the two PDFs and the deterministic source archive to the GitHub
   release as before; Zenodo captures the repository tarball itself.

**Route B — manual deposit with a reserved DOI.** Use this only if the DOI must
be printed in the v2.0.0 PDF. Create a new upload at zenodo.org, press *Reserve
DOI*, paste that DOI into `main.tex`, rebuild the PDF, rebuild the source
archive, re-pin its digest in `ARXIV_SUBMISSION.md`, then upload the artifacts
and publish. This costs one extra rebuild-and-re-pin cycle and takes the
release out of the automated path.

## What the deposit should contain

Route A captures the repository tree automatically. If uploading manually,
include: `paper/main.pdf`, `paper/supplement.pdf`, the deterministic source
archive, `verification/` in full (certificates, checkers, specification, hash
manifests, dependency ledger, run transcripts), `LICENSE`, and this file.

## After the DOI exists

- Add the DOI badge to `README.md`.
- Add a software/data citation to the manuscript bibliography at the next
  revision, citing the concept DOI.
- Record the version DOI beside the release digests in `ARXIV_SUBMISSION.md`.

## Not covered by any of this

A DOI is an archival guarantee, not a review. The independent human audits the
referee asked for -- computational group theory for the checker and soundness
argument, PL or symplectic 4-manifold topology for the geometric
identification -- remain outstanding and cannot be satisfied by further
automated work.
