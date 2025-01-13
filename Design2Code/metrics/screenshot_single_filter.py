import os  
from playwright.sync_api import sync_playwright  
import argparse  
from PIL import Image  
  
def take_screenshot_from_html_content(html_content, output_file="screenshot.png", do_it_again=False):  
    if os.path.exists(output_file) and not do_it_again:  
        print(f"{output_file} exists!")  
        return  
      
    try:  
        with sync_playwright() as p:  
            # Choose a browser, e.g., Chromium, Firefox, or WebKit  
            browser = p.chromium.launch()  
            page = browser.new_page()  
              
            # Set the HTML content of the page  
            page.set_content(html_content, timeout=60000)  
              
            # Take the screenshot  
            page.screenshot(path=output_file, full_page=True, animations="disabled", timeout=60000)  
            browser.close()  
    except Exception as e:  
        print(f"Failed to take screenshot due to: {e}. Generating a blank image.")  
        # Generate a blank image  
        img = Image.new('RGB', (1280, 960), color='white')  
        img.save(output_file)  
  
if __name__ == "__main__":  
    # Initialize the parser  
    parser = argparse.ArgumentParser(description='Generate a PNG from HTML content.')  
      
    # Define the arguments  
    parser.add_argument('--content', type=str, required=True, help='HTML content to render')  
    parser.add_argument('--png', type=str, required=True, help='Output PNG file path')  
      
    # Parse the arguments  
    args = parser.parse_args()  
      
    take_screenshot_from_html_content(args.content, args.png, do_it_again=True)  