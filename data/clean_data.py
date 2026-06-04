import json
import re
from pathlib import Path
from tqdm import tqdm

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def normalize_sample(item):
    instruction = item.get("instruction", "").strip()
    input_text  = item.get("input", "").strip()
    output      = item.get("output", "").strip()

    if not instruction or not output:
        return None
    if len(instruction) < 10:
        return None
    if len(output) < 20:
        return None
    if len(instruction) > 1024:
        return None
    if len(output) > 2048:
        return None

    instruction = re.sub(r'\n{3,}', '\n\n', instruction)
    output      = re.sub(r'\n{3,}', '\n\n', output)

    return {
        "instruction": instruction,
        "input":       input_text,
        "output":      output,
    }

def build_prompt(sample):
    if sample["input"]:
        return (
            f"### Instruction:\n{sample['instruction']}\n\n"
            f"### Input:\n{sample['input']}\n\n"
            f"### Response:\n{sample['output']}"
        )
    else:
        return (
            f"### Instruction:\n{sample['instruction']}\n\n"
            f"### Response:\n{sample['output']}"
        )

def clean_and_format():
    print("=" * 50)
    print("NovaMind — Cleaning & Formatting Data")
    print("=" * 50)

    raw_files = list(RAW_DIR.glob("*.jsonl"))
    print(f"\n📂 Found {len(raw_files)} raw files")

    all_samples  = []
    seen_prompts = set()

    for raw_file in raw_files:
        print(f"\n🔄 Processing: {raw_file.name}")
        before = 0
        after  = 0

        with open(raw_file, encoding="utf-8") as f:
            for line in tqdm(f):
                item = json.loads(line)
                before += 1
                normalized = normalize_sample(item)
                if normalized is None:
                    continue

                key = normalized["instruction"].lower()[:100]
                if key in seen_prompts:
                    continue
                seen_prompts.add(key)

                normalized["text"] = build_prompt(normalized)
                all_samples.append(normalized)
                after += 1

        print(f"   Before: {before:,} | After: {after:,}")

    print(f"\n📊 Total clean samples: {len(all_samples):,}")

    cleaned_path = PROCESSED_DIR / "cleaned.jsonl"
    with open(cleaned_path, "w", encoding="utf-8") as f:
        for sample in all_samples:
            f.write(json.dumps(sample) + "\n")

    print(f"💾 Saved → {cleaned_path}")

if __name__ == "__main__":
    clean_and_format()