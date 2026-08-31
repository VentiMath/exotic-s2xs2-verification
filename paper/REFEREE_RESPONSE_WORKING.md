# Working response to the major-revision reports

This is an internal completion ledger for the unreleased post-v2.2.2
revision. It is not a claim of peer review and is not part of the arXiv
source archive.

| Referee issue | Disposition in the working revision |
|---|---|
| The paper had not chosen between an intrinsic audit paper and a verification of Wuebben. | **Resolved.** The title, abstract, principal theorem, dependency figure, and conclusion now center the separately defined `V_aud`. No theorem identifies it with Wuebben's member and no exotic-manifold conclusion is asserted. |
| The abstract and conclusion repeated validation status. | **Resolved.** The abstract is shortened and begins with the intrinsic theorem; the conclusion is two short paragraphs. One scope/review section carries the detailed caveats. |
| Tables and implementation inventory overwhelmed the main mathematics. | **Resolved.** The main paper now has one dependency figure and two mathematical tables. Record counts, raw paths, hashes other than the normative manifest, and historical inventories are in the supplement. Tables S1 and S2 use landscape pages. |
| Section 6 was logically separate from simple connectivity. | **Resolved.** Simple connectivity and intrinsic topology are complete before the framing section. The section is retained because it now proves the co-primary, source-independent symplecticity assertion in the Audit-Manifold Theorem. |
| Lemma 5.3 displayed the same disk-coordinate formula for both signs. | **Resolved.** The negative-meridian case uses complex conjugation. The induced boundary matrix, four-dimensional orientation, boundary orientation, and extension criterion are stated explicitly. |
| The four sign sheets were not formally distinguished from one manifold. | **Resolved.** Only `P_(+,+)` is geometrically identified with `V_aud`. The other three are explicitly only algebraic robustness sheets. A general torus-filling extension lemma precedes the convention-change corollary. |
| Complement of a torus versus complement of a normal neighborhood was implicit. | **Resolved.** The normal-frontier/complement argument explicitly identifies the deleted subcomplex, punctured complement, and complement of the normal-block interior up to the needed homotopy equivalence. |
| The three-generator presentation was not conceptually explained. | **Resolved.** The manuscript explains what the three surviving generators encode and gives a human-readable terminal collapse `a=bc`, `ac^2=1`, `b^2c=cab`, forcing all three generators to be trivial. |
| Checker acceptance was presented too much like a mathematical theorem. | **Resolved.** The former artifact theorem and detailed inventory moved to the supplement. The main finite theorem rests on a normative grammar and a mathematical soundness theorem, with implementation conformance stated as a trust assumption. |
| The checkers lacked genuinely independent review. | **Open external review, narrowed.** The manuscript does not claim such review. Python and Ruby now exercise the same major corruption classes, and `verification/luttinger/CHECKER_AUDIT_GUIDE.md` maps every specification clause to both implementations and supplies a one-page audit protocol. Only an outside review can close this item. |
| The geometry-to-presentation bridge needed equal emphasis with the framing bridge. | **Resolved editorially; open external review.** The main paper now identifies the PL/peripheral conversion as the principal geometric risk for simple connectivity. `verification/notes/EXTERNAL_REVIEW_GUIDE.md` gives a claim-by-claim review packet. |
| The normalized Thurston form and canonical Lagrangian class were insufficiently isolated. | **Resolved.** A global split-form/protected-collars lemma proves existence, descent, simultaneous collar standardization, absence of mixed terms, and orientation. A separate definition introduces the canonical Lagrangian-framing class before the framing theorem. |
| The framing bridge needed specialist review. | **Open external review, narrowed.** The paper and supplement state the exact six questions. The new external-review guide separates this from the PL review and from source comparison. |
| D1--D14 were too close to assuming the source bridge. | **Resolved by scope reduction.** D1--D14 are no longer hypotheses of a main-paper theorem. They are an open checklist in the supplement; D12--D14 are explicitly the genuine unresolved smooth/framing comparison. |
| The contrary Lidman--Piccirillo computation remained unresolved. | **Unresolved and accurately scoped.** The report remains prominent and neutral. Without their presentation, dictionary, or witness, relation-by-relation reconciliation cannot be performed. No conclusion about Wuebben's manifold is drawn. |
| The standalone significance of `V_aud` was underdeveloped. | **Resolved.** The Audit-Manifold Theorem now gives connected boundary, `chi=2`, complete integral homology, spinness, a primitive square-zero genus-two fiber, a proper section, and symplecticity, all without source comparison. A small arithmetic checker supplies negative controls and corroboration. |
| Section 5 mixed source-derived wording into the intrinsic proof. | **Resolved.** Source comparisons are labeled as consistency history and do not enter the audit-object theorem. The fixed object's paths, tori, and fillings are defined intrinsically. |
| Conditional exotic corollaries in the main article deferred their proof. | **Resolved.** They are removed from the main theorem stream. The supplement preserves the old conditional dependency audit as history, explicitly relative to the open comparison and named external results. |
| Standard topology inputs were too broadly cited. | **Resolved to the available source granularity.** The manuscript now cites Rourke--Sanderson Chapter 4 pp. 50--51, Constantin--Kolev Theorem 3.1 and Proposition 3.2, Hatcher case (IV) pp. 464--465, and ADK Section 2.1 first paragraph, Definition 2.1, and Proposition 2.2. Construction-specific star/link and extension arguments are also written out. |
| The main and supplement needed version identity and PDF metadata. | **Resolved for the working draft.** Both title pages identify the post-v2.2.2 working revision and artifact base; both PDFs carry title, author, subject, and keyword metadata. Final version/DOI replacement remains a release gate. |
| Public files and the immutable release could drift. | **Blocked from accidental submission, not yet released.** `ARXIV_SUBMISSION.md` and `paper/check_release_sync.py` treat this as an unreleased working revision. A new tag, archive DOI, regenerated manifest, hashes, and clean-tag final replay are mandatory before arXiv upload. |
| The final gate could accept stale CFF metadata, a stale README “newest release,” an old normative-root sentence, or old supplement recovery instructions. | **Resolved.** Final mode now checks the exact CFF title, abstract, version, top-level DOI, DOI descriptions, and release date; the README newest-release declaration; the main-paper manifest digest, versioned normative root, and self-citation; and the supplement's exact tag and `git rev-parse VERSION:verification` command. The sole permitted old-version occurrence is the explicit historical statement that the invariant checker was absent from the v2.2.2 manifest. |
| The working manifest did not bind the revised checkers or the invariant checker. | **Resolved for the working revision.** The regenerated 48-file manifest has SHA-256 `e8118b489a1b365c002a1931839fb419ab0f456aaecf724f2acf979612c9b5b9`; both papers record it, the supplement pins verification tree `57ed025145378a84884c5a63293ae35a8c00f899`, and candidate mode now runs the manifest generator in check mode. These are working identifiers until the next immutable release. |

## External items intentionally not represented as completed

1. independent human conformance audit of one filled-group checker;
2. external PL review of the marked-bundle and peripheral conversion;
3. external symplectic review of the framing theorem;
4. the missing Lidman--Piccirillo presentation and reconciliation; and
5. a relative smooth comparison proving D12--D14.

The revised paper does not require any of these five items for the theorem it
actually states. They determine what further claims could responsibly be
made and what a journal referee should examine.
