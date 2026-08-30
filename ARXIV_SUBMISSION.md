# arXiv submission packet

> **RELEASE GATE:** this major revision is prepared for v2.0.0. Do not
> upload the packet until the v2.0.0 release URL resolves and the source and
> PDF assets match the final digests recorded below. Any further edit to
> `paper/main.tex` changes the packet digest, so rebuild and re-pin first.

This packet fixes the metadata for the v2.0.0 manuscript and prevents the
web form from drifting from the rendered paper.

## Build and upload

- From a clean checkout of the v2.0.0 tag, run
  `./paper/build_arxiv_source.sh`. The script fixes the file timestamp,
  numeric owner, archive format, and gzip header, so repeated builds from the
  same `paper/main.tex` are byte-for-byte identical.
- Upload `paper/arxiv-source-v2.0.0.tar.gz` as the v2.0.0 GitHub release asset
  and to arXiv.
- Source-archive SHA-256:
  `4ae6b0a2575af6e7c6975df671d0c669aa5283fc44747fd3b21bccb198021f7b`.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Publish `paper/supplement.pdf` and `paper/supplement.tex` as versioned
  release assets alongside the main paper. The arXiv comments field points to
  that immutable release rather than treating the supplement as a second
  top-level TeX document.
- Main PDF SHA-256:
  `a3c31badad21ee03e405b529813577e4b671c6c32976f494da8cf98e80142d48`.
- Supplement PDF SHA-256:
  `75345ecb1358b0d15e5bfb84bfb214cee9f82b1b06d0cd8651c13eaeee059a1e`.
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

## Metadata

All fields below are ASCII, as required by arXiv.

**Title**

```text
A certificate-based audit of the fundamental-group and framing computations in Wuebben's proposed exotic $S^2 \times S^2$ construction
```

**Authors**

```text
John Clyde (VentiMath)
```

**Abstract**

```text
We audit the fundamental-group and framing calculations in Wuebben's proposed exotic $S^2 \times S^2$ construction. Four explicit, hash-identified finite presentations are proved trivial by replayable derivation certificates under a published certificate specification. From the marked data we define an explicit audit manifold $V_*$ and prove, in separate geometric steps, that those presentations are presentations of $\pi_1(V_*)$; this makes the common whiskers, meridians, product longitudes, drilled transport relation, and product-to-Lagrangian framing bridge inspectable. We then isolate four source-identification assumptions S1--S4 under which $V_*$ is Wuebben's intended fixed surgery member. Thus $V_*$ is simply connected, while the transfer of that conclusion to Wuebben's member is explicitly conditional on S1--S4. Conditional also on twenty-five named external results, the three manifold conclusions of Wuebben's paper follow. A reported contrary fundamental-group computation is stated separately and bears on the source comparison, not on the finite certificate theorem. The theorems are Wuebben's; this note claims only the audit.
```

**Comments**

```text
21 pages, two figures, four tables, with a 10-page computational supplement in the release assets. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.0.0 . The comparison with arXiv:2608.17267v1 is conditional on four explicitly stated source-identification assumptions; downstream consequences are additionally relative to named external results.
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
3. Confirm the generated PDF has 21 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
