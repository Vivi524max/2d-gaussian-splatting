set -e
DTU_ROOT=${DTU_ROOT:-$HOME/data/2dgs/DTU}
SCENE=scan105
OUT=output/ablation_stop5000/${SCENE}
mkdir -p output/ablation_stop5000 logs results/ablation_stop5000 results/package/ablation_png
nvidia-smi
TORCH_LIB=$(python -c "import torch, os; print(os.path.join(os.path.dirname(torch.__file__), chr(108)+chr(105)+chr(98)))")
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$TORCH_LIB:$LD_LIBRARY_PATH python train.py -s ${DTU_ROOT}/${SCENE} -m ${OUT} -r 2 --depth_ratio 1 --iterations 10000 --save_iterations 3000 5000 8000 10000 --checkpoint_iterations 3000 5000 8000 10000 --adaptive_opacity_reset --opacity_reset_stop_iter 5000
nvidia-smi
