#!/bin/bash
#SBATCH --job-name=train
#SBATCH --account=Project_2004353
#SBATCH --partition=gpu
#SBATCH --time=6:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=32G
#SBATCH --gres=gpu:v100:1,nvme:64
#SBATCH -o "o_%j.txt"
#SBATCH -e "e_%j.txt"

echo "Extracting data..."
unzip -q ../benthic-models/data/raw/FIN-Benthic2.zip -d $TMPDIR
echo "Done!"
source tykky
python $TAXONOMIST_PATH/scripts/02_train.py \
                --data_folder "$TMPDIR/IDA/" \
                --dataset_name "finbenthic2" \
                --csv_path $1 \
                --label "taxon" \
                --fold 0 \
                --class_map $2 \
                --imsize 224 \
                --batch_size 256 \
                --aug 'aug-02' \
                --load_to_memory 'False' \
                --model 'efficientnet_b0' \
                --freeze_base 'False' \
                --pretrained 'True' \
                --opt 'adamw' \
                --max_epochs 30 \
                --min_epochs 5 \
                --early_stopping 'False' \
                --early_stopping_patience 50 \
                --criterion 'cross-entropy' \
                --lr 0.0001 \
                --auto_lr 'True' \
                --log_dir 'dnaimg' \
                --out_folder 'outputs' \
                --out_prefix "dnaimg_$3" \
                --deterministic 'True'
