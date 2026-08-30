# arXiv submission packet

> **RELEASE GATE:** this re-typeset manuscript is prepared for v1.5.9. Do not
> upload the packet until the v1.5.9 release URL resolves and the source and
> PDF assets match the final digests recorded below. Any further edit to
> `paper/main.tex` changes the packet digest, so rebuild and re-pin first.

This packet fixes the metadata for the v1.5.9 manuscript and prevents the
web form from drifting from the rendered paper.

## Build and upload

- From a clean checkout of the v1.5.9 tag, run
  `./paper/build_arxiv_source.sh`. The script fixes the file timestamp,
  numeric owner, archive format, and gzip header, so repeated builds from the
  same `paper/main.tex` are byte-for-byte identical.
- Upload `paper/arxiv-source-v1.5.9.tar.gz` as the v1.5.9 GitHub release asset
  and to arXiv.
- SHA-256: `aecb342174a11423b9959c3deffd56984e85724b253f7741fcdedc1b88d2568f`.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
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
We audit the theorem-critical computations in Wuebben's proposed exotic $S^2 \times S^2$ construction. Four explicit, hash-identified finite presentations associated with his fixed surgery parametrization are proved trivial by derivation certificates accepted by separate Python and Ruby checkers. This finite statement concerns only words and relations. To connect it to geometry, we independently reconstruct the marked genus-two bundle, surgery tori, common whiskers, meridians, and product-framed longitudes, and compare the resulting dictionary with the paper. We expose that dictionary and a worked peripheral extraction here. Exact-rational programs audit the framing calculation that identifies the product and Lagrangian longitudes; its remaining inputs are stated differential- and PL-topological results. Conditional on this geometric identification and twenty-five named external results, a replayed dependency chain recovers the paper's three manifold conclusions. We also record an unresolved contrary computation reported by Wuebben: Lidman and Piccirillo reportedly obtain $\pi_1(V)\neq1$, but no presentation or nontriviality witness is public, and their paper does not fix the parametrization needed to determine whether the same manifold was computed. Thus the finite presentation theorem is mechanically checkable, while the model-to-manifold identification remains an explicit human trust boundary. The theorems are Wuebben's; this note claims only the audit.
```

**Comments**

```text
19 pages, two figures, three tables. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v1.5.9 . Audits arXiv:2608.17267v1 relative to explicitly named external results.
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
