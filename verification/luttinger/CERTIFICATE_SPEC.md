# Filled-group certificate specification, version 1

This document is the normative mathematical specification of the
`luttinger-kbmag-proof-v1` certificate format.  The Python and Ruby checkers
are separate implementations of this specification.  Search programs,
KBMAG, certificate compilers, and completed rewriting systems are not part of
the trusted derivation.

## 1. Alphabets and words

Fix `ngens = n > 0`.  The input presentation uses signed generator letters

```text
{+1, -1, ..., +n, -n},
```

where `+j` denotes `g_j` and `-j` denotes `g_j^-1`.

Certificate records use the positive monoid alphabet

```text
L_n = {1, 2, ..., 2n}.
```

The decoding map is

```text
signed(2j-1) = +j,
signed(2j)   = -j.
```

The inverse-letter table is required to be exactly

```text
[2, 1, 4, 3, ..., 2n, 2n-1].
```

A word is a finite list of letters.  Every certificate word must be a list
whose entries are integers in `L_n`.

For a signed word `w`, let `inv(w)` be the reversed word with every sign
changed.  Let `free_reduce(w)` repeatedly cancel adjacent pairs `j,-j`.
Let `cyclic_reduce(w)` first freely reduce and then repeatedly delete an
inverse first/last pair.  For a nonempty cyclically reduced word `w`, define

```text
cyclic_key(w) = lexicographically least cyclic rotation of
                w or inv(w).
```

The key of the empty word is the empty tuple.  For certificate words `u,v`,
define the equation key

```text
equation_key(u,v) = cyclic_key(signed(u) * inv(signed(v))).
```

Thus equal keys identify equations after free reduction, cyclic reduction,
cyclic conjugacy, and inversion.  These operations preserve the normal
closure of the equation word and hence preserve the asserted equality in
the presented group.

## 2. Source binding and case selection

The certificate contains:

- `format`, required to equal `luttinger-kbmag-proof-v1`;
- `input_sha256`, required to equal the SHA-256 digest of the source JSON
  bytes;
- an integer case index in the range of the source filling array and its slug;
- `ngens`, required to equal the source generator count;
- `relators`, required to equal, byte-for-byte as parsed JSON arrays, the
  source complement relators followed by the selected case's two filling
  relators; and
- the inverse-letter table specified above.

The selected filling is the source entry at the certificate's case index.
Its canonical slug is

```text
half_drift + "_" + (p1 or m1 from sign_a)
           + "_" + (p1 or m1 from sign_b).
```

The certificate slug must equal that value.

## 3. Rewrite traces

Records are numbered from zero.  A rewrite trace occurring in record `i` is
a list of pairs `[r,p]` satisfying

```text
0 <= r < i,     p >= 0.
```

Starting with the current word, the trace step requires `p` to be a word
boundary (`0 <= p <= len(word)`) and the left side of record `r` to occur
literally beginning at position `p`; that occurrence is
replaced by the right side of record `r`.  No matching modulo cyclic
conjugacy, inversion, or free reduction is allowed inside a trace.  Each
trace therefore gives a literal sequence of substitutions by previously
proved equations.

## 4. Record grammar

Every record has certificate-word fields `lhs`, `rhs`, and one proof object
of exactly one of the following four kinds.

### 4.1 `inverse_axiom`

Validity requires:

- `rhs` is empty;
- `lhs` has length two; and
- its second letter is the inverse-table partner of its first.

This records a free-group equality `l inv(l) = 1`.

### 4.2 `input_relator`

The proof object contains an integer source-relator index `k` in range.
Validity requires

```text
equation_key(lhs,rhs) = cyclic_key(source_relator[k]).
```

### 4.3 `overlap`

The proof object contains parent record indices `a,b < i`, an integer offset
`d`, and traces `trace_a`, `trace_b`.

Put `A = records[a].lhs` and `B = records[b].lhs`.  Validity requires

```text
-len(B) < d < len(A)
```

and literal agreement of the nonempty overlap when `B` begins at offset `d`
relative to `A`.  Form the shortest source word containing both occurrences.
Replace the occurrence of `A` by `records[a].rhs` to obtain branch A, and
replace the occurrence of `B` by `records[b].rhs` to obtain branch B.  Replay
`trace_a` and `trace_b` on the two branches.  If their outputs are `U,V`,
validity requires

```text
equation_key(lhs,rhs) = equation_key(U,V).
```

### 4.4 `change`

The proof object contains an old record index `o < i`, traces `left_trace`
and `right_trace`, and stored words `reduced_left`, `reduced_right`.
Replay the two traces on the two sides of record `o`.  Their literal outputs
must equal the two stored reduced words.  Validity then requires

```text
equation_key(lhs,rhs)
  = equation_key(reduced_left,reduced_right).
```

## 5. Identity roots

The certificate contains a list `roots` of length exactly `2n`.  For each
monoid letter `l = 1,...,2n`, the corresponding entry must be an in-range
record index whose record has

```text
lhs = [l],     rhs = [].
```

Consequently every generator and inverse-generator letter equals the
identity.

## 6. Batch inventory

Duplicate case indices and duplicate slugs are always rejected.  In
full-inventory mode the batch must additionally:

- contain every filling index exactly once;
- contain one file named `SLUG.json.gz` for each case;
- contain exactly eight fillings, each having two filling relators;
- have the requested complement generator and relator counts; and
- have exactly the set of slugs computed from the source filling table.

## 7. Soundness theorem

Let `G` be the group given by the hash-bound source relators for the selected
case.  If a certificate satisfies Sections 1--5, then `G` is trivial.

Proof.  Induct over the record list.  An inverse axiom is an equality in the
free group.  An input-relator record is a cyclic conjugate or inverse of a
defining relator after free reduction, so it is an equality in `G`.  A trace
replaces a subword using an earlier equality and therefore preserves the
represented element of `G`.  In an overlap record, both branches are obtained
from the same source word using earlier equalities; their traced outputs are
therefore equal in `G`, and equality of equation keys transfers that equality
to the recorded sides.  A change record is identical: both sides of an
earlier equality are rewritten by earlier equalities, and the equation-key
test transfers the result to the recorded sides.  Hence every accepted record
is an equality in `G`.  The roots finally assert that every generator and its
inverse equal `1`, so `G` is trivial.  QED.

## 8. Reference-verifier pseudocode

```text
verify(source_bytes, certificate):
    require certificate.format == "luttinger-kbmag-proof-v1"
    require sha256(source_bytes) == certificate.input_sha256
    select case; require slug, relator list, ngens, and inverse table

    proved = []
    for record in certificate.records:
        require both sides are words over L_n
        if inverse_axiom: check the literal inverse pair
        if input_relator: compare equation keys with the indexed relator
        if overlap: build both branches, replay earlier-rule traces,
                    compare equation keys
        if change: replay both earlier-rule traces, check stored outputs,
                   compare equation keys
        append record to proved

    require one literal [letter] -> [] root for every letter in L_n
    accept
```

The normative requirements are Sections 1--6, not this pseudocode.
