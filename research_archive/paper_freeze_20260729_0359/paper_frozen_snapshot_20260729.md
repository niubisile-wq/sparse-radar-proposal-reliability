# Paper Frozen Snapshot

This snapshot merges the earlier frozen experiment bundle with the three
recently completed parts so the current paper state can be reviewed from one
place.

## Combined frozen state

### Existing freeze

The earlier freeze bundle remains the reference point for the broader paper
story and the established experiment ledger.

### Part 1: protocol freeze

The protocol and ledger layer is frozen through:

- protocol definition
- baseline registry
- corruption specification
- data-license audit
- run ledger

### Part 2: external baseline comparison

The external comparison table is closed for the currently frozen methods and
datasets, with complete seed-level provenance recorded in
`external_baseline_comparison.md` and `.csv`.

### Part 3: corruption / compensation matrix

The corruption matrix is closed.

- 192 total rows
- 48 rows per dataset
- best observed settings are recorded for Astyx, TruckScenes, V2X-Radar-V,
  and K-Radar

### Part 4: hardcase audit substitute

The original manual-label branch is replaced by a deterministic hardcase audit
package.

- no new human labels
- three exported qualitative cases
- candidate-mining table for the broader hardcase surface
- manuscript-ready BEV figures already exported

### Part 5: merged freeze and writing bundle

The freeze bundle now has a single entry point that combines:

- the earlier freeze bundle
- the protocol layer
- the formal external comparison
- the corruption matrix
- the hardcase audit substitute
- the writing-facing indexes and artifacts

## Practical meaning

At this point, the paper-facing experiment package has a stable frozen core:

- the earlier bundle is preserved
- the protocol layer is fixed
- the external baseline comparison is fixed
- the corruption / compensation audit is fixed
- the hardcase audit substitute is fixed
- the merged freeze bundle is fixed

If you reopen this folder later, start from `README.md`, then open this file,
then drill into the linked artifacts in `FREEZE_INDEX.md`.
