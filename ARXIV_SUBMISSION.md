# arXiv submission packet

This packet fixes the metadata for the v1.5.1 manuscript and prevents the
web form from drifting from the rendered paper.

## Upload

- Upload `arxiv-source-v1.5.1.tar.gz` from the v1.5.1 GitHub release.
- SHA-256: `5acc2e134fef9fa29887e300b80f92206554c9befe8c0996e4df3ebc44f5a99f`.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

## Metadata

All fields below are ASCII, as required by arXiv.

**Title**

```text
Independent machine verification of Wuebben's exotic $S^2 \times S^2$
```

**Authors**

```text
John Clyde (VentiMath)
```

**Abstract**

```text
Wuebben (arXiv:2608.17267v1), building on Lidman--Piccirillo (arXiv:2505.14387v1), proves that a specified symplectic 4-manifold $V$ with the homology of $S^2 \times D^2$ is simply connected and deduces three theorems: its symplectic double is an exotic $S^2 \times S^2$; its quotient is homeomorphic to Kawauchi's manifold $B$ but distinguished from it by the smooth sliceness of the figure-eight knot; and the Lidman--Piccirillo regluing is an exotic $\mathbb{CP}^2\#\overline{\mathbb{CP}}^2$. We independently machine-verify this argument. We rebuild the bundle as a simplicial complex from the paper's marked-fiber data, extract the surgery tori and based peripheral curves, and prove the four theorem-critical filled presentations trivial by complete confluent rewriting. Each computation emits a derivation certificate accepted by two independently written checkers. The framing lemma identifying the combinatorial and Lagrangian longitudes is machine-checked. We then express the deductions to the three theorems as an explicit dependency chain: twenty-five external theorems are stated with their hypotheses; every hypothesis is discharged by a named certificate, computation, or earlier step; and two checkers replay every finite calculation. Thus the three theorems are verified relative to explicitly named standard results, with no known project-specific gap. The theorems are Wuebben's; this note claims only the verification. All artifacts are public in a pinned release.
```

**Comments**

```text
11 pages. Verification artifacts and replay instructions: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v1.5.1 . Verifies arXiv:2608.17267v1 relative to explicitly named standard results.
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
3. Confirm the generated PDF has 11 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` on page 1.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
