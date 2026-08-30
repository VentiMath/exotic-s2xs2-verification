# Sealed alpha-longitude identity

This directory proves, in the sealed 3-generator presentation of the torus
complement and without either filling relation,

```text
lb_a_y1^-1 * geom_A * geom_x = 1.
```

`build_input.py` extracts the three named words and all 78 complement
relators from `../sealed_transport/r_presentations.json`, freely reduces the
displayed word to the frozen 72-letter target in `source.json`, and writes the
uncompleted KBMAG input `complement_input.rws`.  The raw proof-producing
completion history is a reproducible build product and is not committed.
`compile_certificate.py` is untrusted: it extracts the 61-step reduction and
its complete ancestry cone.  The permanent result is
`certificate.json.gz` (2,506 retained records).

From the repository root, the complete regeneration path is:

```bash
python3 verification/luttinger/alpha_residual/build_input.py
verification/bin/gap -q verification/luttinger/alpha_residual/build_input.g
docker build -t luttinger-kbmag-proof:local \
  verification/luttinger/kbmag-proof
python3 verification/luttinger/kbmag_history.py \
  verification/luttinger/alpha_residual/complement_input.rws \
  verification/luttinger/alpha_residual/history-me50000.log \
  --kbprog-args '-me 50000 -t 100'
python3 verification/luttinger/alpha_residual/compile_certificate.py \
  verification/luttinger/alpha_residual/history-me50000.log \
  verification/luttinger/alpha_residual/certificate.json.gz
```

Two standard-library verifiers, sharing neither implementation code nor
language runtime, replay every initial relation, inverse axiom, overlap,
tidy change, and target rewrite:

```bash
python3 verification/luttinger/alpha_residual/verify_certificate.py \
  verification/luttinger/alpha_residual/certificate.json.gz \
  --negative-controls
ruby verification/luttinger/alpha_residual/verify_certificate.rb \
  verification/luttinger/alpha_residual/certificate.json.gz \
  --negative-controls
```

Both reject a certificate with the last target step deleted.  The proof is
an identity in the complement group itself; triviality of any filled group
is not used.
