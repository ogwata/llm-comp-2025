"""
Enhanced Multi-Dimensional Anti-Formatting DPO Dataset Generator

u-10bei/dpo-dataset-qwen-cot のchosenデータをベースに、
プログラム的にrejectedデータを生成する。

生成されるrejectedの3カテゴリ:
1. Markdown + 会話フィラー混入 (60%)
2. Tag Leakage混入 (20%)
3. CoT推論混入 (20%)

コンペルール準拠: LLMを使わず、純粋にプログラム的な文字列操作のみ。

使い方 (Colab):
  !pip install datasets huggingface_hub
  %run generate_enhanced_dpo.py
  # または
  exec(open("generate_enhanced_dpo.py").read())
"""

import random
import re
from datasets import load_dataset, Dataset

random.seed(42)

# ========================================
# 1. ベースデータセットの読み込み
# ========================================
print("Loading base dataset: u-10bei/dpo-dataset-qwen-cot")
base_dataset = load_dataset("u-10bei/dpo-dataset-qwen-cot", split="train")
print(f"Loaded {len(base_dataset)} examples")

# ========================================
# 2. Rejected生成テンプレート
# ========================================

# カテゴリ1: Markdown + 会話フィラー (60%)
CONVERSATIONAL_PREFIXES = [
    "Sure! Here is the requested data:\n\n",
    "Certainly. Below is the output:\n\n",
    "Here's the result in the requested format:\n\n",
    "Of course! Here you go:\n\n",
    "I've converted the data as requested. Here it is:\n\n",
    "The following is the generated output:\n\n",
    "Here is the structured data you requested:\n\n",
    "As requested, here's the formatted output:\n\n",
    "Let me provide you with the data:\n\n",
    "Sure thing! The output is:\n\n",
]

CONVERSATIONAL_SUFFIXES = [
    "\n\nI hope this helps! Let me know if you need any changes.",
    "\n\nFeel free to ask if you need modifications.",
    "\n\nThis should meet your requirements. Let me know if you need adjustments.",
    "\n\nPlease verify the output and let me know if any corrections are needed.",
    "\n\nNote: The above output follows the specified format strictly.",
    "\n\nLet me know if you'd like me to modify any part of this output.",
]

MARKDOWN_FENCES = [
    ("```json\n", "\n```"),
    ("```yaml\n", "\n```"),
    ("```toml\n", "\n```"),
    ("```xml\n", "\n```"),
    ("```csv\n", "\n```"),
    ("```\n", "\n```"),
]

# カテゴリ2: Tag Leakage (20%)
LEAKED_TAGS = [
    "<tool_call>\n",
    "</tool_call>\n",
    "<|im_start|>assistant\n",
    "<|im_end|>\n",
    "<|endoftext|>\n",
    "<function_call>\n",
    "</function_call>\n",
    "<result>\n",
    "</result>\n",
]

# カテゴリ3: CoT推論混入 (20%)
COT_PREFIXES = [
    "Let me think step by step about how to generate this data.\n\n"
    "First, I need to understand the required format. "
    "Then, I'll structure the data accordingly.\n\n"
    "Here's my approach:\n"
    "1. Identify the target format\n"
    "2. Map the input fields to the output structure\n"
    "3. Generate the final output\n\n"
    "Based on this analysis, the output is:\n\n",

    "Approach:\n"
    "1. Task: Generate the requested structured data\n"
    "2. Complexity: moderate - requires careful field mapping\n"
    "3. Format rules: Follow strict syntax requirements\n"
    "4. Validation: Ensure all fields are correctly populated\n\n"
    "Let me work through this carefully...\n\n"
    "After careful consideration, here is the result:\n\n",

    "I need to analyze the input and determine the correct output format.\n\n"
    "Step 1: Parse the input data\n"
    "Step 2: Identify the target schema\n"
    "Step 3: Transform and validate\n\n"
    "Processing complete. Output:\n\n",

    "Thinking about this problem:\n"
    "- The user wants structured data output\n"
    "- I need to follow the exact format specification\n"
    "- Each field must be correctly mapped\n\n"
    "After reasoning through the requirements:\n\n",
]


def extract_output_section(text: str) -> str:
    """chosenテキストから 'Output:' 以降の実データ部分を抽出"""
    # "Output:" または "Output:\n" の後のテキストを取得
    match = re.search(r'Output:\s*\n?(.*)', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # "Output:" がない場合はテキスト全体を返す
    return text.strip()


def generate_markdown_filler_rejected(clean_output: str) -> str:
    """カテゴリ1: Markdown + 会話フィラー混入"""
    variant = random.randint(0, 3)

    if variant == 0:
        # Markdown fence のみ
        fence_open, fence_close = random.choice(MARKDOWN_FENCES)
        return fence_open + clean_output + fence_close
    elif variant == 1:
        # 会話プレフィックス + Markdown fence
        prefix = random.choice(CONVERSATIONAL_PREFIXES)
        fence_open, fence_close = random.choice(MARKDOWN_FENCES)
        return prefix + fence_open + clean_output + fence_close
    elif variant == 2:
        # 会話プレフィックス + サフィックス (Markdownなし)
        prefix = random.choice(CONVERSATIONAL_PREFIXES)
        suffix = random.choice(CONVERSATIONAL_SUFFIXES)
        return prefix + clean_output + suffix
    else:
        # フル: プレフィックス + Markdown + サフィックス
        prefix = random.choice(CONVERSATIONAL_PREFIXES)
        fence_open, fence_close = random.choice(MARKDOWN_FENCES)
        suffix = random.choice(CONVERSATIONAL_SUFFIXES)
        return prefix + fence_open + clean_output + fence_close + suffix


def generate_tag_leaked_rejected(clean_output: str) -> str:
    """カテゴリ2: Tag Leakage混入"""
    variant = random.randint(0, 2)

    if variant == 0:
        # タグを先頭に挿入
        tag = random.choice(LEAKED_TAGS)
        return tag + clean_output
    elif variant == 1:
        # タグを末尾に挿入
        tag = random.choice(LEAKED_TAGS)
        return clean_output + "\n" + tag
    else:
        # タグで囲む
        open_tag = random.choice(LEAKED_TAGS)
        close_tag = random.choice(LEAKED_TAGS)
        return open_tag + clean_output + "\n" + close_tag


def generate_cot_rejected(clean_output: str) -> str:
    """カテゴリ3: CoT推論混入"""
    cot_prefix = random.choice(COT_PREFIXES)
    # 一部にMarkdownも追加
    if random.random() < 0.5:
        fence_open, fence_close = random.choice(MARKDOWN_FENCES)
        return cot_prefix + fence_open + clean_output + fence_close
    else:
        return cot_prefix + clean_output


# ========================================
# 3. データセット生成
# ========================================
print("Generating enhanced DPO dataset...")

new_prompts = []
new_chosens = []
new_rejecteds = []

for i, example in enumerate(base_dataset):
    prompt = example["prompt"]
    chosen = example["chosen"]

    # chosenからクリーンな出力部分を抽出
    clean_output = extract_output_section(chosen)

    # カテゴリをランダムに選択 (60% / 20% / 20%)
    roll = random.random()
    if roll < 0.6:
        rejected = generate_markdown_filler_rejected(clean_output)
    elif roll < 0.8:
        rejected = generate_tag_leaked_rejected(clean_output)
    else:
        rejected = generate_cot_rejected(clean_output)

    new_prompts.append(prompt)
    new_chosens.append(chosen)
    new_rejecteds.append(rejected)

# Dataset作成
enhanced_dataset = Dataset.from_dict({
    "prompt": new_prompts,
    "chosen": new_chosens,
    "rejected": new_rejecteds,
})

print(f"Generated {len(enhanced_dataset)} enhanced DPO pairs")
print(f"\nSample rejected (first example):\n{enhanced_dataset[0]['rejected'][:500]}...")

# ========================================
# 4. HuggingFaceにアップロード
# ========================================
REPO_ID = "ogwata/enhanced-dpo-v2"

print(f"\nUploading to {REPO_ID}...")
enhanced_dataset.push_to_hub(REPO_ID, private=False)
print(f"Done! Dataset available at: https://huggingface.co/datasets/{REPO_ID}")
