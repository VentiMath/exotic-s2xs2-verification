# Original Lidman--Piccirillo source-figure audit

## Question

Run 55 proves that an ordered genus-two five-chain with the stated
chain-reversing involution and two fixed points has Wuebben's equivariant
octagon normal form. The remaining source-level question was whether those
hypotheses actually occur in the original Lidman--Piccirillo construction,
rather than entering only through Wuebben's restatement.

Run 56 audits the immutable source archive of Lidman--Piccirillo,
`arXiv:2505.14387v1`, directly. It reads only the original `main.tex` and the
original Figure 1 asset `morecurves.pdf`. It does not read or import Wuebben's
paper, any simplicial model, any correspondence module, or a previous
certificate.

## Textual declarations

The original TeX states all of the non-pictorial inputs:

* `F` is a genus-two surface carrying the named curves `a,b,c,d,e` shown in
  Figure 1;
* the involution exchanges `a` with `e`, exchanges `b` with `d`, and fixes
  `c`;
* `c` is fixed setwise and with orientation; and
* the involution has two fixed points, used to produce the two sections in
  their Lemma 6.

The checker also parses the six TikZ labels and their positions from the
original source rather than using labels supplied by Wuebben.

## Original vector drawing

The Figure 1 asset is a vector PDF, not a flattened screenshot. The checker
converts it to SVG, separates its seven dark-blue vector elements into the
five labeled curve layers, and treats the source's solid and dashed pieces
separately. In the standard handle projection, a dashed piece is the portion
hidden behind the handle; its projected overlap is not an additional
intersection on the surface.

The solid-surface layers have exactly one connected crossing component for
each consecutive pair:

```
ab = 1, bc = 1, cd = 1, de = 1.
```

The full layers, including their hidden projections, have zero overlap for
every nonconsecutive pair:

```
ac = ad = ae = bd = be = ce = 0.
```

The green vector layer independently contains exactly two fixed-point dots,
centered on the same rotation axis. Their measured centers are approximately
`(486.932,117.792)` and `(486.932,514.001)` in the original
`1008 x 612` vector coordinates. This agrees with the TeX's explicit
two-fixed-point statement.

## Reproducibility and provenance

No Lidman--Piccirillo source file is copied into this repository. The checker
instead requires an extracted copy of the immutable arXiv v1 source and
refuses to run unless the two input hashes are

```
main.tex
183f91362b748f7d633bfd12553ee5abb47ba6835607753eecb4bf04e385dcca

morecurves.pdf
40ec26c50b735e9f8a3303dd559d668af5abb45d5b78d2c39c30665156963cca
```

Poppler performs the vector conversion and ImageMagick rasterizes only the
separated vector masks. The checker then performs all component and overlap
calculations itself using the Python standard library.

## Conclusion

Every marked hypothesis consumed by Run 55 is present in the original
Lidman--Piccirillo source. No label, intersection, involution, orientation, or
fixed-point discrepancy was found. The only interpretation left at this
source boundary is the ordinary diagrammatic convention that dashed arcs in
the handle picture denote hidden-side projection rather than extra surface
crossings.
