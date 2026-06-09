#!/usr/bin/env bash
set -e
DTU_ROOT=${DTU_ROOT:-$HOME/data/2dgs/dtu}
SCENE=scan24
OUT=output/baseline/${SCENE}
mkdir -p output/baseline logs results/baseline
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH python train.py -s ${DTU_ROOT}/${SCENE} -m ${OUT} -r 2 --depth_ratio 1 --iterations 15000 --save_iterations 5000 10000 15000 --checkpoint_iterations 15000
