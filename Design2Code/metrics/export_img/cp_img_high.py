import json  
import os  
import shutil  
import random  
  
# Define paths  
image_output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html/images/"  
image_preview_dir = "image_preview_8/"  # Update with the actual path  
  
# Ensure the image_preview directory exists  
os.makedirs(image_preview_dir, exist_ok=True)  
  
# Load data from the file  
html_data_path = "metrics/export_img/high_score_data.json"  
  
with open(html_data_path, "r", encoding="utf-8") as f:  
    data = json.load(f)
  
# Randomly sample 50 items  
# sampled_data = random.sample(data, 50)  
sampled_data = data 
  
# Function to copy images  
def copy_image_to_preview(item):  
    item_id = item.get('id')  
    # predict_img_path = os.path.join(image_output_dir, f"{item_id}.png")  
    predict_img_path = item.get('images')
    # Copy existing image to image_preview directory if it exists  
    if os.path.exists(predict_img_path):  
        shutil.copy(predict_img_path, image_preview_dir)  
  
# Copy images for sampled data  
for item in sampled_data:  
    copy_image_to_preview(item)  
  
print("Copied images for 50 sampled items to the image_preview directory.")  