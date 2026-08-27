"""j-robustness scan: fillings with meridian-shifted longitudes.

Lemma 8.2 identifies the fibered push-off with the Lagrangian framing. If it
failed by j meridians on a torus, the paper's Luttinger surgery would impose
mu * (lambda * mu^j)^e in place of the certified mu * lambda^e. This driver
fills the exported complement presentation with those shifted slopes, using
the same coherent based pairs (geom_M, lb_a_y1), (geom_M_y2, lb_a_y2),
(geom_N, lb_b_s2) and the same GAP/KBMAG completion criterion as the eight
certified direct fillings (group_attack.py direct-paper-export).

Verdicts per case:
  certified_trivial_tietze  simplification reaches zero generators
  certified_trivial_kb      complete confluent system, all generators -> 1
  nontrivial_h1             AbelianInvariants(H) <> [] : provably nontrivial
  inconclusive              KB did not complete within limits
  timeout                   gap exceeded the wall clock

A certified_trivial verdict at (j_a, j_b) means the paper's manifold would
remain simply connected even under that framing discrepancy; nontrivial_h1
means that discrepancy is excluded by the paper's own homology bookkeeping.
Both shrink the conditional gap. Results append to j_robustness_results.jsonl
(one JSON object per attempt; reruns skip decided cases).

Run from this directory:  PATH=../bin:$PATH python3 j_robustness.py --tier 1
"""
import argparse
import json
import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "j_robustness_results.jsonl")


def inverse(word):
    return [-letter for letter in reversed(word)]


def signed(word, sign):
    return word if sign == 1 else inverse(word)


def free_reduce(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def gap_word(word):
    if not word:
        return "One(F)"
    return "*".join(
        f"F.{abs(letter)}" + ("^-1" if letter < 0 else "")
        for letter in word)


def load():
    with open(os.path.join(BASE, "r_presentations.json"),
              encoding="ascii") as stream:
        data = json.load(stream)
    assert data["format"] == "luttinger-filled-presentations-v1"
    return data


def shifted_longitude(meridian, longitude, j):
    tail = meridian * j if j >= 0 else inverse(meridian) * (-j)
    return longitude + tail


def filling_relators(data, half_drift, sign_a, sign_b, j_a, j_b):
    tracked = data["tracked_words"]
    mer_a, lon_a = {
        "n0_y1": (tracked["geom_M"], tracked["lb_a_y1"]),
        "n1_y2": (tracked["geom_M_y2"], tracked["lb_a_y2"]),
    }[half_drift]
    mer_b, lon_b = tracked["geom_N"], tracked["lb_b_s2"]
    rel_a = mer_a + signed(shifted_longitude(mer_a, lon_a, j_a), sign_a)
    rel_b = mer_b + signed(shifted_longitude(mer_b, lon_b, j_b), sign_b)
    return [free_reduce(rel_a), free_reduce(rel_b)]


def assert_control_words_match(data):
    """The j=0 relators must equal the certified paper_fillings exactly."""
    for filling in data["paper_fillings"]:
        built = filling_relators(data, filling["half_drift"],
                                 filling["sign_a"], filling["sign_b"], 0, 0)
        stored = [free_reduce(r) for r in filling["relators"]]
        assert built == stored, (
            f"control mismatch {filling['half_drift']} "
            f"({filling['sign_a']},{filling['sign_b']})")
    print("control words match all eight certified paper fillings")


def slug_of(case):
    half, sign_a, sign_b, j_a, j_b = case
    return (f"{half}_a{sign_a:+d}_b{sign_b:+d}"
            f"_ja{j_a:+d}_jb{j_b:+d}").replace("+", "p").replace("-", "m")


def gap_program(data, case, ordering, slug):
    half, sign_a, sign_b, j_a, j_b = case
    fill = filling_relators(data, half, sign_a, sign_b, j_a, j_b)
    if ordering == "fill_then_base":
        relators = fill + data["relators"]
    else:
        relators = data["relators"] + fill
    body = "LoadPackage(\"kbmag\");;\n"
    body += f"F := FreeGroup({data['ngens']});;\n"
    body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
    body += "G := F/rels;;\n"
    body += "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
    body += "ab := AbelianInvariants(H);;\n"
    body += 'Print("H1=",ab,"\\n");\n'
    body += "fg := FreeGeneratorsOfFpGroup(H);; rl := RelatorsOfFpGroup(H);;\n"
    body += ('Print("simplified=",Length(fg)," gens/",Length(rl),'
             '" rels total_length=",Sum(rl,Length),"\\n");\n')
    body += 'if ab <> [] then\n  Print("VERDICT nontrivial_h1\\n");\n'
    body += 'elif Length(fg)=0 then\n  Print("VERDICT certified_trivial_tietze\\n");\nelse\n'
    body += ("  rws := KBMAGRewritingSystem(H);;\n"
             "  attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;\n"
             "  conf := IsConfluent(rws);;\n"
             "  reds := List(GeneratorsOfGroup("
             "FreeStructureOfRewritingSystem(rws)), z -> ReducedForm(rws,z));;\n"
             "  allone := ForAll(reds,IsOne);;\n"
             "  ok := attempt=[true,true] and conf and allone;;\n"
             '  Print("KB=",attempt," confluent=",conf,'
             '" generators_to_identity=",allone,"\\n");\n')
    body += (f'  if ok then\n    WriteRWS(rws,"j_rws/{slug}.rws");\n'
             '    Print("VERDICT certified_trivial_kb\\n");\n'
             '  else\n    Print("VERDICT inconclusive\\n");\n  fi;\nfi;\n')
    body += "QUIT;;\n"
    return body


def run_case(data, case, gap, timeout):
    slug = slug_of(case)
    outcome = {"slug": slug, "half_drift": case[0], "sign_a": case[1],
               "sign_b": case[2], "j_a": case[3], "j_b": case[4]}
    for ordering in ("fill_then_base", "base_then_fill"):
        program_path = os.path.join(BASE, "j_gap", f"{slug}.{ordering}.g")
        with open(program_path, "w", encoding="ascii") as stream:
            stream.write(gap_program(data, case, ordering, slug))
        try:
            result = subprocess.run(
                [gap, "-q", os.path.join("j_gap", f"{slug}.{ordering}.g")],
                capture_output=True, text=True, timeout=timeout, cwd=BASE)
        except subprocess.TimeoutExpired:
            outcome.update(ordering=ordering, verdict="timeout",
                           timeout_seconds=timeout)
            continue
        verdict = "inconclusive"
        for line in result.stdout.splitlines():
            if line.startswith("VERDICT "):
                verdict = line.split(None, 1)[1].strip()
        outcome.update(ordering=ordering, verdict=verdict,
                       gap_stdout=result.stdout,
                       gap_returncode=result.returncode)
        if verdict in ("certified_trivial_tietze", "certified_trivial_kb",
                       "nontrivial_h1"):
            break
    return outcome


def tier_cases(tier):
    def band(half):
        cases = []
        for sign_a in (1, -1):
            for sign_b in (1, -1):
                for j_a, j_b in SHIFTS:
                    cases.append((half, sign_a, sign_b, j_a, j_b))
        return cases

    single = [(j, 0) for j in (1, -1, 2, -2)] + \
             [(0, j) for j in (1, -1, 2, -2)]
    joint = [(ja, jb) for ja in (1, -1) for jb in (1, -1)]
    if tier == 0:
        SHIFTS = [(0, 0)]
        return band("n0_y1")
    if tier == 1:
        SHIFTS = single
        return band("n0_y1")
    if tier == 2:
        SHIFTS = joint
        return band("n0_y1")
    if tier == 3:
        SHIFTS = single + joint
        return band("n1_y2")
    raise ValueError(tier)


DECISIVE = ("certified_trivial_tietze", "certified_trivial_kb",
            "certified_trivial_ace", "nontrivial_h1", "nontrivial_witness")


def all_rows():
    if not os.path.exists(RESULTS):
        return []
    with open(RESULTS, encoding="ascii") as stream:
        return [json.loads(line) for line in stream]


def decided_slugs():
    return {row["slug"] for row in all_rows() if row["verdict"] in DECISIVE}


def straggler_cases():
    """Unique cases whose best verdict so far is not decisive."""
    decided = decided_slugs()
    seen = {}
    for row in all_rows():
        if row["slug"] not in decided and row["slug"] not in seen:
            seen[row["slug"]] = (row["half_drift"], row["sign_a"],
                                 row["sign_b"], row["j_a"], row["j_b"])
    return list(seen.values())


def ace_program(data, case, slug, workspace):
    half, sign_a, sign_b, j_a, j_b = case
    fill = filling_relators(data, half, sign_a, sign_b, j_a, j_b)
    relators = fill + data["relators"]
    body = "LoadPackage(\"ace\");;\n"
    body += f"F := FreeGroup({data['ngens']});;\n"
    body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
    body += "G := F/rels;;\n"
    body += "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
    body += "fg := FreeGeneratorsOfFpGroup(H);; rl := RelatorsOfFpGroup(H);;\n"
    body += 'Print("simplified=",Length(fg)," gens\\n");\n'
    body += ('if Length(fg)=0 then\n'
             '  Print("VERDICT certified_trivial_tietze\\n");\nelse\n')
    body += (f"  acecall := function() return ACEStats(fg,rl,[] : hard, "
             f"workspace := {workspace}); end;;\n"
             "  att := CALL_WITH_CATCH(acecall,[]);;\n"
             "  if att[1]=true then\n"
             '    Print("ACE index=",att[2].index,'
             '" totcosets=",att[2].totcosets,"\\n");\n'
             "  else\n"
             '    Print("ACE failed\\n");\n'
             "  fi;\n"
             "  if att[1]=true and att[2].index=1 then\n"
             '    Print("VERDICT certified_trivial_ace\\n");\n'
             "  else\n"
             "    targets := [AlternatingGroup(5),PSL(2,7),AlternatingGroup(6),"
             "PSL(2,8),PSL(2,11),PSL(2,13)];;\n"
             "    found := false;;\n"
             "    for target in targets do\n"
             "      epis := GQuotients(H,target);;\n"
             '      Print("quotients ",Size(target),": ",Length(epis),"\\n");\n'
             "      if Length(epis)>0 then found := true; fi;\n"
             "    od;\n"
             "    subs := LowIndexSubgroupsFpGroup(H,8);;\n"
             '    Print("low_index_subgroups<=8: ",Length(subs),"\\n");\n'
             "    if found or Length(subs)>1 then\n"
             '      Print("VERDICT nontrivial_witness\\n");\n'
             "    else\n"
             '      Print("VERDICT inconclusive\\n");\n'
             "    fi;\n"
             "  fi;\nfi;\nQUIT;;\n")
    return body


def run_straggler(data, case, gap, timeout, workspace):
    slug = slug_of(case)
    outcome = {"slug": slug, "half_drift": case[0], "sign_a": case[1],
               "sign_b": case[2], "j_a": case[3], "j_b": case[4],
               "ordering": "ace_pass", "ace_workspace": workspace}
    program_path = os.path.join(BASE, "j_gap", f"{slug}.ace.g")
    with open(program_path, "w", encoding="ascii") as stream:
        stream.write(ace_program(data, case, slug, workspace))
    try:
        result = subprocess.run(
            [gap, "-q", os.path.join("j_gap", f"{slug}.ace.g")],
            capture_output=True, text=True, timeout=timeout, cwd=BASE)
    except subprocess.TimeoutExpired:
        outcome.update(verdict="timeout", timeout_seconds=timeout)
        return outcome
    verdict = "inconclusive"
    for line in result.stdout.splitlines():
        if line.startswith("VERDICT "):
            verdict = line.split(None, 1)[1].strip()
    outcome.update(verdict=verdict, gap_stdout=result.stdout,
                   gap_returncode=result.returncode)
    return outcome


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", type=int, choices=(0, 1, 2, 3))
    parser.add_argument("--stragglers", action="store_true",
                        help="ACE + quotient pass on undecided cases")
    parser.add_argument("--shard", type=int, nargs=2, metavar=("I", "N"),
                        help="process only cases with index %% N == I")
    parser.add_argument("--workspace", type=int, default=50_000_000)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--gap", default=os.path.join(BASE, "..", "bin", "gap"))
    args = parser.parse_args()

    data = load()
    assert_control_words_match(data)
    os.makedirs(os.path.join(BASE, "j_gap"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "j_rws"), exist_ok=True)

    if args.stragglers:
        cases = straggler_cases()
        if args.shard is not None:
            index, count = args.shard
            cases = [c for i, c in enumerate(cases) if i % count == index]
        print(f"{len(cases)} undecided cases for the ACE/quotient pass")
        for index, case in enumerate(cases):
            slug = slug_of(case)
            print(f"[{index + 1}/{len(cases)}] {slug}: ace pass", flush=True)
            outcome = run_straggler(data, case, args.gap, args.timeout,
                                    args.workspace)
            with open(RESULTS, "a", encoding="ascii") as stream:
                stream.write(json.dumps(outcome, sort_keys=True) + "\n")
            print(f"    -> {outcome['verdict']}", flush=True)
        return

    assert args.tier is not None, "--tier or --stragglers required"
    cases = tier_cases(args.tier)
    done = decided_slugs()
    for index, case in enumerate(cases):
        slug = slug_of(case)
        if slug in done:
            print(f"[{index + 1}/{len(cases)}] {slug}: already decided, skip")
            continue
        print(f"[{index + 1}/{len(cases)}] {slug}: running", flush=True)
        outcome = run_case(data, case, args.gap, args.timeout)
        with open(RESULTS, "a", encoding="ascii") as stream:
            stream.write(json.dumps(outcome, sort_keys=True) + "\n")
        print(f"    -> {outcome['verdict']} ({outcome.get('ordering')})",
              flush=True)


if __name__ == "__main__":
    main()
