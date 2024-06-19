from pathlib import Path
import pandas as pd
import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--label_list", type=str, required=True)

    args = parser.parse_args()

    with open(args.label_list, "r", encoding="utf-8") as f:
        labels = [x.strip() for x in f.readlines()]

    for label in labels:
        subprocess.run([
            "sbatch", "batchjobs/train/finbenthic2/train_single_classifier.sh",
            f"data/processed/finbenthic2/leave-one-out/02_finbenthic2_outliers_{label}.csv", 
            f"data/processed/finbenthic2/leave-one-out/label_map02_finbenthic2_outliers_{label}.txt",
            f"{label}"])
