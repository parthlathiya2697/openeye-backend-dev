import os
from server.utils.classes.openai.GPT import GPT
from server.utils.io import readTextFile
from config import BASE_DIR
from server.models.responses import ErrorResponseModel

class Completion(GPT):

    def __init__(self, model, tag):
        super().__init__(model)
        self.tag = tag

    def set_params(self, **kwargs):
        self.inference_parameters.update(kwargs)

    def rephrase(self, content):
        
        if self.tag == "fewshots":
            # Read fewshots text file
            try:
                prompt_filename = 'rephrase.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
    
            prompt = examples + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "instructions":
            prompt = "Paraphrase the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Paraphrase the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def summeriser(self, content):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'summeriser.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n###\n\nContent: " + content + "\n\n***\n\nSummary:"
            response = self.completion(prompt)
        elif self.tag == "instructions":
            prompt = "Summarise the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Summarise the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def email_writer(self, content):
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'email_writer.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n###\n\nContent: " + content + "\n***\Email:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Write an Email using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Write an Email using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def tagline_generator(self, content):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'tagline_generator.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n###\n\nDescription: " + content + "\n***\Tagline:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate a Tagline using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate a Tagline using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def blogpost_outline(self, content):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'blogpost_outline.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n###\Topic: " + content + "\n\n***\n\nOutlines:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate Blogpost Outlines using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate Blogpost Outlines using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def blogpost_hashtags(self, content):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'blogpost_hashtags.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n\n###\n\n\Description: " + content + "\n***\Hashtags:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate Blogpost Hashtags using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate Blogpost Hashtags using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def headline_generator(self, content):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'headline_generator.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n\n###\n\n\Description: " + content + "\n***\Headline:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate Interesting Headlines using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate Interesting Headlines using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def sentence_expander(self, content):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'sentence_expander.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n###\n\nSentence: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Rewrite and Expand using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Rewrite and Expand using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)

    def product_description(self, content, content2= ''):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'product_description.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n###\n\nProduct Name: " + content + "\nProduct Characteristics: " + content2 + "\n***\Product Description:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate a Product Description using the below-given Content" + "\n\n###\n\n Product Name: " + content + "Product Description: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate a Product Description using the below-given Content" + "\n\n###\n\n Product Name: " + content + "Product Description: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def creative_story(self, content, content2= ''):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'creative_story.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
            
            prompt = examples + "\n\n###\n\nTitle: " + content + "\nDescription: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Create a story using the below-given Content" + "\n\n###\n\nTitle: " + content + "\nDescription: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Create a story using the below-given Content" + "\n\n###\n\nTitle: " + content + "\nDescription: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)
    
    def poem(self, content, content2= ''):
        
        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'poem.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
                
            prompt = examples + "\n\n###\n\nTitle: " + content + "\nKeywords: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate a Poem using the below-given Content" + "\n\n###\n\nTitle: " + content + "\nKeywords: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate a Poem using the below-given Content" + "\n\n###\n\nTitle: " + content + "\nKeywords: " + content2 + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
            
        return self.extract_result(response)

    def intro(self, content):

        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'article_intro.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
                
            prompt = examples + "\n\n###\n\nTitle: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate a Introduction using the below-given Content" + "\n\n###\n\Title: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate a Introduction using the below-given Content" + "\n\n###\n\Title: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)

        prompt = f'{content}\n\n***\n\n'
        response = self.completion(prompt)
        return self.extract_result(response)

    def outlines(self, content):

        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'poem.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
                
            prompt = examples + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate Outlines using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate Outlines using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)

        prompt = f'{content}\n\n***\n\n'
        response = self.completion(prompt)
        return self.extract_result(response)

    def outlines_generated(self, content):

        if self.tag == "fewshots":
            
            # Read fewshots text file
            try:
                prompt_filename = 'poem.prompt'
                examples = readTextFile( os.path.join(BASE_DIR, 'server', 'prompts', prompt_filename) )
            except Exception as err:
                return ErrorResponseModel(f'{err}', 500, "Problems reading server files, Please try again sometime later.")
                
            prompt = examples + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)        
        elif self.tag == "instructions":
            prompt = "Generate Outline content using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)
        elif self.tag == "finetuning":
            prompt = "Generate Outline content using the below-given Content" + "\n\n###\n\nContent: " + content + "\n\n***\n\nOutput:"
            response = self.completion(prompt)

        prompt = f'{content}\n\n***\n\n'
        response = self.completion(prompt)
        return self.extract_result(response)

    def article(self, content: str, content2: str= None, content3: list= None):

        # Generate Introduction
        intro = self.intro(content) if not content2 else content2
        
        # Generate Outlines if not passed
        if not content3:
            outlines = self.outlines(f'{content}\n\n{intro}')
        else:
            outlines = ''
            for outline in outlines:
                outlines += f'\n{outline}'

        outlines_generated = self.outlines_generated(f'{content}\n\n{intro}\n\n{outlines}')
        article = f'{content}\n\n{intro}\n\n{outlines_generated}'
        return article