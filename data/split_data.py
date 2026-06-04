import json
import random
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
SEED          = 42
TRAIN_RATIO   = 0.90
VAL_RATIO     = 0.05
TEST_RATIO    = 0.05

def split_data():
    print("=" * 50)
    print("NovaMind — Splitting Dataset")
    print("=" * 50)

    cleaned_path = PROCESSED_DIR / "cleaned.jsonl"
    with open(cleaned_path, encoding="utf-8") as f:
        samples = [json.loads(line) for line in f]

    random.seed(SEED)
    random.shuffle(samples)

    total     = len(samples)
    train_end = int(total * TRAIN_RATIO)
    val_end   = train_end + int(total * VAL_RATIO)

    train_data = samples[:train_end]
    val_data   = samples[train_end:val_end]
    test_data  = samples[val_end:]

    print(f"\n📊 Split Summary:")
    print(f"   Total : {total:,}")
    print(f"   Train : {len(train_data):,} (90%)")
    print(f"   Val   : {len(val_data):,}  (5%)")
    print(f"   Test  : {len(test_data):,}  (5%)")

    splits = {
        "train": train_data,
        "val":   val_data,
        "test":  test_data,
    }

    for split_name, split_samples in splits.items():
        out_path = PROCESSED_DIR / f"{split_name}.jsonl"
        with open(out_path, "w", encoding="utf-8") as f:
            for sample in split_samples:
                f.write(json.dumps(sample) + "\n")
        print(f"   💾 Saved {split_name} → {out_path}")

    stats = {
        "total": total,
        "train": len(train_data),
        "val":   len(val_data),
        "test":  len(test_data),
        "seed":  SEED,
    }
    with open(PROCESSED_DIR / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print("\n✅ Split complete!")

if __name__ == "__main__":
    split_data()