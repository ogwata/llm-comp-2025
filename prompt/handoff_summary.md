# LLM講義2025 メインコンペ 進捗サマリー（2026/02/08時点）

## 現在の状況

- **ベースライン提出完了**: スコア **0.677113**
- **モデル**: ogwata/baseline-v2（HuggingFace、Public）
- **ベースモデル**: Qwen/Qwen3-4B-Instruct-2507
- **学習方式**: QLoRA (4-bit) + Unsloth、Colab T4

## ベースライン設定（標準コード1のデフォルト）

```
dataset: u-10bei/structured_data_with_cot_dataset_512_v2 (3.65k rows)
lora_r: 64
lora_alpha: 128
learning_rate: 1e-6  ← 最優先の変更対象
epochs: 1
batch_size: 2
gradient_accumulation: 8
max_seq_len: 512
warmup_ratio: 0.1
weight_decay: 0.05
```

## 次のアクション：Phase 1（ハイパーパラメータ最適化）

**実験1**: learning_rate を `2e-4` に変更して再学習 → 推論 → 提出

### 変更箇所（標準コード1の環境変数設定セル）

```python
# 変更する行（27行目付近）
os.environ["SFT_LR"] = "2e-4"  # 元は "1e-6"
```

### HuggingFaceアップロード先

```python
os.environ["HF_REPO_ID"] = "ogwata/exp1-lr2e4"
title_line = "exp1-lr2e4"
```

### 推論（標準コード2）

```python
ADAPTER_ID = "ogwata/exp1-lr2e4"
```

## 実行フロー

1. 標準コード1: learning_rate変更 → 全セル実行（30〜40分）→ HFアップロード
2. 標準コード2: ADAPTER_ID変更 → public_150.jsonアップロード → 全セル実行 → inference.jsonダウンロード
3. Omnicampus: inference.json + HuggingFace URL を提出

## 使用可能なデータセット（10種類）

**u-10beiシリーズ:**
- 1-1: structured_data_with_cot_dataset_512_v2（現在使用中）
- 1-2: structured_data_with_cot_dataset_512_v4
- 1-3: structured_data_with_cot_dataset_512_v5
- 1-4: structured_data_with_cot_dataset_512
- 1-5: structured_data_with_cot_data_v2
- 1-6: structured_data_with_cot_dataset

**daichiraシリーズ:**
- 2-1: structured-3k-mix-sft
- 2-2: structured-5k-mix-sft
- 2-3: structured-hard-sft-4k

## 改善計画（Phase順）

- Phase 1: ハイパーパラメータ最適化（learning_rate最優先）← 今ここ
- Phase 2: データセット変更
- Phase 3: DPO（標準コード3）

## 重要な制約

- 提出回数: 最大50回（計画的に）
- 推論コード（標準コード2）: モデル情報以外の改変禁止、RAG/ToolUse/外部サービス連携禁止
- 学習データ: 運営提供・紹介データのみ使用可、LLMによるデータ合成禁止
- inference.jsonの手動編集禁止
- 締切: 2026/03/02（月）12:00

## アドバンスドコンペ

- 判定タイミング（02/08 17:00）には間に合わなかった可能性あり
- アドバンスドコンペオープン: 02/09 12:00
- エントリー済み

## 関連チャットリンク

- 前チャット: https://claude.ai/chat/a61335e1-f3d7-4650-a665-01094fea4aae
