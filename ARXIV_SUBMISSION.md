# arXiv submission packet

> **WORKING-DRAFT GATE:** the manuscript and supplement are now visibly
> labeled as an unreleased v2.2.2 working revision built on the immutable
> v2.2.1 artifact. Do not upload this packet to arXiv until a new exact-version
> DOI has been reserved, the title pages and data sections have been updated,
> all PDFs and archives have been rebuilt, and the final release gate passes.

This file preserves the intended arXiv metadata while preventing the web form
from drifting from the rendered paper.  Release-specific hashes below must be
regenerated after the prose is frozen; no v2.2.2 release is claimed here.

## Build and upload

- From a clean checkout of the eventual v2.2.2 tag, run
  `./paper/build_arxiv_source.sh`. The script fixes the file timestamp,
  numeric owner, archive format, and gzip header, so repeated builds from the
  same `paper/main.tex` are byte-for-byte identical.
- Upload `paper/arxiv-source-v2.2.2.tar.gz` as the v2.2.2 GitHub release asset
  and to arXiv.
- Source-archive SHA-256: **TBD after the final deterministic build.**
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Publish `paper/supplement.pdf` and `paper/supplement.tex` as versioned
  release assets alongside the main paper. The arXiv comments field points to
  that immutable release rather than treating the supplement as a second
  top-level TeX document.
- Main PDF SHA-256: **TBD after the final build.**
- Supplement PDF SHA-256: **TBD after the final build.**
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

## Synchronization gate

Run `python3 paper/check_release_sync.py` while preparing the candidate.  It
checks the PDF/source hashes, page/figure/table counts, Source Comparison Hypotheses D1--D14
terminology, and the two theorem-artifact manifests.  After reserving the
exact version DOI and replacing every candidate placeholder, run
`python3 paper/check_release_sync.py --final` from the clean checkout that is
tagged `v2.2.2`.  Final mode must pass before arXiv upload; it also requires
the same release URL and version DOI in the manuscript, supplement, README,
and this packet.  The script does not make a network request, so open both
links from a logged-out browser as the last release check.

## Metadata

All fields below are ASCII, as required by arXiv.

**Title**

```text
A certificate-based audit of simple connectivity for an explicit model associated with Wuebben's proposed exotic $S^2 \times S^2$ construction
```

**Authors**

```text
John Clyde (VentiMath)
```

**Abstract**

```text
We define an explicit marked surface-bundle surgery manifold $V_aud$ modeled on data in Wuebben's proposed exotic $S^2 \times S^2$ construction. Four hash-identified presentations are trivial under a published derivation-certificate specification. Operational replay assumes that at least one checker conforms to that specification; the two shipped implementations were developed within the project and have not received an independent human line-by-line audit. Separate combinatorial and geometric arguments identify the fixed $(+,+)$ presentation with $\pi_1(V_aud)$, proving that $V_aud$ is simply connected; the other three sign sheets are algebraic robustness checks. A logically separate theorem identifies the product-framing curves with their Lagrangian-framing classes. Transfer to Wuebben's fixed member is isolated behind fourteen Source Comparison Hypotheses, D1--D14: a sufficiency proposition proves that their conjunction would give the transfer but does not discharge them. The downstream manifold conclusions are additionally conditional on cited classification, symplectic, and Floer-theoretic results. A reported contrary fundamental-group computation remains unreconciled. Thus the source-independent audit theorem, not confirmation of the proposed exotic manifolds, is the paper's primary result.
```

**Comments**

```text
27 pages, three figures, five tables, with a 16-page mathematical and computational supplement planned as a release asset. The primary result is the source-independent theorem $\pi_1(V_aud)=1$. The present working revision is built on the immutable v2.2.1 verification artifact, https://doi.org/10.5281/zenodo.22181589; replace this sentence with the exact v2.2.2 release URL and DOI before submission. The comparison with arXiv:2608.17267v1 is conditional on Source Comparison Hypotheses D1--D14; downstream consequences are additionally relative to named external results.
```

**Classification**

```text
Primary category: math.GT
MSC-class: 57R55 (Primary), 57K40, 57M05 (Secondary)
```

Leave journal reference, report number, and DOI blank. The submitter should
select `yes` for "Are you an author of this paper?" and must use a current,
truthful affiliation. If arXiv requests endorsement for `math.GT`, obtain it
through the account's endorsement link before submitting.

## Final web-form checks

1. Confirm the title, author, and abstract match this packet exactly.
2. Confirm the abstract is below arXiv's 1,920-character limit.
3. Confirm the generated PDF has 27 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
