# External review guide for the intrinsic audit-manifold theorem

This guide turns the manuscript's remaining specialist-review caveat into
three bounded tasks. It is **not** an external review and must not be cited
as one. The source-comparison checklist D1--D14 is a fourth, separate task;
none of those clauses is an input to the intrinsic theorem about
`V_aud`.

## 1. Certificate-checker conformance

The finite group-theoretic task is specified independently of either
implementation in `verification/luttinger/CERTIFICATE_SPEC.md`. Review
`verification/luttinger/CHECKER_AUDIT_GUIDE.md` and audit either the Python
or Ruby checker clause by clause. The required conclusion is whether one
checker conforms to the published specification, not whether KBMAG is
trustworthy. KBMAG generates certificates and is outside the trust base.

## 2. PL and peripheral conversion

This is the principal geometric risk for the theorem
`pi_1(V_aud) = 1`. Review the following claims in order.

| Main-paper claim | Finite evidence to inspect | Mathematical question | Failure consequence |
|---|---|---|---|
| Lemma 4.2, equivariant marked fiber | `fiber.py`, `independent_fiber.py`, `independent_fiber_certificate.json`, `lemma71_normal_form_check.py` | Do the ribbon, complementary disks, marked points, involution, and ordered five-chain determine the stated marked genus-two surface and equivariant extension? | The simplicial fiber may not model the audit definition. |
| Lemma 4.3, relative monodromy and graph clutching | `graph_clutching_check.py`, `graph_clutching_certificate.json`, `surface_bundle_theorem_audit.py`, `alternative_bundle_audit.py` | Do the certified relative monodromies and seam maps give a marked bundle homeomorphism that preserves the protected collars? | The model bundle may not be `R_aud`. |
| Lemma 5.1, local flatness and normal frontier | `torus_local_flatness.py`, `torus_local_flatness_certificate.json`, `frontier_normal_equivalence.py`, `frontier_normal_equivalence_certificate.json` | Do the simplex-link pairs prove local flatness, and does the explicit frontier map identify every stored dual meridian with the normal-circle fiber? | The extracted boundary words may live on the wrong peripheral boundary. |
| Lemma 5.2, complement presentation | `complement_theorem_audit.py`, the sealed Tietze transport, and `verification/notes/complement_presentation_referee_packet_2026-08-26.md` | Do the deleted subcomplex, punctured complement, and complement of the normal-block interior have the stated common homotopy type, and is the presentation complete rather than merely a list of valid relations? | The finite presentation may fail to present `pi_1(C_aud)`. |
| Lemmas 5.5--5.6, based peripheral pairs | `independent_peripheral_extractor.py`, `independent_peripheral_certificate.json`, `alpha_residual/`, `beta_residual/` | Are the meridians and longitudes based by the same literal whiskers, with the stated orientation, and does the beta sweep contribute exactly `r^-1 M r`? | The filling relators may be wrong. |
| Lemma 5.7, drilled transport relation | `r3_complement_audit.py` and run 67 | Does every cell of the transported homotopy avoid both surgery tori, including the pushed-off beta sweep? | A relation valid before drilling may have been used in the complement. |
| Theorem 5.8, filling comparison | Lemma 5.2 plus the exact two stored slope words | Does van Kampen add precisely the normal closure of the two displayed slopes, and does the complete complement presentation make the map an isomorphism? | Triviality of the explicit group would not prove simple connectivity of `V_aud`. |

A useful PL review report should give a yes/no/incomplete disposition for
every row, name the exact commit and artifact digests, and distinguish a
defect in finite evidence from a defect in the prose-to-topology inference.

## 3. Symplectic and framing conversion

This task is not an input to simple connectivity. It is the principal risk
for the intrinsic assertion that `V_aud` is symplectic.

1. Check that the common invariant fiber area form and the base area form
   descend to the global closed split form and give the stated orientation.
2. Check simultaneous standardization on the two protected collars and the
   claimed absence of mixed terms.
3. Check the relative Moser map, alpha quotient seam, beta mapping-torus
   seam, and orientation of the normal momentum plane.
4. Check that the named product push-offs become constant-covector copies
   and have zero coefficient in the meridian direction after radial
   projection.
5. Check that the fiber-dilation comparison of Weinstein charts remains
   uniformly in the punctured neighborhood over each entire named curve.
6. Check that the two unit product-framed fillings meet the hypotheses and
   sign convention of ADK Definition 2.1 and Proposition 2.2.

The detailed internal packet is
`verification/notes/framing_lemma_referee_packet_2026-08-25.md`. Supporting
finite checks include `framing_check.py`, `moser_cumulative_flow.py`,
`equivariant_moser_lift.py`, and `simplicial_lift_check.py`. These programs
localize the review; they do not replace the geometric argument.

## 4. Source comparison is not part of these reviews

The comparison between `V_aud` and Wuebben's fixed member remains open.
The supplement divides it into textual/diagrammatic clauses D1--D11 and
smooth/framing clauses D12--D14. In particular, D12--D14 must eventually be
replaced by an actual relative smooth comparison theorem if one wants to
transfer the intrinsic result to Wuebben's object. Neither the intrinsic
simple-connectivity theorem nor the intrinsic symplectic theorem assumes
that transfer.

