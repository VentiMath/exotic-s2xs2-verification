# arXiv submission packet

This packet fixes the metadata for the v1.5.1 manuscript and prevents the
web form from drifting from the rendered paper.

## Upload

- Upload `arxiv-source-v1.5.1.tar.gz` from the v1.5.1 GitHub release.
- SHA-256: `e8934464b1859d54352399dc77cfaef6891498aefc64f86861c32b5602e833c0`.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

## Metadata

All fields below are ASCII, as required by arXiv.

**Title**

```text
Certificate-based verification of the fundamental-group and framing steps in Wuebben's exotic $S^2 \times S^2$ construction
```

**Authors**

```text
John Clyde (VentiMath)
```

**Abstract**

```text
Wuebben (arXiv:2608.17267v1), building on Lidman--Piccirillo (arXiv:2505.14387v1), proves that a specified symplectic 4-manifold $V$ with the homology of $S^2 \times D^2$ is simply connected and deduces three theorems, including an exotic $S^2 \times S^2$. We give a certificate-based verification of the theorem-critical fundamental-group and framing steps and a machine-replayed audit of the downstream argument. Starting from the paper's marked-fiber data, we independently rebuild the bundle, extract the surgery tori and based peripheral curves, and compare the resulting relations, sign tables, and filling words with the paper; every compared item agrees. The four convention-specialized relator sheets containing the paper's single fixed filling are proved trivial by complete confluent rewriting, with derivation certificates accepted by independently implemented Python and Ruby checkers. Exact-rational Python programs verify the displayed calculus of the framing lemma and finite scripts check its stated combinatorial hypotheses. Finally, an explicit dependency chain states twenty-five external theorems with their hypotheses and discharges each hypothesis by a named certificate, computation, or earlier step. Thus the three theorems are verified relative to explicitly named standard results, with no known project-specific gap. The theorems are Wuebben's; this note claims only the verification.
```

**Comments**

```text
12 pages. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v1.5.1 . Verifies arXiv:2608.17267v1 relative to explicitly named standard results.
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
3. Confirm the generated PDF has 12 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
