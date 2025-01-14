import json  
import os  
  
# 机器 ID 变量  
machine_id = 6  # 设置当前机器的 ID，例如 1  
  
# 分片文件路径模板  
split_file_template = "/mnt/lingjiejiang/multimodal_code/data/Web2Code/Web2Code_split_{}.json"  
  
# 读取指定分片文件  
split_file = split_file_template.format(machine_id)  
with open(split_file, 'r') as f:  
    split_data = json.load(f)  
  
# 用于保存不存在图片的 item 的列表  
missing_items = []  
  
# 处理每个 item  
for item in split_data:  
    image_path = item['images'][0]  
      
    # 构造新的图片路径  
    predict_img_path = os.path.join(  
        '/mnt/lingjiejiang/multimodal_code/data/web2code_new_images',  
        os.path.relpath(image_path, '/mnt/lingjiejiang/multimodal_code/data/Web2Code/')  
    )  
  
    # 检查路径是否存在  
    if not os.path.exists(predict_img_path):  
        missing_items.append(item)  
  
# 将不存在图片的 item 保存到 JSON 文件  
missing_file = f"/mnt/lingjiejiang/multimodal_code/data/Web2Code/missing_items_machine_{machine_id}.json"  
with open(missing_file, 'w') as f:  
    json.dump(missing_items, f, ensure_ascii=False, indent=0)  
  
print(f"Missing items saved to {missing_file}")  
print(f"len Missing items {len(missing_items)}")