
# LLM講義2025 メインコンペ 完全攻略計画

## 現在の進捗状況

### ✅ 完了
- Phase 0: ベースライン確立
- 標準コード1（SFT学習）実行完了
- HuggingFaceアップロード: ogwata/baseline-v2
- Write権限トークン設定完了

### ⬜ 次のタスク
- 標準コード2（推論）実行
- public_150.jsonで推論
- inference.json生成・提出

---

## Phase別実行計画

### Phase 0: ベースライン（完了）
- ✅ 標準コード1実行
- ✅ ogwata/baseline-v2作成

### Phase 1: ハイパーパラメータ最適化（次回）
目標: ベースライン + 10-20%改善

**実験1-1: Learning Rate**
- lr=5e-5, 1e-4, 2e-4を試す
- 固定: dataset=v2, r=64, epochs=1

**実験1-2: LoRA設定**
- r=16, 32, 64を試す
- 期待: r=16が最良

**実験1-3: Epoch調整**
- epochs=1, 2, 3
- 注意: Colab無料版90分制限

### Phase 2: データセット実験
目標: 88% → 91-94%

- u-10bei/v4, v5を試す
- daichira/structured-5k-mix-sft
- MASK_COT設定に注意

### Phase 5: DPO（後半）
- 標準コード3使用
- SFT→DPO推奨
- 期待: +2-5%改善

---

## 重要な設定値

### 必須記入項目（毎回変更）
```python
os.environ["HF_REPO_ID"] = "ogwata/実験ID"
title_line = "実験ID"
```

### デフォルト設定
```python
BASE_MODEL = "Qwen/Qwen3-4B-Instruct-2507"
DATASET = "u-10bei/structured_data_with_cot_dataset_512_v2"
LORA_R = 64
LORA_ALPHA = 128
LEARNING_RATE = "1e-6"
EPOCHS = 1
```

---

## トラブルシューティング

### HuggingFaceアップロードエラー
- Write権限トークン確認
- HF_REPO_IDが"ogwata/xxx"形式か確認

### OOMエラー
- batch_size=2→1
- lora_r=64→16

---

## ファイル管理

### 標準コード
- 標準コード1: SFT学習
- 標準コード2: 推論・提出
- 標準コード3: DPO最適化

### データ
- public_150.json: Google Driveから入手
- inference.json: 提出用

### HuggingFace
- ogwata/baseline-v2: 完了
- ogwata/exp1-1a: 次回以降
