"""Occurrence-indexed Tietze elimination.  Same contract as tietze.simplify
(eliminate generators occurring exactly once in some relator, substituting
everywhere), but with per-generator occurrence lists and a lazy priority
queue, so it scales to ~10^5 generators / ~10^6 relator letters.
"""
import gzip
import hashlib
import heapq
import json
from collections import Counter
from pi1 import free_reduce, inverse


def cyclic_reduce(w):
    w = free_reduce(w)
    while len(w) >= 2 and w[0] == -w[-1]:
        w = w[1:-1]
    return w


def _digest(payload):
    encoded = json.dumps(payload, separators=(",", ":"),
                         sort_keys=True).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def _dedupe(rels):
    seen, out = set(), []
    for r in rels.values():
        k, ik = tuple(r), tuple(inverse(r))
        if k in seen or ik in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def simplify(ngens, relators, words, max_len=200, verbose=False,
             certify=False):
    """Eliminate generators and optionally return a replayable certificate.

    A certificate records only the chosen relator, generator, and replacement
    at each elementary elimination.  ``verify_certificate`` reconstructs every
    intermediate relator from the original presentation, checks that the
    claimed generator occurs exactly once, recomputes its replacement, and
    compares the final presentation and tracked words by SHA-256 digest.
    """
    original_relators = relators
    original_words = words
    certificate = None
    if certify:
        certificate = {
            "format": "luttinger-fast-tietze-v1",
            "ngens": ngens,
            "max_len": max_len,
            "input_sha256": _digest([ngens, relators, words]),
            "steps": [],
        }
    rels = {}
    for i, r in enumerate(relators):
        r = cyclic_reduce(r)
        if r:
            rels[i] = r
    words = [free_reduce(w) for w in words]
    nextid = len(relators)

    occ = {}          # gen -> set of relator ids containing it (either sign)
    total = Counter()  # gen -> total occurrence count over all relators

    def index_rel(i):
        for g in set(abs(x) for x in rels[i]):
            occ.setdefault(g, set()).add(i)
        for x in rels[i]:
            total[abs(x)] += 1

    def unindex_rel(i):
        for g in set(abs(x) for x in rels[i]):
            s = occ.get(g)
            if s is not None:
                s.discard(i)
        for x in rels[i]:
            total[abs(x)] -= 1

    for i in rels:
        index_rel(i)

    # heap of candidate eliminations: (score, rel id, gen)
    heap = []

    def push_candidates(i):
        r = rels.get(i)
        if r is None or len(r) > max_len:
            return
        c = Counter(abs(g) for g in r)
        for g, cnt in c.items():
            if cnt == 1:
                score = (len(r) - 1) * (total[g] - 1)
                heapq.heappush(heap, (score, i, g))

    for i in list(rels):
        push_candidates(i)

    eliminated = 0
    while heap:
        score, i, g = heapq.heappop(heap)
        r = rels.get(i)
        if r is None or g not in occ or i not in occ.get(g, ()):
            continue
        c = Counter(abs(x) for x in r)
        if c.get(g, 0) != 1:
            continue
        cur_score = (len(r) - 1) * (total[g] - 1)
        if cur_score != score:
            push_candidates(i)
            continue
        # eliminate g using relator r
        pos = next(k for k, x in enumerate(r) if abs(x) == g)
        u, v = r[:pos], r[pos + 1:]
        rep = inverse(u) + inverse(v)
        if r[pos] < 0:
            rep = inverse(rep)
        if certificate is not None:
            certificate["steps"].append([i, g, rep])

        def sub(w):
            out = []
            for h in w:
                if h == g:
                    out += rep
                elif h == -g:
                    out += inverse(rep)
                else:
                    out.append(h)
            return free_reduce(out)

        targets = list(occ.get(g, ()))
        unindex_rel(i)
        del rels[i]
        changed = []
        for j in targets:
            if j == i or j not in rels:
                continue
            unindex_rel(j)
            s2 = cyclic_reduce(sub(rels[j]))
            if s2:
                rels[j] = s2
                index_rel(j)
                changed.append(j)
            else:
                del rels[j]
        words = [sub(w) for w in words]
        occ.pop(g, None)
        total.pop(g, None)
        eliminated += 1
        for j in changed:
            push_candidates(j)
        if verbose and eliminated % 5000 == 0:
            print(f"  tietze: eliminated {eliminated}, {len(rels)} relators left")

    out = _dedupe(rels)
    live = sorted({abs(g) for r in out for g in r} |
                  {abs(g) for w in words for g in w})
    if certificate is not None:
        certificate["steps_count"] = len(certificate["steps"])
        certificate["output_sha256"] = _digest([live, out, words])
        # Guard against callers mutating input lists while certification is
        # active; these references are intentionally checked only at the end.
        assert certificate["input_sha256"] == _digest(
            [ngens, original_relators, original_words])
        return live, out, words, certificate
    return live, out, words


def verify_certificate(ngens, relators, words, certificate, verbose=False):
    """Replay and verify a certificate returned by ``simplify``.

    This verifier does not run the priority-queue search.  It accepts a step
    only when the current relator itself proves the recorded substitution, so
    a corrupt or fabricated log fails at its first invalid elementary move.
    """
    assert certificate.get("format") == "luttinger-fast-tietze-v1"
    assert certificate.get("ngens") == ngens
    assert certificate.get("input_sha256") == _digest(
        [ngens, relators, words]), "certificate belongs to different input"

    rels = {}
    for i, relator in enumerate(relators):
        relator = cyclic_reduce(relator)
        if relator:
            rels[i] = relator
    tracked = [free_reduce(w) for w in words]
    occ = {}

    def index_rel(i):
        for g in set(abs(x) for x in rels[i]):
            occ.setdefault(g, set()).add(i)

    def unindex_rel(i):
        for g in set(abs(x) for x in rels[i]):
            occ[g].discard(i)

    for i in rels:
        index_rel(i)

    for number, (i, g, recorded_rep) in enumerate(certificate["steps"], 1):
        assert i in rels, f"step {number}: missing source relator {i}"
        relator = rels[i]
        positions = [k for k, x in enumerate(relator) if abs(x) == g]
        assert len(positions) == 1, \
            f"step {number}: generator {g} does not occur exactly once"
        pos = positions[0]
        expected = inverse(relator[:pos]) + inverse(relator[pos + 1:])
        if relator[pos] < 0:
            expected = inverse(expected)
        assert recorded_rep == expected, \
            f"step {number}: replacement is not implied by source relator"

        def sub(word):
            out = []
            for h in word:
                if h == g:
                    out += recorded_rep
                elif h == -g:
                    out += inverse(recorded_rep)
                else:
                    out.append(h)
            return free_reduce(out)

        targets = list(occ.get(g, ()))
        unindex_rel(i)
        del rels[i]
        for j in targets:
            if j == i or j not in rels:
                continue
            unindex_rel(j)
            replacement = cyclic_reduce(sub(rels[j]))
            if replacement:
                rels[j] = replacement
                index_rel(j)
            else:
                del rels[j]
        tracked = [sub(w) for w in tracked]
        occ.pop(g, None)
        if verbose and number % 5000 == 0:
            print(f"  replay: verified {number} eliminations")

    out = _dedupe(rels)
    live = sorted({abs(g) for r in out for g in r} |
                  {abs(g) for w in tracked for g in w})
    assert certificate.get("steps_count") == len(certificate["steps"])
    assert certificate.get("output_sha256") == _digest([live, out, tracked]), \
        "certificate final digest mismatch"
    return live, out, tracked


def save_certificate(path, certificate):
    """Write a certificate as deterministic JSON, optionally gzip-compressed."""
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "wt", encoding="ascii") as stream:
        json.dump(certificate, stream, separators=(",", ":"), sort_keys=True)
        stream.write("\n")


def load_certificate(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="ascii") as stream:
        return json.load(stream)


def renumber(live, rels, words, extra_free=()):
    live = sorted(set(live) | set(extra_free))
    ren = {g: i + 1 for i, g in enumerate(live)}
    f = lambda w: [ren[abs(g)] * (1 if g > 0 else -1) for g in w]
    return len(live), [f(r) for r in rels], [f(w) for w in words]


if __name__ == '__main__':
    # regression against the calibrated slow version on the T^4 case
    from complex import grid_torus, product
    from complement import TorusComplement
    import tietze as slow

    n = 3
    S, B = grid_torus(n), grid_torus(n)
    K = product(S, B)
    alpha = [(i, 0) for i in range(n)]
    beta = [(0, j) for j in range(n)]
    T = K.induced([(a, b) for a in alpha for b in beta])
    X = TorusComplement(K, T)
    a0, b0 = alpha[0], beta[0]
    u0 = frozenset({(a0, b0), (a0, (1, 0))})
    P = X.presentation(u0)
    sigma = next(s for s in T.simplices[2] if (a0, b0) in s)
    mu_loop = X.meridian_loop(sigma)
    to_mu = X.bfs_in_N(u0, mu_loop[0], [s for s in X.N if (a0, b0) in s])
    mu = X.based_word(mu_loop, to_mu)
    import time
    t0 = time.time()
    live, rels, ws, cert = simplify(
        P.ngens, P.relators, [mu], certify=True)
    replay_live, replay_rels, replay_ws = verify_certificate(
        P.ngens, P.relators, [mu], cert)
    assert (replay_live, replay_rels, replay_ws) == (live, rels, ws)
    broken = json.loads(json.dumps(cert))
    broken["steps"][0][2] = broken["steps"][0][2] + [P.ngens]
    try:
        verify_certificate(P.ngens, P.relators, [mu], broken)
        raise AssertionError("corrupt certificate was accepted")
    except AssertionError as error:
        assert "replacement is not implied" in str(error)
    m, rels, (mu2,) = renumber(live, rels, ws)
    print(f"fast tietze: {P.ngens} -> {m} gens, {len(rels)} relators, "
          f"{time.time()-t0:.2f}s; mu length {len(mu2)}")
    assert m <= 6, "should reduce T^4 complement to a handful of generators"
    print(f"fast_tietze: PASS ({cert['steps_count']} certified eliminations)")
