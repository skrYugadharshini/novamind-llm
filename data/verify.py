import json
from pathlib import Path

def verify():
    print("=" * 50)
    print("NovaMind — Data Verification")
    print("=" * 50)

    files = [
        "data/processed/train.jsonl",
        "data/processed/val.jsonl",
        "data/processed/test.jsonl",
    ]

    for filepath in files:
        path = Path(filepath)
        if not path.exists():
            print(f"❌ MISSING: {filepath}")
            continue

        with open(path, encoding="utf-8") as f:
            samples = [json.loads(line) for line in f]

        print(f"\n📄 {filepath}")
        print(f"   Samples : {len(samples):,}")

        sample = samples[0]
        required = ["instruction", "input", "output", "text"]
        for field in required:
            status = "✅" if field in sample else "❌"
            print(f"   {status} Field '{field}' present")

        print(f"\n   🔍 Sample preview:")
        print(f"   Instruction : {sample['instruction'][:60]}...")
        print(f"   Output      : {sample['output'][:60]}...")
        print(f"   Prompt len  : {len(sample['text'])} chars")

    print("\n✅ Verification complete!")

if __name__ == "__main__":
    verify()