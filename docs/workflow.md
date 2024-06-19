# Data download

Download the FinBenthic 2 dataset from HERE

Put it to ```data/raw```

```bash
python scripts/preprocessing/process_finbenthic2.py \
    --IDA_folder $TMPDIR/IDA \
    --out_folder data/processed/finbenthic2

# This script puts all the samples that have the "leave_out_label" to the test set of the train-test-splits. The splits have only a single fold always
python scripts/preprocessing/create_outlier_datasets_from_file.py \
    --input_csv "data/processed/finbenthic2/01_finbenthic2_processed.csv" \
    --label_list "data/processed/finbenthic2/label_map_01_taxon.txt" \
    --label_col "taxon" \
    --out_prefix "02_finbenthic2_outliers" \
    --out_folder "data/processed/finbenthic2/leave-one-out"

# Training the models
python scripts/01_train_all_models.py
python scripts/02_predict_all_models.py -i data/processed/finbenthic2/trained_models.yaml

```

The predictions are then collected manually from the `outputs/finbenthic2/