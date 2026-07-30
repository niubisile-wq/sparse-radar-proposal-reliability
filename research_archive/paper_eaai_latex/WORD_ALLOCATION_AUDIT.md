# EAAI word-allocation audit

Date: 2026-07-29

## Published-paper sample

Counts were extracted from the abstract through the section immediately before
the references. PDF extraction introduces small errors, but the section ratios
are sufficient for manuscript planning.

| Paper | Total words | Background / related | Method / technical | Results / discussion | Conclusion |
|---|---:|---:|---:|---:|---:|
| A-KIT | 6,938 | 46.1% | 28.8% | 18.3% | 6.8% |
| Explainable RL for powertrain control | 7,601 | 27.6% | 26.8% | 32.2% | 13.5% |
| FLAME district-heating diagnosis | 10,242 | 27.4% | 20.7% | 46.1% | 5.8% |
| Interpretable T-wave manifold learning | 14,774 | 25.1% | 25.4% | 45.8% | 3.7% |

The practical pattern is that method plus experiments/results occupy about
55%--70% of an EAAI algorithm/application paper. Long introductions are not
the main route to a complete manuscript.

## Current manuscript

| Section | Approximate words | Share of six main sections |
|---|---:|---:|
| Introduction | 986 | 10.4% |
| Related Work | 1,250 | 13.2% |
| Method | 2,741 | 29.0% |
| Experiments | 2,905 | 30.8% |
| Discussion | 1,375 | 14.6% |
| Conclusion | 189 | 2.0% |
| **Six-section total** | **9,446** | **100%** |

The `detex` count for the complete manuscript excluding references is
approximately 9,971 words. This includes the 209-word abstract, Highlights,
table text, and declarations.

## Structural decision

- Keep Introduction and Related Work near 24% combined.
- Keep Method and Experiments near 60% combined.
- Treat the strict route and high-performance route as separate operating
  points.
- Treat the seed-2028 progressive table as construction evidence, not as a
  three-seed monotonic ablation.
- Do not add prose only to increase length; future expansion should add new
  verified experiments, reproducibility details, or error analysis.
