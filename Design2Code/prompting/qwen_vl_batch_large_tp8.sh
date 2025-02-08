export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
MODEL_NAME="Qwen2-VL-72B-Instruct"
python3 prompting/qwen_vl_batch_large.py \
 --prompt_method direct_prompting \
 --file_name all \
 --subset testset_final \
 --take_screenshot

python3 metrics/multi_processing_eval.py --eval_name ${MODEL_NAME} --data_path saves/${MODEL_NAME}_direct_prompting