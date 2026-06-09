#!/usr/bin/env bash
set -e
mkdir -p logs results/baseline
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH python metrics.py -m output/baseline/scan24 2>&1 | tee logs/metrics_baseline_scan24.log
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH python metrics.py -m output/baseline/scan105 2>&1 | tee logs/metrics_baseline_scan105.log
