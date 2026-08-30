# Sealed beta-longitude identity

This directory proves, in the sealed 3-generator presentation of the torus
complement and without either filling relation,

```text
lb_b_s2^-1 * geom_r^-1 * geom_M * geom_r * geom_B = 1.
```

Equivalently, `lb_b_s2 = (geom_r^-1 * geom_M * geom_r) * geom_B`, the paper's
beta-coordinate formula. `build_input.py` extracts the four named factors and
all 78 complement relators from `../sealed_transport/r_presentations.json` and
freely reduces the displayed word to the frozen 113-letter target in
`source.json`. The proof-producing completion uses the identical
complement-only KBMAG input frozen by Run 68 at
`../alpha_residual/complement_input.rws`.

The raw 50,000-equation history is a reproducible build product and is not
committed. `compile_certificate.py` is untrusted: it extracts the 82-step
reduction and its complete ancestry cone. The permanent result is
`certificate.json.gz`.

Two standard-library verifiers, sharing neither implementation code nor
language runtime, replay every initial relation, inverse axiom, overlap, tidy
change, and target rewrite:

```bash
python3 verification/luttinger/beta_residual/verify_certificate.py \
  verification/luttinger/beta_residual/certificate.json.gz \
  --negative-controls
ruby verification/luttinger/beta_residual/verify_certificate.rb \
  verification/luttinger/beta_residual/certificate.json.gz \
  --negative-controls
```

Both also reject four independent corruptions: an altered target, a forged
derivation record, an altered presentation relator, and a spliced target
trace. Triviality of a filled group is not used.
