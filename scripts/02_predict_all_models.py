from pathlib import Path
import argparse
import subprocess
import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, required=True)

    args = parser.parse_args()

    with open(args.i, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for label,ckpt_path in zip(config["labels"], config["ckpts"]):
        subprocess.run([
            "bash", "batchjobs/predict/finbenthic2/predict_single_classifier.sh",
            f"data/processed/finbenthic2/leave-one-out/02_finbenthic2_outliers_{label}.csv",
            f"data/processed/finbenthic2/leave-one-out/label_map02_finbenthic2_outliers_{label}.txt",
            ckpt_path])
