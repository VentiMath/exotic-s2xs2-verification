# Formalization and risk register (2026-08-23)

## Bottom line

The proof can be formalized further, but the useful target is not to formalize
Freedman theory or Heegaard Floer homology from foundations. The useful target
is the narrow seam between the paper's smooth geometric data and the finite
presentation whose triviality is computed.

The current evidence is strong, but it is not a fully kernel-checked formal
proof. `luttinger/proof_ledger.py` now makes the trust boundary explicit and
refuses missing dependencies, cycles, or absent evidence files.

## Risks, in descending order

### R1. Peripheral semantic identification — highest remaining risk

The computation is only relevant if its based meridians and Lagrangian
push-offs are exactly the paper's. A simultaneous conjugacy, inverse, or
half-drift error can change the filled group while leaving abelian invariants
and many fingerprints unchanged.

Already formalized: literal based fiber generators and monodromies; path-level
M1--M3 corrections and the local `N` meridian; direct boundary longitudes at
the actual torus corners; slope permutation and whisker conjugacies; exact
half-drift/framing coordinate algebra; and a basing-sensitive calibration.

Still theorem-level: smoothing the PL mapping-cylinder bundle as the marked
smooth bundle; relative/equivariant Moser and Weinstein invariance; and carrying
the named Lagrangian framings to the combinatorial product framings. The first
two are standard. The last is where an expert should try hardest to falsify,
although Lemma 8.2 and the executable chart audit give a direct argument.

Update 2026-08-24: these ingredients and the common `y_1`/`s_2` whiskers are
now assembled into the standalone conventional proof
`notes/peripheral_identification_lemma_2026-08-24.md`. This closes the logical
bridge for an ordinary proof subject to the explicitly named standard
theorems.

Update 2026-08-25: `independent_peripheral_extractor.py` supplies the second
computational route. Starting only from the marked triangulation, it
reimplements the derived frontier, orientations, dual meridians, product
push-offs, retraction, named loops, and literal `y_1`/`s_2` lassos without
importing the original complement, path, sweep, or peripheral modules. It
recovers both paper peripheral pairs with no discrepancy, separately records
the local `s_2`-based `N_grid` and its transported Table-1 word
`A*N_grid^-1*A^-1`, and includes controls that distinguish the opposite
half-section, opposite whisker, and meridian inverse; see Run 30. The residual
formal risk was the shared bundle triangulation.

Update 2026-08-25 (Run 31): the bundle assembly itself now has a second route.
`alternative_bundle.py` shares only the separately certified marked fiber and
reimplements products, mapping cylinders, paired flip traces, twist stack,
seams, total 4-complex, and marked tori without importing `bundle.py` or
`layers.py`. Its 64-interface triangulation is genuinely different and
reproduces the marked beta homology action and every peripheral semantic
field. Run 32 further proves its full based-pi1 action with an independently
replayed 34,735-step Tietze certificate, eliminating the possibility that the
second route merely agrees after abelianization. The residual formal risk is
now the shared marked fiber and the standard PL/smooth topology. Run 33
computationally checks all 128 local flip balls, untouched prisms, slab ends,
and global vertex links, reducing the flip-trace input to the elementary
interpretation of one explicitly verified labeled 2-2 cone-ball. None of the
remaining general topology is proof-assistant verified.

### R2. Trust in KBMAG completion — closed computationally (2026-08-25)

The former replay-only evidence has been replaced by eight compressed
derivation DAGs in `luttinger/proof_certificates/`. They start from the
original four-generator filled presentations, not GAP's Tietze-simplified
surrogates. A minimal KBMAG patch logs overlap parents, pre-orientation reduced
words, and every equation changed or discarded during tidying. The compiler is
untrusted: `verify_kbmag_certificate.py` independently checks every retained
input-relator or inverse axiom, overlap, literal rewrite step, cyclic
group-equation orientation, and final rule sending each generator and inverse
to the identity. All eight pass; see `runs/29`.

This removes KBMAG soundness and GAP presentation simplification from the
logical boundary of the triviality claim. Residual software risk is now the
small checker and Python runtime, which is substantially narrower and suitable
for a second implementation or proof-assistant port.

### R3. The square-zero section — moderate geometric risk

The no-torus argument needs the closed section `Gamma` to have square zero,
not merely even square. The paper computes its normal Euler number from
derivatives `I` and `-I`, a flat relative framing on each punctured-torus half,
and a constant boundary clutching map. The conclusion is coherent: the two
relative Euler numbers and the clutching degree are zero.

Update 2026-08-24: the missing calculation is now implemented in
`luttinger/pl_self_intersection.py` and recorded in `runs/28`. It extracts the
actual `p`-section and 24-cycle normal link from `K`, verifies the `-I` and `I`
normal monodromies, constructs the triangulated genus-2 double for every
constant simplicial clutching rotation, and produces a disjoint normal
push-off with an exact radial 3-chain. The signed intersection list is empty,
so the self-intersection is zero. R3 is closed computationally; the residual
input is the already-listed marked PL/smooth identification and the paper's
constant-clutching statement.

### R4. Implementation errors in the triangulation engine — independently cross-checked

The code is not verified software, but the former shared bundle-construction
boundary is removed computationally. The primary 32-interface and alternative
64-interface builders use separate product, trace, seam, and torus-assembly
code and yield different complexes; the independent extractor returns the
same marked peripheral semantics on both. They share `fiber.build_fiber`, whose
filling five-chain and involution have their own finite checks and the paper's
Lemma 7.1. Run 34 now supplies that further cross-check: an independently
triangulated 58-vertex ribbon surface, importing no `fiber.py`, has the exact
same canonical crossing rotations, p/O face cycles, and involution action as
the primary 86-vertex plumbing. Explicit common subdivisions are recorded for
every curve segment. The remaining risk is the elementary general theorem
boundary or proof-assistant formalization, not a shared fiber implementation.

Run-36 update (2026-08-25): `pl_theorem_audit.py` now binds Runs 28, 33, and
34 into a single reproducible hypothesis certificate. The remaining general
PL facts are separated into rotation-system thickening, the labeled
bistellar trace, low-dimensional compatible smoothing, and homological
intersection naturality, with precise references in
`notes/pl_bridge_referee_packet_2026-08-25.md`.

### R5. Downstream 4-manifold theorems — lower risk

The hypotheses of the classification, Kodaira-dimension, symplectic Thom,
relative Rokhlin, and Heegaard Floer results are checked in the downstream
audit. The remaining trust is ordinary reliance on published theorems, not an
identified novel gap.

## A realistic high-assurance endpoint

1. An explicit marked triangulation and section of the double.
2. A second, independent realization of the marked fiber itself. **Complete:**
   Run 34.
3. A second implementation or proof-assistant replay of the now-complete
   normal-closure certificates.
4. A concise conventional proof with every external hypothesis listed.
5. Independent expert reproduction.

A foundational proof assistant development would additionally require formal
libraries for PL 4-manifolds, surface bundles, symplectic surgery, Freedman
classification, and Floer theory. That is a separate research program.
