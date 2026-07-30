# Citation verification update

Date: 2026-07-26

## Summary

This update resolves the main citation-risk issue in `manuscript_working_draft_v1.md`.

## RDAR handling

Targeted searches in the project files and on the web did not identify a reliable public RDAR radar-detection paper/source matching the current experimental baseline. Because of that, the manuscript no longer cites `RDAR_manual_needed`.

Current manuscript wording:

> In this study, RDAR denotes our recovery-oriented primary baseline route in the experimental framework.

This is safer than implying RDAR is an externally published method. If a real RDAR source is later identified, it can be added to Related Work and `references_draft.bib`.

## Astyx update

The Astyx dataset citation has been improved from partial metadata to a usable draft entry:

- Meyer, Michael and Kuschk, Georg.
- "Automotive Radar Dataset for Deep Learning Based 3D Object Detection."
- 2019 16th European Radar Conference (EuRAD), pp. 129-132.
- IEEE Xplore document: 8904734.

Final DOI should still be checked before submission if the target journal requires DOI completeness.

## V2X-Radar update

The V2X-Radar citation has been updated using the official repository citation:

- Yang, Lei; Zhang, Xinyu; Li, Jun; Wang, Chen; Ma, Jiaqi; Song, Zhiying; Zhao, Tong; Song, Ziying; Wang, Li; Zhou, Mo; Shen, Yang; Wu, Kai; Lv, Chen.
- "V2X-Radar: A Multi-modal Dataset with 4D Radar for Cooperative Perception."
- Advances in Neural Information Processing Systems, 2025.

The manuscript still uses the key `V2XRadar2024` to avoid changing all placeholders, but the BibTeX entry now records year 2025 according to the official repository. This key can be renamed later during final BibTeX cleanup.

## Verification status after update

Remote consistency check:

- `remaining_cite_placeholders = 0`
- `rdar_manual_in_manuscript = False`
- `missing_keys = []`
- `citation_keys_in_manuscript = 18`
- `draft_bib_entries = 20`

## Remaining citation tasks

1. Final DOI/style audit for Astyx.
2. Final target-journal citation formatting.
3. Optional key rename from `V2XRadar2024` to `V2XRadar2025`.
4. Add RDAR citation only if a verified original source is provided or located later.
