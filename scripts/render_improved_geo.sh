set -e
DTU_ROOT=${DTU_ROOT:-$HOME/data/2dgs/DTU}
mkdir -p logs results/package/geo_png
TORCH_LIB=$(python -c "import torch, os; print(os.path.join(os.path.dirname(torch.__file__), chr(108)+chr(105)+chr(98)))")
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$TORCH_LIB:$LD_LIBRARY_PATH python render.py -s ${DTU_ROOT}/scan24 -m output/improved_geo/scan24 -r 2 --depth_ratio 1 --iteration 10000
CUDA_HOME=$CONDA_PREFIX PATH=$CONDA_PREFIX/bin:$PATH LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$TORCH_LIB:$LD_LIBRARY_PATH python render.py -s ${DTU_ROOT}/scan105 -m output/improved_geo/scan105 -r 2 --depth_ratio 1 --iteration 10000
