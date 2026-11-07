#!/usr/bin/env python3
"""posts.csv から投稿ボード（board.html）を作る。

使い方（リポジトリの一番上で）:
    python3 ai-shigoto/tools/build_board.py
    python3 ai-shigoto/tools/build_board.py --fragment /tmp/board_artifact.html   # Claude のページ用（<html> なし）

- posts.csv の列は Google スプレッドシートの「投稿ボード」と同じ
  （順番・区分・いつ・題・本文・続き・メモ・タグ・完了・完了した日時・画像・鍵）＋ 型
- 本文・続きが 500 字を超えていたら止める（Threads の上限）
- 鍵は英数字と _ - . ~ : @ + だけ（記録の保存先の決まり）
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "board_src.html"
CSV_PATH = ROOT / "posts.csv"
OUT = ROOT / "board.html"

COLUMNS = ["順番", "区分", "いつ", "題", "本文", "続き", "メモ", "タグ", "完了", "完了した日時", "画像", "鍵", "型"]
KEY_RE = re.compile(r"^[A-Za-z0-9_\-.~:@+]+$")
LIMIT = 500

PAGE_HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""


def load_rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"posts.csv に列がありません: {missing}")
        rows = []
        for r in reader:
            if not (r.get("題") or r.get("本文")):
                continue
            rows.append({c: (r.get(c) or "").replace("\r\n", "\n") for c in COLUMNS})
    return rows


def check(rows):
    errors, keys = [], set()
    for r in rows:
        k = r["鍵"]
        if not KEY_RE.match(k):
            errors.append(f"鍵に使えない文字があります: {k!r}")
        if k in keys:
            errors.append(f"鍵が重複しています: {k}")
        keys.add(k)
        if r["区分"] == "設定":
            continue
        for col in ("本文", "続き"):
            n = len(r[col])
            if n > LIMIT:
                errors.append(f"{k} の{col}が {n} 字です（{LIMIT} 字まで）")
    return errors


def build(rows, fragment_path=None):
    src = SRC.read_text(encoding="utf-8")
    data = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    meta = json.dumps({"account": "Threads｜AIで仕事を取る"}, ensure_ascii=False)
    page = re.sub(r"/\*DATA\*/.*?/\*END\*/", lambda m: "/*DATA*/" + data + "/*END*/", src, count=1, flags=re.S)
    page = re.sub(r"/\*META\*/.*?/\*END\*/", lambda m: "/*META*/" + meta + "/*END*/", page, count=1, flags=re.S)
    if fragment_path:
        Path(fragment_path).write_text(page, encoding="utf-8")
    head, sep, body = page.partition('<header class="bar">')
    if not sep:
        sys.exit("board_src.html に <header class=\"bar\"> が見つかりません")
    full = PAGE_HEAD + head.strip() + "\n</head>\n<body>\n" + sep + body.rstrip() + "\n</body>\n</html>\n"
    OUT.write_text(full, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fragment", help="<html> を付けない版も書き出す先（Claude のページ用）")
    args = ap.parse_args()
    rows = load_rows()
    errors = check(rows)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    build(rows, args.fragment)
    posts = [r for r in rows if r["区分"] != "設定"]
    days = sorted({m.group(1) for r in posts for m in [re.search(r"(\d+)日目", r["いつ"])] if m}, key=int)
    print(f"OK: 設定 {len(rows) - len(posts)} 行 / 投稿 {len(posts)} 本 / {len(days)} 日分 → {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
