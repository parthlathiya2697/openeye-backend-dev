from pydantic import BaseModel, validator
from typing import List, Optional
from config import config

# Base Models
MODEL_DAVINCI= config.get("openai", "DAVINCI")
MODEL_CURIE=config.get("openai", "CURIE")
MODEL_BABBAGE=config.get("openai", "BABBAGE")
MODEL_ADA=config.get("openai", "ADA")

# Finetune links
MODEL_PARAPHRASER = config.get("openai", "PARAPHRASER")
MODEL_INTRO_FROM_TITLE = config.get("openai", "INTRO_FROM_TITLE")
MODEL_OUTLINE_FROM_INTRO_TITLE = config.get("openai", "OUTLINE_FROM_INTRO_TITLE")
MODEL_ARTICLE_GEN_FROM_TITLE_INTRO_OUTLINE = config.get("openai", "ARTICLE_GEN_FROM_TITLE_INTRO_OUTLINE")

# Word limits
# Article
MIN_WORDS_ARTICLE_TITLE = 3
MAX_WORDS_ARTICLE_TITLE = 20

MAX_WORDS_ARTICLE_TITLE = 10
MAX_WORDS_ARTICLE_INTRO = 300

MAX_WORDS_ARTICLE_TITLE_PARA_OUTLINES = 20
MAX_WORDS_ARTICLE_INTRO_PARA_OUTLINES = 700

# Paraphraser
MIN_WORDS_PARAPHRASING_TITLE = 3
MAX_WORDS_PARAPHRASING_TITLE = 300

def length_limit_checker(length: int, limit: tuple):
    if length < limit[0] or length > limit[1]:
        raise ValueError(f'Please enter minimum of {limit[0]+1} words or a maximum of {limit[1]}')


# Inner Models
class InferenceParameters(BaseModel):
    temperature  : Optional[float] = 0.7
    max_tokens : Optional[int] = 200
    top_p : Optional[float] = 1
    frequency_penalty : Optional[float] = 0.4
    presence_penalty : Optional[float] = 0.2
    stop : Optional[List[str]] = ["\n\n***\n\n", "\n\n###\n\n", "##END##"]

    @validator('stop', check_fields=False)
    def listlimit_checker(cls, v, **kwargs):
        if len(v) > 5:
            raise ValueError('Please enter correct contact number')
        return v

# Outer Models
class Rephrase(BaseModel):
    
    tag: str
    model: str= MODEL_ADA
    inference_parameters: InferenceParameters

    content: str

    @validator('content', check_fields=False)
    def assert_word_limit(cls, v, **kwargs):
        length_limit_checker(length= len( v.split(" ")), limit= (MIN_WORDS_PARAPHRASING_TITLE, MAX_WORDS_PARAPHRASING_TITLE))
        return v

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }

class Summeriser(BaseModel):
    tag: str
    model: str= MODEL_ADA
    inference_parameters: InferenceParameters

    content: str

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California. Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }
    
class EmailWriter(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California. Join today to get the most out of it.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }
    
class TaglineGenerator(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str
    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }
    
class BlogpostOutline(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str
    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }

class BlogpostHashtags(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str
    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }

class HeadlineGenerator(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }
    
class SentenceExpander(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }
    
class ProductDescription(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str
    content2: str

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc.",
                "content2": "Salesforce, Inc. is an American cloud-based software company, headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }
    
class CreativeStory(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str
    content2: str

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Ducks go down the street",
                "content2": "Two ducks travelling in the rain. Walk accross the street. Are happy and enjoying their life.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }
    
class Poem(BaseModel):
    tag: str
    model: str= MODEL_ADA
    
    inference_parameters: InferenceParameters

    content: str
    content2: str

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Ducks go down the street",
                "content2": "Two ducks travelling in the rain. Walk accross the street. Are happy and enjoying their life.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }

# Article
class Intro(BaseModel):
    tag: str
    model: str= MODEL_INTRO_FROM_TITLE

    inference_parameters: InferenceParameters

    content : str

    @validator('content', check_fields=False)
    def assert_word_limit(cls, v, **kwargs):
        length_limit_checker(length= len( v.split(" ")), limit= (MIN_WORDS_ARTICLE_TITLE, MAX_WORDS_ARTICLE_TITLE))
        return v

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }

class Outlines(BaseModel):
    
    tag: str
    model: str= MODEL_OUTLINE_FROM_INTRO_TITLE
    
    inference_parameters: InferenceParameters

    content : str

    @validator('content', check_fields=False)
    def assert_word_limit(cls, v, **kwargs):
        length_limit_checker(length= len(v.split(" ")), limit= (MAX_WORDS_ARTICLE_TITLE, MAX_WORDS_ARTICLE_INTRO))
        return v

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }  

class OutlinesGen(BaseModel):
    
    tag: str
    model: str= MODEL_ARTICLE_GEN_FROM_TITLE_INTRO_OUTLINE

    inference_parameters: InferenceParameters

    content : str

    @validator('content', check_fields=False)
    def assert_word_limit(cls, v, **kwargs):
        length_limit_checker(length= len( v.split(" ")), limit= (MAX_WORDS_ARTICLE_TITLE_PARA_OUTLINES, MAX_WORDS_ARTICLE_INTRO_PARA_OUTLINES))  
        return v

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California. Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California. Salesforce, Inc. is an American cloud-based software company headquartered in San Francisco, California.",
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }

class CreateArticle(BaseModel):

    tag: str
    model: str= MODEL_ARTICLE_GEN_FROM_TITLE_INTRO_OUTLINE
    inference_parameters: InferenceParameters

    content: str
    content2: Optional[str]
    content3: Optional[list]


    @validator('content', check_fields=False)
    def assert_word_limit(cls, v, **kwargs):
        length_limit_checker(length= len( v.split(" ")), limit= (MIN_WORDS_ARTICLE_TITLE, MAX_WORDS_ARTICLE_TITLE))
        return v

    class Config:
        schema_extra = {
            "example": {
                "tag": "instructions",
                "content": "How to earn  more money everday",
                "content2": "There are many ways now-a-days that you can earn money online.",
                "content3": [ "Youtube", "Glicth", "Ads" ],
                "inference_parameters": {
                        "temperature"  :0.7,
                        "max_tokens" : 200,
                        "top_p" : 1,
                        "frequency_penalty" : 0.4,
                        "presence_penalty" : 0.2,
                        "stop" : ["\n\n***\n\n", "\n\n###\n\n", "##END##"]
                    }
            }
        }

