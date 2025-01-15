#!/bin/bash  
  
# 定义一个数组，包含所有需要处理的模型名称  
model_names=(  
    "pretrain_mm_only-7b_3072_bsz128_1e3_web2code_filter_670k_500,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_web2code_filter_670k/sft/full/checkpoint-500/"
    "pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed_5820,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed/sft/full/checkpoint-5820/"
    "pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed_5000,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed/sft/full/checkpoint-5000/"
    "pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed_3000,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed/sft/full/checkpoint-3000/"
    "pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed_2000,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed/sft/full/checkpoint-2000/"
    "pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed_1000,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_web2code_fixed/sft/full/checkpoint-1000/"

    # "pretrain_mm_only-7b_3072_bsz128_1e3_mix_data_ocr_code_pretrain_v2_600k_1000,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_mix_data_ocr_code_pretrain_v2_600k/sft/full/checkpoint-1000/"
    # "pretrain_mm_only-7b_3072_bsz128_1e3_mix_data_ocr_code_pretrain_v2_600k_4248,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_mix_data_ocr_code_pretrain_v2_600k/sft/full/checkpoint-4248/"
    # "pretrain_mm_only-7b_3072_bsz128_1e3_mix_data_ocr_code_pretrain_v2_600k_3000,/mnt/lingjiejiang/multimodal_code/exp/saves/pretrain_mm_only-7b_3072_bsz128_1e3_mix_data_ocr_code_pretrain_v2_600k/sft/full/checkpoint-3000/"

    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job_3000,/mnt/lingjiejiang/multimodal_code/exp/saves/qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job/sft/full/checkpoint-3000/"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job_4000,/mnt/lingjiejiang/multimodal_code/exp/saves/qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job/sft/full/checkpoint-4000/"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job_5000,/mnt/lingjiejiang/multimodal_code/exp/saves/qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job/sft/full/checkpoint-5000/"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job_6000,/mnt/lingjiejiang/multimodal_code/exp/saves/qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job/sft/full/checkpoint-6000/"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job_6000,/mnt/lingjiejiang/multimodal_code/exp/saves/qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_mid_lenqi_1M_job/sft/full/checkpoint-7000/"
)  
  
# 确保日志目录存在  
log_dir="eval_log"  
mkdir -p "$log_dir"  
  
# 初始化一个用于存储日志文件名的变量  
log_file_prefix=""  
  
# 通过循环最多提取两个模型名称来生成日志文件名  
for ((i = 0; i < ${#model_names[@]} && i < 2; i++)); do  
    # 替换非法文件名字符（如果有）  
    sanitized_name="${model_names[i]//\//_}"  
    if [ -z "$log_file_prefix" ]; then  
        log_file_prefix="$sanitized_name"  
    else  
        log_file_prefix="${log_file_prefix}_${sanitized_name}"  
    fi  
done  
  
# 生成完整的日志文件路径  
log_file="${log_dir}/${log_file_prefix}.log"  
  
echo "开始处理所有模型..." | tee -a "$log_file"  
  
# 循环遍历数组中的每个模型名称  
for model_info in "${model_names[@]}"; do  
    
    IFS=',' read -r model_name model_path <<< "$model_info" 
    echo "正在处理模型: $model_name" | tee -a "$log_file"  
    # 调用 eval_scripts/auto_eval.sh 并传入 model_name，将输出追加到同一个日志文件  
    # bash eval_scripts/auto_eval_merge.sh "$model_name" 2>&1 | tee -a "$log_file" 
    bash eval_scripts/auto_eval_self_path_v2_prompt.sh "$model_name" "$model_path" 2>&1 | tee -a "$log_file"   
done  
  
echo "所有模型处理完成。" | tee -a "$log_file"  