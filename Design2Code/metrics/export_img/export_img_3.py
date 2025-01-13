import json
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # 进度条库

# 机器 ID 变量
machine_id = 3  # 设置当前机器的 ID，例如 1

# 分片文件路径模板
split_file_template = "/mnt/lingjiejiang/multimodal_code/data/Web2Code/Web2Code_split_{}.json"

# 读取指定分片文件
split_file = split_file_template.format(machine_id)
with open(split_file, 'r') as f:
    split_data = json.load(f)

# 定义处理函数
def process_item(item):
    html_content = item['messages'][1]['content']
    image_path = item['images'][0]

    # 构造保存路径
    predict_img_path = os.path.join(
        '/mnt/lingjiejiang/multimodal_code/data/web2code_new_images',
        os.path.relpath(image_path, '/mnt/lingjiejiang/multimodal_code/data/Web2Code/')
    )

    # 如果图片已经存在，跳过处理
    if os.path.exists(predict_img_path):
        return f"Image already exists at {predict_img_path}, skipping conversion."

    # 确保目录存在
    os.makedirs(os.path.dirname(predict_img_path), exist_ok=True)

    # 调用 screenshot_single_filter.py 脚本以生成图片
    try:
        result = subprocess.run(
            ["python3", "metrics/screenshot_single_filter.py", "--content", html_content, "--png", predict_img_path],
            check=True,
            text=True,
            capture_output=True
        )
        return f"Image saved at {predict_img_path}"
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.stderr}"

# 使用 ThreadPoolExecutor 进行多线程处理
def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_item, item): item for item in split_data}

        # 使用 tqdm 显示进度条
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing items"):
            item = futures[future]
            try:
                result = future.result()
                # 打印保存结果或错误信息
                # print(result)
            except Exception as exc:
                print(f"Item generated an exception: {exc}")

if __name__ == "__main__":
    main()
