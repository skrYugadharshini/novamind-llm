from datasets import load_dataset
import json
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def download_datasets():
    print("=" * 50)
    print("NovaMind — Downloading Datasets")
    print("=" * 50)

    datasets_to_load = [
        {
            "name": "sahil2801/CodeAlpaca-20k",
            "split": "train",
            "label": "codealpaca"
        },
        {
            "name": "iamtarun/python_code_instructions_18k_alpaca",
            "split": "train",
            "label": "python_instructions"
        }
    ]

    all_data = []

    for ds_info in datasets_to_load:
        print(f"\n📥 Downloading: {ds_info['name']}")
        try:
            ds = load_dataset(ds_info['name'], split=ds_info['split'])
            print(f"   ✅ Loaded {len(ds)} samples")
            print(f"   📋 Columns: {ds.column_names}")
            print(f"   🔍 Sample: {ds[0]}")

            raw_path = RAW_DIR / f"{ds_info['label']}.jsonl"
            with open(raw_path, "w") as f:
                for item in ds:
                    f.write(json.dumps(item) + "\n")
            print(f"   💾 Saved to {raw_path}")
            all_data.append(ds)

        except Exception as e:
            print(f"   ❌ Failed: {e}")

    print(f"\n✅ Total datasets downloaded: {len(all_data)}")
    return all_data

if __name__ == "__main__":
    download_datasets()