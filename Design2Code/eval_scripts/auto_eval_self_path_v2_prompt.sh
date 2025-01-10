#!/bin/bash
  
# 检查是否传入了两个参数  
if [ "$#" -ne 2 ]; then  
    echo "Usage: $0 <model_name> <path>"  
    exit 1  
fi   
  
MODEL_NAME="$1"  
MODEL_PATH="$2"
echo "MODEL_NAME: $MODEL_NAME"
echo "MODEL_PATH: $MODEL_PATH"

python3 prompting/qwen_vl_batch.py \
 --prompt_method direct_prompting \
 --file_name all \
 --subset testset_final \
 --take_screenshot \
 --model_name ${MODEL_NAME} \
 --model_path ${MODEL_PATH}

python3 metrics/multi_processing_eval.py --eval_name ${MODEL_NAME} --data_path saves/${MODEL_NAME}_direct_prompting
