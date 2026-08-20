#!/usr/bin/env python3
"""Build and verify the journal-facing CCOC submission package.

Canonical scientific sources remain under manuscript/. This script creates a
submission preview without changing theorem claims. Author-controlled fields stay
explicitly unresolved until a human author supplies them.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
SUBMISSION = MANUSCRIPT / "submission"
BUILD = SUBMISSION / "build"
MAIN_MD = MANUSCRIPT / "main.md"
SUPPLEMENT_MD = MANUSCRIPT / "supplement.md"
DECLARATIONS_MD = SUBMISSION / "declarations_template.md"
COVER_LETTER_MD = SUBMISSION / "cover_letter_template.md"
REFERENCES_BIB = MANUSCRIPT / "references.bib"

TITLE = "Causal Compression under Open Composition"
KEYWORDS = [
    "theoretical ecology",
    "ecological state abstraction",
    "causal compression",
    "open composition",
    "model reduction",
    "ecological networks",
]

FIGURES = [
    (
        "Fig1",
        MANUSCRIPT / "figures" / "fig1_future_grammar.svg",
        "Same controlled system, different future grammar. The physical plant and transition rules are fixed; opening enlarges only the set of legal futures, so a response-equivalence class valid under the closed grammar can split under the open grammar.",
        "**Figure 1** summarizes this contract: the controlled plant is unchanged, but the set of legal futures expands, and a state merge that was exact under the closed grammar can be split by the newly admissible future.",
    ),
    (
        "Fig2",
        MANUSCRIPT / "figures" / "fig2_operational_lower_bound.svg",
        "Operational lower-bound mechanism. Concrete legal decoder words expose the focal coordinate and exterior coordinates. Any pair that differs in a readable coordinate is separated by a legal future response, yielding the open-interface lower bound.",
        "The condition is operational rather than merely combinatorial: each distinction counted in the lower bound has an explicit legal future experiment that can expose it. **Figure 2** shows this pair-separation mechanism and the resulting injection into open response classes.",
    ),
    (
        "Fig3",
        MANUSCRIPT / "figures" / "fig3_extremal_relay.svg",
        "One-action extremal bounded-local witness. The same relay network has two closed response classes when fire is illegal, while legalizing only fire exposes all dormant leaf bits and makes the open quotient discrete on 2^(m+1) comparison states. The construction keeps a fixed four-symbol action alphabet, bounded local alphabets, degree at most three, and logarithmic query length.",
        "**Figure 3** displays the relay, the single newly legal `fire` action, and the simultaneous bounds on quotient size, degree, local alphabets, cut width, and access length.",
    ),
    (
        "Fig4",
        MANUSCRIPT / "figures" / "fig4_portability_split.svg",
        "Portability versus forced split. A newly legal action is harmless when it remains uniform inside an old macro fiber and preserves common macro dynamics; a future word that produces different traces or successors from two formerly merged states invalidates that proposed merge.",
        "The positive and negative results therefore meet at the same conceptual boundary: future expansion is harmless exactly in examples where newly legal behavior continues to factor through the old macro semantics; it forces refinement when it exposes distinctions internal to an old macro fiber. **Figure 4** contrasts these two cases.",
    ),
]

REFERENCE_LIST = """## References

Aziz A, Singhal V, Swamy GM, Brayton RK (1993) Minimizing Interacting Finite State Machines. UCB/ERL M93/68, University of California, Berkeley

Hartmanis J, Stearns RE (1962) Some Dangers in State Reduction of Sequential Machines. Information and Control 5:252–260. https://doi.org/10.1016/S0019-9958(62)90588-0

Paull MC, Unger SH (1959) Minimizing the Number of States in Incompletely Specified Sequential Switching Functions. IRE Transactions on Electronic Computers EC-8:356–367. https://doi.org/10.1109/TEC.1959.5222697

Wang H-Y, Brayton RK (1993) Input Don't Care Sequences in FSM Networks. UCB/ERL M93/64, University of California, Berkeley

Watanabe Y, Brayton RK (1993) The Maximum Set of Permissible Behaviors for FSM Networks. UCB/ERL M93/61, University of California, Berkeley
"""

CITATION_SENTENCE = (
    "Classical incompletely specified-machine minimization, environment/input-dependent reduction, "
    "interacting-FSM optimization, and reduction/realization noncommutation already establish that "
    "state reduction depends on the behavior or environment one asks a machine to preserve "
    "(Paull and Unger 1959; Hartmanis and Stearns 1962; Wang and Brayton 1993; Aziz et al. 1993; "
    "Watanabe and Brayton 1993)."
)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def extract_abstract(text: str) -> str:
    match = re.search(r"## Abstract\s+(.*?)\s+## 1\.", text, flags=re.S)
    if not match:
        raise ValueError("Could not locate Abstract section in manuscript/main.md")
    return match.group(1).strip()


def source_sha() -> str:
    env_sha = os.environ.get("GITHUB_SHA")
    if env_sha:
        return env_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "UNKNOWN"


def author_front_matter() -> str:
    return f"""---
title: \"{TITLE}\"
author:
  - \"[AUTHOR INPUT REQUIRED]\"
---

**Affiliation(s):** [AUTHOR INPUT REQUIRED]

**Corresponding author:** [AUTHOR INPUT REQUIRED]

**E-mail:** [AUTHOR INPUT REQUIRED]

**ORCID:** [OPTIONAL AUTHOR INPUT]

"""


def strip_development_header(text: str) -> str:
    text = re.sub(r"^# Causal Compression under Open Composition\s*\n", "", text)
    text = re.sub(
        r"^> Working manuscript\. Primary target lane: \*Theoretical Ecology\*\.\s*\n",
        "",
        text,
    )
    return text


def normalize_math_delimiters(text: str) -> str:
    """Convert canonical backslash math delimiters to Pandoc dollar math.

    The scientific Markdown uses LaTeX-style \(...\) and \[...\]. Pandoc's
    Markdown reader otherwise interprets the delimiters as escaped punctuation,
    which can place commands such as \mathcal outside math mode in generated TeX.
    This transformation is build-only and does not modify canonical sources.
    """

    text = re.sub(
        r"\\\[(.*?)\\\]",
        lambda m: "\n$$\n" + m.group(1).strip() + "\n$$\n",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"\\\((.*?)\\\)",
        lambda m: "$" + m.group(1).strip() + "$",
        text,
        flags=re.S,
    )
    return text


def inject_keywords(text: str) -> str:
    marker = "## 1. Ecological question"
    keyword_line = "**Keywords:** " + "; ".join(KEYWORDS) + "\n\n"
    if marker not in text:
        raise ValueError("Could not locate Section 1 for keyword insertion")
    return text.replace(marker, keyword_line + marker, 1)


def inject_related_work_citations(text: str) -> str:
    old = (
        "Classical incompletely specified-machine minimization, environment/input-dependent reduction, "
        "interacting-FSM optimization, and reduction/realization noncommutation already establish that "
        "state reduction depends on the behavior or environment one asks a machine to preserve."
    )
    if old not in text:
        raise ValueError("Expected Related Work ancestry sentence not found")
    text = text.replace(old, CITATION_SENTENCE, 1)
    text = text.replace(
        "The source-checked comparison is summarized in `manuscript/related_work.md`.",
        "These sources are treated as direct ancestry for the broad claim that the relevant equivalence can depend on the surrounding behavioral contract.",
        1,
    )
    return text


def inject_figures(text: str, extension: str) -> str:
    for name, _source, caption, anchor_sentence in FIGURES:
        if anchor_sentence not in text:
            raise ValueError(f"Expected figure anchor not found for {name}")
        image = f"\n\n![{caption}]({name}.{extension})\n"
        text = text.replace(anchor_sentence, anchor_sentence + image, 1)
    return text


def replace_internal_supplement_note(text: str) -> str:
    old = (
        "## Supplement\n\nThe manuscript-facing supplement is `manuscript/supplement.md`. "
        "It contains the proof spine, theorem-to-CORE/source traceability, and final replay contract. "
        "Figure production is controlled by `manuscript/figures_spec.md`."
    )
    new = (
        "## Supplementary Information\n\n"
        "Complete analytic proofs, theorem-to-source traceability, and finite replay provenance are supplied as Online Resource 1."
    )
    if old not in text:
        raise ValueError("Expected internal supplement note not found")
    return text.replace(old, new, 1)


def assemble_submission_markdown(image_extension: str) -> str:
    text = MAIN_MD.read_text(encoding="utf-8")
    text = strip_development_header(text)
    text = inject_keywords(text)
    text = inject_related_work_citations(text)
    text = inject_figures(text, image_extension)
    text = replace_internal_supplement_note(text)
    text = normalize_math_delimiters(text)
    declarations = DECLARATIONS_MD.read_text(encoding="utf-8").strip()
    return (
        author_front_matter()
        + text.strip()
        + "\n\n"
        + REFERENCE_LIST.strip()
        + "\n\n"
        + declarations
        + "\n"
    )


def validate() -> dict:
    manuscript = MAIN_MD.read_text(encoding="utf-8")
    abstract = extract_abstract(manuscript)
    abstract_words = word_count(abstract)
    cover = COVER_LETTER_MD.read_text(encoding="utf-8")
    declarations = DECLARATIONS_MD.read_text(encoding="utf-8")
    references = REFERENCES_BIB.read_text(encoding="utf-8")

    blockers: list[str] = []
    if not (150 <= abstract_words <= 250):
        blockers.append(f"abstract word count {abstract_words} is outside 150–250")
    if not (4 <= len(KEYWORDS) <= 6):
        blockers.append(f"keyword count {len(KEYWORDS)} is outside 4–6")

    missing_figures = [str(path) for _, path, _, _ in FIGURES if not path.exists()]
    if missing_figures:
        blockers.append("missing figure sources: " + ", ".join(missing_figures))

    reviewer_slots = len(re.findall(r"\*\*\[Reviewer [1-5] name\]\*\*", cover))
    if reviewer_slots != 5:
        blockers.append(f"cover letter has {reviewer_slots} reviewer slots rather than 5")

    for heading in ("## Funding", "## Competing Interests", "## Author Contributions"):
        if heading not in declarations:
            blockers.append(f"missing declarations heading: {heading}")

    for key in (
        "HartmanisStearns1962",
        "PaullUnger1959",
        "WangBrayton1993",
        "AzizEtAl1993",
        "WatanabeBrayton1993",
    ):
        if key not in references:
            blockers.append(f"missing bibliography key: {key}")

    report = {
        "target_journal": "Theoretical Ecology",
        "source_sha": source_sha(),
        "abstract_words": abstract_words,
        "keyword_count": len(KEYWORDS),
        "keywords": KEYWORDS,
        "figure_source_count": len(FIGURES) - len(missing_figures),
        "reviewer_template_slots": reviewer_slots,
        "automated_blockers": blockers,
        "automated_checks_pass": not blockers,
        "author_controlled_blockers": {
            "author_metadata_required": True,
            "funding_required": True,
            "competing_interests_required": True,
            "author_contributions_required": True,
            "five_actual_reviewers_required": True,
            "final_ai_use_wording_requires_human_review": True,
            "final_source_claim_text_review_required": True,
        },
        "submission_ready": False,
        "submission_ready_reason": (
            "repository-controlled structure passes only after automated validation; "
            "author-controlled metadata/declarations/reviewer selection and final human review remain required"
        ),
    }
    return report


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required build command not found: {name}")


def convert_figures() -> None:
    try:
        import cairosvg  # type: ignore
    except ImportError as exc:
        raise RuntimeError("cairosvg is required to build figure variants") from exc

    for name, source, _caption, _anchor in FIGURES:
        cairosvg.svg2png(
            url=str(source), write_to=str(BUILD / f"{name}.png"), output_width=1800
        )
        cairosvg.svg2pdf(url=str(source), write_to=str(BUILD / f"{name}.pdf"))
        cairosvg.svg2eps(url=str(source), write_to=str(BUILD / f"{name}.eps"))


def run(cmd: list[str], cwd: Path = BUILD) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def build(report: dict) -> None:
    if report["automated_blockers"]:
        raise RuntimeError("Submission build blocked by automated validation")

    require_command("pandoc")
    require_command("pdflatex")

    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    convert_figures()

    docx_md = BUILD / "main_docx.md"
    tex_md = BUILD / "main_tex.md"
    docx_md.write_text(assemble_submission_markdown("png"), encoding="utf-8")
    tex_md.write_text(assemble_submission_markdown("pdf"), encoding="utf-8")

    run(
        [
            "pandoc",
            docx_md.name,
            "--standalone",
            "--from=markdown+tex_math_dollars+raw_tex",
            "-o",
            "CCOC_Theoretical_Ecology.docx",
        ]
    )

    run(
        [
            "pandoc",
            tex_md.name,
            "--standalone",
            "--from=markdown+tex_math_dollars+raw_tex",
            "-t",
            "latex",
            "-o",
            "main.tex",
        ]
    )
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
    if (BUILD / "main.pdf").exists():
        (BUILD / "main.pdf").replace(BUILD / "CCOC_Theoretical_Ecology.pdf")

    supplement_text = normalize_math_delimiters(
        SUPPLEMENT_MD.read_text(encoding="utf-8")
    )
    supplement_source = BUILD / "online_resource_1.md"
    supplement_source.write_text(
        "---\ntitle: \"Online Resource 1: Analytic proofs and replay traceability\"\nauthor:\n  - \"[AUTHOR INPUT REQUIRED]\"\n---\n\n"
        + supplement_text,
        encoding="utf-8",
    )
    run(
        [
            "pandoc",
            supplement_source.name,
            "--standalone",
            "--from=markdown+tex_math_dollars+raw_tex",
            "--pdf-engine=pdflatex",
            "-o",
            "Online_Resource_1.pdf",
        ]
    )

    cover_source = BUILD / "cover_letter.md"
    cover_source.write_text(
        normalize_math_delimiters(COVER_LETTER_MD.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    run(["pandoc", cover_source.name, "--standalone", "-o", "Cover_Letter_Template.docx"])

    shutil.copy2(REFERENCES_BIB, BUILD / "references.bib")
    shutil.copy2(SUBMISSION / "metadata.yaml", BUILD / "metadata.yaml")
    shutil.copy2(DECLARATIONS_MD, BUILD / "declarations_template.md")
    shutil.copy2(COVER_LETTER_MD, BUILD / "cover_letter_template.md")

    sha = source_sha()
    (BUILD / "SOURCE_SHA.txt").write_text(sha + "\n", encoding="utf-8")
    report["build_completed"] = True
    report["build_outputs"] = [
        "CCOC_Theoretical_Ecology.docx",
        "CCOC_Theoretical_Ecology.pdf",
        "main.tex",
        "Online_Resource_1.pdf",
        "Fig1.eps",
        "Fig2.eps",
        "Fig3.eps",
        "Fig4.eps",
        "Cover_Letter_Template.docx",
    ]
    report_path = BUILD / "submission_report.json"
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    bundle_members = [
        "CCOC_Theoretical_Ecology.docx",
        "CCOC_Theoretical_Ecology.pdf",
        "main.tex",
        "Online_Resource_1.pdf",
        "Fig1.eps",
        "Fig2.eps",
        "Fig3.eps",
        "Fig4.eps",
        "Fig1.pdf",
        "Fig2.pdf",
        "Fig3.pdf",
        "Fig4.pdf",
        "references.bib",
        "Cover_Letter_Template.docx",
        "cover_letter_template.md",
        "declarations_template.md",
        "metadata.yaml",
        "SOURCE_SHA.txt",
        "submission_report.json",
    ]
    bundle = BUILD / "CCOC_Theoretical_Ecology_submission_bundle.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename in bundle_members:
            zf.write(BUILD / filename, arcname=filename)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="validate journal-facing structural requirements"
    )
    parser.add_argument(
        "--build", action="store_true", help="build Word/LaTeX/PDF submission preview"
    )
    parser.add_argument(
        "--write-report", action="store_true", help="write the structural report without building"
    )
    args = parser.parse_args()

    if not (args.check or args.build or args.write_report):
        args.check = True

    report = validate()
    if args.build:
        build(report)
    elif args.write_report:
        BUILD.mkdir(parents=True, exist_ok=True)
        (BUILD / "submission_report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["automated_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
