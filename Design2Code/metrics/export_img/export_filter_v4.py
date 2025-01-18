import json  
import subprocess  
import os  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from tqdm import tqdm  
  
# Define paths  
html_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html_v4/html_files/"  
image_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html_v4/images/"  
json_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html_v4/"  
json_output_path = os.path.join(json_output_dir, 'miss_item4.json')  
  
# Ensure the directories exist  
os.makedirs(html_output_dir, exist_ok=True)  
os.makedirs(image_output_dir, exist_ok=True)  
  
# Load data from the file  
html_data_path = "/mnt/unilm/shaohanh/data/code/purehtml_v4/merged.jsonl"  
miss_item = []  
  
with open(html_data_path, "r", encoding="utf-8") as f:  
    lines = f.readlines()  
    data = [json.loads(line) for line in lines]  

# data = data[:10]
# Function to call the external script to convert HTML file to an image  
def html_file_to_image(item):  
    html_content = item.get('text')  
    item_id = item.get('id')  
    html_file_path = os.path.join(html_output_dir, f"{item_id}.html")  
    predict_img_path = os.path.join(image_output_dir, f"{item_id}.png")  
      
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
        print(f"Command failed for item {item_id} with error: {e.stderr}")  
        return item  
  
    return None  
  
# Use ThreadPoolExecutor for multithreading  
with ThreadPoolExecutor(max_workers=8) as executor:  
    # Start the load operations and mark each future with its item  
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