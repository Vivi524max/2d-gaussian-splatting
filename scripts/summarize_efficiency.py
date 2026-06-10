from pathlib import Path
import re, csv, datetime

def parse_train_time(log_path):
    p=Path(log_path)
    if not p.exists(): return ""
    text=p.read_text(errors="ignore")
    ts=re.findall(r"\[(\d{2}/\d{2} \d{2}:\d{2}:\d{2})\]", text)
    if len(ts)<2: return ""
    a=datetime.datetime.strptime(ts[0], "%d/%m %H:%M:%S")
    b=datetime.datetime.strptime(ts[-1], "%d/%m %H:%M:%S")
    sec=(b-a).total_seconds()
    if sec<0: sec+=24*3600
    return int(sec)

def parse_vram_snapshot(log_path):
    p=Path(log_path)
    if not p.exists(): return ""
    text=p.read_text(errors="ignore")
    vals=[int(x) for x in re.findall(r"\|\s+\d+%\s+\d+C.*?\|\s+(\d+)MiB\s*/", text)]
    return max(vals) if vals else ""

def dir_size_mb(path):
    p=Path(path)
    if not p.exists(): return ""
    return round(sum(f.stat().st_size for f in p.rglob("*") if f.is_file())/1024/1024,2)

def parse_render_fps(log_path, tag):
    p=Path(log_path)
    if not p.exists(): return ""
    lines=p.read_text(errors="ignore").splitlines()
    active=False
    for line in lines:
        if tag in line: active=True
        elif active and "export images:" in line:
            m=re.search(r",\s*([0-9.]+)it/s\]", line)
            return float(m.group(1)) if m else ""
    return ""

items=[
("baseline","scan24","logs/baseline_scan24_10000.log","output/baseline/scan24","logs/render_baseline.log","Rendering output/baseline/scan24"),
("baseline","scan105","logs/baseline_scan105_10000.log","output/baseline/scan105","logs/render_baseline.log","Rendering output/baseline/scan105"),
("opacity_stop5000","scan24","logs/ablation_scan24_stop5000_10000.log","output/ablation_stop5000/scan24","logs/render_ablation_stop5000_scan24.log","Rendering output/ablation_stop5000/scan24"),
("opacity_stop5000","scan105","logs/ablation_scan105_stop5000_10000.log","output/ablation_stop5000/scan105","logs/render_ablation_stop5000.log","Rendering output/ablation_stop5000/scan105"),
("progressive_geo","scan24","logs/improved_geo_scan24_10000.log","output/improved_geo/scan24","logs/render_improved_geo.log","Rendering output/improved_geo/scan24"),
("progressive_geo","scan105","logs/improved_geo_scan105_10000.log","output/improved_geo/scan105","logs/render_improved_geo.log","Rendering output/improved_geo/scan105")]

out=Path("results/package/metrics/efficiency_summary.csv")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="") as f:
    w=csv.writer(f)
    w.writerow(["method","scene","train_time_sec","train_time_min","nvidia_smi_snapshot_max_mib","output_size_mb","render_fps_it_per_sec"])
    for method,scene,train_log,out_dir,render_log,tag in items:
        sec=parse_train_time(train_log)
        w.writerow([method,scene,sec,round(sec/60,2) if sec!="" else "",parse_vram_snapshot(train_log),dir_size_mb(out_dir),parse_render_fps(render_log,tag)])
print(out.read_text())
