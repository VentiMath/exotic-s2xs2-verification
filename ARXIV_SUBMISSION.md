# arXiv submission packet

> **WORKING-REVISION GATE:** the metadata below describes the unreleased
> post-v2.2.2 manuscript. Do not upload it to arXiv until the revision has a
> new immutable tag and exact archive DOI, every printed identifier has been
> regenerated, and `python3 paper/check_release_sync.py --final --version VERSION` passes from
> a clean checkout of that new tag. The v2.2.2 identifiers below are only the
> archived artifact base, not identifiers for the revised PDFs.

This file preserves the intended arXiv metadata while preventing the web form
from drifting from the rendered paper.  Final release hashes must be inserted
only after the next immutable archive is built.

## Build and upload

- From a clean checkout of the eventual revision tag, run
  `./paper/build_arxiv_source.sh`. The script fixes the file timestamp,
  numeric owner, archive format, and gzip header, so repeated builds from the
  same `paper/main.tex` are byte-for-byte identical.
- Upload the newly versioned source archive as a GitHub release asset and to
  arXiv.
- Record the new source-archive SHA-256 here during the release cut.
- The archive contains one necessary file, `main.tex`, at its root. Do not
  upload the generated PDF alongside TeX source.
- Publish `paper/supplement.pdf` and `paper/supplement.tex` as versioned
  release assets alongside the main paper. The arXiv comments field points to
  that immutable release rather than treating the supplement as a second
  top-level TeX document.
- Record the new main and supplement PDF SHA-256 values here during the
  release cut.
- Confirm or regenerate the filled-group proof manifest after the final code
  change. It must bind the revised Python checker and
  `audit_manifold_invariants.py`; rerun both certificate checkers, the
  invariant checker, and the release gate from the clean tagged checkout.
- Rewrite `CITATION.cff` as one coherent record for the new release: exact
  manuscript title, abstract, version, release date, version DOI, DOI
  descriptions, and tag URL. The abstract must match this packet verbatim,
  and the ISO release date must match the human-readable date on both PDF
  title pages. Final mode checks each of these fields.
- Select the automatically detected PDFLaTeX-compatible processor and
  `main.tex` as the top-level file. Inspect arXiv's generated PDF before the
  final submission step.

## Synchronization gate

Run `python3 paper/check_release_sync.py` while preparing the candidate.  It
checks the PDF/source hashes, page/figure/table counts, open-checklist
D1--D14 terminology, executes every documented theorem-facing replay in both
implementations where available, and checks both artifact digests.  After reserving the
exact version DOI and replacing every candidate placeholder, run
`python3 paper/check_release_sync.py --final --version VERSION` from the clean checkout carrying
the new tag.  Final mode must pass before arXiv upload; it also requires
the same release URL and version DOI in the manuscript, supplement, README,
and this packet.  The script does not make a network request, so open both
links from a logged-out browser as the last release check.

## Metadata

All fields below are ASCII, as required by arXiv.

**Title**

```text
Certificate-checked simple connectivity of a surface-bundle surgery manifold
```

**Authors**

```text
John Clyde (VentiMath)
```

**Abstract**

```text
We define a compact marked surface-bundle surgery manifold $V_{aud}$ and prove that $\pi_1(V_{aud})=1$. Four explicit finite presentations are trivial under a published derivation-certificate specification; a geometric reconstruction identifies one of them with $\pi_1(V_{aud})$. The same construction gives $\chi(V_{aud})=2$, integral homology concentrated in degrees zero and two, spinness, a primitive square-zero genus-two fiber, and a surviving relative section. A separate framing theorem identifies the product push-offs used in the definition with canonical Lagrangian-framing classes, so standard Luttinger surgery gives a symplectic structure on $V_{aud}$. Automated certificate replay assumes that at least one checker conforms to the mathematical specification; the two shipped implementations have not received an independent human line-by-line audit. The construction was motivated by Wuebben's proposed exotic $S^2 \times S^2$, but identifying $V_{aud}$ with Wuebben's fixed member remains an open comparison problem recorded clause by clause in the supplement. No exotic-manifold conclusion is asserted here.
```

**Comments**

```text
22 pages, four figures, and two tables, with a 17-page mathematical and computational supplement planned as a release asset. The primary result is the source-independent theorem $\pi_1(V_aud)=1$. The comparison with arXiv:2608.17267v1 remains open and is recorded as checklist D1--D14 in the supplement; no exotic-manifold conclusion is asserted. Replace this sentence with the new immutable release URL and exact archive DOI before submission.
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
3. Confirm the generated PDF has 22 pages, no missing references, and the
   target/version line `arXiv:2608.17267v1` in the introduction.
4. Confirm the source processor selected `main.tex` and did not treat
   `TARGET.md` or a generated PDF as source; neither is in the upload archive.
5. Choose the arXiv distribution license deliberately and complete the final
   submission from the author's own account.
