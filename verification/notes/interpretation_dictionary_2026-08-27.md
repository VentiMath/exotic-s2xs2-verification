# The interpretation dictionary

Every other artifact in this repository certifies mathematics *given a
reading* of arXiv:2608.17267. This note and its checker make the reading
itself a first-class, bound artifact: one table of every convention the
verification takes from the paper, with three columns of support per entry —
the certified computation that would fail under a rival reading, the
author's own machine-readable formulation where his committed code defines
the same convention, and an honest RESIDUAL flag where neither exists.

The motivation is that after runs 48–52 the dominant project-specific risk
is no longer any theorem citation but this translation layer. Managing it
means three things: keep the dictionary in one place, name the
discriminating witness per entry, and use the author's committed code — not
his prose, and not his attention — as an independent confirmation channel.

## The author-code cross-check

`luttinger/interpretation_dictionary.py` parses, without executing, the
author's committed scripts:

* the beta action is AST-extracted from `psi_letter` in
  `author_scripts/develop.py` and equals our certified reading
  `x -> y^-1, y -> yx, r -> r, s -> s`, and his own displayed relation
  `B kappa_3 B^-1 = psi(kappa_3)` ties that action to conjugation by `B`,
  matching our convention's direction;
* his `decide.g` base relators give, after the checker's own free-reduction
  derivation, the alpha swap `x<->r, y<->s` and the clean beta relators;
* his derived-correction shapes `mkAs`, `mkBy`, `mkBs` — including his own
  conjugator `delta := r^-1` — specialize at `eA=+1, eB=-1` to exactly the
  certified package `M1: AsA^-1 = N*y`, `M2: ByB^-1 = M^-1*(yx)`,
  `M3: BsB^-1 = (r^-1*M^-1*r)*s` of runs 13–14;
* the meridian-killed shadows of his corrected relations reproduce the psi
  action, so his complement-level and fiber-level conventions agree with
  each other and with ours.

A misreading of the paper that survives this comparison would have to be a
misreading shared, independently, by the author's own machine formulation of
his construction. That is a much stronger position than agreement with our
own transcription, and it does not require the author's attention.

## Residual entries

Three entries have no fully independent discriminating witness and are
declared as the honest remainder:

1. **beta-word-order** (`psi0 = T_a o T_b`, `T_b` first). The author's code
   pins the *action*, not the word. Scope: a rival word with the same action
   leaves every `pi_1` conclusion unchanged; it could affect only the
   marked-bundle assembly of runs 51–52.
2. **ribbon-dictionary** (the five-chain figure transcription). Mitigated by
   runs 22 and 34: two independently built realizations agree equivariantly.
3. **twist-sign-convention** (`b:+1, a:-1`). Discriminated only through the
   run-12 action calibration.

These three are where a referee should look first, and where author
confirmation — if it ever arrives — would add the most.

## Ledger position

`M_interpretation_dictionary` enters the ledger as a machine certificate and
is attached to `G_marked_bundle_identification`: the identification of our
model with the paper's bundle now cites, alongside the based-monodromy
replays and the thickening interpretations, the fact that the author's own
committed formulation matches the dictionary on every machine-comparable
entry.
