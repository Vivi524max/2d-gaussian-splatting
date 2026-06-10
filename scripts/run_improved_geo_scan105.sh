set -e
DTU_ROOT=${DTU_ROOT:-$HOME/data/2dgs/DTU}
SCENE=scan105
OUT=output/improved_geo/${SCENE}
mkdir -p output/improved_geo logs results/improved_geo results/package/geo_png
nvidia-smi
TORCH_LIB=$(python -c "import torch, os; print(os.path.join(os.path.dirname(torch.__file__), chr(108)+chr(105)+chr(98)))")
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$TORCH_LIB:$LD_LIBRARY_PATH python train.py -s ${DTU_ROOT}/${SCENE} -m ${OUT} -r 2 --depth_ratio 1 --iterations 10000 --save_iterations 3000 5000 8000 10000 --checkpoint_iterations 3000 5000 8000 10000 --progressive_geo_reg --dist_ramp_start 3000 --normal_ramp_start 7000 --geo_ramp_length 2000
nvidia-smi
