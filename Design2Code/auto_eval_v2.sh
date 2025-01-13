#!/bin/bash  
  
# 定义一个数组，包含所有需要处理的模型名称  
model_names=(  
    "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_3000"
    "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_4000"
    "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_5000"
    "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_5820"
    # "qwen2_vl_coder-7b_3072_code_pretrain_bsz128_1e5_web2code_job_3000"
    # "qwen2_vl_coder-7b_3072_code_pretrain_bsz128_1e5_web2code_job_4000"
    # "qwen2_vl_coder-7b_3072_code_pretrain_bsz128_1e5_web2code_job_5000"
    # "qwen2_vl_coder-7b_3072_code_pretrain_bsz128_1e5_web2code_job_5820"
    # "qwen2_vl_coder_mn_only-7b_3072_1.5pretrain_bsz128_1e5_web2code_job_5000"
    # "qwen2_vl_coder_mn_only-7b_3072_1.5pretrain_bsz128_1e5_web2code_job_3000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_1000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_1500"  
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_2000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_3000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_2000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_3000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_4000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_5000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_6000"    
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_7000"
    # "qwen2_vl_coder_mn_pretrain_LLM_sft-7b_3072_bsz128_1e4_web2code_job_8000"

    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_500"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_1000"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_1500"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_2000"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_3000"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_4000"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_5000"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_6000"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_7000"
    # "qwen2_vl_coder_mn_only-7b_3072_bsz128_1e4_web2code_merger_8000"
    # "another_model_name_part1_part2" # 可以添加其他模型名称  
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
for model_name in "${model_names[@]}"; do  
    echo "正在处理模型: $model_name" | tee -a "$log_file"  
  
    # 调用 eval_scripts/auto_eval.sh 并传入 model_name，将输出追加到同一个日志文件  
    bash eval_scripts/auto_eval_merge_v2.sh "$model_name" 2>&1 | tee -a "$log_file"  
done  
  
echo "所有模型处理完成。" | tee -a "$log_file"  