from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from server.models.responses import ErrorResponseModel

from server.models.responses import ResponseModel
from server.models.image.image_processing import ImageProcessing

router = APIRouter()

@router.post('/rephrase', dependencies=[Depends(JWTBearer())])
def rephrase_():

    pass
