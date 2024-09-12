import os

import openai
openai.api_key = os.getenv('OPENAI_API_KEY_NEW')

class GPT:

    model = 'text-ada-001'
    inference_parameters = {
        "temperature" : 0.6,
        "max_tokens" : 200,
        "top_p" : 1,
        "frequency_penalty" : 0.4,
        "presence_penalty" : 0.2,
        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
    }
    
    def __init__(self, model) -> None:
        self.model =  model if model else self.model
        
    def completion(self, user_content):
        return openai.Completion.create(
                    model = self.model,
                    prompt = user_content,
                    **self.inference_parameters
                )
    
    def extract_result(self, response):
        return response['choices'][0]['text']