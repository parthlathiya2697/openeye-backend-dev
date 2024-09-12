from pydantic import BaseModel, validator
from typing import List, Optional
from config import config

class ImageProcessing(BaseModel):

    image
    