from pathlib import Path
import re, csv, datetime

def parse_train_time(log_path):
    p=Path(log_path)
    if not p.exists(): return "NA"
    text=p.read_text(errors="ignore")
    if "Training complete" not in text: return "NA"
    ts=re.findall(r"\[(\d{2}/\d{2} \d{2}:\d{2}:\d{2})\]", text)
    if len(ts)<2: return "NA"
    a=datetime.datetime.strptime(ts[0], "%d/%m %H:%M:%S")
    b=datetime.datetime.strptime(ts[-1], "%d/%m %H:%M:%S")
    sec=(b-a).total_seconds()
    if sec<0: sec+=24*3600
    if sec<60: return "NA"
    return int(sec)

def parse_vram_snapshot(log_path):
    p=Path(log_path)
    if not p.exists(): return "NA"
    text=p.read_text(errors="ignore")
    vals=[int(x) for x in re.findall(r"\|\s+\d+%\s+\d+C.*?\|\s+(\d+)MiB\s*/", text)]
    return max(vals) if vals else "NA"

def dir_size_mb(path):
    p=Path(path)
    if not p.exists(): return "NA"
    return round(sum(f.stat().st_size for f in p.rglob("*") if f.is_file())/1024/1024,2)

def render_fps_list(log_path):
    p=Path(log_path)
    if not p.exists(): return []
    text=p.read_text(errors="ignore")
    return [float(x) for x in re.findall(r"export images:.*?,\s*([0-9.]+)it/s\]", text)]

fps_baseline=render_fps_list("logs/render_baseline.log")
fps_stop_scan24=render_fps_list("logs/render_ablation_stop5000_scan24.log")
fps_stop_scan105=render_fps_list("logs/render_ablation_stop5000.log")
fps_geo=render_fps_list("logs/render_improved_geo.log")
items=[
("baseline","scan24","logs/baseline_scan24_10000.log","output/baseline/scan24",fps_baseline[0] if len(fps_baseline)>0 else "NA"),
("baseline","scan105","logs/baseline_scan105_10000.log","output/baseline/scan105",fps_baseline[1] if len(fps_baseline)>1 else "NA"),
("opacity_stop5000","scan24","logs/ablation_scan24_stop5000_10000.log","output/ablation_stop5000/scan24",fps_stop_scan24[0] if len(fps_stop_scan24)>0 else "NA"),
("opacity_stop5000","scan105","logs/ablation_scan105_stop5000_10000.log","output/ablation_stop5000/scan105",fps_stop_scan105[0] if len(fps_stop_scan105)>0 else "NA"),
("progressive_geo","scan24","logs/improved_geo_scan24_10000.log","output/improved_geo/scan24",fps_geo[0] if len(fps_geo)>0 else "NA"),
("progressive_geo","scan105","logs/improved_geo_scan105_10000.log","output/improved_geo/scan105",fps_geo[1] if len(fps_geo)>1 else "NA")]
out=Path("results/package/metrics/efficiency_summary.csv")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="") as f:
    w=csv.writer(f)
    w.writerow(["method","scene","train_time_sec","train_time_min","nvidia_smi_snapshot_max_mib","output_size_mb","render_fps_it_per_sec"])
    for method,scene,train_log,out_dir,fps in items:
        sec=parse_train_time(train_log)
        w.writerow([method,scene,sec,round(sec/60,2) if isinstance(sec,int) else "NA",parse_vram_snapshot(train_log),dir_size_mb(out_dir),fps])
print(out.read_text())
