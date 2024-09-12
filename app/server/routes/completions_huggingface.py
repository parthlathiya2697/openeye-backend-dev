import logging
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder


from server.models.completions_huggingface import Summerisation, Translation, QuestionAnswering, TextGeneration, SentimentClassification
from server.models.main import ResponseModel, ErrorResponseModel

from server.utils.classes.hugging_face.summarization import Summarizer as TextSummarizer
from server.utils.classes.hugging_face.translation import Translator as TextTranslator
from server.utils.classes.hugging_face.sentiment_classification import SentimentClassifier as TextSentimentClassifier
from server.utils.classes.hugging_face.question_answering import QuestionAnswerer as TextQuestionAnswerer
from server.utils.classes.hugging_face.text_generation import TextGenerator as TextTextGenerator

from server.utils.auth_handler import get_user as get_auth_user
from server.utils.auth_bearer import JWTBearer

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post('/summarizer', dependencies=[Depends(JWTBearer())])
def summarize(req: Request, summeriser: Summerisation):

    # Get the user
    user = get_auth_user(req)

    summeriser = jsonable_encoder(summeriser)
    text_summarizer = TextSummarizer('google/pegasus-xsum')
    output = text_summarizer(summeriser.get('content'))
    return ResponseModel(output, "Summarization complete")

@router.post('/translator', dependencies=[Depends(JWTBearer())])
def translate(req: Request, translator: Translation):

    # Get the user
    user = get_auth_user(req)

    translator = jsonable_encoder(translator)
    try:
        text_translator = TextTranslator('t5-small', language_to= translator.get('language_to'))
    except ValueError as err:
        return ErrorResponseModel(err, 400 , 'Please enter a supported language and try again.')
    output = text_translator(translator.get('content'))
    return ResponseModel(output, "Summarization complete")

@router.post('/question_answerer', dependencies=[Depends(JWTBearer())])
def answer_question(req: Request, question_answerer: QuestionAnswering):

    # Get the user
    user = get_auth_user(req)

    question_answerer = jsonable_encoder(question_answerer)
    text_answerer = TextQuestionAnswerer('deepset/roberta-base-squad2')
    output = text_answerer(question_answerer.get('content'), question_answerer.get('context'))
    return ResponseModel(output, 'Question Answered complete')

@router.post('/text_generation', dependencies=[Depends(JWTBearer())])
def generate_text(req: Request, text_generator: TextGeneration):

    # Get the user
    user = get_auth_user(req)

    text_generator = jsonable_encoder(text_generator)
    text_answerer = TextTextGenerator('distilgpt2')
    output = text_answerer(text_generator.get('content'))
    return ResponseModel(output, 'Text Generation complete')

@router.post('/sentiment_classification', dependencies=[Depends(JWTBearer())])
def generate_text(sentiment_classifier: SentimentClassification):

    # Get the user
    user = get_auth_user(req)

    sentiment_classifier = jsonable_encoder(sentiment_classifier)
    text_answerer = TextSentimentClassifier('distilbert-base-uncased-finetuned-sst-2-english')
    output = text_answerer(sentiment_classifier.get('content'))
    return ResponseModel(output, 'Text Generation complete')
