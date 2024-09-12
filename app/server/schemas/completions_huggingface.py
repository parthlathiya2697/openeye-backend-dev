from pydantic import BaseModel

class Summerisation(BaseModel):
    content: str

class SentimentClassification(BaseModel):
    content: str

class Translation(BaseModel):
    content: str
    language_to: str 

class QuestionAnswering(BaseModel):
    content: str
    context: str

    
class TextGeneration(BaseModel):
    content: str
