# put install configs here
import os
import nltk, spacy
from app.config import BASE_DIR

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

print("Running install.py")

model_path = os.path.join(BASE_DIR, 'models')
if not os.path.exists(model_path):
    try:
        os.mkdir(model_path)
    except Exception as err:
        print(f'Cannot create Model directory: {model_path}')
    
    # HuggingFace models directory
    os.environ['TRANSFORMERS_CACHE'] = model_path

def downlaod_necessary_components():
    try:
        if not spacy.util.is_package("en_core_web_md"):
            spacy.cli.download("en_core_web_md")
        nltk.data.find("tokenizers/punkt")
        nltk.data.find("corpora/wordnet")
        nltk.data.find("corpora/omw-1.4")
        nltk.data.find("stopwords")
    except LookupError:
        nltk.download("punkt")
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        nltk.download("stopwords")

def download_huggingface_models(models_tags_list):
    
    for model_tag in models_tags_list:    
        _ = AutoTokenizer.from_pretrained(model_tag)
        _ = AutoModelForSeq2SeqLM.from_pretrained(model_tag)

downlaod_necessary_components()
download_huggingface_models(["prithivida/grammar_error_correcter_v1"])

print("Finished installing packages from install.py")
