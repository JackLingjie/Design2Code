import json  
import subprocess  
import os  
  
# Define paths  
image_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html/images/"  
json_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html/"  
json_output_path = os.path.join(json_output_dir, 'miss_item.json')  
  
# Ensure the image output directory exists  
os.makedirs(image_output_dir, exist_ok=True)  
  
# Load data from the file  
html_data_path = "/mnt/unilm/shaohanh/data/code/purehtml_v2.txt"  
miss_item = []  
  
with open(html_data_path, "r", encoding="utf-8") as f:  
    lines = f.readlines()  
    data = [json.loads(line) for line in lines]  
  
# Function to call the external script to convert HTML to an image  
def html_to_image_with_script(html_content, output_path):  
    try:  
        result = subprocess.run(  
            [  
                "python3",   
                "metrics/screenshot_single_filter.py",   
                "--content", html_content,   
                "--png", output_path  
            ],  
            check=True,  
            text=True,  
            capture_output=True  
        )  
        return f"Image saved at {output_path}"  
    except subprocess.CalledProcessError as e:  
        print(f"Command failed with error: {e.stderr}")  
        return None  
  
# Process each item  
for item in data:  
    html_content = item.get('text')  
    # Save image with the item ID as the filename in the specified directory  
    predict_img_path = os.path.join(image_output_dir, f"{item['id']}.png")  
      
    result = html_to_image_with_script(html_content, predict_img_path)  
      
    if result is None:  
        miss_item.append(item)  
  
# Save missed items to JSON in the specified directory  
with open(json_output_path, 'w', encoding='utf-8') as f:  
    json.dump(miss_item, f, ensure_ascii=False, indent=4)  
  
print(f"Processed {len(data)} items. Missed items saved to '{json_output_path}'.")  