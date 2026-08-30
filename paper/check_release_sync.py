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
import contextlib
import hashlib
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path


VERSION = "v2.1.0"
TITLE_FRAGMENT = "A certificate-based audit of simple connectivity"
ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
ARXIV = ROOT / "ARXIV_SUBMISSION.md"
README = ROOT / "README.md"
MAIN_TEX = PAPER / "main.tex"
SUPP_TEX = PAPER / "supplement.tex"
CITATION = ROOT / "CITATION.cff"
MAIN_PDF = PAPER / "main.pdf"
SUPP_PDF = PAPER / "supplement.pdf"
SOURCE = PAPER / f"arxiv-source-{VERSION}.tar.gz"
BUILD_SOURCE = PAPER / "build_arxiv_source.sh"


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


def source_archive(stack: contextlib.ExitStack) -> Path:
    """Return the arXiv source archive, rebuilding it when the tree has none.

    The archive is an ignored, deterministic build product, so a clean
    checkout carries no copy.  Rebuilding it into a temporary directory lets
    this gate run from a fresh clone instead of only from a working tree that
    happens to have built one.
    """
    if SOURCE.is_file():
        return SOURCE
    if not BUILD_SOURCE.is_file():
        fail(f"missing release input {BUILD_SOURCE.relative_to(ROOT)}")
    staging = Path(stack.enter_context(tempfile.TemporaryDirectory()))
    built = staging / SOURCE.name
    run("sh", str(BUILD_SOURCE), str(built))
    return built


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
        CITATION,
        MAIN_PDF,
        SUPP_PDF,
    ):
        if not path.is_file():
            fail(f"missing release input {path.relative_to(ROOT)}")

    metadata = ARXIV.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    main_tex = MAIN_TEX.read_text(encoding="utf-8")
    supplement = SUPP_TEX.read_text(encoding="utf-8")
    citation = CITATION.read_text(encoding="utf-8")
    public_texts = {
        "README.md": readme,
        "ARXIV_SUBMISSION.md": metadata,
        "paper/main.tex": main_tex,
        "paper/supplement.tex": supplement,
        "CITATION.cff": citation,
    }

    for name, text in public_texts.items():
        require(text, "Source Comparison Hypotheses", f"Source Comparison Hypotheses D in {name}")
        require(text, TITLE_FRAGMENT, f"v2.1 title in {name}")
        if re.search(r"S1\s*(?:--|–|---)\s*S4", text):
            fail(f"obsolete S1--S4 formulation survives in {name}")

    with contextlib.ExitStack() as stack:
        source = source_archive(stack)

        expected = {
            "Source-archive SHA-256": source,
            "Main PDF SHA-256": MAIN_PDF,
            "Supplement PDF SHA-256": SUPP_PDF,
        }
        for label, path in expected.items():
            actual = sha256(path)
            recorded = recorded_hash(metadata, label)
            if actual != recorded:
                fail(f"{label} mismatch: recorded {recorded}, actual {actual}")

        with tarfile.open(source, "r:gz") as archive:
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

    if pdf_pages(MAIN_PDF) != 25 or pdf_pages(SUPP_PDF) != 14:
        fail("PDF page counts are not main=25 and supplement=14")
    require(metadata, "25 pages, three figures, five tables", "arXiv counts")
    if main_tex.count(r"\begin{figure}") != 3:
        fail("main.tex does not contain exactly three figure environments")
    table_count = main_tex.count(r"\begin{table}") + main_tex.count(
        r"\begin{longtable}"
    )
    if table_count != 5:
        fail("main.tex does not contain exactly five table/longtable environments")

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
    require(
        main_tex,
        r"P_{+,+}\twoheadrightarrow\pione(V_{\mathrm{aud}})",
        "fixed-sheet audit-model map",
    )
    require(
        main_tex,
        r"No geometric identification of $P_{+,-},",
        "scope boundary for the other three sign sheets",
    )
    if "For each coherent convention sheet" in main_tex:
        fail("obsolete all-sheets geometric identification survives in main.tex")
    require(
        main_tex,
        "The preceding proof of $\\pione(V_{\\mathrm{aud}})=1$ is complete before this",
        "logical separation of simple connectivity from the framing bridge",
    )
    require(
        main_tex,
        "does not publish this\ncontrary presentation",
        "neutral statement that the contrary presentation is unavailable",
    )
    require(
        main_tex,
        "Relation-by-relation\nreconciliation requires the missing artifact.",
        "unresolved contrary-computation boundary",
    )
    for overclaim in (
        "resolves the contrary computation",
        "proves the contrary computation wrong",
        "refutes the contrary computation",
    ):
        if overclaim in main_tex.lower():
            fail(f"contrary-computation overclaim survives: {overclaim!r}")

    if not args.final:
        print("PASS: the local v2.1.0 candidate is internally synchronized")
        print("  main=25 pages/3 figures/5 tables; supplement=14 pages")
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
