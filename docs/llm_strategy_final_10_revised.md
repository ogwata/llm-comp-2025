# 松尾研LLM開発コンペ2025：StructEval 0.8突破 最終決戦戦略（修正版）

**作成日:** 2026-03-01
**残り提出:** 24回（うち10回を本戦略に配分）
**締切:** 2026/03/02 12:00

## 0. 原案からの変更点

- **exp28（Error Sniper）を削除**: 評価データの推論結果をDPO学習データに転用する行為はコンペルール違反（「推論結果の分析をもとに学習データを評価に適合する形で編集・加工することも禁止」）
- **削除分の提出枠をTask Arithmetic探索に追加**: 学習ベースのハイパーパラメータ探索は0.760プラトーで飽和済み（exp21-24で確認）。マージ探索の回数を増やす方が期待値が高い

## 1. 現状分析（exp21 フォーマット別パス率）

| フォーマット | パス率 | 主なエラー |
|:--:|:--:|:--|
| JSON | 98.0% | markdown_block混入 |
| YAML | 82.9% | markdown_block, natural_language_prefix |
| TOML | 80.0% | Cannot overwrite a value（キー重複） |
| XML | 80.0% | markdown_block, not well-formed |
| CSV | 100% | なし |
| **全体** | **89.3%** | **16件失敗** |

## 2. 提出配分（10回）

### Phase A: 部品作成（2回）

| 提出 | 内容 | ベースモデル | 設定 | 目的 |
|:--:|:--|:--|:--|:--|
| exp27 | DPO epoch=1 | exp26-sft-r16-merged (r=16) | LR=7e-7, β=0.2, dpo-qwen-cot | r=16の広い容量にDPO抑制力を注入。Task Arithmetic用の「論理修正ベクトル」 |
| exp29 | DPO epoch=2 | exp2-merged (r=64) | LR=7e-7, β=0.2, dpo-qwen-cot | Markdown汚染をさらに抑制。Task Arithmetic用の「ノイズ除去ベクトル」 |

### Phase B: Task Arithmetic 統合（8回）

mergekitを使用し、ベースモデル W₀ に対するタスクベクトルを合成する。

```
W_final = W_exp21 + λ_logic × (W_exp27 - W₀) - λ_noise × (W_exp29 - W₀)
```

| 提出 | λ_logic | λ_noise | 狙い |
|:--:|:--:|:--:|:--|
| exp30 | 0.3 | 0.0 | 論理ベクトル単体の効果測定 |
| exp31 | 0.5 | 0.0 | 論理ベクトル強め |
| exp32 | 0.7 | 0.0 | 論理ベクトル最大 |
| exp33 | 0.0 | 0.3 | ノイズ除去ベクトル単体の効果測定 |
| exp34 | 0.0 | 0.5 | ノイズ除去ベクトル強め |
| exp35 | best_logic | 0.3 | ベスト論理 + ノイズ除去 |
| exp36 | best_logic | 0.5 | ベスト論理 + ノイズ除去強め |
| exp37 | 予備 | 予備 | exp30-36の結果に基づき最終調整 |

## 3. 技術的前提

- **W₀（ベースモデル）**: `Qwen/Qwen3-4B-Instruct-2507`（素のベースモデル）
- **W_exp21**: `ogwata/exp21-sft-dpo-lr7e7-beta02`（現ベスト 0.760）
- **W_exp27**: exp27で作成するr=16 DPOモデル
- **W_exp29**: exp29で作成するDPO epoch=2モデル
- **マージツール**: mergekit（GPU不要、CPU上で重み演算のみ）
- **推論コード**: 標準コード2（改変禁止）

## 4. ルール遵守チェック

- [x] 推論コードはモデル情報以外改変しない
- [x] inference.jsonを手動編集しない
- [x] 評価データ・推論結果を学習データに転用しない
- [x] LLMによるデータ合成を行わない
- [x] 学習データソースは既存公開データセットのみ使用
- [x] マージ済みモデルをHuggingFaceにアップロード

## 5. 実行順序

1. **exp27**: DPOノートブックでexp26-merged → DPO学習 → HFアップロード → 推論・提出
2. **exp29**: DPOノートブックでexp2-merged → DPO epoch=2学習 → HFアップロード → 推論・提出
3. **exp30-37**: mergekitでTask Arithmetic → HFアップロード → 推論・提出（各30分以内で回転可能）
