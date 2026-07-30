# EAAI submission readiness

Audit date: 2026-07-29

## Current status

The anonymous manuscript is technically ready, but the complete submission
package is not ready until the author-supplied title-page fields and final
approvals below are completed.

## Completed

- EAAI single-column Elsevier LaTeX format.
- Anonymous manuscript contains no author or affiliation metadata.
- Six figures and six tables are present, cited, and captioned.
- Blue review highlighting and visible hyperlink borders are disabled.
- No placeholders, undefined references, missing citations, overfull boxes,
  or critical LaTeX errors remain in the anonymous manuscript.
- All 36 bibliography entries are cited; no uncited entries remain.
- Astyx and MAN TruckScenes dataset papers are cited.
- Highlights are provided separately in `highlights.txt`, with four bullets
  below 85 characters each.
- Generative-AI use, competing-interest, and data-availability statements are
  present.
- Main manuscript PDF is below the journal's 50 MB limit.

## Blocking author inputs

- Complete `title_page_template.tex` with all author names and affiliations.
- Provide the corresponding author's full postal address and email.
- Complete the author-by-author CRediT contribution statement.
- Insert final acknowledgements and funding grant numbers, or state `None`.
- Confirm that every author approves the manuscript and author order.
- Confirm that the manuscript is not under review elsewhere.
- Confirm the generative-AI declaration accurately describes the authors'
  actual use and that every author accepts responsibility for the final text.
- Confirm the data-availability statement and whether a public code/results
  repository will be supplied at submission.

## Scientific risks to accept before submission

- The strict threshold was selected on the same four-dataset protocol used for
  the main strict result; there is no independent held-out selection dataset.
- Three seeds and four datasets support a bounded paired result, not a general
  no-regression guarantee.
- The smallest strict gain is 0.1718 AP, so exact reproducibility matters.
- The point-dropout comparison uses mixed available checkpoint seeds and is
  supportive rather than a fully paired robustness experiment.
- Figure 6 contains selected successful qualitative cases and is not a
  frequency estimate.
- The custom mini/400 conversions and frozen outputs need sufficiently clear
  release or access instructions for independent replication.
