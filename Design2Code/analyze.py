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
            current_res = np.mean(np.array(values), axis=0)  
            res = get_score(current_res)  
            all_scores[key_name] = res  
  
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
  
# Save the DataFrame to a CSV file  
df.to_csv('all_scores_design2code.csv', index=True)  
  
print("Results saved to all_scores.csv")  