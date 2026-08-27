# Local flatness of both surgery tori

Run 48 exhausts every simplex of the two full torus subcomplexes in the
certified marked bundle. The relevant codimension-two local-flatness
criterion is that each link pair is standard:

\[
 (\operatorname{lk}_K\sigma,\operatorname{lk}_T\sigma)=
 \begin{cases}
 (S^3,\text{unknotted }S^1),&\dim\sigma=0,\\
 (S^2,S^0),&\dim\sigma=1,\\
 (S^1,\varnothing),&\dim\sigma=2.
 \end{cases}
\]

The checker enumerates 144 simplices of `T_alpha` and 1,632 simplices of
`T_beta`, with no sampling or quotienting by an assumed symmetry.

## Triangle and edge links

For every one of the 592 triangles, the ambient link is checked to be one
connected cycle. For every one of the 888 edges, the ambient link is checked
as a connected triangulated surface with Euler characteristic two and
circular vertex links, hence a 2-sphere; the torus link consists of exactly
two points. These are the standard pairs `(S1,empty)` and `(S2,S0)`.

## Vertex links

There are 296 torus vertices. For each one, the ambient link is checked to be
a closed combinatorial 3-manifold. The checker then chooses a tetrahedron,
deletes its interior, checks that the result is a compact combinatorial
3-manifold with `S2` boundary, and records an elementary-collapse sequence to
one point. An independent replay checks that each removed face is free at
that stage. The standard contractible-PL-3-manifold ball criterion then makes
the punctured link a 3-ball, so every ambient vertex link is a PL 3-sphere.

The torus link is checked to be a full connected circle in that 3-sphere.
The explicit barycentric-coordinate retraction for complements of full
subcomplexes identifies its open complement with the induced complex on the
remaining vertices. For every vertex, that induced complex carries a second
replayed elementary-collapse sequence whose final spine is a single cycle.
Consequently its fundamental group is infinite cyclic. The classical unknot
criterion for PL knots in `S3` then identifies the torus-link circle as the
unknot. This proves that every vertex link pair is the standard
`(S3,unknotted S1)` pair.

The finite witnesses are stored in
`luttinger/torus_local_flatness_certificate.json`. The per-simplex records
have aggregate SHA-256
`211c4d2f70d7708292a601e7574bfa282aaaae872e2ba6f1fbf20b17ca59e355`;
the certificate file has SHA-256
`24eb97b4a7878e17ef11373a57cb2941cde0a56122ed01384665b5140909e0a1`.

## Exact boundary after this run

Local flatness is no longer inferred from the bundle picture. It is certified
simplex by simplex, relative only to elementary surface classification, the
contractible-PL-3-manifold ball criterion, and the standard cyclic-knot-group
unknot criterion. The separate theorem that
the derived neighborhood of a full locally flat submanifold is a regular
neighborhood, with frontier its normal sphere-bundle boundary, remains the
next target.
