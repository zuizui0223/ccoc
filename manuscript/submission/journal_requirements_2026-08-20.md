# Theoretical Ecology submission requirements — checked 2026-08-20

Primary source: Springer Nature journal-level submission guidelines for *Theoretical Ecology*.

- https://link.springer.com/journal/12080/submission-guidelines
- https://www.springernature.com/gp/authors/campaigns/latex-author-support

## Requirements implemented in the build

- abstract: **150–250 words**;
- keywords: **4–6**;
- title page: title, author name(s), affiliations, corresponding-author email, ORCID if available;
- mathematical manuscripts may be submitted in LaTeX; Springer Nature recommends its current LaTeX authoring template;
- in-text references use **author–year** style;
- reference list contains only cited works that are published or accepted, alphabetized by first-author surname, with DOI links when available;
- required **Statements and Declarations** follow the References section;
- figures are numbered consecutively and cited in text;
- figure captions belong in the manuscript text, not inside the artwork;
- electronic figures are required; vector graphics are preferred as EPS and lettering must remain legible at final size;
- supplementary text should be provided as PDF and cited as an Online Resource;
- the cover letter should suggest **5 potential reviewers**;
- editable source files must be supplied at submission/revision.

## LLM / generative-AI policy note

The journal-level instructions state that LLMs do not qualify for authorship. Substantive LLM use should be documented in the Methods section or another suitable part when no Methods section exists; AI-assisted copy editing alone does not require declaration. Human authors remain accountable for the final text.

The repository does not automatically finalize an AI-use statement because the final wording must describe what actually occurred and must be approved by the human author(s) at submission.

## Build policy

The build treats author metadata, declarations, reviewer names, and final AI disclosure as author-controlled blockers rather than inventing them. It can still verify all repository-controlled structural requirements.