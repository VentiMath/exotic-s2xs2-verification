#!/usr/bin/env python3
"""Retry every undecided framing-shift group before GAP simplification.

The original robustness scan called ``IsomorphismSimplifiedFpGroup`` before
Knuth--Bendix.  Run 58 and an independent random-case dig showed that this can
be counterproductive: the simplified two-generator presentation resists,
while the original four-generator/97-relator presentation completes at the
default bounds.  This driver applies that exact raw-presentation test to all
18 scan holdouts in one GAP process.

For each case it writes both the untouched input rewriting system and, on a
successful completion, the confluent system.  It also writes a small
``presentation.json`` whose relator list is the exact list sent to GAP; that
is the source file used by the derivation-DAG compiler and independent
certificate verifiers.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

from j_robustness import RESULTS, filling_relators, gap_word, load


BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DEFAULT_OUTPUT = BASE / "raw_j_certificates"


def undecided_cases():
    cases = {}
    with open(RESULTS, encoding="ascii") as stream:
        for line in stream:
            row = json.loads(line)
            if row.get("ordering") != "ace_pass":
                continue
            case = (row["half_drift"], row["sign_a"], row["sign_b"],
                    row["j_a"], row["j_b"])
            cases[row["slug"]] = case
    assert len(cases) == 18, f"expected 18 frozen holdouts, found {len(cases)}"
    return sorted(cases.items())


def gap_list(words):
    return "[" + ",".join(gap_word(word) for word in words) + "]"


def source_payload(data, slug, case, relators, ordering):
    half, sign_a, sign_b, j_a, j_b = case
    return {
        "format": "j-scan-raw-certificate-source-v1",
        "ngens": data["ngens"],
        "relators": relators,
        "paper_fillings": [{
            "half_drift": half,
            "sign_a": sign_a,
            "sign_b": sign_b,
            "relators": [],
        }],
        "counterfactual_shift": {"j_a": j_a, "j_b": j_b},
        "note": (f"full unsimplified presentation of {slug}, exactly as in "
                 f"the generated {ordering} GAP input"),
    }


def build_program(data, cases, output_dir, ordering):
    relative_output = output_dir.relative_to(BASE)
    lines = ['LoadPackage("kbmag");;', 'Print("RAW_BATCH_BEGIN\\n");;']
    manifests = []
    for slug, case in cases:
        half, sign_a, sign_b, j_a, j_b = case
        filling = filling_relators(data, half, sign_a, sign_b, j_a, j_b)
        relators = (filling + data["relators"] if ordering == "fill_then_base"
                    else data["relators"] + filling)
        assert len(relators) == 97
        payload = source_payload(data, slug, case, relators, ordering)
        encoded = (json.dumps(payload, separators=(",", ":"), sort_keys=True)
                   + "\n")
        source_path = output_dir / f"{slug}_presentation.json"
        source_path.write_text(encoded, encoding="ascii")
        manifests.append({
            "slug": slug,
            "case": case,
            "nrelators": len(relators),
            "total_length": sum(map(len, relators)),
            "presentation": str(source_path.relative_to(ROOT)),
            "presentation_sha256": sha256(encoded.encode("ascii")).hexdigest(),
        })

        input_rws = relative_output / f"{slug}_input.rws"
        confluent_rws = relative_output / f"{slug}_confluent.rws"
        lines += [
            f'Print("CASE {slug}\\n");;',
            f'F := FreeGroup({data["ngens"]});;',
            f'rels := {gap_list(relators)};',
            'G := F/rels;',
            'rws := KBMAGRewritingSystem(G);;',
            f'WriteRWS(rws,"{input_rws}");;',
            'attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;',
            'completed := attempt[1]=true;',
            'if completed then conf := IsConfluent(rws); else conf := false; fi;',
            ('if conf then allone := ForAll(GeneratorsOfGroup('
             'FreeStructureOfRewritingSystem(rws)), z -> '
             'IsOne(ReducedForm(rws,z))); else allone := false; fi;'),
            (f'Print("RESULT {slug} completed=",completed,'
             '" confluent=",conf," generators_to_identity=",allone,"\\n");;'),
            'if conf and allone then',
            f'  WriteRWS(rws,"{confluent_rws}");',
            'fi;',
        ]
    lines += ['Print("RAW_BATCH_END\\n");;', 'QUIT;;']
    return "\n".join(lines) + "\n", manifests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--gap", type=Path, default=ROOT / "bin" / "gap")
    parser.add_argument("--ordering", choices=("fill_then_base", "base_then_fill"),
                        default="fill_then_base")
    parser.add_argument("--slug", action="append",
                        help="run only this frozen holdout (repeatable)")
    parser.add_argument("--parse-only", action="store_true",
                        help="parse the existing raw_completion.log without GAP")
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.relative_to(BASE)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load()
    cases = undecided_cases()
    if args.slug:
        requested = set(args.slug)
        cases = [item for item in cases if item[0] in requested]
        missing = requested - {item[0] for item in cases}
        if missing:
            raise SystemExit(f"unknown holdout slugs: {sorted(missing)}")
    program, manifests = build_program(data, cases, output_dir, args.ordering)
    gap_path = output_dir / "raw_completion.g"
    gap_path.write_text(program, encoding="ascii")

    log_path = output_dir / "raw_completion.log"
    if args.parse_only:
        gap_output = log_path.read_text(encoding="utf-8")
    else:
        result = subprocess.run(
            [str(args.gap.resolve()), "-q", str(gap_path.relative_to(BASE))],
            cwd=BASE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        gap_output = result.stdout
        log_path.write_text(gap_output, encoding="utf-8")
        if result.returncode:
            raise SystemExit(
                f"GAP failed with status {result.returncode}; see {log_path}")

    verdicts = {}
    pattern = re.compile(
        r"RESULT (\S+) completed=(true|false) confluent=(true|false) "
        r"generators_to_identity=(true|false)")
    normalized_output = gap_output.replace("\\\n", "")
    for match in pattern.finditer(normalized_output):
        verdicts[match.group(1)] = {
            "completed": match.group(2) == "true",
            "confluent": match.group(3) == "true",
            "generators_to_identity": match.group(4) == "true",
        }
    if len(verdicts) != len(cases):
        raise SystemExit(
            f"parsed {len(verdicts)} of {len(cases)} verdicts; see {log_path}")

    for manifest in manifests:
        manifest.update(verdicts[manifest["slug"]])
        manifest["certified_trivial"] = (
            manifest["confluent"] and manifest["generators_to_identity"])
    summary = {
        "format": "j-scan-raw-completion-v1",
        "ordering": args.ordering,
        "cases": manifests,
    }
    summary_path = output_dir / "raw_completion_results.json"
    summary_path.write_text(
        json.dumps(summary, separators=(",", ":"), sort_keys=True) + "\n",
        encoding="ascii",
    )
    successes = sum(item["certified_trivial"] for item in manifests)
    print(f"raw completion: {successes}/{len(manifests)} certified trivial")
    for item in manifests:
        print(item["slug"], "TRIVIAL" if item["certified_trivial"] else "OPEN")
    print(summary_path)


if __name__ == "__main__":
    main()
