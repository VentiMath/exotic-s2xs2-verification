# Provenance

This verification was produced with AI assistance under human direction, and
the project treats *who computed what* as part of the scientific record.

## The discipline

* Every commit in the working repository is attributed to the model (or
  person) that produced it, in a log table where the boundary is always a
  commit hash — never a date or a model's claim about itself.
* When the acting model changes, the log gains a row. Nothing is
  retroactively relabeled: if one model builds something and another later
  fixes it, the fix belongs to the fixer and the original stays with the
  builder.
* Commits carry no assistant attribution trailers; substantive model
  authorship is stated in plain sentences in commit bodies and in the log.

## The actors

* **Anthropic Claude Fable 5** — the original machine derivation: the
  simplicial engine extensions, the bundle build, the proof-producing Tietze
  pipeline, and the first certified run; later bookkeeping and the
  slope-robustness scan.
* **Anthropic Claude Opus 5** — intermediate bookkeeping.
* **OpenAI Codex (GPT-5 family)** — the basing sweeps, the explicit based
  peripheral identifications, the complete confluent rewriting certificates
  for all eight filled groups and their independent checker, the redundant
  second-route implementations, the downstream hypothesis audit, and the
  framing-lemma referee packet.
* **John Clyde** — direction, adjudication between the models' competing
  assessments, and responsibility for every mathematical claim.

The full commit-level ledger is imported with the working repository's
history. Cross-model review was adversarial by design: each model's
assessments were put to the other, and several decisive corrections in
the record (the basing double-count resolution, the corrected blast-radius
statement for the framing lemma) came out of exactly that exchange.

## Why publish this

Machine-assisted mathematics is only as trustworthy as its audit trail. The
certificates in this repository are designed to be replayed without trusting
any model; the provenance ledger exists so that a reader can also ask the
weaker question — who wrote this, and who checked it — and get a precise
answer.
