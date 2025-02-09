#!/bin/bash  
export LD_LIBRARY_PATH=/home/lidong1/miniconda3/envs/design/lib/python3.10/site-packages/nvidia/nvjitlink/lib:$LD_LIBRARY_PATH  
export CUDA_VISIBLE_DEVICES=3
# 定义一个数组，包含所有需要处理的模型名称  
model_names=(  
    # "dpo_qwen2vl_mix_v3_chart_dpo_v1_origin_img_24k-348"
    
    "dpo_html_chart_mix_v3_html_chart_code37_origin_89k-1260"
    # "dpo_qwen2vl_mix_v3_html_chart_code37_origin_89k-1260_fixed"
    # "dpo_qwentext25_html_chart_code37_origin_89k-1260"
    # "qwen2vl_html_code_chart_stack_256k-1811"
    # "stage2_qwen2_text2.5_1M_html_code_chart_stack_256k-1811"

    # "dpo_qwen2vl_v1_code_190k_origin_chart_24k_html_mix52k-734"
    # "dpo_qwen2vl_v1_raw_190k_origin_chart_24k_html_mix52k-734"
    # "stage2_llm_2nodes_1e5_html_chart_code_data_v2_code_190k-1342"
    # "dpo_qwen2vl_mix_v3_fixed_127k_html_origin_7b_27k-386"
    # "dpo_qwen2vl_v1_code_190k_html_origin_image_7b_27k-386"
    # "dpo_qwentext25_html_origin_image_7b_27k-386"
    # "qwen2vl_html_chartbench_mix_v3_127k_fixed"
    # "dpo_qwen2vl_v3_html_chart_code37_origin_89k-1260"
    # "dpo_qwen2vl_v1_code_190k_chart_html_origin_95k_1340"
    # "dpo_qwen2vl_v1_code_190k_html_chart_code37_origin_89k_1260"
    # "qwen2vl_html_chartbench_mix_v3_127k"
    # "stage2_llm_2nodes_1e5_html_code_chart_stack_256k_1811"
    # "dpo_mix190k_origin_image_45k_chart_bench_642"

    # "stage2_llm_2nodes_1e5_html_chart_stack_data_170k"
    # "dpo_mix190k_origin_image_7b_18k_chart_bench_score80_256"
    # "dpo_mix190k_origin_image_7b_32k_score80"
    # "dpo_mix190k_origin_image_7b_32k_score80"
    # "dpo_mix190k_html_chart_code37_4oimg_89k-1260"
    # "dpo_mix190k_html_chart_code37_origin_89k-1260"
    # "stage2_qwen2_text2.5_1M_html_chart_code_data_v2_code_190k"
    # "stage2_qwen2_text2.5_500k_html_chart_code_data_v2_code_190k"
    # "stage2_qwencoder2.5_500k_html_chart_code_data_v2_code_190k"
    # "dpo_html_chart_mix_chart_html_code_4o_95k-500"
    # "dpo_html_chart_mix_v3_chart_html_origin_95k-500"
    # "dpo_html_chart_mix_v3_4o_code_score80_42k-604"
    # "dpo_qwen2vl_v1_code_190k_origin_chart_24k_html_mix52k-734"
    # "dpo_qwen2vl_v1_raw_190k_origin_chart_24k_html_mix52k-734"
    # "dpo_chart_html_origin_41k_72b-580"
    # "dpo_chart32k_html_60k-844"
    # "qwen2vl_chart_code_data_v1_raw_190k—1342"
    # "qwen2vl_html_chart_code_data_v2_code_190k—1342"
    # "dpo_html_chart_mix_v3_mimic_image_7b_27k"
    # "dpo_html_chart_mix_v3_origin_image_7b_27k-386"
    # "dpo_html_chart_mix_v3_4oimg_chart_24k_html_mix52k-734"
    # "dpo_html_chart_mix_v3_origin_chart_24k_html_mix52k-734"
    # "dpo_html_chart_mix_v3_dpo_4o_image_7b_32k_score70"
    # "dpo_html_chart_mix_v3_origin_image_7b_32k_score70-458"
    # "dpo_origin_image_7b_24k_raw-348"
    # "stage2_llm_2nodes_1e5_html_chart_code_data_v1_raw_190k-1342"
    # "stage2_llm_2nodes_1e5_html_chart_code_data_v2_code_190k-1342"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_html_chart_stack_data_193k-1362"
    # "dpo_html_chart_mix_v3_chart_v1_origin_img_24k"
    # "dpo_html_chart_mix_v3_chart_v2_4o_img_24k"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_chart_revised_evol_bench_mix_v2_137k-963"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_chart_evol_bench_mix_v1_97k-685"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_html_chartbench_mix_v3_127k_893"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_revised_cot_39k_276"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_html_chart_mix_v1_119k_841"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_html_chart_mix_v2_130k_917"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_chartbench_images_46k_code-330"
    # "stage2_llm_2nodes_1e5_web2code_bsz128_1e5_chartbench_images_46k_raw_answer-330"
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