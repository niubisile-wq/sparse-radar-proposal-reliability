# Figure and Table Callout Plan

This file defines where each main-text figure or table is first cited and what
the citation paragraph tells the reader to inspect. Blue numbered placeholders
and their callout paragraphs are now integrated into `paper.tex`; each
placeholder will be replaced by approved artwork or audited numerical content.

## Integration rules

1. Cite every figure and table before the float appears.
2. Do not end a paragraph with a bare parenthetical reference.
3. Name the comparison or mechanism the reader should inspect.
4. State the main observation in the same paragraph, but leave detailed
   interpretation to the Results or Discussion.
5. Use `\figref{...}` and `\tabref{...}` consistently.
6. Refer to individual panels as `\figref{...}(a)` rather than asking the
   reader to inspect an undifferentiated multi-panel figure.

## Figure 1: Framework overview

- Proposed label: `fig:framework`
- First citation: Method, immediately after "Baseline detector and framework
  overview" introduces the two operating routes.
- Reader task: distinguish the shared proposal-processing stages from the
  high-performance and strict endpoints.

Proposed callout paragraph:

> \figref{fig:framework} summarizes the complete decision path and should
> be read from left to right. M1 and M2 preserve and recover proposal evidence,
> whereas M3 changes the confidence target used by the accuracy-oriented
> branch. The lower branch is a distinct strict endpoint: it retains
> RDAR-compatible primary proposals and applies expert-consistency gating and
> conservative local voting. The branch point in the figure is important
> because the strict route is not obtained by appending voting to the final
> high-performance configuration.

## Figure 2: Proposal mechanisms

- Proposed label: `fig:proposal-mechanisms`
- First citation: Method, after "Strict consistency refinement" and before
  "Operating routes and selection criteria."
- Reader task: inspect which proposal attributes each module may change and
  which safeguards prevent weak evidence from dominating.

Proposed callout paragraph:

> The proposal-level effects of the four operations are illustrated in
> \figref{fig:proposal-mechanisms}. The reader should compare candidate
> survival after M1, the score-capped residuals introduced by M2, the reordered
> confidence values produced by M3, and the restricted center-and-heading
> update used by strict voting. The illustration also marks the invariants:
> residual proposals cannot enter the voting pool, and voting does not resize
> a primary box.

## Figure 3: Paired performance differences

- Proposed label: `fig:paired-differences`
- First citation: Results, "Main comparison," after the dataset means have
  been introduced.
- Reader task: inspect the sign and magnitude of every matched-seed difference,
  especially the one negative high-performance cell.

Proposed callout paragraph:

> Aggregate means do not show whether an operating route regresses under an
> individual initialization. \figref{fig:paired-differences} therefore
> displays the AP difference from RDAR for each of the 12 matched
> dataset--seed cells. All strict-route markers lie on the positive side of
> zero, whereas the high-performance route contains one negative TruckScenes
> result at seed 2027. The figure should be used to assess consistency; the
> exact AP values and summary statistics are reported separately in
> \tabref{tab:paired-results}.

## Figure 4: Progressive construction analysis

- Proposed label: `fig:progressive-analysis`
- First citation: Results, opening of "Progressive module ablation."
- Reader task: follow the change produced by each successive module and notice
  that this is a seed-2028 construction analysis, not a three-seed factorial
  ablation.

Proposed callout paragraph:

> \figref{fig:progressive-analysis} traces the seed-2028 construction path
> from the PointPillars screen through M1, M2, M3, and the final
> accuracy-oriented adjustment. The reader should compare both the macro
> trajectory and the four dataset-specific trajectories: M1 contributes most
> visibly on Astyx, M2 produces a small incremental change, and M3 supplies the
> largest macro step, driven especially by K-Radar. Because only one seed is
> shown, this figure explains module behavior but does not establish
> three-seed monotonicity.

## Figure 5: Diagnostic and boundary analyses

- Proposed label: `fig:diagnostics`
- Panels: (a) ECE, (b) point dropout, (c) voting-threshold response surface,
  (d) no-regression region.
- First citation: Results, opening of "Calibration and diagnostic behavior."
- Repeated citations: "Robustness and corruption tests" cites panel (b);
  "Voting-threshold sensitivity" cites panels (c) and (d).
- Reader task: separate calibration, average corruption robustness, and
  parameter-region consistency from the main AP claim.

Proposed first callout paragraph:

> The auxiliary diagnostics are collected in \figref{fig:diagnostics} but
> answer different questions. Panel (a) compares ECE and shows that the two
> quality-aware routes improve confidence calibration relative to RDAR,
> whereas strict voting is not supported by the same calibration claim. Panels
> (b)--(d) are addressed in the subsequent robustness and sensitivity
> subsections and should not be interpreted as additional samples in the
> formal 12-cell comparison.

Proposed robustness callout:

> \figref{fig:diagnostics}(b) reports the macro response to deterministic
> point dropout. The high-performance route retains an average advantage at
> each tested dropout level, but the reader should note the single
> TruckScenes failure at 30\% dropout. The panel therefore supports
> average-positive corruption behavior rather than a no-regression claim.

Proposed sensitivity callout:

> The threshold response surface in \figref{fig:diagnostics}(c) shows how
> macro AP changes with voting IoU and vote strength, while
> \figref{fig:diagnostics}(d) marks how many of the 12 paired cells remain
> positive. The selected setting lies inside a region containing more than one
> 12-of-12 configuration; stronger voting can increase the macro result while
> sacrificing the strict criterion.

## Figure 6: Qualitative BEV cases

- Proposed label: `fig:qualitative-cases`
- First citation: Results, opening of "Qualitative cases."
- Reader task: inspect one example for recovery, one for quality-based
  reranking, one for voting across the IoU threshold, and one failure case.

Proposed callout paragraph:

> \figref{fig:qualitative-cases} provides mechanism-oriented BEV examples
> rather than a representative performance sample. The first case shows a
> candidate retained or recovered by M1--M2, the second shows a ranking change
> after quality-aligned training, and the third shows strict voting moving a
> nearly correct center across the 0.50-IoU match boundary. The final case is a
> failure under sparse or conflicting evidence and bounds the visual claim.

## Table 2: Datasets and evaluation protocol

- Proposed label: `tab:datasets`
- First citation: Experimental Setup, after all four datasets are named.
- Reader task: verify dataset scope, split, sensor representation, evaluation
  range, class mapping, seeds, and metric.

Proposed callout paragraph:

> \tabref{tab:datasets} defines the scope of the cross-dataset comparison.
> The reader should use it to verify the frozen data partitions, sensor inputs,
> car-class mapping, spatial evaluation ranges, and three training seeds.
> These quantities differ across datasets, whereas AP$_{R40}$, the 0.50 3D-IoU
> match threshold, and the paired-seed comparison rule remain common.

## Table 1: Route and configuration definitions

- Proposed label: `tab:routes`
- First citation: Method, "Operating routes and selection criteria."
- Reader task: distinguish shared modules, route-specific settings, and the
  criterion used to select each endpoint.

Proposed callout paragraph:

> \tabref{tab:routes} lists the exact operations enabled by each reported
> configuration. It should be consulted when comparing the quality-aligned,
> high-performance, and strict endpoints because they optimize different
> objectives and are not successive aliases for one model. In particular, the
> table separates relaxed positive assignment in the high-performance route
> from expert gating and local voting in the strict route.

## Table 3: Main three-seed comparison

- Proposed label: `tab:main-results`
- First citation: Results, first paragraph of "Main comparison."
- Reader task: compare dataset mean and standard deviation, macro AP, and the
  improvement from RDAR.

Proposed callout paragraph:

> The formal three-seed results are summarized in
> \tabref{tab:main-results}. Dataset means and standard deviations quantify
> average performance and between-seed variation, while the unweighted macro
> column gives each dataset equal influence. The high-performance route
> provides the largest macro gain, whereas the strict route is the only
> reported endpoint selected by the paired no-regression criterion.

## Table 4: Complete paired reliability results

- Proposed label: `tab:paired-results`
- First citation: Results, opening of "Paired reliability across datasets and
  seeds."
- Reader task: audit each RDAR-to-route difference and the aggregate paired
  statistics.

Proposed callout paragraph:

> \tabref{tab:paired-results} expands the strict-route mean into all 12
> matched comparisons. The sign of every row, rather than only the average
> difference, determines whether Eq.~\eqref{eq:strict-gate} is satisfied. The
> table also reports the mean, median, minimum difference, bootstrap interval,
> and exact sign test so that effect magnitude and finite-sample consistency
> remain distinguishable.

## Table 5: Numerical progressive ablation

- Proposed label: `tab:progressive-ablation`
- First citation: Results, after Fig. 4 is introduced.
- Reader task: retrieve exact dataset and macro AP values underlying the
  trajectories in Fig. 4.

Proposed callout paragraph:

> Exact values for the trajectories in
> \figref{fig:progressive-analysis} are given in
> \tabref{tab:progressive-ablation}. The incremental columns should be read
> relative to the immediately preceding configuration, not only relative to
> the starting screen. This distinction exposes the small contribution of M2
> and the much larger M3 step without promoting the single-seed analysis to a
> formal multi-seed claim.

## Table 6: Accuracy and computational cost

- Proposed label: `tab:efficiency`
- First citation: Results, opening of "Efficiency."
- Reader task: compare parameter count, detector latency, proposal-refinement
  latency, total latency, and macro AP.

Proposed callout paragraph:

> \tabref{tab:efficiency} compares accuracy and computational cost under the
> same profiling protocol. The quality-aware routes retain the RDAR parameter
> count because M3 changes supervision rather than network width, whereas the
> strict route adds no trainable voting parameters but incurs a measurable
> proposal-refinement latency. The separate timing columns prevent
> ``parameter-free'' from being misread as ``zero-cost.''

## Recommended float order

1. Figure 1: framework overview
2. Figure 2: proposal mechanisms
3. Table 1: route definitions
4. Table 2: datasets and protocol
5. Table 3: main comparison
6. Figure 3: paired differences
7. Table 4: paired reliability
8. Figure 4: progressive analysis
9. Table 5: progressive ablation
10. Figure 5: diagnostics and boundaries
11. Figure 6: qualitative cases
12. Table 6: efficiency
