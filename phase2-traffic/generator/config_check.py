import yaml
from pathlib import Path

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def index_data_sources(ds_cfg):
    srcs = {}
    for item in ds_cfg.get("data_sources", []):
        srcs[item["id"]] = item
    return srcs

def validate_traffic_cfg(traffic_cfg, data_sources):
    problems = []
    for profile in traffic_cfg.get("traffic_profiles", []):
      name = profile.get("name", "<noname>")
      src_id = profile.get("target_source_id")
      if src_id not in data_sources:
          problems.append(f"profile '{name}': target_source_id '{src_id}' not found in data-sources.yaml")
      # 检查模式
      if profile.get("pattern") not in ("constant", "burst", "ramp", "trace"):
          problems.append(f"profile '{name}': unsupported pattern '{profile.get('pattern')}'")
      # 合理性检查
      if profile.get("tps", 0) <= 0:
          problems.append(f"profile '{name}': tps must be > 0")
      if profile.get("duration_sec", 0) <= 0:
          problems.append(f"profile '{name}': duration_sec must be > 0")
    return problems

if __name__ == "__main__":
    base = Path("ai-shared-sequencer/phase2-traffic/config")
    ds_cfg = load_yaml(base / "data-sources.yaml")
    traffic_cfg = load_yaml(base / "traffic.yaml")

    data_sources = index_data_sources(ds_cfg)
    problems = validate_traffic_cfg(traffic_cfg, data_sources)

    if problems:
        print("config check failed:")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)
    else:
        print("config check ok.")
