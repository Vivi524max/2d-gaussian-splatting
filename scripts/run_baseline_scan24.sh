set -e
DTU_ROOT=${DTU_ROOT:-$HOME/data/2dgs/DTU}
SCENE=scan24
OUT=output/baseline/${SCENE}
mkdir -p output/baseline logs results/baseline
nvidia-smi
TORCH_LIB=$(python -c "import torch, os; print(os.path.join(os.path.dirname(torch.__file__), 'lib'))") CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$TORCH_LIB:$LD_LIBRARY_PATH python train.py -s ${DTU_ROOT}/${SCENE} -m ${OUT} -r 2 --depth_ratio 1 --iterations 10000 --save_iterations 3000 5000 8000 10000 --checkpoint_iterations 3000 5000 8000 10000
nvidia-smi
