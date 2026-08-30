# Provenance

This verification was produced with AI assistance under human direction, and
the project treats *who computed what* as part of the scientific record.

## The discipline

* Substantive model authorship is stated in plain sentences in commit bodies.
  Commits carry no assistant attribution trailers.
* Nothing is retroactively relabeled: if one model builds something and
  another later fixes it, the fix belongs to the fixer and the original stays
  with the builder.
* The repository history is the authority on which commits produced which
  artifacts.

## The actors

* **Anthropic Claude Fable 5** — the original machine derivation: the
  simplicial engine extensions, the bundle build, the proof-producing Tietze
  pipeline, and the first certified run; the framing-robustness scan.
* **Anthropic Claude Opus 5** — independent replay and adversarial review of
  the certificates, ledger, and manuscript claims.
* **OpenAI Codex (GPT-5 family)** — the basing sweeps, the explicit based
  peripheral identifications, the complete confluent rewriting certificates
  for the filled groups and their independent checker, the redundant
  second-route implementations, the downstream hypothesis audit, and the
  framing-lemma referee packet.
* **John Clyde** — direction, adjudication between the models' competing
  assessments, and responsibility for every mathematical claim.

Cross-model review was adversarial by design: each model's assessments were
put to the other, and several decisive corrections in the record — the basing
double-count resolution, the corrected blast-radius statement for the framing
lemma, the polarity correction to the slicing theorem — came out of exactly
that exchange.

## Why publish this

Machine-assisted mathematics is only as trustworthy as its audit trail. The
certificates in this repository are designed to be replayed without trusting
any model; this document exists so that a reader can also ask the weaker
question — who wrote this, and who checked it — and get a precise answer.

The certificates do not depend on the answer. The finite certificate
assertions — that the named presentations present the trivial group, and that
each derivation record follows from earlier ones — are carried by artifacts a
reader can replay with two separately implemented checkers. The geometric
identifications, the Source Comparison Hypotheses, and the applications of
cited external theorems are not of that kind, and are not replayable in that
sense; `verification/STATUS.md` states which is which.
