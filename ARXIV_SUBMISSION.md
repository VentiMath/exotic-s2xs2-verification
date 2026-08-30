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
  `cc1879c8151a96ecc152d6eb23db50e888246c587eaa91d624fc7da19dd7c876`.
  Two independent invocations of the deterministic build script produced
  byte-for-byte identical archives.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Publish `paper/supplement.pdf` and `paper/supplement.tex` as versioned
  release assets alongside the main paper. The arXiv comments field points to
  that immutable release rather than treating the supplement as a second
  top-level TeX document.
- Final local PDF SHA-256 digests are
  `79e05ef8ff6addf339fa42ea68ddac7a39718a4f54ce7ac9424564283afc5e87`
  for `paper/main.pdf` and
  `892823769623d6cfa50d69cfa4e1c14d08aea71d006c0467bea74cfa353de0e9`
  for `paper/supplement.pdf`. Recompute both after any source edit.
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
We audit the fundamental-group and framing calculations in Wuebben's proposed exotic $S^2 \times S^2$ construction. Four explicit, hash-identified finite presentations are proved trivial by replayable derivation certificates under a published certificate specification. We then reconstruct the marked genus-two bundle and surgery tori independently and prove, in separate geometric steps, that the certified presentations surject onto the fundamental group of Wuebben's fixed surgery manifold. The proof makes explicit the common whiskers, meridians, product longitudes, drilled transport relation, and the product-to-Lagrangian framing bridge. Consequently the fixed manifold is simply connected, conditional on this geometric identification; twenty-five named external results then yield the three manifold conclusions claimed in Wuebben's paper. The finite certificate theorem is mechanically checkable, whereas the marked model-to-manifold identification remains the principal human-review boundary. We state separately an unresolved contrary computation reported by Wuebben. The theorems are Wuebben's; this note claims only the audit.
```

**Comments**

```text
19 pages, two figures, three tables, with a 10-page computational supplement in the release assets. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.0.0 . Audits arXiv:2608.17267v1 relative to a stated geometric identification and explicitly named external results.
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
3. Confirm the generated PDF has 19 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
