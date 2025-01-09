#!bin/bash
MODEL_NAME=qwen2_vl_coder_mn_only-7b_3072_bsz64_test_job

python3 prompting/qwen_vl_batch.py \
 --prompt_method direct_prompting \
 --file_name all \
 --subset testset_final \
 --take_screenshot \
 --model_name ${MODEL_NAME} \
 --model_path /mnt/lingjiejiang/multimodal_code/exp/saves/${MODEL_NAME}/fullft/bsz128_epoch1

python3 metrics/multi_processing_eval.py --eval_name ${MODEL_NAME} --data_path saves/${MODEL_NAME}_direct_prompting