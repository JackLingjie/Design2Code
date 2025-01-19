# python3 prompting/gpt4o_mini.py \
#  --prompt_method direct_prompting \
#  --file_name all \
#  --subset testset_final \
#  --take_screenshot

MODEL_NAME=gpt-4o-mini
python3 metrics/multi_processing_eval.py --eval_name ${MODEL_NAME} --data_path saves/${MODEL_NAME}_direct_prompting
