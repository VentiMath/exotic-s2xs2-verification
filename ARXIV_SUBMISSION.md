# arXiv submission packet

> **RELEASE GATE:** this major revision is prepared for v2.2.0. Do not
> upload or circulate the packet until the v2.2.0 release URL resolves and the source and
> PDF assets match the final digests recorded below. Any further edit to
> `paper/main.tex` changes the packet digest, so rebuild and re-pin first.

This packet fixes the metadata for the v2.2.0 manuscript and prevents the
web form from drifting from the rendered paper.

## Build and upload

- From a clean checkout of the v2.2.0 tag, run
  `./paper/build_arxiv_source.sh`. The script fixes the file timestamp,
  numeric owner, archive format, and gzip header, so repeated builds from the
  same `paper/main.tex` are byte-for-byte identical.
- Upload `paper/arxiv-source-v2.2.0.tar.gz` as the v2.2.0 GitHub release asset
  and to arXiv.
- Source-archive SHA-256:
  `f4947a7a6e16f6095626d71d007ac4fe166da495601f1e187928e7011475fa0b`.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Publish `paper/supplement.pdf` and `paper/supplement.tex` as versioned
  release assets alongside the main paper. The arXiv comments field points to
  that immutable release rather than treating the supplement as a second
  top-level TeX document.
- Main PDF SHA-256:
  `39d794b830ba8e60ff96777f2f4c4dfe0ee1f88d203125a367a4b0fafd9b0b53`.
- Supplement PDF SHA-256:
  `b399f4100b4a3c69fb7df68c8bd0859548207fdb881693e7c9138f51209dca9e`.
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

## Synchronization gate

Run `python3 paper/check_release_sync.py` while preparing the candidate.  It
checks the PDF/source hashes, page/figure/table counts, Source Comparison Hypotheses D1--D14
terminology, and the two theorem-artifact manifests.  After reserving the
exact version DOI and replacing every candidate placeholder, run
`python3 paper/check_release_sync.py --final` from the clean checkout that is
tagged `v2.2.0`.  Final mode must pass before arXiv upload; it also requires
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
We define an explicit marked surface-bundle surgery manifold $V_aud$ modeled on the data in Wuebben's proposed exotic $S^2 \times S^2$ construction. Four hash-identified finite presentations are proved trivial by replayable derivation certificates under a published certificate specification. Automated acceptance of the stored derivations additionally assumes that at least one checker conforms to that specification; the two shipped implementations were developed within the project and have not received an independent human line-by-line audit. Separate combinatorial and geometric arguments identify the fixed $(+,+)$ presentation with $\pi_1(V_aud)$, including the marked clutching, normal frontiers, commonly based peripheral curves, and drilled transport relation; the other three sign sheets are algebraic robustness checks. Consequently $V_aud$ is simply connected. A logically separate theorem identifies the product-framing curves with the Lagrangian-framing classes needed for comparison with the symplectic source construction. Comparison with Wuebben's fixed surgery member is isolated as fourteen explicit Source Comparison Hypotheses, D1--D14, classified as textual, diagrammatic, or smooth/framing assumptions. The three downstream manifold conclusions are then conditional on those hypotheses and the cited classification, symplectic, and Floer-theoretic results. A reported contrary fundamental-group computation remains unreconciled; the paper lists all live failure locations rather than assigning the discrepancy in advance. Thus the source-independent audit theorem, not the conditional transfer to the proposed exotic manifolds, is the paper's primary result.
```

**Comments**

```text
25 pages, three figures, five tables, with a 14-page mathematical and computational supplement in the release assets. The primary result is the source-independent theorem $\pi_1(V_aud)=1$. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.2.0 . Exact v2.2.0 archive DOI: https://doi.org/10.5281/zenodo.22181233. The comparison with arXiv:2608.17267v1 is conditional on Source Comparison Hypotheses D1--D14; downstream consequences are additionally relative to named external results.
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
3. Confirm the generated PDF has 25 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
