import argparse, json, math
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from skimage.metrics import structural_similarity as ssim_fn
import lpips

def load_img(path):
    img = Image.open(path).convert("RGB")
    arr = np.asarray(img).astype(np.float32) / 255.0
    return arr

def psnr(pred, gt):
    mse = np.mean((pred - gt) ** 2)
    if mse <= 1e-12:
        return 99.0
    return -10.0 * math.log10(mse)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", required=True)
    parser.add_argument("--method", default="baseline")
    parser.add_argument("--iteration", type=int, default=10000)
    parser.add_argument("--split", default="train")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    root = Path("output") / args.method / args.scene / args.split / f"ours_{args.iteration}"
    render_dir = root / "renders"
    gt_dir = root / "gt"
    files = sorted(render_dir.glob("*.png"))
    if not files:
        raise SystemExit(f"No rendered PNG found in {render_dir}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    loss_fn = lpips.LPIPS(net="vgg").to(device)
    rows = []
    psnrs, ssims, lpipss = [], [], []
    for f in files:
        g = gt_dir / f.name
        if not g.exists():
            continue
        pred = load_img(f)
        gt = load_img(g)
        h = min(pred.shape[0], gt.shape[0])
        w = min(pred.shape[1], gt.shape[1])
        pred = pred[:h, :w, :]
        gt = gt[:h, :w, :]
        p = psnr(pred, gt)
        s = ssim_fn(gt, pred, channel_axis=2, data_range=1.0)
        with torch.no_grad():
            pt = torch.from_numpy(pred).permute(2,0,1).unsqueeze(0).to(device) * 2 - 1
            gt_t = torch.from_numpy(gt).permute(2,0,1).unsqueeze(0).to(device) * 2 - 1
            l = float(loss_fn(pt, gt_t).item())
        psnrs.append(p); ssims.append(s); lpipss.append(l)
        rows.append({"image": f.name, "psnr": p, "ssim": float(s), "lpips": l})
    if not rows:
        raise SystemExit(f"No matched render/gt PNG pairs found in {root}")
    summary = {"method": args.method, "scene": args.scene, "iteration": args.iteration, "split": args.split, "num_images": len(rows), "psnr": float(np.mean(psnrs)), "ssim": float(np.mean(ssims)), "lpips": float(np.mean(lpipss))}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "per_image": rows}, indent=2), encoding="utf-8")
    csv = out.with_suffix(".csv")
    csv.write_text("method,scene,iteration,split,num_images,psnr,ssim,lpips\n{method},{scene},{iteration},{split},{num_images},{psnr:.6f},{ssim:.6f},{lpips:.6f}\n".format(**summary), encoding="utf-8")
    print(summary)
    print(f"saved {out} and {csv}")

if __name__ == "__main__":
    main()
