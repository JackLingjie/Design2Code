import os  
from tqdm import tqdm  
from concurrent.futures import ThreadPoolExecutor  
import json  
import random  
  
# 输入文件路径  
input_file = "/mnt/lingjiejiang/multimodal_code/data/Web2Code/Web2Code_sharegpt_format_abspath_filter.json"  

# 打开并加载原始数据  
with open(input_file, 'r') as f:  
    web2code_all_data = json.load(f) 

def check_item(item):  
    filename = item['images'][0]  
    if filename.endswith(".png"):  
        filename = filename.replace(".png", ".html")  
    elif filename.endswith(".jpg"):  
        filename = filename.replace(".jpg", ".html")  
    return not os.path.exists(filename)  
  
miss_item = []  
  
with ThreadPoolExecutor() as executor:  
    results = list(tqdm(executor.map(check_item, web2code_all_data), total=len(web2code_all_data)))  
  
miss_item = [item for item, missing in zip(web2code_all_data, results) if missing]  
  
len(miss_item)  
with open("metrics/miss_item.json", 'w') as f:  
    json.dump(miss_item, f, indent=2)