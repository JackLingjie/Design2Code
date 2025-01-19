import json  
import subprocess  
import os  
import shutil  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from tqdm import tqdm  
  
data_file = "/mnt/lingjiejiang/multimodal_code/data/html_revised/final_output.json"
  
with open(data_file, 'r') as f:  
    split_data = json.load(f)  
  
def process_item(item):  
    # html_content = item['messages'][1]['content']  
    html_content = item["revised_html"]
    id = item["id"]  
    # 设置 HTML 文件和图片的路径  
    html_file_path = os.path.join('img_preview_revised/img_preview_rick', f"{id}.html")  
    predict_img_path = os.path.join('img_preview_revised/img_preview_rick', f"{id}.png")  
  
    # 确保目录存在  
    html_directory = os.path.dirname(html_file_path)  
    img_directory = os.path.dirname(predict_img_path)  
    os.makedirs(html_directory, exist_ok=True)  
    os.makedirs(img_directory, exist_ok=True)  
  
    # 如果图片已经存在，跳过处理  
    # if os.path.exists(predict_img_path):  
    #     return f"Image already exists at {predict_img_path}, skipping conversion."  
  
    # 将 HTML 内容写入文件  
    with open(html_file_path, 'w', encoding='utf-8') as html_file:  
        html_file.write(html_content)  
  
    # 如果目录是第一次创建，或者目录下没有 rick.jpg，则复制  
    rick_img_path = 'img_process/rick.jpg'  
    target_rick_path = os.path.join(img_directory, 'rick.jpg')  
    if not os.path.exists(target_rick_path):
        if os.path.exists(rick_img_path):
            shutil.copy(rick_img_path, target_rick_path)
    # if not os.path.exists(target_rick_path):  
    #     if os.path.exists(rick_img_path):  
    #         shutil.copy(rick_img_path, target_rick_path)  
  
    # 调用 screenshot_single.py 脚本以生成图片  
    try:  
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
                if result:  
                    print(result)  
            except Exception as exc:  
                print(f"Item generated an exception: {exc}")  
  
if __name__ == "__main__":  
    main()  