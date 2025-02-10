import requests  
from PIL import Image  
from io import BytesIO  
import base64  
from transformers import AutoProcessor  
from qwen_vl_utils import process_vision_info  
from vllm import LLM, SamplingParams  
import os  
  
class VllmModel:  
    def __init__(self, model_path, max_image=1):  
        self.llm = LLM(  
            model=model_path,  
            trust_remote_code=True,
            limit_mm_per_prompt={"image": max_image},  
            tensor_parallel_size=4
        )  
        self.tokenizer = self.llm.get_tokenizer()  
        self.model_path = model_path  
        self.processor = AutoProcessor.from_pretrained(self.model_path) 
    def get_response(self, query, image_source, temperature=0.9, max_tokens=2048, top_p=0.95, repetition_penalty=1.05):  
        sampling_params = SamplingParams(  
            temperature=temperature,  
            top_p=top_p,  
            repetition_penalty=repetition_penalty,  
            max_tokens=max_tokens,  
            stop_token_ids=[self.tokenizer.eos_token_id],  
        )  
  
        messages = [  
            {"role": "system", "content": "You are a helpful assistant."},  
            {  
                "role": "user",  
                "content": [  
                    {  
                        "type": "image",  
                        "image": image_source,  
                        "min_pixels": 224 * 224,  
                        "max_pixels": 1280 * 28 * 28,  
                    },  
                    {"type": "text", "text": query},  
                ],  
            },  
        ]  
  
        processor = AutoProcessor.from_pretrained(self.model_path)  
        prompt = processor.apply_chat_template(  
            messages,  
            tokenize=False,  
            add_generation_prompt=True,  
        )  
  
        image_inputs, video_inputs = process_vision_info(messages)  
        mm_data = {}  
        if image_inputs is not None:  
            mm_data["image"] = image_inputs  
        if video_inputs is not None:  
            mm_data["video"] = video_inputs  
  
        llm_inputs = {  
            "prompt": prompt,  
            "multi_modal_data": mm_data,  
        }  
        outputs = self.llm.generate([llm_inputs], sampling_params=sampling_params)  
        generated_text = outputs[0].outputs[0].text  
        return generated_text  

    def generate(self, messages, temperature=0.9, max_tokens=2048, top_p=0.95, repetition_penalty=1.05):  
        
        sampling_params = SamplingParams(  
            temperature=temperature,  
            top_p=top_p,  
            repetition_penalty=repetition_penalty,  
            max_tokens=max_tokens,  
            stop_token_ids=[self.tokenizer.eos_token_id],  
        )  

         
        prompt = self.processor.apply_chat_template(  
            messages,  
            tokenize=False,  
            add_generation_prompt=True,  
        )  

        image_inputs, video_inputs = process_vision_info(messages)  
        mm_data = {}  
        if image_inputs is not None:  
            mm_data["image"] = image_inputs  
        if video_inputs is not None:  
            mm_data["video"] = video_inputs  

        llm_inputs = {  
            "prompt": prompt,  
            "multi_modal_data": mm_data,  
        }  
        outputs = self.llm.generate([llm_inputs], sampling_params=sampling_params)  
        generated_text = outputs[0].outputs[0].text  
        return generated_text  
 
    def batch_generate(self, messages, temperature=0.9, max_tokens=2048, top_p=0.95, repetition_penalty=1.05):  
        sampling_params = SamplingParams(  
            temperature=temperature,  
            top_p=top_p,  
            repetition_penalty=repetition_penalty,  
            max_tokens=max_tokens,  
            stop_token_ids=[self.tokenizer.eos_token_id],  
        )  

        # processor = AutoProcessor.from_pretrained(self.model_path)  
        prompts = []
        for mess in messages:
            prompt = self.processor.apply_chat_template(  
                mess,  
                tokenize=False,  
                add_generation_prompt=True,  
            )  
            prompts.append(prompt)
        # prompt = processor.apply_chat_template(  
        #     messages,  
        #     tokenize=False,  
        #     add_generation_prompt=True,  
        # )  
        mm_datas = []
        for mess in messages:
            image_inputs, video_inputs = process_vision_info(mess)  
            mm_data = {}  
            if image_inputs is not None:  
                mm_data["image"] = image_inputs  
            if video_inputs is not None:  
                mm_data["video"] = video_inputs  
            mm_datas.append(mm_data)

        llm_inputs = [{"prompt": prompt, "multi_modal_data": mm_data} for prompt, mm_data in zip(prompts, mm_datas)]

        # llm_inputs = {  
        #     "prompt": prompt,  
        #     "multi_modal_data": mm_data,  
        # }  
        outputs = self.llm.generate(llm_inputs, sampling_params=sampling_params)  
        generated_texts = [output.outputs[0].text for output in outputs]
        # generated_text = outputs[0].outputs[0].text  
        return generated_texts 
       
if __name__ == '__main__':  
    MODEL_PATH = "/mnt/lingjiejiang/multimodal_code/checkpoints/llms/Qwen2-VL-72B-Instruct"  
    model = VllmModel(MODEL_PATH)  
    query = "What is the text in the image?"  
    image_source = "https://modelscope.oss-cn-beijing.aliyuncs.com/resource/qwen.png"  
    response = model.get_response(query, image_source)  
    print(response)  