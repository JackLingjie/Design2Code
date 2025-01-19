import json  
import os  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from gpt4o_mini import Openai, API_INFOS  # Assuming you have this module for API calls  
from tqdm import tqdm  
import re

# Define the classification prompt  
prompt_template = \
"""  
I will provide you with an HTML code snippet that may not be visually appealing and lacks proper structure. Your task is to refactor this HTML code to make it more visually attractive and modern.  
  
Requirements:  
1. Return a single HTML file using HTML and CSS to recreate the given website.  
2. If there are any images, use "rick.jpg" as a placeholder and ensure that all images have appropriate size and positioning styles.  
3. Do not create any dependencies on external files, and do not include JavaScript scripts for dynamic interactions.  
4. Pay attention to the size, text, position, and color of all elements, as well as the overall layout, ensuring a harmonious and aesthetically pleasing design.  
5. Ensure the entire content can be displayed on a single page. If the original content is too extensive, redesign the layout to fit a single page display.  
6. Use semantic HTML tags to improve code readability and maintainability.  
7. Include CSS at the top or bottom of the page using the `<style>` tag.  
8. Apply responsive design principles to ensure good display across different devices.  
  
Below is the original HTML code. Please provide the modified HTML code following the specified format:  
  
## Original HTML:  
{RAW_HTML}  
  
## Reference Output Format:  
<|REVISED HTML BEGIN|>  
<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Heyevent</title>
<style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
            color: #333;
        }
        h1 {
            font-size: 24px;
            color: #007bff;
            margin-bottom: 10px;
        }
        p {
            line-height: 1.6;
            margin-bottom: 20px;
        }
        .blue-rectangle {
            width: 100%;
            height: 4px;
            background-color: #007bff;
            margin: 20px 0;
        }
        .projects {
            margin-top: 20px;
        }
        .project {
            margin-bottom: 10px;
        }
        .project a {
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
        }
        .project a:hover {
            text-decoration: underline;
        }
        .project-description {
            margin-left: 10px;
            color: #555;
        }
        .placeholder-image {
            width: 100%;
            height: 200px;
            background-image: url('rick.jpg');
            background-size: cover;
            background-position: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
<h1>Heyevent</h1>
<div class="blue-rectangle"></div>
<p>Heyevent was at one point the world's most popular event recommendation service with 600k+ registered users. We fetched events from Facebook and sent out weekly personal recommendations for upcoming events.</p>
<p>Unfortunately, due to newly imposed limitations of the Facebook API, as well as expensive hosting costs and dwindling traffic, we've had to close down Heyevent and move on to new projects. Below are links to some other projects.</p>
<div class="projects">
<div class="project">
<a href="#">Roni</a>
<span class="project-description">A fun mobile word game for iOS and Android.</span>
</div>
<div class="project">
<a href="#">Locust: Load testing tool</a>
<span class="project-description">Locust is a widely used load testing tool. It's also Open Source.</span>
</div>
<div class="project">
<a href="#">Heyman.info</a>
<span class="project-description">My personal website.</span>
</div>
<div class="project">
<a href="#">Hotel Websites</a>
<span class="project-description">Comprehensive guides to the best boutique hotels, luxury hotels, spa hotels and bed &amp; breakfasts around the world.</span>
</div>
</div>
<div class="placeholder-image"></div>
</body>
</html>
<|REVISED HTML END|>  
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