# Direct relative representatives for the marked bundle

## What this closes

The surface-bundle comparison formerly invoked a relative isotopy-extension
choice after identifying the two absolute monodromy mapping classes. That is
unnecessary here. The representatives defining both marked torus subbundles
can be compared in the appropriate relative mapping classes from the outset.

## Alpha

The independent ribbon equivalence is equivariant for the chain-reversing
involution. On the complete three-row annular collar of `c`, the primary
involution is literally

\[
  (c,r,i)\longmapsto(c,r,i+4),
  \qquad r\in\{-1,0,1\},\quad i\in\mathbb Z/8.
\]

It fixes `p` and `O`. Thus the comparison conjugates the alpha monodromies
exactly on the marked collar; there is no absolute equality that must later
be adjusted by an isotopy.

## Beta

The paper defines

\[
 \psi_0=T_a\circ T_b
\]

with `T_b` applied first, supported in the left handle and equal to the
identity on the right handle. The combinatorial representative is built from
the same ordered twist word: the `b` shear is applied first and the `a` shear
second. Its calibrated combinatorial directions are `b:+1` and `a:-1`.

The checker constructs the entire 32-interface flip trace and the full
three-row annular collar of `e`. All 1,536 cone cells in the two twist traces
avoid that collar. More strongly, restriction to the collar is exactly the
staircase triangulation of the product at every interface: all 3,072 expected
tetrahedra occur and there are no additional collar tetrahedra. Run 28
independently verifies product behavior at the fixed `p` neighborhood through
the same 32 interfaces.

Consequently both beta representatives are the same product of relative
Dehn twists supported outside the `e` collar and `p`. Their equality belongs
to the relative mapping class group by construction. No isotopy-extension
theorem is being used to convert an absolute comparison into a relative one.

## Remaining theorem boundary

Run 52 uses these exact representatives to construct the two
mapping-cylinder maps and glue them directly. Thus ordinary bundle
classification and Dehn--Nielsen--Baer are no longer required either.
The elementary fact that the certified annular shear is the stated relative
Dehn twist remains part of the already exposed labeled bistellar-trace
interpretation, not a new smooth or relative-isotopy assumption.
