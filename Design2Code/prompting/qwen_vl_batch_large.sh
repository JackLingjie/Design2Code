export LD_LIBRARY_PATH=/home/lidong1/miniconda3/envs/design/lib/python3.10/site-packages/nvidia/nvjitlink/lib:$LD_LIBRARY_PATH  
export CUDA_VISIBLE_DEVICES=0,1,2,3
MODEL_NAME="Qwen2-VL-72B-Instruct"
python3 prompting/qwen_vl_batch_large.py \
 --prompt_method direct_prompting \
 --file_name all \
 --subset testset_final \
 --take_screenshot

python3 metrics/multi_processing_eval.py --eval_name ${MODEL_NAME} --data_path saves/${MODEL_NAME}_direct_prompting