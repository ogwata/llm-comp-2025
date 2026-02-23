# 松尾研LLM開発コンペ2025 メインコンペ

松尾研LLM講義2025の最終課題「StructEval-T ベンチマーク」への取り組み記録です。

## コンペ概要

- **ベンチマーク:** StructEval-T（構造化データ生成能力の評価）
- **ベースモデル:** Qwen2.5-7B
- **タスク:** JSON/YAML/TOML/XML/CSV の構造化出力を正確に生成する
- **期間:** 2026/02/02 〜 2026/03/02
- **提出上限:** 50回

## 現在の成績

| カテゴリ | 実験ID | スコア | 設定 |
|:-------:|:------:|:-----:|:-----|
| SFT単体最高 | exp2 | **0.751** | v2, LR=5e-5 |
| SFT+DPO最高 | exp11 | **0.742** | v2→dpo-qwen-cot, DPO LR=5e-7, β=0.2 |

## リポジトリ構成

```
├── docs/                    # 実験記録・分析
│   ├── 実験結果一覧_exp1-19.md
│   ├── レトロスペクション_exp1-19.md
│   └── 判断基準.md
├── notebooks/               # Colab用ノートブック
├── scripts/                 # ユーティリティスクリプト
├── configs/                 # 実験設定ファイル
├── results/                 # 推論ログ（inference.jsonは除外）
│   └── inference_logs/
├── CLAUDE.md                # Claude Code用コンテキスト
└── .gitignore
```

## 手法

### SFT (Supervised Fine-Tuning)
- データセット: `u-10bei/cot_512_v2`（約3,650件）
- 最適LR: 5e-5（1e-4でも同等）
- Epoch: 1（2 epochでは過学習）

### DPO (Direct Preference Optimization)
- ベースモデル: exp2のSFTモデル
- DPOデータセット: `u-10bei/dpo-dataset-qwen-cot`
- 最適DPO LR: 5e-7, β=0.2

## 分析ツール

- [StructEval Analyzer](https://huggingface.co/spaces/ogwata/structeval-analyz) — 推論結果の分析用Webアプリ（HuggingFace Spaces）
- [分析ノートブック](https://colab.research.google.com/drive/1b5KB_5wnTEqGZJzMW1yhPsYeCnpiclqL#scrollTo=SFd6J4YGZGt4) — Colab上の詳細分析用ノートブック

## HuggingFace

モデルは [ogwata](https://huggingface.co/ogwata) で公開しています。

## 注意

- `public_150.json`（評価データ）はリポジトリに含めていません
- `inference.json`（推論結果）はリポジトリに含めていません
- HuggingFaceトークンはリポジトリに含めていません
