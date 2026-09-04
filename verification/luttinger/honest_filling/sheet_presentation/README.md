# Presentation of Q on the eight sheet loops (origin of derived_01..19)

`mtc.g` / `mtc3.g` (GAP): load the sealed 3-generator Q (`generation_input.g`,
78 relators) and the eight sheet loops x, y, r, s, A, B, M, N as words in Q
(`extra_words.g`, the tracked geom words), and call
`IsomorphismFpGroupByGenerators(Q, sheet, "h")`, which returns a presentation
P of Q on generators h1..h8 = the sheet letters (GAP's modified Todd-Coxeter
route; hence "MTC" in the older notes).  `mtc3.log` holds P's relators.

`certify_P_relators.py`: each relator of P is substituted back into Q letters
through the geom words and reduced in the halted complement system
`alpha_residual/complement_input.rws.kbprog`; the relators that reduce to the
empty word are identities of pi_1(C_aud) and were saved as
`certified_P_relators.json`.  Those, deduplicated against the eight sheet rows,
are the `derived_NN` relations of `honest_filling.json`.

**Do not read the coset-enumeration lines of `mtc3.log` / `mtc4.log` as results.**
Those scripts (and `hand.g`, `core.g`, `robust.g`, `qtilde.g`) write the surface
row as GAP's `Comm(x,y)*Comm(r,s)`, which is `x^-1 y^-1 x y r^-1 s^-1 r s`, not the
audit's literal `x y x^-1 y^-1 r s r^-1 s^-1`.  In the halted complement system the
literal word reduces to the empty word (certified) while the `Comm` form leaves a
42-letter residual, so it is not a certified relation of `Q`; every "index 1" that
those scripts report for an honest single-half group is about a proper quotient
and is not evidence of triviality.  With the literal row the same eight honest
cases overflow (`../collapse_full.g`; the other agent's `direct_z/probe_honest_half.py`
replays `mtc3`'s relator ordering with the literal rows and also overflows, so the
old collapse was the convention, not the ordering).  Only P's relators from these
scripts are used, and each of those was certified separately (above).

The remaining files (`hand.g`, `hand2.g`, `core.g`, `iterate.g`, `lowindex.g`,
`cyclic_cosets.g`, `kb_y1pp.g`, `mcheck.g`, logs) are the early decision
attempts on the sheet-letter groups; the ones that mattered are summarised in
`../README.md`.  All of this was recovered from the session scratchpad on
2026-09-03 so that the provenance in `../WORD_PROVENANCE.md` points at files
in the tree.
