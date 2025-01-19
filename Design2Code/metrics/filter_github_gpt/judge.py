import json  
import os  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from gpt4o_mini import Openai, API_INFOS  # Assuming you have this module for API calls  
from tqdm import tqdm  
import re

# Define the classification prompt  
prompt_template = """  
Please evaluate the aesthetic quality of the rendered HTML image based on the following considerations:  
  
1. Layout and Structure: Assess if the page layout is organized, balanced, and visually appealing. Consider the alignment of elements and use of space.  
2. Design Coherence: Evaluate if the design elements (such as colors, fonts, and graphics) are consistent and harmonious throughout the page.  
3. Readability and Accessibility: Check if the text is legible, well-structured, and easy to read. Consider if the page provides a good user experience across different devices.  
4. Content Appropriateness: Ensure that the content is relevant and free of errors. Non-English text should be minimal unless contextually appropriate.  
5. Overall Impression: Consider the overall visual appeal and professionalism of the page.  
  
If the page is overly long, cannot be displayed on a single screen, contains non-English text without context, or includes garbled text, a lower score should be given.  
  
Please provide a final score from 0 to 10 directly, where 0 indicates poor quality and 10 indicates excellent quality, formatted as follows: "Final Score: X". 
## HTML:
{}  

## Rendered HTML Image:
"""
prompt2 = \
"""
## Output Format: 
Final Score: 5

Your Answer:
"""  
  
# Load JSON data  
def load_data(file_path):  
    try:  
        with open(file_path, 'r') as f:  
            return json.load(f)  
    except Exception as e:  
        print(f"Error loading data from {file_path}: {e}")  
        return []  
  
# Call GPT API and parse response for scoring  
def get_image_score(client, html_content, image_path):  
    content = prompt_template.format(html_content)  
    try:  
        gpt_answer = client.get_image_response_v2(content=content, prompt2=prompt2, image=image_path, max_tokens=500)  
    except Exception as e:  
        print(f"Error calling GPT API: {e}")  
        return 0, ""  # Default to 0 and empty response if there's an error  
  
    # Use regex to extract score from GPT response  
    try:  
        # Adjust regex to match both formats: with or without brackets  
        match = re.search(r"Final Score: \[?(\d+)\]?", gpt_answer)  
        if match:  
            score = int(match.group(1))  
            return score, gpt_answer  
        else:  
            print("Score not found in response")  
            return 0, gpt_answer  
    except Exception as e:  
        print(f"Error extracting score: {e}")  
        return 0, gpt_answer  
    
# Process each item in the dataset  
def process_item(index, client, item):  
    html_content = item['text']  
    image_path = item['images']  
    score, gpt_response = get_image_score(client, html_content, image_path)  
  
    # Update item with score and raw GPT response  
    item['gpt4score'] = score  
    item['gptresponse'] = gpt_response  
    return item  
  
def main():  
    data_path = "/mnt/lingjiejiang/multimodal_code/data/github_html_v4/githubv4_img_rick.json"  
    output_dir = "/mnt/lingjiejiang/multimodal_code/data/github_html_v4/intermediate_results"  
    os.makedirs(output_dir, exist_ok=True)  
  
    data = load_data(data_path)  
    clients = [Openai(apis=[API_INFOS[i]]) for i in range(len(API_INFOS))]  
  
    revised_data = []  
    batch_size = 1000  # Save every 1000 items  
  
    with ThreadPoolExecutor(max_workers=len(clients)) as executor:  
        futures = [  
            executor.submit(process_item, i, clients[i % len(clients)], item)  
            for i, item in enumerate(data)  
        ]  
  
        for i, future in enumerate(tqdm(as_completed(futures), total=len(futures))):  
            revised_data.append(future.result())  
            if (i + 1) % batch_size == 0:  
                batch_number = (i + 1) // batch_size  
                intermediate_file = os.path.join(output_dir, f"intermediate_batch_{batch_number}.json")  
                with open(intermediate_file, 'w') as f:  
                    json.dump(revised_data, f, indent=2)  
                print(f"Saved batch {batch_number} to {intermediate_file}")  
  
    # Save the final results  
    final_file = os.path.join(output_dir, "final_output.json")  
    with open(final_file, 'w') as f:  
        json.dump(revised_data, f, indent=2)  
    print(f"Saved final results to {final_file}")  

  
if __name__ == "__main__":  
    main() 