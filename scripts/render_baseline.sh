#!/usr/bin/env bash
set -e
DTU_ROOT=${DTU_ROOT:-$HOME/data/2dgs/dtu}
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH python render.py -s ${DTU_ROOT}/scan24 -m output/baseline/scan24 -r 2 --depth_ratio 1
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH python render.py -s ${DTU_ROOT}/scan105 -m output/baseline/scan105 -r 2 --depth_ratio 1
