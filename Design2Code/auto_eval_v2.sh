#!/bin/bash  
  
# 定义一个数组，包含所有需要处理的模型名称  
model_names=(  
    "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_revised_cot_39k_276"
    "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_html_chart_mix_v1_119k_841"
    "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_html_chart_mix_v2_130k_917"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_code_revised_evol_50k_355"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_chart_evol_40k_282"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_code20_html80_mix_100k_705"

    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_revised_750k_v1_500"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_revised_750k_v1_1000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_revised_750k_v1_1500"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_revised_html_tag_750k_v2_500"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_revised_html_tag_750k_v2_1000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_revised_html_tag_750k_v2_1500"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_img_revised_80k_v1-563"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_img_revised_html_tag_80k_v2-563"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_chart52k_369"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_760k_v1_2000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_760k_v1_3000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_760k_v1_4000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_760k_prompt_added_v2_2000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_760k_prompt_added_v2_3000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_rick_760k_prompt_added_v2_4000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_filter_669k_new_img_1000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_filter_669k_new_img_3000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_filter_669k_new_img_4000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_filter_669k_new_img_4710"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_filter_670k_4000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_job_fixed-4000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_job_fixed-5820"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_3000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_4000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_5000"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_web2code_5820"
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