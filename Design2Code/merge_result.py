import os  
import json  
import numpy as np  
import pandas as pd  
  
def get_score(multi_score):  
    _, final_size_score, final_matched_text_score, final_position_score, final_text_color_score, final_clip_score = multi_score  
    res = {  
        "Block-Match": final_size_score,  
        "Text": final_matched_text_score,  
        "Position": final_position_score,  
        "Color": final_text_color_score,  
        "CLIP": final_clip_score  
    }  
    return res  
  
all_scores = {}  
  
# Directory containing JSON files  
metrics_dir = 'metrics'  
  
# Iterate through all files in the metrics directory  
for filename in os.listdir(metrics_dir):  
    if filename.startswith('res_dict_') and filename.endswith('.json'):  
        file_path = os.path.join(metrics_dir, filename)  
        with open(file_path) as f:  
            data = json.load(f)  
          
        # Extract key name from filename  
        key_name = filename[len('res_dict_'):-len('.json')]  
          
        for key, value in data.items():  
            values = list(value.values())  
            if len(values) == 0:  
                print(f"Warning: The list 'values' is empty for key {key} in file {filename}.")  
                continue  
            try:  
                current_res = np.mean(np.array(values), axis=0)  
                if not isinstance(current_res, (list, np.ndarray)):  
                    print(f"Warning: 'current_res' is not iterable for key {key} in file {filename}.")  
                    continue  
                res = get_score(current_res)  
                all_scores[key_name] = res  
            except Exception as e:  
                print(f"Error processing key {key} in file {filename}: {e}")  
  
# Convert all_scores to a DataFrame  
df = pd.DataFrame.from_dict(all_scores, orient='index')  
  
# Calculate the mean of the first four columns and then the overall average with "CLIP"  
df['Intermediate Average'] = df[['Block-Match', 'Text', 'Position', 'Color']].mean(axis=1)  
df['Weighted Average'] = (df['Intermediate Average'] + df['CLIP']) / 2  
  
# Calculate the direct average of all columns  
df['Direct Average'] = df[['Block-Match', 'Text', 'Position', 'Color', 'CLIP']].mean(axis=1)  
  
# Reorder columns to place 'Weighted Average' and 'Direct Average' as the first columns  
columns = ['Weighted Average', 'Direct Average'] + [col for col in df.columns if col not in ['Weighted Average', 'Direct Average']]  
df = df[columns]  
  
df_sorted = df.sort_values(by='Direct Average', ascending=False)
# Save the DataFrame to a CSV file  
df_sorted.to_csv('all_scores_design2code.csv', index=True)  
  
print("Results saved to all_scores_design2code.csv")  