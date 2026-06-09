set -e
echo "========== Date =========="
date
echo "========== OS =========="
lsb_release -a || true
echo "========== GPU =========="
nvidia-smi || true
echo "========== CUDA =========="
nvcc --version || true
echo "========== Python =========="
which python
python --version
echo "========== PyTorch =========="
python -c "import torch; print(\"torch:\", torch.__version__); print(\"cuda available:\", torch.cuda.is_available()); print(\"torch cuda:\", torch.version.cuda); print(\"gpu:\", torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\")"
echo "========== 2DGS Extensions =========="
python -c "from diff_surfel_rasterization import GaussianRasterizationSettings, GaussianRasterizer; from simple_knn._C import distCUDA2; print(\"diff_surfel_rasterization ok\"); print(\"simple_knn ok\")"
echo "========== Git =========="
git branch || true
git remote -v || true
git log --oneline -5 || true
echo "========== Pip List =========="
pip list
