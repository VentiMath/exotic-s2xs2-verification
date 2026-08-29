#!/usr/bin/env python3
"""Write deterministic hashes for the filled-group proof artifacts."""

import argparse
import json
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "proof_certificates" / "manifest.json"
FILES = [
    ROOT / "r_presentations.json",
    ROOT / "compile_kbmag_certificate.py",
    ROOT / "verify_kbmag_certificate.py",
    ROOT / "verify_certificates.rb",
    ROOT / "export_kbmag_proof_inputs.py",
    ROOT / "kbmag_history.py",
    ROOT / "kbmag-proof" / "Dockerfile",
    ROOT / "kbmag-proof" / "kbfns-proof.patch",
] + sorted((ROOT / "raw_proof_inputs").glob("*.rws")) \
  + sorted((ROOT / "proof_certificates").glob("*.json.gz"))


def case_slug(filling):
    return (f'{filling["half_drift"]}_'
            f'{"p" if filling["sign_a"] > 0 else "m"}1_'
            f'{"p" if filling["sign_b"] > 0 else "m"}1')


def check_inventory():
    """The certificate directory must hold exactly one file per filling of
    r_presentations.json, named by its case slug."""
    source = json.loads((ROOT / "r_presentations.json").read_text(encoding="ascii"))
    expected = sorted(case_slug(f) + ".json.gz" for f in source["paper_fillings"])
    present = sorted(p.name for p in (ROOT / "proof_certificates").glob("*.json.gz"))
    assert present == expected, \
        f"certificate inventory mismatch: expected {expected}, found {present}"
    return len(expected)


def payload():
    return {
        "format": "luttinger-filled-group-proof-manifest-v1",
        "sha256": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in FILES
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    inventory = check_inventory()
    current = payload()
    if args.check:
        assert json.loads(OUTPUT.read_text(encoding="ascii")) == current, \
            "proof manifest mismatch"
        print("PASS:", OUTPUT, len(FILES), "hashes match;",
              inventory, "certificates, one per filling")
        return
    OUTPUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n",
                      encoding="ascii")
    print(OUTPUT, len(FILES), "hashed files")


if __name__ == "__main__":
    main()
