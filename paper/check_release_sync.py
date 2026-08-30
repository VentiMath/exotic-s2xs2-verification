#!/usr/bin/env python3
"""Check that the v2.1.0 paper, supplement, metadata, and release agree.

Candidate mode verifies everything that can be fixed before reserving the
version DOI and cutting the tag.  Final mode additionally requires the exact
DOI, final wording, a clean tagged checkout, and v2.1.0 release URLs in every
public-facing document.  The script deliberately has no network access; the
release URL and DOI must still be opened from a logged-out browser.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import tarfile
from pathlib import Path


VERSION = "v2.1.0"
TITLE_FRAGMENT = "A certificate-based audit of simple connectivity"
ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
ARXIV = ROOT / "ARXIV_SUBMISSION.md"
README = ROOT / "README.md"
MAIN_TEX = PAPER / "main.tex"
SUPP_TEX = PAPER / "supplement.tex"
COMPANION = ROOT / "docs/verification-note.md"
MAIN_PDF = PAPER / "main.pdf"
SUPP_PDF = PAPER / "supplement.pdf"
SOURCE = PAPER / f"arxiv-source-{VERSION}.tar.gz"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(*args: str) -> str:
    return subprocess.run(
        args, cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def recorded_hash(metadata: str, label: str) -> str:
    match = re.search(
        rf"{re.escape(label)}:\s*\n\s*`([0-9a-f]{{64}})`", metadata
    )
    if not match:
        fail(f"missing {label} in ARXIV_SUBMISSION.md")
    return match.group(1)


def pdf_pages(path: Path) -> int:
    output = run("pdfinfo", str(path))
    match = re.search(r"^Pages:\s+(\d+)\s*$", output, re.MULTILINE)
    if not match:
        fail(f"could not read page count from {path}")
    return int(match.group(1))


def require(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        fail(f"missing {label}: {fragment!r}")


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--final",
        action="store_true",
        help="also require the reserved DOI, final tag, and public-facing final wording",
    )
    args = parser.parse_args()

    for path in (
        ARXIV,
        README,
        MAIN_TEX,
        SUPP_TEX,
        COMPANION,
        MAIN_PDF,
        SUPP_PDF,
        SOURCE,
    ):
        if not path.is_file():
            fail(f"missing release input {path.relative_to(ROOT)}")

    metadata = ARXIV.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    main_tex = MAIN_TEX.read_text(encoding="utf-8")
    supplement = SUPP_TEX.read_text(encoding="utf-8")
    companion = COMPANION.read_text(encoding="utf-8")
    public_texts = {
        "README.md": readme,
        "ARXIV_SUBMISSION.md": metadata,
        "paper/main.tex": main_tex,
        "paper/supplement.tex": supplement,
        "docs/verification-note.md": companion,
    }

    for name, text in public_texts.items():
        require(text, "Source Formalization", f"Source Formalization D in {name}")
        require(text, TITLE_FRAGMENT, f"v2.1 title in {name}")
        if re.search(r"S1\s*(?:--|–|---)\s*S4", text):
            fail(f"obsolete S1--S4 formulation survives in {name}")

    expected = {
        "Source-archive SHA-256": SOURCE,
        "Main PDF SHA-256": MAIN_PDF,
        "Supplement PDF SHA-256": SUPP_PDF,
    }
    for label, path in expected.items():
        actual = sha256(path)
        recorded = recorded_hash(metadata, label)
        if actual != recorded:
            fail(f"{label} mismatch: recorded {recorded}, actual {actual}")

    with tarfile.open(SOURCE, "r:gz") as archive:
        names = archive.getnames()
        if names != ["main.tex"]:
            fail(f"arXiv source archive inventory is {names!r}, expected ['main.tex']")
        archived_main = archive.extractfile("main.tex")
        if archived_main is None or archived_main.read() != MAIN_TEX.read_bytes():
            fail("arXiv source archive does not contain the current paper/main.tex")

    main_pdf_text = normalize_space(run("pdftotext", str(MAIN_PDF), "-"))
    supp_pdf_text = normalize_space(run("pdftotext", str(SUPP_PDF), "-"))
    pdf_title = "A certificate-based audit of simple connectivity for an explicit"
    require(main_pdf_text, pdf_title, "v2.1 title in main PDF")
    require(supp_pdf_text, pdf_title, "v2.1 title in supplement PDF")

    if pdf_pages(MAIN_PDF) != 24 or pdf_pages(SUPP_PDF) != 12:
        fail("PDF page counts are not main=24 and supplement=12")
    require(metadata, "24 pages, three figures, six tables", "arXiv counts")
    if main_tex.count(r"\begin{figure}") != 3:
        fail("main.tex does not contain exactly three figure environments")
    table_count = main_tex.count(r"\begin{table}") + main_tex.count(
        r"\begin{longtable}"
    )
    if table_count != 6:
        fail("main.tex does not contain exactly six table/longtable environments")

    manifest = ROOT / "verification/luttinger/proof_certificates/manifest.json"
    downstream = ROOT / "verification/luttinger/downstream_chain_certificate.json"
    for path in (manifest, downstream):
        digest = sha256(path)
        if digest not in supplement:
            fail(f"supplement does not record the digest of {path.relative_to(ROOT)}")

    require(
        metadata,
        "The primary result is the source-independent theorem $\\pi_1(V_aud)=1$.",
        "primary-result statement in arXiv comments",
    )

    if not args.final:
        print("PASS: the local v2.1.0 candidate is internally synchronized")
        print("  main=24 pages/3 figures/6 tables; supplement=12 pages")
        print("  PDF, source-archive, proof-manifest, and downstream hashes agree")
        print("NOT FINAL: reserve the version DOI, replace candidate wording, cut the")
        print("  v2.1.0 tag, publish the release/deposit, then rerun with --final")
        return

    forbidden = ("[INSERT AFTER DEPOSIT]", "release candidate", "release candidates")
    for name, text in public_texts.items():
        for phrase in forbidden:
            if phrase.lower() in text.lower():
                fail(f"final-mode placeholder {phrase!r} survives in {name}")
        if "v2.0.1" in text:
            fail(f"obsolete release v2.0.1 survives in final-facing file {name}")
        require(
            text,
            f"releases/tag/{VERSION}",
            f"exact {VERSION} release URL in {name}",
        )

    doi_match = re.search(
        rf"Exact {re.escape(VERSION)} archive DOI:\s*"
        r"(https://doi\.org/10\.5281/zenodo\.\d+)",
        metadata,
    )
    if not doi_match:
        fail(f"missing exact {VERSION} archive DOI in ARXIV_SUBMISSION.md")
    version_doi = doi_match.group(1)
    for name, text in public_texts.items():
        require(text, version_doi, f"exact version DOI in {name}")

    head = run("git", "rev-parse", "HEAD")
    try:
        tagged = run("git", "rev-list", "-n", "1", VERSION)
    except subprocess.CalledProcessError:
        fail(f"tag {VERSION} does not exist")
    if head != tagged:
        fail(f"tag {VERSION} does not point at HEAD")
    if run("git", "status", "--porcelain", "--untracked-files=no"):
        fail("tracked working tree is not clean")

    print(f"PASS: {VERSION} final packet, tag, hashes, counts, and DOI agree")
    print("NETWORK CHECK STILL REQUIRED: open the release URL and DOI logged out")


if __name__ == "__main__":
    main()
