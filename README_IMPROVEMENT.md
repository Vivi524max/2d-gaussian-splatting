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

Train scan24 baseline: bash scripts/run_baseline_scan24.sh 2>&1 | tee logs/baseline_scan24_10000.log

Train scan105 baseline: bash scripts/run_baseline_scan105.sh 2>&1 | tee logs/baseline_scan105_10000.log

## Improvement Commands

Train scan24 improvement: bash scripts/run_improvement_scan24.sh 2>&1 | tee logs/improvement_scan24_10000.log

Train scan105 improvement: bash scripts/run_improvement_scan105.sh 2>&1 | tee logs/improvement_scan105_10000.log

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

Baseline scan24: bash scripts/run_baseline_scan24.sh 2>&1 | tee logs/baseline_scan24_10000.log

Baseline scan105: bash scripts/run_baseline_scan105.sh 2>&1 | tee logs/baseline_scan105_10000.log

Render baseline: bash scripts/render_baseline.sh 2>&1 | tee logs/render_baseline.log

Evaluate baseline: bash scripts/eval_baseline.sh 2>&1 | tee logs/eval_baseline.log

## Improvement Commands

Improvement scan24: bash scripts/run_improvement_scan24.sh 2>&1 | tee logs/improvement_scan24_10000.log

Improvement scan105: bash scripts/run_improvement_scan105.sh 2>&1 | tee logs/improvement_scan105_10000.log

## Logs and Results

Environment log: logs/env_info.txt

Baseline logs: logs/baseline_scan24_10000.log and logs/baseline_scan105_10000.log

Rendered PNG results and raw metrics for the final ZIP package will be stored under results/.


## Baseline Iteration Setting

For the one-day course experiment schedule, baseline reproduction uses 10000 iterations with saved checkpoints at 3000, 5000, 8000, and 10000 iterations. The same setting will be used for the improved version to ensure fair comparison.

## Improvement Method: Late-stage Opacity Reset Suppression



The baseline 2DGS training periodically resets Gaussian opacity during densification. This is useful in the early stage, but repeated opacity reset in the late stage may disturb already stable Gaussian opacity, color, and geometry. Therefore, this improvement keeps the original opacity reset strategy in the early stage and disables opacity reset after 7000 iterations.



Improved training command for scan24:

python train.py -s $HOME/data/2dgs/DTU/scan24 -m output/improved/scan24 -r 2 --depth_ratio 1 --iterations 10000 --save_iterations 3000 5000 8000 10000 --checkpoint_iterations 3000 5000 8000 10000 --adaptive_opacity_reset --opacity_reset_stop_iter 7000



Improved training command for scan105:

python train.py -s $HOME/data/2dgs/DTU/scan105 -m output/improved/scan105 -r 2 --depth_ratio 1 --iterations 10000 --save_iterations 3000 5000 8000 10000 --checkpoint_iterations 3000 5000 8000 10000 --adaptive_opacity_reset --opacity_reset_stop_iter 7000


## Experimental Results



All experiments use DTU scan24 and scan105 with 10000 training iterations. Metrics are computed on the train split using rendered images and ground-truth images under `train/ours_10000`.



| Method | Scene | PSNR | SSIM | LPIPS |

|---|---|---:|---:|---:|

| Baseline | scan24 | 32.289862 | 0.941775 | 0.131309 |

| Improved | scan24 | 32.261173 | 0.942483 | 0.128960 |

| Baseline | scan105 | 33.732391 | 0.916614 | 0.278894 |

| Improved | scan105 | 33.926934 | 0.918174 | 0.276408 |



The improved late-stage opacity reset suppression strategy slightly improves SSIM and LPIPS on both scenes. PSNR improves on scan105 but slightly decreases on scan24, indicating that the method improves overall perceptual and structural stability but is still scene-dependent.



## Final Ablation Result

The opacity reset stop iteration was further tested on DTU scan105 and scan24. Compared with the original stop_iter=7000 setting, stop_iter=5000 achieved better results. Therefore, the final improved method uses --adaptive_opacity_reset --opacity_reset_stop_iter 5000.

| Method | Scene | PSNR | SSIM | LPIPS |
|---|---|---:|---:|---:|
| Baseline | scan24 | 32.289862 | 0.941775 | 0.131309 |
| Final stop5000 | scan24 | 32.664114 | 0.944202 | 0.127627 |
| Baseline | scan105 | 33.732391 | 0.916614 | 0.278894 |
| Final stop5000 | scan105 | 34.053622 | 0.919169 | 0.274352 |

The final stop5000 strategy improves PSNR and SSIM on both scenes and reduces LPIPS on both scenes, showing that earlier suppression of opacity reset can reduce late-stage disturbance and improve rendering stability.


## Improvement 2: Progressive Geometry Regularization

The second identified limitation is that geometry regularization terms are activated by hard iteration thresholds. This may introduce an abrupt optimization objective change. To test this limitation, a progressive ramp-up strategy was implemented for distortion and normal regularization. Distortion regularization is gradually increased from iteration 3000, and normal regularization is gradually increased from iteration 7000.

| Method | Scene | PSNR | SSIM | LPIPS |
|---|---|---:|---:|---:|
| Baseline | scan24 | 32.289862 | 0.941775 | 0.131309 |
| Progressive Geo | scan24 | 32.334978 | 0.941994 | 0.130860 |
| Baseline | scan105 | 33.732391 | 0.916614 | 0.278894 |
| Progressive Geo | scan105 | 33.640359 | 0.916722 | 0.280186 |

The hypothesis is only partially supported. The method slightly improves all metrics on scan24, but on scan105 it decreases PSNR and worsens LPIPS while only slightly improving SSIM. This suggests that progressive geometry regularization is scene-dependent and may weaken late-stage geometric constraints when the training budget is limited to 10000 iterations.
