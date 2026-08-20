# Theoretical Ecology submission source

This directory is the journal-facing build layer for the first CCOC paper. The canonical scientific prose remains in `../main.md`; theorem proofs remain in `../supplement.md`; rendered conceptual figures remain in `../figures/`.

## Target

**Journal:** *Theoretical Ecology*  
**Article type:** regular research article  
**Working title:** *Causal Compression under Open Composition*

The 2026-08-20 journal-level requirements used by this build are recorded in `journal_requirements_2026-08-20.md`.

## Build

From the repository root:

```bash
python scripts/build_theoretical_ecology_submission.py --check --build
```

The build produces a flat upload bundle under `manuscript/submission/build/` containing:

- a Word manuscript preview;
- a self-contained LaTeX manuscript source and compiled PDF;
- vector/print figure variants;
- Online Resource 1 (analytic proof supplement);
- cover-letter template;
- a machine-readable submission report;
- the exact source SHA used for the build.

The generated files are build artifacts, not the scientific source of record.

## Author-controlled fields

The build deliberately leaves the following unresolved until the human author finalizes them:

- author name(s);
- affiliation(s);
- corresponding-author email;
- ORCID(s), if used;
- acknowledgements;
- funding statement;
- competing-interest statement;
- author-contribution statement;
- final wording for any generative-AI/LLM disclosure required by the live publisher policy;
- five actual reviewer suggestions for the cover letter.

The submission report therefore distinguishes **automated manuscript readiness** from **author-controlled submission readiness**.

## Stop rule

Do not expand the theorem family from this directory. Any scientific change must first be made in the canonical manuscript/proof/claim surfaces and pass the CCOC claim-control rules.