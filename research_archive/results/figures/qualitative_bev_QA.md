# Qualitative BEV figure QA

## Figure contract

- Core conclusion: strict proposal voting can convert selected RDAR misses into hits by small BEV box refinements around sparse radar targets.
- Evidence chain: three rows show Astyx, TruckScenes, and V2X-Radar-V cases. Each row compares RDAR and strict matched boxes against the same target GT.
- Archetype: image plate + qualitative validation.
- Backend: Python / matplotlib only.
- Export bundle: SVG, PDF, PNG, and 600-dpi TIFF are generated under `results/figures/`.

## Case-level evidence

| Dataset | Frame | Target GT | RDAR IoU | Strict IoU | Gain |
|---|---|---:|---:|---:|---:|
| Astyx | 000499 | 2 | 0.4203 | 0.5235 | +0.1032 |
| TruckScenes | 000267 | 11 | 0.4940 | 0.6599 | +0.1658 |
| V2X-Radar-V | 000361 | 2 | 0.4970 | 0.5420 | +0.0449 |

## QA checklist

| Check | Status |
|---|---|
| Panel labels | Pass: lowercase labels a/b/c present. |
| Legend | Pass after revision: no overlap with axis labels. |
| Text/readability | Pass for manuscript preview; keep final-size check before submission. |
| Editable text | Pass by export setting: SVG fonttype none, PDF fonttype 42. |
| Color coding | Pass: target GT green, RDAR red dashed, strict blue dashed, radar points gray. |
| Source traceability | Pass: each panel traces to `.npz` and `.json` assets in `results/qualitative_cases/`. |
| Claim scope | Pass with limitation: this figure is qualitative only; it must not be used as aggregate performance evidence. |

## Use decision

- Keep as main-figure candidate if the manuscript needs visual evidence of proposal refinement.
- Caption must state that panels are representative selected cases.
- Do not claim range/sparsity robustness from this figure.
