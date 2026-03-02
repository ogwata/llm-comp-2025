# 標準コード3 修正手順（exp19: 強化版DPO）

## 概要
- ベースモデル: exp2のマージ済みモデル（v2, SFT LR=5e-5）
- DPOデータ: 強化版（オリジナル + anti_tool_call + anti_markdown + anti_porous）
- DPOパラメータ: LR=5e-7, Beta=0.2（exp11の最適値）

## 手順

### 手順0: 強化版DPOデータの生成（新規セル）
標準コード3の最初のセルの前に、新しいセルを追加して以下を実行：

```python
# dpo_enhanced_generator.py の内容をここに貼り付けて実行
# → /content/dpo_enhanced.jsonl が生成される
```

### 手順1: 環境設定セルの実行
通常通り実行。

### 手順2: HFログインセル
通常通り実行（シークレット自動読み込みセルが既にあるはず）。

### 手順3: exp2のマージ（セル4）
前回と同じ手順でexp2のアダプタをベースモデルにマージ。
/content/merged_sft_model に保存。

### 手順4: マージ済みモデルのUnsloth読み込み（追加セル）
前回と同じ。

### 手順5: データセット整形セルの変更（★重要）
データセット読み込み部分を変更：

```python
# 変更前
dataset = load_dataset("u-10bei/dpo-dataset-qwen-cot", split="train")

# 変更後
dataset = load_dataset("json", data_files="/content/dpo_enhanced.jsonl", split="train")
```

### 手順6: DPOConfigセル
- learning_rate = 5e-7（exp11と同じ）
- beta = 0.2（exp11と同じ）

### 手順7: DPOトレーニング実行
通常通り実行。

### 手順8: READMEセル
- title_line = "exp19-enhanced-dpo"

### 手順9: アップロードセル
- repo_name = "exp19-enhanced-dpo"

### 手順10: 標準コード2で推論
- MODEL_SOURCE = "adapter_merge"
- ADAPTER_ID = "ogwata/exp19-enhanced-dpo"

## 注意事項
- 強化版DPOデータの件数はオリジナルの約2.8倍になるため、学習時間も長くなる
- 学習が不安定な場合はanti_*データの比率を下げることを検討
