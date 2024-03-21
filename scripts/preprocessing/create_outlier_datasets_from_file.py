from pathlib import Path
import pandas as pd
import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--label_list", type=str, required=True)
    parser.add_argument("--label_col", type=str, required=True)
    parser.add_argument("--out_prefix", type=str)
    parser.add_argument("--out_folder", type=str, default=".")

    args = parser.parse_args()

    input_csv_fname = Path(args.input_csv)
    out_folder = Path(args.out_folder)
    out_folder.mkdir(exist_ok=True, parents=True)

    with open(args.label_list, "r") as f:
        labels = [x.strip() for x in f.readlines()]

    for label in labels:
        print("Creating dataset for label: ", label)
        subprocess.run(["python", "scripts/preprocessing/create_outlier_dataset.py",
            "--input_csv", str(input_csv_fname),
            "--label_col", str(args.label_col),
            "--leave_out_label", label,
            "--out_prefix", str(args.out_prefix),
            "--out_folder", str(args.out_folder)])


