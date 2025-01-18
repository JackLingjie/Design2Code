import json  
import subprocess  
import os  
import shutil  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from tqdm import tqdm  
  
data_file = "img_process/with_img_sampled_data_cate.json"  
  
with open(data_file, 'r') as f:  
    split_data = json.load(f)  
  
def process_item(item):  
    html_content = item['messages'][1]['content']  
    image_path = item['images'][0]  
    id = item["id"]  
    predict_img_path = os.path.join(  
        '/mnt/lingjiejiang/multimodal_code/data/web2code_img_rick',  
        os.path.relpath(f"{id}.png")  
    )  
  
    if os.path.exists(predict_img_path):  
        return f"Image already exists at {predict_img_path}, skipping conversion."  
  
    # 确保目录存在  
    directory = os.path.dirname(predict_img_path)  
    was_created = not os.path.exists(directory)  
    os.makedirs(directory, exist_ok=True)  
  
    # 如果目录是第一次创建，或者目录下没有 rick.jpg，则复制  
    rick_img_path = 'img_process/rick.jpg'  
    target_rick_path = os.path.join(directory, 'rick.jpg')  
    if was_created or not os.path.exists(target_rick_path):  
        if os.path.exists(rick_img_path):  
            shutil.copy(rick_img_path, target_rick_path)  
  
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
  
def main():  
    with ThreadPoolExecutor(max_workers=5) as executor:  
        futures = {executor.submit(process_item, item): item for item in split_data}  
  
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing items"):  
            item = futures[future]  
            try:  
                result = future.result()  
            except Exception as exc:  
                print(f"Item generated an exception: {exc}")  
  
if __name__ == "__main__":  
    main()  