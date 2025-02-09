#!/bin/bash  
export LD_LIBRARY_PATH=/home/lidong1/miniconda3/envs/design/lib/python3.10/site-packages/nvidia/nvjitlink/lib:$LD_LIBRARY_PATH  
export CUDA_VISIBLE_DEVICES=0,1,2,3
# 定义一个数组，包含所有需要处理的模型名称  
model_names=(  
    "qwen72b_html_chartbench_mix_v3_127k-893"
    "qwen72b_html_chart_stack_data_193k-1362"
    "qwen72b_html_chart_code_data_v2_code_190k_1343"

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
    bash eval_scripts/auto_eval_merge_v2_large.sh "$model_name" 2>&1 | tee -a "$log_file"  
done  
  
python merge_result_2.py
cp all_scores_design2code_100.csv /mnt/lingjiejiang/multimodal_code/eval/Design2code/job/
cp -r saves/ /mnt/lingjiejiang/multimodal_code/eval/Design2code/job/
cp metrics/*.json /mnt/lingjiejiang/multimodal_code/eval/Design2code/job/metrics/
echo "run_gpu"
python run_gpu.py

echo "所有模型处理完成。" | tee -a "$log_file"  