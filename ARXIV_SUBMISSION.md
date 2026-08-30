# arXiv submission packet

> **RELEASE GATE:** this major revision is prepared for v2.1.0. Do not
> upload or circulate the packet until the v2.1.0 release URL resolves and the source and
> PDF assets match the final digests recorded below. Any further edit to
> `paper/main.tex` changes the packet digest, so rebuild and re-pin first.

This packet fixes the metadata for the v2.1.0 manuscript and prevents the
web form from drifting from the rendered paper.

## Build and upload

- From a clean checkout of the v2.1.0 tag, run
  `./paper/build_arxiv_source.sh`. The script fixes the file timestamp,
  numeric owner, archive format, and gzip header, so repeated builds from the
  same `paper/main.tex` are byte-for-byte identical.
- Upload `paper/arxiv-source-v2.1.0.tar.gz` as the v2.1.0 GitHub release asset
  and to arXiv.
- Source-archive SHA-256:
  `fbd40f12faa361c89dfe7ca9d5d6393b9197176fad9980afed8b7d160daf62a4`.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Publish `paper/supplement.pdf` and `paper/supplement.tex` as versioned
  release assets alongside the main paper. The arXiv comments field points to
  that immutable release rather than treating the supplement as a second
  top-level TeX document.
- Main PDF SHA-256:
  `d6b3c985c79167e4ca79f0d4b971ba3d0cda03d8b0e8780bc8fc3d819cbec6b9`.
- Supplement PDF SHA-256:
  `360b2b302a73779b32d1c68d19e196c3c84a566caef891d1ff23e3f4e64df7df`.
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

## Synchronization gate

Run `python3 paper/check_release_sync.py` while preparing the candidate.  It
checks the PDF/source hashes, page/figure/table counts, Source Formalization D
terminology, and the two theorem-artifact manifests.  After reserving the
exact version DOI and replacing every candidate placeholder, run
`python3 paper/check_release_sync.py --final` from the clean checkout that is
tagged `v2.1.0`.  Final mode must pass before arXiv upload; it also requires
the same release URL and version DOI in the manuscript, supplement, README,
and this packet.  The script does not make a network request, so open both
links from a logged-out browser as the last release check.

## Metadata

All fields below are ASCII, as required by arXiv.

**Title**

```text
Certified simple connectivity of an audit model for Wuebben's proposed exotic $S^2 \times S^2$ construction
```

**Authors**

```text
John Clyde (VentiMath)
```

**Abstract**

```text
We define an explicit marked surface-bundle surgery manifold $V_aud$ modeled on the data in Wuebben's proposed exotic $S^2 \times S^2$ construction. Four hash-identified finite presentations are proved trivial by replayable derivation certificates under a published certificate specification. Separate combinatorial and geometric arguments identify those presentations with $\pi_1(V_aud)$, including the marked clutching, normal frontiers, commonly based peripheral curves, drilled transport relation, and product-to-Lagrangian framing bridge. Consequently $V_aud$ is simply connected. Comparison with Wuebben's fixed surgery member is isolated as a fourteen-clause Source Formalization D, with each clause tied to a target location, mechanical evidence, and its remaining non-mechanical content. The three downstream manifold conclusions are then conditional on that formalization and the cited classification, symplectic, and Floer-theoretic results. A reported contrary fundamental-group computation remains unreconciled; the paper lists all live failure locations rather than assigning the discrepancy in advance. Thus the source-independent audit theorem, not the conditional transfer to the proposed exotic manifolds, is the paper's primary result.
```

**Comments**

```text
24 pages, three figures, six tables, with an 11-page mathematical and computational supplement in the release assets. The primary result is the source-independent theorem $\pi_1(V_aud)=1$. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.1.0 . Exact v2.1.0 archive DOI: [INSERT AFTER DEPOSIT]. The comparison with arXiv:2608.17267v1 is conditional on the fourteen clauses of Source Formalization D; downstream consequences are additionally relative to named external results.
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
3. Confirm the generated PDF has 24 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
