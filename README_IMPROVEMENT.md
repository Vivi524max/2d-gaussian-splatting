# README_IMPROVEMENT

## Project

This repository is forked from the official implementation of 2D Gaussian Splatting for Geometrically Accurate Radiance Fields.

## Branch

All course project modifications are implemented in the improvement branch.

## Environment

Hardware: NVIDIA RTX 3080Ti 12GB VRAM. OS: Ubuntu 20.04. Conda environment: surfel_splatting. Python, CUDA, PyTorch and dependency versions are recorded in logs/env_info.txt.

## Dataset

The experiments use DTU scan24 and DTU scan105.

## Baseline Commands

Train scan24 baseline: bash scripts/run_baseline_scan24.sh 2>&1 | tee logs/baseline_scan24_15000.log

Train scan105 baseline: bash scripts/run_baseline_scan105.sh 2>&1 | tee logs/baseline_scan105_15000.log

## Improvement Commands

Train scan24 improvement: bash scripts/run_improvement_scan24.sh 2>&1 | tee logs/improvement_scan24_15000.log

Train scan105 improvement: bash scripts/run_improvement_scan105.sh 2>&1 | tee logs/improvement_scan105_15000.log

## Logs

Environment log: logs/env_info.txt

Build logs: logs/build_diff_surfel.log and logs/build_simple_knn.log

Training logs are stored in logs/.

## Results

Rendered PNG results are stored in results/baseline and results/improvement.

Raw metrics are stored as CSV or JSON files in results/.

## Planned Improvement

The final method-level improvement will modify the original 2DGS optimization process, such as adding a geometry-aware regularization term or changing the densification/pruning behavior. The exact implementation will be documented after baseline reproduction.

## AI Usage Statement

AI tools were used for environment setup guidance, debugging assistance, command organization, and report writing support. All code changes and experimental results were checked and executed by the author.


## Reproduction Commands

Baseline scan24: bash scripts/run_baseline_scan24.sh 2>&1 | tee logs/baseline_scan24_15000.log

Baseline scan105: bash scripts/run_baseline_scan105.sh 2>&1 | tee logs/baseline_scan105_15000.log

Render baseline: bash scripts/render_baseline.sh 2>&1 | tee logs/render_baseline.log

Evaluate baseline: bash scripts/eval_baseline.sh 2>&1 | tee logs/eval_baseline.log

## Improvement Commands

Improvement scan24: bash scripts/run_improvement_scan24.sh 2>&1 | tee logs/improvement_scan24_15000.log

Improvement scan105: bash scripts/run_improvement_scan105.sh 2>&1 | tee logs/improvement_scan105_15000.log

## Logs and Results

Environment log: logs/env_info.txt

Baseline logs: logs/baseline_scan24_15000.log and logs/baseline_scan105_15000.log

Rendered PNG results and raw metrics for the final ZIP package will be stored under results/.
