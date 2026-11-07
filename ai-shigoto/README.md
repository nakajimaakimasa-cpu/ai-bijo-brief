# Threads「AIで仕事を取る」一式

Threads → note → 公式LINE → 個別相談 までの設計と、毎日の投稿をまとめたフォルダです。

| ファイル | 中身 |
|---|---|
| [01_account_design.md](01_account_design.md) | **アカウント設計書**：結論・参考アカウントの実測・海外のAIのプロ比較と採用ルート・ターゲット・プロフィール・投稿の型・導線・3週間の計画・数字 |
| [board.html](board.html) | **投稿ボード**（スマホで開いて、コピー→投稿→「投稿した」） |
| [posts.csv](posts.csv) | 投稿ボードの中身。今使っている「投稿ボード」のシートと同じ列（＋「型」）なので、そのままシートに貼れる |
| [03_note.md](03_note.md) | **note**：ラインナップと値段、無料noteの全文、有料noteの無料部分・目次・特典の中身 |
| [04_line.md](04_line.md) | **公式LINE と 個別相談**：あいさつ・7日間の配信・note購入者の流れ・リッチメニュー・予約・相談の進め方 |
| [05_openchat.md](05_openchat.md) | **オープンチャット**：ノート・ルール・週の流れ・月1の7日間チャレンジ |
| [06_rules.md](06_rules.md) | **規約・法律**：Threads／note／LINE／特定商取引法／景品表示法のチェックリスト |

有料noteの本文（第1〜6章）と特典の章は、売り物なのでこのリポジトリには置いていません（公開されているため）。

## 投稿ボードの更新

`posts.csv` を直したら、リポジトリの一番上で：

```
python3 ai-shigoto/tools/build_board.py
```

本文・続きが500字を超えていたり、鍵が重なっていたりすると止まって教えてくれます。

## 【】の扱い

投稿・note・LINEの文面にある【】は、**事実に合わせて直す所**です（件数・金額・URL・日付など）。
分からない数字は書かずに、言い方を変えてください。盛った数字は出さない、が全体のルールです。

## ローカルで続ける（Mac）

案件の実例・数字はローカルの資料にあるので、仕上げはローカルの Claude Code でやる。

```bash
git clone https://github.com/nakajimaakimasa-cpu/ai-bijo-brief.git
```

```bash
cd ai-bijo-brief && git checkout claude/hopeful-brown-umq34v
```

1. 非公開キット（`ai-shigoto-private.zip`）を `ai-shigoto/private/` に展開する（`.gitignore` 済みなので公開されない）
2. リポジトリの一番上で `claude` を起動し、`ai-shigoto/private/LOCAL_START.md` の「最初に送る指示」を貼る
3. 作業のルールは [CLAUDE.md](CLAUDE.md)
