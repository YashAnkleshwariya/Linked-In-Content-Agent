import os, json, time, pathlib

ROOT = pathlib.Path(__file__).parent
OUT_DIR = ROOT / "out"
OUT_DIR.mkdir(exist_ok=True)

def save_json(data, name):
    fp = OUT_DIR / f"{int(time.time())}_{name}.json"
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(fp)

def save_txt(text, name):
    fp = OUT_DIR / f"{int(time.time())}_{name}.txt"
    fp.write_text(text, encoding="utf-8")
    return str(fp)
