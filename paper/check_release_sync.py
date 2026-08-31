#!/usr/bin/env python3
"""Check the working paper, supplement, metadata, and release packet.

Candidate mode verifies everything that can be fixed before reserving the
version DOI and cutting the tag, and permits explicitly marked TBD hashes.
Final mode additionally requires an explicit version, the exact DOI,
recorded hashes, final wording, a clean tagged checkout, and that version's
release URLs in every
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


ARCHIVED_BASE_VERSION = "v2.2.2"
TITLE_FRAGMENT = "Certificate-checked simple connectivity"
PDF_TITLE = "Certificate-checked simple connectivity of a surface-bundle surgery manifold"
ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
ARXIV = ROOT / "ARXIV_SUBMISSION.md"
README = ROOT / "README.md"
MAIN_TEX = PAPER / "main.tex"
SUPP_TEX = PAPER / "supplement.tex"
CITATION = ROOT / "CITATION.cff"
MAIN_PDF = PAPER / "main.pdf"
SUPP_PDF = PAPER / "supplement.pdf"
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
    """Build and return a fresh deterministic archive of the current source."""
    if not BUILD_SOURCE.is_file():
        fail(f"missing release input {BUILD_SOURCE.relative_to(ROOT)}")
    staging = Path(stack.enter_context(tempfile.TemporaryDirectory()))
    built = staging / "arxiv-source-working.tar.gz"
    run("sh", str(BUILD_SOURCE), str(built))
    return built


def rebuilt_pdf(tex: Path, stack: contextlib.ExitStack) -> Path:
    """Build one TeX source in a temporary directory for freshness checks."""
    staging = Path(stack.enter_context(tempfile.TemporaryDirectory()))
    run("tectonic", "--outdir", str(staging), str(tex))
    built = staging / f"{tex.stem}.pdf"
    if not built.is_file():
        fail(f"Tectonic did not produce {built.name} from {tex.relative_to(ROOT)}")
    return built


def recorded_hash(metadata: str, label: str, *, required: bool) -> str | None:
    match = re.search(
        rf"{re.escape(label)}:\s*\n\s*`([0-9a-f]{{64}})`", metadata
    )
    if not match and not required and re.search(
        rf"{re.escape(label)}:\s*\*\*TBD\b", metadata
    ):
        return None
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
    parser.add_argument(
        "--version",
        help="exact release version to require in final mode, for example v2.3.0",
    )
    args = parser.parse_args()
    if args.final and not args.version:
        fail("--final requires --version VERSION")
    version = args.version or ARCHIVED_BASE_VERSION

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
    draft_texts = {
        "README.md": readme,
        "ARXIV_SUBMISSION.md": metadata,
        "paper/main.tex": main_tex,
        "paper/supplement.tex": supplement,
    }

    for name, text in draft_texts.items():
        if name != "ARXIV_SUBMISSION.md":
            require(text, "D1--D14", f"open comparison checklist in {name}")
        require(text, TITLE_FRAGMENT, f"current title in {name}")
        if re.search(r"S1\s*(?:--|–|---)\s*S4", text):
            fail(f"obsolete S1--S4 formulation survives in {name}")

    candidate_source_digest = ""
    with contextlib.ExitStack() as stack:
        source = source_archive(stack)
        candidate_source_digest = sha256(source)

        for tex, committed in ((MAIN_TEX, MAIN_PDF), (SUPP_TEX, SUPP_PDF)):
            rebuilt = rebuilt_pdf(tex, stack)
            rebuilt_text = run("pdftotext", "-layout", str(rebuilt), "-")
            committed_text = run("pdftotext", "-layout", str(committed), "-")
            if rebuilt_text != committed_text:
                fail(
                    f"{committed.relative_to(ROOT)} is stale relative to "
                    f"{tex.relative_to(ROOT)}; rebuild the PDF"
                )
            if pdf_pages(rebuilt) != pdf_pages(committed):
                fail(
                    f"{committed.relative_to(ROOT)} page count differs from a fresh build"
                )

        expected = {
            "Source-archive SHA-256": source,
            "Main PDF SHA-256": MAIN_PDF,
            "Supplement PDF SHA-256": SUPP_PDF,
        }
        for label, path in expected.items():
            actual = sha256(path)
            recorded = (
                recorded_hash(metadata, label, required=True)
                if args.final
                else None
            )
            if recorded is not None and actual != recorded:
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
    require(main_pdf_text, PDF_TITLE, "current title in main PDF")
    require(supp_pdf_text, PDF_TITLE, "current title in supplement PDF")

    if pdf_pages(MAIN_PDF) != 22 or pdf_pages(SUPP_PDF) != 17:
        fail("PDF page counts are not main=22 and supplement=17")
    require(metadata, "22 pages, four figures, and two tables", "arXiv counts")
    if main_tex.count(r"\begin{figure}") != 4:
        fail("main.tex does not contain exactly four figure environments")
    table_count = main_tex.count(r"\begin{table}") + main_tex.count(
        r"\begin{longtable}"
    )
    if table_count != 2:
        fail("main.tex does not contain exactly two table/longtable environments")

    manifest = ROOT / "verification/luttinger/proof_certificates/manifest.json"
    downstream = ROOT / "verification/luttinger/downstream_chain_certificate.json"
    for path in (manifest, downstream):
        digest = sha256(path)
        if digest not in supplement:
            fail(f"supplement does not record the digest of {path.relative_to(ROOT)}")

    # The supplement pins the archived verification/ tree by its git tree
    # object.  Pinning a commit goes stale on every later commit; the tree
    # object only changes when verification/ itself changes.
    tree_ref = "HEAD:verification" if args.final else f"{ARCHIVED_BASE_VERSION}:verification"
    tree = run("git", "rev-parse", tree_ref)
    if tree not in supplement:
        fail(
            "supplement does not pin the current verification/ tree object "
            f"{tree}; rebuild the supplement after changing verification/"
        )

    require(
        metadata,
        "The primary result is the source-independent theorem $\\pi_1(V_aud)=1$.",
        "primary-result statement in arXiv comments",
    )
    require(
        main_tex,
        r"P_{+,+}\;\cong\;\pione(V_{\mathrm{aud}})",
        "fixed-sheet audit-model isomorphism",
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
        "The proof of simple connectivity and the intrinsic topological assertions is\ncomplete before this section begins.",
        "logical separation of simple connectivity from the framing bridge",
    )
    require(
        main_tex,
        "does not publish this\ncontrary presentation",
        "neutral statement that the contrary presentation is unavailable",
    )
    require(
        main_tex,
        "relation-by-relation reconciliation requires the missing presentation",
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
        print("PASS: the post-v2.2.2 working revision is internally synchronized")
        print("  main=22 pages/4 figures/2 tables; supplement=17 pages")
        print("  fresh source archive matches main.tex; archived-base manifest pins agree")
        print(f"  candidate source SHA-256: {candidate_source_digest}")
        print(f"  candidate main PDF SHA-256: {sha256(MAIN_PDF)}")
        print(f"  candidate supplement PDF SHA-256: {sha256(SUPP_PDF)}")
        print("NOT FINAL: regenerate the proof manifest to bind the modified Python")
        print("  checker and new invariant checker; reserve a new version DOI, replace")
        print("  working wording, cut the new tag, and rerun --final --version VERSION")
        return

    forbidden = (
        "[INSERT AFTER DEPOSIT]",
        "release candidate",
        "release candidates",
        "working revision",
        "artifact base",
        "TBD after",
        "planned as a release asset",
    )
    final_texts = {**draft_texts, "CITATION.cff": citation}
    for name, text in final_texts.items():
        for phrase in forbidden:
            if phrase.lower() in text.lower():
                fail(f"final-mode placeholder {phrase!r} survives in {name}")
        for stale in ("v2.2.1", "v2.2.0", "v2.1.0", "v2.0.1"):
            if stale in text:
                fail(f"obsolete release {stale} survives in final-facing file {name}")
        require(
            text,
            f"releases/tag/{version}",
            f"exact {version} release URL in {name}",
        )

    doi_match = re.search(
        rf"Exact {re.escape(version)} archive DOI:\s*"
        r"(https://doi\.org/10\.5281/zenodo\.\d+)",
        metadata,
    )
    if not doi_match:
        fail(f"missing exact {version} archive DOI in ARXIV_SUBMISSION.md")
    version_doi = doi_match.group(1)
    for name, text in final_texts.items():
        require(text, version_doi, f"exact version DOI in {name}")

    head = run("git", "rev-parse", "HEAD")
    try:
        tagged = run("git", "rev-list", "-n", "1", version)
    except subprocess.CalledProcessError:
        fail(f"tag {version} does not exist")
    if head != tagged:
        fail(f"tag {version} does not point at HEAD")
    if run("git", "status", "--porcelain", "--untracked-files=no"):
        fail("tracked working tree is not clean")

    print(f"PASS: {version} final packet, tag, hashes, counts, and DOI agree")
    print("NETWORK CHECK STILL REQUIRED: open the release URL and DOI logged out")


if __name__ == "__main__":
    main()
