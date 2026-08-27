# Independent reconstruction of the paper-to-model dictionary

## Independence design

`paper_coordinate_extractor.py` is deliberately quarantined. It uses only
the Python standard library and reads only the raw text extraction of
arXiv:2608.17267. It does not import or read `paper_data.md`, the authors'
scripts, any fiber/bundle/layer/correspondence/peripheral module, or any prior
certificate. It locates and hashes the paper passages for the Section 3.2
handle dictionary, Lemma 7.1 and the five-chain, Section 7.2's twists, the
cut-square surgery tori, Sections 8.3--8.5's whiskers and directions, and
Table 1. It then reconstructs the abstract marked ribbon and word algebra.

Only after that certificate has been frozen does the separate
`paper_model_dictionary_compare.py` process read Runs 34, 51, and 52 and the
path-level evidence from Runs 12, 14--16, and 30. This one-way split prevents
the extractor from learning the answer from the model it is meant to audit.

## Independent reconstruction

The paper gives the ordered five-chain `a,b,c,d,e`, with consecutive curves
intersecting once and all other pairs disjoint. The involution reverses the
chain (`a<->e`, `b<->d`, `c->c`) and fixes the marked points `p` and `O`. The
handle dictionary is reconstructed as

```
a ~ x,  b ~ y,  c ~ xr,  d ~ s,  e ~ r.
```

The `c` curve based at `V_2` is the word `XR`, split into the named halves
`R` and `x`. With right twists written exactly as in the paper,

```
T_a: x -> x,      y -> yx
T_b: x -> x y^-1, y -> y
```

and applying `T_b` first in `psi_0=T_a T_b` gives

```
x -> y^-1,  y -> yx.
```

The extractor also reconstructs the two surgery tori (`c` over the alpha
direction and `e` over the beta direction), the named common whiskers `y_1`
and `s_2`, the order `c_s` before `s_e`, `delta=r^-1`, and the paper-coordinate
direction words `A x` and `(r^-1 M^-epsilon r) B`. Mutation controls verify
that reversing the twist order or reversing the sign of `T_b` changes the
marked action, so these are genuinely discriminating checks rather than
homological fingerprints.

## Comparison result

The frozen paper reconstruction agrees exactly with:

* Run 34 on the five-chain intersection matrix, involution, and fixed marks;
* Run 51 on the `c` half-rotation, `T_b`-then-`T_a` factor order, beta action,
  and product behavior on the `e` collar;
* Run 52 on the alpha seam atoms and the ordered beta twist tokens;
* Run 30 on the literal `y_1` and `s_2` whiskers;
* Run 15 on the selected `A x` half; and
* Runs 12, 14, and 16 on the corrected `M1`--`M3` words and the two named
  surgery directions.

No paper-to-model dictionary discrepancy was found.

## Honest boundary

This is an independent semantic extraction from the paper's raw text, not a
computer-vision reading of Figure 1. It uses Lemma 7.1 and the paper's prose
and displayed declarations to reconstruct the marked ribbon. Thus it attacks
shared transcription, order, sign, label, and whisker errors, but it does not
prove Lemma 7.1 itself or replace the elementary ribbon-thickening argument
that realizes the declared figure as a surface.

Runs 55--56 subsequently close that stated boundary relative to the
Kerékjártó periodic-disk theorem: Run 55 exhausts the equivariant ribbon
normal form, and Run 56 recovers its marked hypotheses directly from the
original Lidman--Piccirillo TeX and vector Figure 1.
