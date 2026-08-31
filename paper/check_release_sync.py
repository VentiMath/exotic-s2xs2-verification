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
from datetime import date
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
LUTTINGER = ROOT / "verification/luttinger"
MANIFEST = ROOT / "verification/luttinger/proof_certificates/manifest.json"
DOWNSTREAM = ROOT / "verification/luttinger/downstream_chain_certificate.json"


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


def checked_run(label: str, *args: str, cwd: Path = ROOT) -> str:
    """Run a release check and report its own output if it fails."""
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        detail = "\n".join(part for part in (result.stdout, result.stderr) if part)
        fail(f"{label} failed\n{detail.rstrip()}")
    return result.stdout.strip()


def replay_suite() -> None:
    """Run every theorem-facing replay documented for a clean checkout."""
    sealed_certificates = sorted(
        str(path.relative_to(LUTTINGER))
        for path in (LUTTINGER / "sealed_transport/proof_certificates").glob("*.json.gz")
    )
    commands: list[tuple[str, tuple[str, ...]]] = [
        ("proof manifest", ("python3", "make_proof_manifest.py", "--check")),
        ("sealed Tietze transport (Python)",
         ("python3", "verify_tietze_transport.py", "--negative-controls")),
        ("sealed Tietze transport (Ruby)",
         ("ruby", "verify_tietze_transport.rb", "--negative-controls")),
        ("sealed filled groups (Python)",
         ("python3", "verify_kbmag_certificate.py", "--input",
          "sealed_transport/r_presentations.json", "--full-inventory",
          "--expect-generators", "3", "--expect-relators", "78",
          "--negative-controls", *sealed_certificates)),
        ("sealed filled groups (Ruby)",
         ("ruby", "verify_certificates.rb", "--root", "sealed_transport",
          "--full-inventory", "--expect-generators", "3",
          "--expect-relators", "78", "--negative-controls")),
        ("audit-manifold invariant arithmetic",
         ("python3", "audit_manifold_invariants.py")),
        ("downstream chain regeneration check",
         ("python3", "downstream_chain.py", "--check")),
        ("downstream chain independent replay",
         ("ruby", "verify_downstream_chain.rb")),
        ("proof ledger", ("python3", "proof_ledger.py")),
        ("publication semantics", ("python3", "publication_semantics_check.py")),
        ("alpha residual (Python)",
         ("python3", "alpha_residual/verify_certificate.py",
          "--negative-controls", "alpha_residual/certificate.json.gz")),
        ("alpha residual (Ruby)",
         ("ruby", "alpha_residual/verify_certificate.rb",
          "--negative-controls", "alpha_residual/certificate.json.gz")),
        ("beta residual (Python)",
         ("python3", "beta_residual/verify_certificate.py",
          "--negative-controls", "beta_residual/certificate.json.gz")),
        ("beta residual (Ruby)",
         ("ruby", "beta_residual/verify_certificate.rb",
          "--negative-controls", "beta_residual/certificate.json.gz")),
    ]
    for label, command in commands:
        checked_run(label, *command, cwd=LUTTINGER)


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


def folded_cff_field(text: str, field: str) -> str:
    """Read the simple folded scalar form used for top-level CFF fields."""
    match = re.search(
        rf"^{re.escape(field)}:\s*>-\s*\n((?:[ \t]+.*(?:\n|$))+)",
        text,
        re.MULTILINE,
    )
    if not match:
        fail(f"CITATION.cff does not give {field!r} as a folded scalar")
    return normalize_space(match.group(1))


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

    # Execute the documented theorem-facing replays, not merely their hashes.
    # This catches checker drift, a stale conditional chain, editorial-scope
    # regression, and failure of either independent implementation.
    replay_suite()
    for path in (MANIFEST, DOWNSTREAM):
        digest = sha256(path)
        if digest not in supplement:
            fail(f"supplement does not record the digest of {path.relative_to(ROOT)}")
    manifest_digest = sha256(MANIFEST)
    if manifest_digest not in main_tex:
        fail("main paper does not record the current proof-manifest digest")

    # The supplement pins the working verification/ tree by its git tree
    # object.  Pinning a repository commit would go stale after unrelated
    # paper edits; the subtree object changes only when verification/ changes.
    tree_ref = "HEAD:verification"
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
        print("  complete replay suite passes; working manifest/tree pins agree")
        print("  fresh source archive matches main.tex and both committed PDFs")
        print(f"  candidate source SHA-256: {candidate_source_digest}")
        print(f"  candidate main PDF SHA-256: {sha256(MAIN_PDF)}")
        print(f"  candidate supplement PDF SHA-256: {sha256(SUPP_PDF)}")
        print("NOT FINAL: reserve a new version DOI, replace")
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

    # Exact current-release assertions.  These close holes that generic URL
    # and placeholder checks miss: a stale CFF title/version, a README that
    # still calls the previous tag newest, an old normative-root sentence,
    # or an old self-citation/recovery command can no longer pass final mode.
    if folded_cff_field(citation, "title") != PDF_TITLE:
        fail("CITATION.cff title is not the exact manuscript title")
    abstract_match = re.search(
        r"\*\*Abstract\*\*\s*```text\s*(.*?)\s*```",
        metadata,
        re.DOTALL,
    )
    if not abstract_match:
        fail("could not read the arXiv abstract from ARXIV_SUBMISSION.md")
    if folded_cff_field(citation, "abstract") != normalize_space(abstract_match.group(1)):
        fail("CITATION.cff abstract does not exactly match the arXiv abstract")
    require(citation, f"version: {version}", "exact CFF version")
    doi_value = version_doi.removeprefix("https://doi.org/")
    if not re.search(rf"^doi:\s*{re.escape(doi_value)}\s*$", citation, re.MULTILINE):
        fail("CITATION.cff top-level DOI is not the exact version DOI")
    release_date_match = re.search(
        r"^date-released:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?\s*$",
        citation,
        re.MULTILINE,
    )
    if not release_date_match:
        fail("CITATION.cff lacks a valid ISO release date")
    release_date = date.fromisoformat(release_date_match.group(1))
    human_date = f"{release_date.day} {release_date.strftime('%B %Y')}"
    require(main_tex, human_date, "CFF release date on main title page")
    require(supplement, human_date, "CFF release date on supplement title page")
    require(
        citation,
        f"description: 'Version DOI for the {version} archived artifact'",
        "version-specific CFF DOI description",
    )
    require(
        citation,
        f"description: 'Resolver link for the {version} version DOI'",
        "version-specific CFF resolver description",
    )
    require(
        readme,
        f"**{version} release.** The newest public immutable release is:",
        "README newest-release declaration",
    )
    require(main_tex, f"the {version} proof manifest", "current normative root")
    require(
        main_tex,
        r"\emph{Certificate-checked simple connectivity of a surface-bundle surgery manifold}",
        "current artifact title in the bibliography",
    )
    require(main_tex, f"verification artifact {version}", "current artifact version")
    require(
        supplement,
        f"tagged release \\texttt{{{version}}}",
        "current tagged release in supplement",
    )
    require(
        supplement,
        f"git rev-parse {version}:verification",
        "current verification-tree recovery command",
    )

    # v2.2.2 may survive only in the one explicit historical statement that
    # the newly added invariant checker was absent from that archived manifest.
    if version != ARCHIVED_BASE_VERSION:
        for name, text in (
            ("README.md", readme),
            ("ARXIV_SUBMISSION.md", metadata),
            ("paper/main.tex", main_tex),
            ("CITATION.cff", citation),
        ):
            if ARCHIVED_BASE_VERSION in text:
                fail(f"archived base {ARCHIVED_BASE_VERSION} survives in final-facing {name}")
        historical = "It is not part of the archived v2.2.2 manifest"
        normalized_supplement = normalize_space(supplement)
        if historical not in normalized_supplement:
            fail("supplement lost the allowed v2.2.2 historical statement")
        if ARCHIVED_BASE_VERSION in normalized_supplement.replace(historical, ""):
            fail("v2.2.2 survives outside its one allowed historical statement")

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
