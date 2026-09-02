# arXiv submission packet

This file preserves the intended arXiv metadata while preventing the web form
from drifting from the rendered paper.

## Release identifiers

- Release URL: https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.4.0
- Exact v2.4.0 archive DOI: https://doi.org/10.5281/zenodo.22254457
- Concept DOI: https://doi.org/10.5281/zenodo.22169753

Source-archive SHA-256:
  `52e23b16abd9e30e8a4309d3c9e201764838bfdfbfd9b2524deecaba66d96331`

Main PDF SHA-256:
  `589bf0b7448f50cf12c262bc05621fb09f7e052bb3adca8d7b0f9c6b2dc6fe75`

Supplement PDF SHA-256:
  `0e970f3e848c4cf3aa79519303bdf265ba79eee1533ebf94b8e5160bb3c29adb`

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
An exotic $S^2 \times S^2$ from a certificate-checked surface-bundle surgery manifold
```

**Authors**

```text
John Clyde (VentiMath)
```

**Abstract**

```text
We define a compact marked surface-bundle surgery manifold $V_{aud}$, prove that $\pi_1(V_{aud})=1$, and double it along an explicit involution $\sigma_{aud}$ of its boundary. The closed manifold $Z_{aud} = V_{aud} \cup_{\sigma_{aud}} V_{aud}$ is simply connected and spin with intersection form $H$, hence homeomorphic to $S^2 \times S^2$ by Freedman; it is a closed genus-two surface bundle over a genus-two surface surgered along four Lagrangian tori, hence symplectic with symplectic Kodaira dimension at least zero by Auroux-Donaldson-Katzarkov, Liu, and Ho-Li; hence, since Li's Kodaira dimension is an invariant of the oriented diffeomorphism type, it is not diffeomorphic to $S^2 \times S^2$. The final classification and non-diffeomorphism deductions use named external theorems whose hypotheses are discharged in the text. Simple connectivity itself rests on ten explicit relations in the torus complement together with the two product-filling words: the group they present is trivial, a four-line coset enumeration, and the geometric content of the paper is that those relations and filling words hold. Sealed derivation certificates derive the same relations from the triangulation and re-prove triviality by a second route; their automated replay assumes that at least one checker conforms to the mathematical specification, and the two shipped implementations have not received an independent human line-by-line audit. The construction was motivated by Wuebben's proposed exotic $S^2 \times S^2$; whether $Z_{aud}$ is his manifold is an attribution question, recorded clause by clause as checklist D1--D14 in the supplement, on which no theorem here depends.
```

**Comments**

```text
33 pages, five figures, and two tables, with an 18-page mathematical and computational supplement available as a release asset at https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.4.0 (archived at https://doi.org/10.5281/zenodo.22254457). The primary result is Theorem A': the double $Z_{aud}$ of the certificate-checked simply connected surgery manifold $V_{aud}$ along its intrinsic boundary involution is a closed symplectic 4-manifold homeomorphic but not diffeomorphic to $S^2 \times S^2$. The comparison with arXiv:2608.17267v1 is attribution, recorded as checklist D1--D14 in the supplement; no theorem depends on it.
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
