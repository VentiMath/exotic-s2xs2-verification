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
  `94fae57ad99db0ce8de888d1c0f69a0d50d18592911597ceb8fa4e7e70a63b5e`.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Publish `paper/supplement.pdf` and `paper/supplement.tex` as versioned
  release assets alongside the main paper. The arXiv comments field points to
  that immutable release rather than treating the supplement as a second
  top-level TeX document.
- Main PDF SHA-256:
  `65e7ce69164e504e44de6d385261654220c95a4bb45276a3a255b4ef5c903971`.
- Supplement PDF SHA-256:
  `3e458c08a860e2f3e715a3a7354cea3e49ce280303f9f8c49ef0bcab97ae5ad7`.
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

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
We define an explicit marked surface-bundle surgery manifold $V_aud$ modeled on the data in Wuebben's proposed exotic $S^2 \times S^2$ construction. Four hash-identified finite presentations are proved trivial by replayable derivation certificates under a published certificate specification. Separate combinatorial and geometric arguments identify those presentations with $\pi_1(V_aud)$, including the marked clutching, normal frontiers, commonly based peripheral curves, drilled transport relation, and product-to-Lagrangian framing bridge. Consequently $V_aud$ is simply connected. Comparison with Wuebben's fixed surgery member is isolated as a fourteen-clause Source Formalization D, with each clause tied to a target location, mechanical evidence, and its remaining non-mechanical content. The three downstream manifold conclusions are then conditional on that formalization and the cited classification, symplectic, and Floer-theoretic results. A reported contrary fundamental-group computation remains unreconciled; the paper lists all live failure locations rather than assigning the discrepancy in advance.
```

**Comments**

```text
23 pages, three figures, six tables, with an 11-page mathematical and computational supplement in the release assets. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.1.0 . Exact v2.1.0 archive DOI: [INSERT AFTER DEPOSIT]. The comparison with arXiv:2608.17267v1 is conditional on the fourteen clauses of Source Formalization D; downstream consequences are additionally relative to named external results.
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
3. Confirm the generated PDF has 23 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
