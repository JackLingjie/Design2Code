#!/bin/bash  
export LD_LIBRARY_PATH=/home/lidong1/miniconda3/envs/design/lib/python3.10/site-packages/nvidia/nvjitlink/lib:$LD_LIBRARY_PATH  
export CUDA_VISIBLE_DEVICES=0,1,2,3

# 检查是否传入了模型名称参数  
if [ "$#" -ne 1 ]; then  
    echo "Usage: $0 <model_name>"  
    exit 1  
fi  
  
MODEL_NAME="$1"  

python3 prompting/llama_batch_large.py \
 --prompt_method direct_prompting \
 --file_name all \
 --subset testset_final \
 --take_screenshot \
 --model_name ${MODEL_NAME} \
 --model_path /mnt/lingjiejiang/multimodal_code/checkpoints/llms/${MODEL_NAME}

python3 metrics/multi_processing_eval.py --eval_name ${MODEL_NAME} --data_path saves/${MODEL_NAME}_batch_direct_prompting