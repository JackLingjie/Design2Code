from visual_score_filter import visual_eval_v3_multi, visual_eval_v4_multi
from multiprocessing import Pool
import contextlib, joblib
from joblib import Parallel, delayed
from tqdm import tqdm
import numpy as np
import json
import os
import shutil
import argparse

@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def print_multi_score(multi_score):
    _, final_size_score, final_matched_text_score, final_position_score, final_text_color_score, final_clip_score = multi_score
    print()
    print("Block-Match: ", final_size_score)
    print("Text: ", final_matched_text_score)
    print("Position: ", final_position_score)
    print("Color: ", final_text_color_score)
    print("CLIP: ", final_clip_score)
    print("--------------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate code for problems.")
    parser.add_argument("--eval_name", type=str, default="qwenvl2_direct_prompting", help="Model to eavl")    
    parser.add_argument("--data_path", type=str, default="saves/Llama-3.2-11B-Vision-Instruct_batch_direct_prompting", help="eval data path")    
    args = parser.parse_args()

    debug = False
    multiprocessing = True

    orig_reference_dir = "testset_final"
    # eval_name = "qwenvl2_direct_prompting"
    eval_name = args.eval_name
    ## copy the original reference directory to a new directory
    ## because we will be creating new screenshots
    reference_dir = "testset_final" + eval_name
    reference_dir = "Web2Code"
    # os.makedirs(reference_dir, exist_ok=True)
    # for filename in os.listdir(orig_reference_dir):
    #     if filename.endswith(".html") or filename == "rick.jpg":
    #         shutil.copy(os.path.join(orig_reference_dir, filename), os.path.join(reference_dir, filename))
    # print ("copied original reference directory to ", reference_dir)

    # test_dirs = {
    #     # "gpt4o_direct_prompting": "saves/gpt4o_direct_prompting",
    #     # "qwenvl2_direct_prompting": "saves/Qwen2-VL-7B-Instruct_direct_prompting",
    #     eval_name: args.data_path,
    #     # ""
    #     # "gemini_direct_prompting": "../predictions_final/gemini_direct_prompting"
    # }
    test_dirs = {
        "webcode_filter": "webcode_test",
    }
    web2code_path = "/mnt/lingjiejiang/multimodal_code/data/Web2Code/Web2Code_sharegpt_format_abspath_filter.json"
    with open(web2code_path, "r") as f:
        data = json.load(f)
    data = data[:5]
    file_name_list = []

    prefix_to_remove = "/mnt/lingjiejiang/multimodal_code/data/Web2Code/" 
    for item in tqdm(data):
        filename = item['images'][0]
        filename = filename[len(prefix_to_remove):]
        # if filename.endswith(".png"):
        #     filename = filename.replace(".png", ".html")
        #     file_name_list.append(filename)
        # item["original_img"] = item['images'][0]
        item["original_img"] = f"img_test/{filename}"
        
        item["predict_filename"] = f"predict/{filename}"
        # item[""]
    # ## check if the file is in all prediction directories
    # for filename in os.listdir(reference_dir):
    #     if filename.endswith(".html"):
    #         if all([os.path.exists(os.path.join(test_dirs[key], filename)) for key in test_dirs]):
    #             file_name_list.append(filename)

    print ("total #egs: ", len(data))

    # input_lists = []
    # for item in data:
    #     filename = item["filename"]
    #     input_pred_list = [os.path.join(test_dirs[key], filename) for key in test_dirs]
    #     # input_pred_list = [os.path.join(test_dirs[key], filename), filename]
    #     full_dir_path = os.path.dirname(input_pred_list[0])
    #     # Create the directory if it does not exist  
    #     os.makedirs(full_dir_path, exist_ok=True)  
    #     item["predict_filename"] = input_pred_list[0]
    #     # original = os.path.join(reference_dir, filename)
    #     # input_pred_list = [filename]
    #     original = filename
    #     input_list = [input_pred_list, original]
    #     input_lists.append(input_list)

    # print ("input_list: ", input_lists)
    if multiprocessing:
        with tqdm_joblib(tqdm(total=len(data))) as progress_bar:
            return_score_lists = list(tqdm(Parallel(n_jobs=8)(delayed(visual_eval_v4_multi)(item, debug=debug) for item in data), total=len(data)))
    else:
        return_score_lists = []
        for item in tqdm(data):
            return_score_list = visual_eval_v4_multi(item, debug=debug)
            return_score_lists.append(return_score_list)
        # print ("return lists: ", return_score_lists)
    
    res_dict = {}
    for key in test_dirs:
        res_dict[key] = {}

    for i, item in enumerate(data):
        filename = item["original_img"]
        idx = 0
        return_score_list = return_score_lists[i]
        # print ("return score list: ", return_score_list)
        if return_score_list:
            for key in test_dirs:
                if multiprocessing:
                    matched, final_score, multi_score = return_score_list[idx]
                else:
                    matched = return_score_list[idx][0]
                    final_score = return_score_list[idx][1]
                    multi_score = return_score_list[idx][2]
                idx += 1
                current_score = [final_score] + [item for item in multi_score]
                res_dict[key][filename] = current_score
        else:
            print (filename + " didn't get a score")
            for key in test_dirs:
                res_dict[key][filename] = [0, 0, 0, 0, 0, 0]

    ## cache all scores 
    with open("metrics/web2code_filter_{}.json".format(eval_name), "w") as f:
        json.dump(res_dict, f, indent=4)

    for key in test_dirs:
        print(key)
        values = list(res_dict[key].values())
        # print (values)
        current_res = np.mean(np.array(values), axis=0)
        # print(current_res)
        print_multi_score(current_res)