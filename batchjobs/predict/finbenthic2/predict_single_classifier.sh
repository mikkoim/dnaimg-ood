# echo "Extracting data..."
# unzip -q ../benthic-models/data/raw/FIN-Benthic2.zip -d $TMPDIR
# echo "Done!"
# source tykky
python $TAXONOMIST_PATH/scripts/03_predict.py \
    --data_folder "$TMPDIR/IDA/" \
    --dataset_name "finbenthic2" \
    --csv_path $1 \
    --label "taxon" \
    --fold 0 \
    --class_map $2 \
    --imsize 224 \
    --batch_size 1024 \
    --aug 'none' \
    --load_to_memory 'False' \
    --out_folder 'outputs' \
    --tta 'False' \
    --out_prefix 'preds' \
    --ckpt_path $3

#!/bin/bash
#SBATCH --job-name=pred
#SBATCH --account=Project_2004353
#SBATCH --partition=gpu
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=32G
#SBATCH --gres=gpu:v100:1,nvme:64
#SBATCH -o "o_pred_%j.txt"
#SBATCH -e "e_pred_%j.txt"