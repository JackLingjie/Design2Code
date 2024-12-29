python3 metrics/multi_processing_eval.py --eval_name qwen2_vl --data_path saves/Qwen2-VL-7B-Instruct_direct_prompting
python3 metrics/multi_processing_eval.py --eval_name llama3.2_vl_batch --data_path saves/Llama-3.2-11B-Vision-Instruct_batch_direct_prompting
python3 metrics/multi_processing_eval.py --eval_name gpt4o --data_path saves/gpt4o_direct_prompting
python3 metrics/multi_processing_eval.py --eval_name llava_onevision --data_path saves/llava-onevision-qwen2-7b-ov-hf_batch_direct_prompting
python3 metrics/multi_processing_eval.py --eval_name mini_cpm --data_path saves/MiniCPM-V-2_6_batch_direct_prompting

python3 metrics/multi_processing_eval.py --eval_name qwen2_vl-7b_3072_bsz8_web2code --data_path saves/qwen2_vl-7b_3072_bsz8_web2code_direct_prompting