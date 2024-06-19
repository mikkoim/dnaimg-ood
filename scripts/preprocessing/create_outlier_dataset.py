
from pathlib import Path
import pandas as pd
import argparse
import numpy as np
from sklearn.model_selection import StratifiedGroupKFold

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--label_col", type=str, required=True)
    parser.add_argument("--leave_out_label", type=str, required=True)
    parser.add_argument("--out_prefix", type=str)
    parser.add_argument("--out_folder", type=str, default=".")

    args = parser.parse_args()

    input_csv_fname = Path(args.input_csv)
    out_folder = Path(args.out_folder)
    out_folder.mkdir(exist_ok=True, parents=True)

    df = pd.read_csv(input_csv_fname)
    n_taxa = df[args.label_col].nunique()

    loo_taxon = args.leave_out_label

    # Create empty column for the train-test-split
    df = df.assign(**{str(0): "0"})

    # Separate the leave-one-out labels
    loo_df = df.query("taxon == @loo_taxon")
    rest_df = df.query("taxon != @loo_taxon")

    # Make the splitting
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)

    temp_idx, test_idx = next(iter(cv.split(rest_df, rest_df["taxon"], rest_df["individual"])))
    test_df = rest_df.iloc[test_idx]
    temp_df = rest_df.iloc[temp_idx]

    # Split rest to train and validation
    train_idx, val_idx = next(
        iter(cv.split(temp_df, temp_df["taxon"], temp_df["individual"]))
    )
    train_df = temp_df.iloc[train_idx]
    val_df = temp_df.iloc[val_idx]

    # Print train test val sizes
    print("train len:", len(train_df), 
          "test len:", len(test_df),
          "val len:", len(val_df))
    assert set(train_df.index).isdisjoint(set(test_df.index))
    assert set(test_df.index).isdisjoint(set(val_df.index))
    assert set(train_df.index).isdisjoint(set(val_df.index))


    # Assign splits to the empty column
    train_list = train_df["individual"].unique()
    test_list = test_df["individual"].unique()
    val_list = val_df["individual"].unique()
    loo_list = loo_df["individual"].unique()

    df.loc[df["individual"].isin(train_list), "0"] = "train"
    df.loc[df["individual"].isin(test_list), "0"] = "test"
    df.loc[df["individual"].isin(val_list), "0"] = "val"
    df.loc[df["individual"].isin(loo_list), "0"] = "test"

    # Print classes of train and test splits
    print("Train set")
    print(df[df["0"] == "train"].taxon.value_counts())
    print("Test set")
    print(df[df["0"] == "test"].taxon.value_counts())

    # Create label map file
    ingroup_list = [x for x in df[args.label_col].unique().tolist() if x != loo_taxon]

    with open(out_folder / f"label_map{args.out_prefix}_{loo_taxon}.txt", "w") as f:
        f.write(f"{loo_taxon}\n") # The outlier label is mapped to 0 
        f.write("\n".join(ingroup_list))

    # Save everything
    out_fname = f"{args.out_prefix}_{loo_taxon}.csv"
    df.to_csv(out_folder / out_fname)
    print(out_folder / out_fname)