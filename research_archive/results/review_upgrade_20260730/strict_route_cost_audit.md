# Strict-route cost audit — 2026-07-30

## Evidence status

The current archive does not contain the full checkpoint directory needed for a fresh same-process end-to-end batch-1 profile. Therefore this document does not label a component sum as a direct end-to-end measurement.

## Existing component measurements

| Dataset | RDAR detector ms/frame | Stable expert ms/frame | Voting loop ms/frame | Conservative component sum |
|---|---:|---:|---:|---:|
| Astyx | 87.73 | 77.27 | 22.71 | 187.71 |
| TruckScenes | 18.17 | 17.77 | 22.01 | 57.95 |
| V2X-Radar-V | 22.97 | 20.10 | 22.54 | 65.61 |
| K-Radar | 23.90 | 21.33 | 22.85 | 68.08 |

The detector values come from completed evaluation logs; the voting values come from the dedicated overhead report. They use different measurement contexts, so the sums are conservative engineering estimates rather than a claim of direct synchronized end-to-end latency.

## Manuscript decision

- Report the direct voting-loop overhead separately (`~22 ms/frame`).
- Report the component sum only as an upper-bound-style estimate with its provenance.
- Do not claim real-time strict-route deployment until a same-process batch-1 profile is run with both detector checkpoints available.

## Proposal-scaling profile

Using frozen RDAR predictions and excluding one CUDA warm-up frame, the voting-only path scales from approximately 1.5--1.6 ms/frame at 50 proposals to approximately 9.5--10.1 ms/frame at 500 proposals across the four datasets. The 500-proposal runs used about 6.7 MB peak allocated GPU memory for the dense IoU/voting profile. These numbers measure the refinement path only and do not include either detector forward pass.
