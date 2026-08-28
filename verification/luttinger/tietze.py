"""Cheap Tietze simplification so GAP gets a small presentation.
Repeatedly pick a generator g that occurs exactly once in some relator r
(r = u g v, so g = u^-1 v^-1), substitute for g everywhere (relators and the
tracked words), delete r.  Prefer short r and rarely-used g to limit growth."""
from pi1 import free_reduce, inverse
from collections import Counter


def cyclic_reduce(w):
    w = free_reduce(w)
    while len(w) >= 2 and w[0] == -w[-1]:
        w = w[1:-1]
    return w


def simplify(ngens, relators, words, max_len=60, rounds=100000):
    rels = [cyclic_reduce(r) for r in relators]
    rels = [r for r in rels if r]
    words = [free_reduce(w) for w in words]
    total = Counter(abs(g) for r in rels for g in r)
    for _ in range(rounds):
        best = None
        for i, r in enumerate(rels):
            if len(r) > max_len:
                continue
            c = Counter(abs(g) for g in r)
            for pos, g in enumerate(r):
                if c[abs(g)] == 1:
                    score = (len(r) - 1) * (total[abs(g)] - 1)
                    if best is None or score < best[0]:
                        best = (score, i, pos)
            if best is not None and best[0] == 0:
                break
        if best is None:
            break
        _, i, pos = best
        r = rels[i]
        g = r[pos]
        u, v = r[:pos], r[pos + 1:]
        rep = inverse(u) + inverse(v)            # value of g
        if g < 0:
            rep = inverse(rep)
        G = abs(g)

        def sub(w):
            out = []
            for h in w:
                if h == G:
                    out += rep
                elif h == -G:
                    out += inverse(rep)
                else:
                    out.append(h)
            return free_reduce(out)
        new = []
        for j, s in enumerate(rels):
            if j == i:
                continue
            s2 = cyclic_reduce(sub(s)) if G in (abs(h) for h in s) else s
            if s2:
                new.append(s2)
        rels = new
        words = [sub(w) for w in words]
        total = Counter(abs(g) for r in rels for g in r)
    # dedupe
    seen, out = set(), []
    for r in rels:
        k, ik = tuple(r), tuple(inverse(r))
        if k in seen or ik in seen:
            continue
        seen.add(k); out.append(r)
    rels = out
    live = sorted({abs(g) for r in rels for g in r} | {abs(g) for w in words for g in w})
    # generators that vanished from everything but were never eliminated are free
    # factors; we must keep them: they are those in 1..ngens never eliminated.
    return live, rels, words


def renumber(live, rels, words, extra_free=()):
    live = sorted(set(live) | set(extra_free))
    ren = {g: i + 1 for i, g in enumerate(live)}
    f = lambda w: [ren[abs(g)] * (1 if g > 0 else -1) for g in w]
    return len(live), [f(r) for r in rels], [f(w) for w in words]
