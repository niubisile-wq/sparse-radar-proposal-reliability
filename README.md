# Reliability-Oriented Proposal Refinement for Sparse Radar-Based 3D Object Detection

This repository contains the reproducibility materials for the manuscript
“Reliability-Oriented Proposal Refinement for Sparse Radar-Based Three-Dimensional
Object Detection” by Zixuan Liu and Wei Xiong.

## Contents

- `research_archive/paper_eaai_latex/`: manuscript LaTeX source, references,
  figures, compiled PDFs, and submission-readiness materials.
- `research_archive/`: experiment configurations, evaluation scripts, figure
  generation scripts, result summaries, protocol notes, and frozen-analysis
  documentation.

The formal study compares radar-only proposal refinement across Astyx,
MAN TruckScenes, V2X-Radar-V, and K-Radar with three training seeds. The paper
reports both a high-performance route and a strict paired-reliability route.

## Reproducibility scope

The repository contains source code, configuration files, derived summaries,
and manuscript materials. Original datasets, downloaded checkpoints, raw
experiment artifacts, large TIFF assets, and private infrastructure scripts are
not included. Dataset access remains subject to the original providers’ terms.

The manuscript’s current data-availability statement is therefore:

> Astyx, MAN TruckScenes, V2X-Radar-V, and K-Radar are available from their
> original providers subject to their respective access and licence terms.
> Derived experimental configurations, result summaries, manuscript sources,
> and reproducibility materials supporting the findings are publicly available
> in this repository and archived at Zenodo. Raw datasets and model checkpoints
> are not redistributed.

The latest review-strengthening audit is in
`research_archive/results/review_upgrade_20260730/`. It includes fixed
Soft-NMS, weighted-box-fusion, and standard box-voting controls, a
training-only leave-one-dataset-out threshold audit, dataset-clustered
bootstrap statistics, and GPU voting-runtime scaling measurements.

## Citation

Please cite the accompanying manuscript when using these materials. The
repository is released as `v1.0.0` and archived at Zenodo:
[10.5281/zenodo.21696782](https://doi.org/10.5281/zenodo.21696782).

## Contact

Corresponding author: Wei Xiong, xw@mail.hbut.edu.cn
