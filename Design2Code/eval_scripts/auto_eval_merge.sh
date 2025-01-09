#!/bin/bash  
  
# 检查是否传入了模型名称参数  
if [ "$#" -ne 1 ]; then  
    echo "Usage: $0 <model_name>"  
    exit 1  
fi  
  
MODEL_NAME="$1"  
  
python3 prompting/qwen_vl_batch.py \
 --prompt_method direct_prompting \
 --file_name all \
 --subset testset_final \
 --take_screenshot \
 --model_name ${MODEL_NAME} \
 --model_path /mnt/lingjiejiang/multimodal_code/sft_checkpoints/${MODEL_NAME}

python3 metrics/multi_processing_eval.py --eval_name ${MODEL_NAME} --data_path saves/${MODEL_NAME}_direct_prompting
