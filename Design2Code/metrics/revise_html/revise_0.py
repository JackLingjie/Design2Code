import json  
import os  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from tqdm import tqdm  
from gpt4o import Openai, API_INFOS  
import re  
# Define the new prompt template for HTML refactoring  

MACHINE_ID = 0

prompt_template = \
"""  
I will provide you with an HTML image. Please design a perfect HTML based on the style of this image.

Include all CSS code in the HTML file itself.
Please use "rick.jpg" as a placeholder for any images. 
Do not assume or include any dependencies on external files. There is no need to incorporate JavaScript for dynamic interactions. 
Ensure careful attention to details such as element sizes, text formatting, positioning, colors, and the overall layout. 
Ensure all content is fully visible within a single, non-scrollable screen, and delete or redesign any parts that exceed this boundary.
If the original style does not meet your needs, feel free to change it.

## HTML Image:
"""
prompt2 = \
"""
Your response should include the complete content of the HTML and CSS file:
"""  
  
# Load JSON data from a file  
def load_data(file_path):  
    try:  
        with open(file_path, 'r') as f:  
            return json.load(f)  
    except Exception as e:  
        print(f"Error loading data from {file_path}: {e}")  
        return []  
  
# Call GPT API and parse the response  
def get_revised_html(client, html_code, prompt_template, image_path, max_tokens=2048):  
    content = prompt_template.replace("{RAW_HTML}", html_code)
    # content = prompt_template.format(RAW_HTML="hello")  
    try:  
        gpt_answer, stop_reason = client.get_image_response_v2_raw(content=content, prompt2=prompt2, image=image_path, max_tokens=max_tokens)  
    except Exception as e:  
        print(f"Error calling GPT API: {e}")  
        return ""  
  
    if not gpt_answer:  
        return ""  
  
    revised_html = extract_revised_html(gpt_answer)  
    return gpt_answer, revised_html, stop_reason  
  
def extract_revised_html(gpt_answer):  
    try:  
        # Use regex to extract the HTML code between ```html and ```  
        match = re.search(r"```html(.*?)```", gpt_answer, re.DOTALL)  
        if match:  
            return match.group(1).strip()  
        else:  
            print("Revised HTML not found")  
            return ""  
    except Exception as e:  
        print(f"Error extracting revised HTML: {e}")  
        return ""  
# def extract_revised_html(gpt_answer):  
#     start = gpt_answer.find("<|REVISED HTML BEGIN|>") + len("<|REVISED HTML BEGIN|>")  
#     end = gpt_answer.find("<|REVISED HTML END|>", start)  
#     return gpt_answer[start:end].strip() if start != -1 and end != -1 else ""  
  
# Process a single row of data  
def process_row(index, client, row, prompt_template, max_tokens=2048):  
    html_code = row['messages'][1]['content'].strip()  # Assuming HTML is in the second message  
    image_path = row['images'][0] 
    gpt_answer, revised_html, stop_reason = get_revised_html(client, html_code, prompt_template, image_path, max_tokens=max_tokens)  
  
    result = {  
        'revised_html': revised_html,  
        'original_html': html_code,
        "gpt_answer": gpt_answer,
        "stop_reason": stop_reason,
        "model": "gpt4o"
    }  
    row.update(result)

    return row
  
def main():  
    # input_file = "/mnt/lingjiejiang/multimodal_code/data/Web2Code/Web2Code_onetrun_with_img_newimg.json"
    input_file = f'/mnt/lingjiejiang/multimodal_code/data/Web2Code/Web2Code_onetrun_with_img_newimg_split{MACHINE_ID}.json'
    output_dir = '/mnt/lingjiejiang/multimodal_code/data/html_revised_{MACHINE_ID}'  
    os.makedirs(output_dir, exist_ok=True)  
  
    data = load_data(input_file)  
    data = data[:10]  # Limit to 100 rows for testing
    clients = [Openai(apis=[API_INFOS[i]]) for i in range(len(API_INFOS))]  
    print(f"len(clients): {len(clients)}")  
    max_tokens = 2048  
    batch_size = 5000  
    revised_data = []  
  
    with ThreadPoolExecutor(max_workers=len(clients)) as executor:  
        futures = [  
            executor.submit(  
                process_row, i, clients[i % len(clients)], row, prompt_template, max_tokens  
            ) for i, row in enumerate(data)  
        ]  
  
        for i, future in enumerate(tqdm(as_completed(futures), total=len(futures))):  
            revised_data.append(future.result())  
            if (i + 1) % batch_size == 0:  
                batch_number = (i + 1) // batch_size  
                intermediate_file = os.path.join(output_dir, f"intermediate_batch_{batch_number}.json")  
                with open(intermediate_file, 'w') as f:  
                    json.dump(revised_data, f, indent=0)  
  
    final_file = os.path.join(output_dir, f"final_output_{MACHINE_ID}.json")  
    with open(final_file, 'w') as f:  
        json.dump(revised_data, f, indent=0)  
  
if __name__ == "__main__":  
    main()  