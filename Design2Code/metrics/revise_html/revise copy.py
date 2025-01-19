import json  
import os  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from tqdm import tqdm  
from gpt4o import Openai, API_INFOS  
  
# Define the new prompt template for HTML refactoring  
prompt_template = \
"""  
I will provide you with an HTML code snippet that needs a complete redesign to enhance its visual appeal and structure. Your task is to completely rewrite this HTML code, using modern web design principles to create an aesthetically pleasing and user-friendly layout.  
  
Requirements:  
1. Return a single HTML file using HTML and CSS to recreate the given website.  
2. Use "rick.jpg" as a placeholder for all images, ensuring they are properly sized and positioned for a professional look.  
3. Avoid any dependencies on external files, and do not include JavaScript. Focus solely on HTML and CSS for styling.  
4. Pay special attention to typography, spacing, and color schemes to create a harmonious and visually appealing design.  
5. Ensure the layout is responsive and fits well on a single page. Redesign the content if necessary to fit all information onto one page without scrolling.  
  
Below is the original HTML code. Please provide a completely redesigned HTML code following the specified format:  
  
## Original HTML:  
{RAW_HTML}  
  
## Reference Output Format:  
<|REVISED HTML BEGIN|>  
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mailcow: Dockerized Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f8f8;
        }
        .header {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 14px;
        }
        .header a {
            color: #1e90ff;
            text-decoration: none;
        }
        .navbar {
            background-color: #3b5998;
            color: white;
            display: flex;
            align-items: center;
            padding: 10px;
        }
        .navbar img {
            height: 30px;
            margin-right: 10px;
        }
        .navbar h1 {
            font-size: 18px;
            margin: 0;
            flex-grow: 1;
        }
        .navbar input {
            padding: 5px;
            margin-right: 10px;
        }
        .navbar a {
            color: white;
            text-decoration: none;
        }
        .content {
            display: flex;
            padding: 20px;
        }
        .sidebar {
            width: 200px;
            padding-right: 20px;
        }
        .sidebar ul {
            list-style-type: none;
            padding: 0;
        }
        .sidebar li {
            margin-bottom: 10px;
        }
        .sidebar a {
            color: #333;
            text-decoration: none;
        }
        .main-content {
            flex-grow: 1;
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .main-content h1 {
            font-size: 24px;
            color: #666;
        }
        .main-content h2 {
            font-size: 20px;
            color: #333;
            margin-top: 20px;
        }
        .main-content p {
            font-size: 14px;
            color: #333;
            line-height: 1.6;
        }
        .main-content a {
            color: #1e90ff;
            text-decoration: none;
        }
        .code-block {
            background-color: #f0f0f0;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
            font-size: 14px;
            overflow-x: auto;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #666;
            padding: 20px;
            background-color: #f0f0f0;
        }
    </style>
</head>
<body>
    <div class="header">
        All Commands are available according to the <a href="#">Docker Compose Plugin</a> and the <a href="#">Standalone Version</a> syntax
    </div>
    <div class="navbar">
        <img src="rick.jpg" alt="Logo">
        <h1>mailcow: dockerized documentation</h1>
        <input type="text" placeholder="Search">
        <a href="#">mailcow/mailcow-docke...</a>
    </div>
    <div class="content">
        <div class="sidebar">
            <ul>
                <li><strong>mailcow: dockerized documentation</strong></li>
                <li><a href="#">Information & Support</a></li>
                <li><a href="#">Prerequisites</a></li>
                <li><a href="#">Installation, Update & Migration</a></li>
                <li><a href="#">Post Installation Tasks</a></li>
            </ul>
        </div>
        <div class="main-content">
            <h1>Microsoft Outlook</h1>
            <h2>Outlook 2016 or higher from Office 365 on Windows</h2>
            <p>This is only applicable if your server administrator has not disabled EAS for Outlook. If it is disabled, please follow the guide for Outlook 2007 instead.</p>
            <p>Outlook 2016 has an <a href="#">issue with autodiscover</a>.</p>
            <div class="code-block">
                C:\Program Files (x86)\Microsoft Office\root\Office16\OLCFG.EXE
            </div>
            <p>For EAS you must use the old assistant by launching this application opens, you can go to step 4 of the guide for Outlook 2013 below.</p>
            <p>If it does not open, you can completely <a href="#">disable the new account creation wizard</a> and follow the guide for Outlook 2013 below.</p>
            <h2>Outlook 2007 or 2010 on Windows</h2>
            <ol>
                <li>Download and install <a href="#">Outlook CalDav Synchronizer</a>.</li>
                <li>Launch Outlook.</li>
                <li>If this is the first time you launched Outlook, it asks you to set up your account. Proceed to step 5.</li>
                <li>Go to the <em>File</em> menu and click <em>Add Account</em>.</li>
            </ol>
            <h2>Outlook 2013 or higher on Windows (Active Sync - not recommended)</h2>
            <p>This is only applicable if your server administrator has not disabled EAS for Outlook. If it is disabled, please follow the guide for Outlook 2007 instead.</p>
            <ol>
                <li>Launch Outlook.</li>
                <li>If this is the first time you launched Outlook, it asks you to set up your account. Proceed to step 4.</li>
                <li>Go to the <em>File</em> menu and click <em>Add Account</em>.</li>
                <li>Enter your name, email address and your password. Click <em>Next</em>.</li>
            </ol>
            <h2>Outlook 2011 or higher on macOS</h2>
            <p>The Mac version of Outlook does not synchronize calendars and contacts and therefore is not supported.</p>
            <p><em>Last update: 2022-02-16 15:23:03</em></p>
        </div>
    </div>
    <div class="footer">
        Copyright © 2023 mailcow Team & Community<br>
        Made with Material for MkDocs
    </div>
</body>
</html>
<|REVISED HTML END|>  
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
def get_revised_html(client, html_code, prompt_template, max_tokens=2048):  
    content = prompt_template.replace("{RAW_HTML}", html_code)
    # content = prompt_template.format(RAW_HTML="hello")  
    try:  
        gpt_answer, stop_reason = client.get_response(content=content, max_tokens=max_tokens)  
    except Exception as e:  
        print(f"Error calling GPT API: {e}")  
        return ""  
  
    if not gpt_answer:  
        return ""  
  
    revised_html = extract_revised_html(gpt_answer)  
    return gpt_answer, revised_html, stop_reason  
  
def extract_revised_html(gpt_answer):  
    start = gpt_answer.find("<|REVISED HTML BEGIN|>") + len("<|REVISED HTML BEGIN|>")  
    end = gpt_answer.find("<|REVISED HTML END|>", start)  
    return gpt_answer[start:end].strip() if start != -1 and end != -1 else ""  
  
# Process a single row of data  
def process_row(index, client, row, prompt_template, max_tokens=2048):  
    html_code = row['messages'][1]['content'].strip()  # Assuming HTML is in the second message  
    gpt_answer, revised_html, stop_reason = get_revised_html(client, html_code, prompt_template, max_tokens=max_tokens)  
  
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
    input_file = '/mnt/lingjiejiang/multimodal_code/data/Web2Code/Web2Code_onetrun_with_img.json'  
    output_dir = '/mnt/lingjiejiang/multimodal_code/data/html_revised'  
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
  
    final_file = os.path.join(output_dir, "final_output.json")  
    with open(final_file, 'w') as f:  
        json.dump(revised_data, f, indent=0)  
  
if __name__ == "__main__":  
    main()  