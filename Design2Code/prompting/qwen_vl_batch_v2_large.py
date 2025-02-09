import os
from tqdm import tqdm
from Design2Code.data_utils.screenshot import take_screenshot
from gpt4v_utils import cleanup_response, encode_image, gpt_cost, extract_text_from_html, index_text_from_html
import json
from openai import OpenAI, AzureOpenAI
import argparse
import retry
import shutil 
from gpt_azure import API_INFOS, Openai
import base64
from io import BytesIO
from PIL import Image

def open_model_call(model, image_file, prompt):
    # model="gpt-4o"
    image_data = base64.b64decode(image_file)  
    img = Image.open(BytesIO(image_data))
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": img,
                    "min_pixels": 224 * 224,  
                    "max_pixels": 1280 * 28 * 28,  
                },
                {
                    "type": "text", 
                    "text": prompt
                }
            ],
        }
    ]
    max_tokens=4096
    temperature=0.0
    response = ""
    response = model.generate(messages=messages, temperature=temperature, max_tokens=max_tokens)
    response = cleanup_response(response)

    return response

def open_model_call_batch(model, image_files, prompt):  
    # Convert images to base64 and prepare them for batch processing  
    images_data = []  
    for image_file in image_files:  
        image_data = base64.b64decode(image_file)  
        img = Image.open(BytesIO(image_data))  
        images_data.append(img)  
  
    # Prepare messages for each image with the same prompt  
    messages = [  
        [  
            {  
                "role": "user",  
                "content": [  
                    {  
                        "type": "image",  
                        "image": img,  
                        "min_pixels": 224 * 224,  
                        "max_pixels": 1280 * 28 * 28,  
                    }, 
                    {"type": "text", "text": prompt},  
                ]
            }  
        ] for img in images_data  
    ]  
      
    max_tokens = 4096  
    temperature = 0.0  
    responses = model.batch_generate(messages=messages, temperature=temperature, max_tokens=max_tokens)  
    cleaned_responses = [cleanup_response(response) for response in responses]  
    return cleaned_responses  

def direct_prompting_batch(openai_client, image_files):  
    '''  
    {original input images + prompt} -> {output htmls}  
    '''  
    # The prompt  
    ## the prompt 

    direct_prompt = ""
    direct_prompt += "You are an expert web developer who specializes in HTML and CSS.\n"
    direct_prompt += "A user will provide you with a screenshot of a webpage.\n"
    direct_prompt += "You need to return a single html file that uses HTML and CSS to reproduce the given website.\n"
    direct_prompt += "Include all CSS code in the HTML file itself.\n"
    direct_prompt += "If it involves any images, use \"rick.jpg\" as the placeholder.\n"
    direct_prompt += "Some images on the webpage are replaced with a blue rectangle as the placeholder, use \"rick.jpg\" for those as well.\n"
    direct_prompt += "Do not hallucinate any dependencies to external files. You do not need to include JavaScript scripts for dynamic interactions.\n"
    direct_prompt += "Pay attention to things like size, text, position, and color of all the elements, as well as the overall layout.\n"
    direct_prompt += "Respond with the content of the HTML+CSS file:\n"
  
    # Encode images  
    base64_images = [encode_image(image_file) for image_file in image_files]  
  
    # Call GPT-4V  
    htmls = open_model_call_batch(openai_client, base64_images, direct_prompt)  
    return htmls  

def direct_prompting(openai_client, image_file):
    '''
    {original input image + prompt} -> {output html}
    '''

    ## the prompt 
    direct_prompt = ""
    direct_prompt += "You are an expert web developer who specializes in HTML and CSS.\n"
    direct_prompt += "A user will provide you with a screenshot of a webpage.\n"
    direct_prompt += "You need to return a single html file that uses HTML and CSS to reproduce the given website.\n"
    direct_prompt += "Include all CSS code in the HTML file itself.\n"
    direct_prompt += "If it involves any images, use \"rick.jpg\" as the placeholder.\n"
    direct_prompt += "Some images on the webpage are replaced with a blue rectangle as the placeholder, use \"rick.jpg\" for those as well.\n"
    direct_prompt += "Do not hallucinate any dependencies to external files. You do not need to include JavaScript scripts for dynamic interactions.\n"
    direct_prompt += "Pay attention to things like size, text, position, and color of all the elements, as well as the overall layout.\n"
    direct_prompt += "Respond with the content of the HTML+CSS file:\n"
    
    ## encode image 
    base64_image = encode_image(image_file)

    ## call GPT-4V
    html = open_model_call(openai_client, base64_image, direct_prompt)

    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt_method', type=str, default='text_augmented_prompting', help='prompting method to be chosen from {direct_prompting, text_augmented_prompting, revision_prompting, layout_marker_prompting}')
    parser.add_argument('--orig_output_dir', type=str, default='gpt4o_text_augmented_prompting', help='directory of the original output that will be further revised')
    parser.add_argument('--file_name', type=str, default='all', help='any particular file to be tested')
    parser.add_argument('--subset', type=str, default='testset_100', help='evaluate on the full testset or just a subset (choose from: {testset_100, testset_full})')
    parser.add_argument('--take_screenshot', action="store_true", help='whether to render and take screenshot of the webpages')
    parser.add_argument('--auto_insertion', type=bool, default=False, help='whether to automatically insert texts into marker positions')
    parser.add_argument("--model_type", type=str, default="qwen2vl", help="test model type.")
    parser.add_argument("--model_name", type=str, default="Qwen2-VL-7B-Instruct", help="test model name.")
    parser.add_argument("--model_path", type=str, default="/mnt/lingjiejiang/textual_aesthetics/model_checkpoint/vlm_checkpoints/Qwen2-VL-7B-Instruct", help="test model path.")

    args = parser.parse_args()

    if args.model_type == "qwen2vl":
        from Design2Code.models.vllm_qwen_large import VllmModel
        model = VllmModel(args.model_path)

    test_data_dir = "testset_final"
    cache_dir = "./saves/"

    if args.model_type == "qwen2vl":
        from Design2Code.models.vllm_qwen_large import VllmModel
        model = VllmModel(args.model_path)
    
    ## create cache directory if not exists
    os.makedirs(predictions_dir, exist_ok=True)
    shutil.copy(test_data_dir + "/rick.jpg", os.path.join(predictions_dir, "rick.jpg"))
    
    test_files = []
    if args.file_name == "all":
        test_files = [item for item in os.listdir(test_data_dir) if item.endswith(".png") and "_marker" not in item]
    else:
        test_files = [args.file_name]
    print(f"predictions_dir:{predictions_dir}")

    # Process files in batches  
    batch_size = 32  # Adjust the batch size as necessary  
    for i in range(0, len(test_files), batch_size):  
            batch_files = test_files[i:i + batch_size] 
            try:
                if args.prompt_method == "direct_prompting":  
                    htmls = direct_prompting_batch(model, [os.path.join(test_data_dir, f) for f in batch_files])   
                    for filename, html in zip(batch_files, htmls):  
                        output_filename = os.path.join(predictions_dir, os.path.basename(filename).replace(".png", ".html"))  
                        with open(output_filename, "w", encoding="utf-8") as f:  
                            f.write(html)  
                        print(f'file saved to {output_filename}')  
                        if args.take_screenshot:  
                            take_screenshot(output_filename, output_filename.replace(".html", ".png"), do_it_again=True)  
            except Exception as e:  
                print(f"An error occurred during processing: {e}")  
                continue



