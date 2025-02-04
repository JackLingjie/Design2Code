import json  
import subprocess  
import os  
import shutil  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from tqdm import tqdm  
  
# Define paths  
# html_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html_v4/new_images"  
# image_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html_v4/new_images"  
# 机器 ID 变量
machine_id = 2  # 设置当前机器的 ID，例如 1

# 分片文件路径模板
split_file_template = "/mnt/lingjiejiang/multimodal_code/data/dpo/html/qwen2-72b/qwen72b_html_91k_split{}.json"

json_output_dir = "/mnt/lingjiejiang/multimodal_code/data/dpo/html/qwen2-72b/"  
json_output_path = os.path.join(json_output_dir, f'miss_item_revised_v{machine_id}.json')  
  
# Ensure the directories exist  
# os.makedirs(html_output_dir, exist_ok=True)  
# os.makedirs(image_output_dir, exist_ok=True)  
  
# Load data from the file  
html_data_path = split_file_template.format(machine_id)
print(html_data_path)
print(json_output_path)
miss_item = []  
  
with open(html_data_path, "r", encoding="utf-8") as f:  
    data = json.load(f)

# data = data[:10]

def html_file_to_image(item):  
    html_content = item.get('code_extract')  
    predict_img_path = item.get('mimic_image')  
    html_file_path = predict_img_path.replace('png', 'html')  
    # Ensure directories exist  
    html_directory = os.path.dirname(html_file_path)  
    img_directory = os.path.dirname(predict_img_path)  
    os.makedirs(html_directory, exist_ok=True)  
    os.makedirs(img_directory, exist_ok=True)  
      
    # Check and copy rick.jpg if not exists  
    rick_img_path = 'img_process/rick.jpg'  
    target_rick_path = os.path.join(img_directory, 'rick.jpg')  
    if not os.path.exists(target_rick_path):  
        if os.path.exists(rick_img_path):  
            shutil.copy(rick_img_path, target_rick_path)  
  
    # Skip conversion if the image already exists  
    if os.path.exists(predict_img_path):  
        return None  
  
    # Write HTML content to file  
    with open(html_file_path, 'w', encoding='utf-8') as html_file:  
        html_file.write(html_content)  
  
    try:  
        # Convert HTML file to image  
        subprocess.run(  
            [  
                "python3",  
                "metrics/screenshot_single.py",  
                "--html", html_file_path,  
                "--png", predict_img_path  
            ],  
            check=True,  
            text=True,  
            capture_output=True  
        )  
    except subprocess.CalledProcessError as e:  
        print(f"Command failed for item {predict_img_path} with error: {e.stderr}")  
        return item  
  
    return None  
  
# Use ThreadPoolExecutor for multithreading  
with ThreadPoolExecutor(max_workers=8) as executor:  
    future_to_item = {executor.submit(html_file_to_image, item): item for item in data}  
    for future in tqdm(as_completed(future_to_item), total=len(data), desc="Processing HTML files"):  
        item = future_to_item[future]  
        try:  
            result = future.result()  
            if result is not None:  
                miss_item.append(result)  
        except Exception as exc:  
            print(f"Item {item['id']} generated an exception: {exc}")  
            miss_item.append(item)  
  
# Save missed items to JSON in the specified directory  
with open(json_output_path, 'w', encoding='utf-8') as f:  
    json.dump(miss_item, f, ensure_ascii=False, indent=4)  
  
print(f"Processed {len(data)} items. Missed items saved to '{json_output_path}'.")  