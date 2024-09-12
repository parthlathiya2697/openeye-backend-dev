from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from server.models.responses import ErrorResponseModel

from server.models.responses import ResponseModel
from server.models.completions_openai import Rephrase, Summeriser, EmailWriter, TaglineGenerator, BlogpostHashtags, BlogpostOutline, HeadlineGenerator
from server.models.completions_openai import ProductDescription, CreativeStory, Poem, SentenceExpander, Intro, Outlines, OutlinesGen
from server.models.completions_openai import CreateArticle

from server.utils.auth_handler import get_user as get_auth_user
from server.utils.auth_bearer import JWTBearer
from server.utils.classes.openai.completions import Completion

from server.controllers.user_generations import create_user_generation

from functools import wraps

from config import config

router = APIRouter()

@router.post('/rephrase', dependencies=[Depends(JWTBearer())])
def rephrase_(req: Request, task: Rephrase):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
        
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.rephrase(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result
    return ResponseModel(input_data, "Rephrasing complete !" + msg)

@router.post('/summeriser', dependencies=[Depends(JWTBearer())])
def summeriser_(req: Request, task: Summeriser):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.summeriser(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Summarization complete !")

@router.post('/email_writer', dependencies=[Depends(JWTBearer())])
def email_writer_(req: Request, task: EmailWriter):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.email_writer(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Drafting Email complete !")

@router.post('/tagline_generator', dependencies=[Depends(JWTBearer())])
def tagline_generator_(req: Request, task: TaglineGenerator):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.tagline_generator(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Finished Up generating awesome Tagline !")

@router.post('/blogpost_outline', dependencies=[Depends(JWTBearer())])
def blogpost_outline_(req: Request, task: BlogpostOutline):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.blogpost_outline(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Beautiful Outlines generated !")

@router.post('/blogpost_hashtags', dependencies=[Depends(JWTBearer())])
def blogpost_hashtags_(req: Request, task: BlogpostHashtags):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.blogpost_hashtags(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Rephrasing complete !")

@router.post('/headline_generator', dependencies=[Depends(JWTBearer())])
def headline_generator_(req: Request, task: HeadlineGenerator):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.headline_generator(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Fruitful headlines are now generated !")

@router.post('/product_description', dependencies=[Depends(JWTBearer())])
def product_description_(req: Request, task: ProductDescription):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.product_description(content= task.get('content'), content2= task.get('content2'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Generated very intuitive description for your Product !")

@router.post('/creative_story', dependencies=[Depends(JWTBearer())])
def creative_story_(req: Request, task: CreativeStory):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.creative_story(content= task.get('content'), content2= task.get('content2'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Your Story has been crafted !")

@router.post('/poem', dependencies=[Depends(JWTBearer())])
def poem_(req: Request, task: Poem):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.poem(content= task.get('content'), content2= task.get('content2'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "I wrote a Mind blowing poem for you !")

@router.post('/sentence_expander', dependencies=[Depends(JWTBearer())])
def sentence_expander_(req: Request, task: SentenceExpander):
	
    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.sentence_expander(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Rephrasing complete !")

@router.post('/intro', dependencies=[Depends(JWTBearer())])
def intro_(req: Request, task: Intro):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.intro(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Generated Title !")

@router.post('/outlines', dependencies=[Depends(JWTBearer())])
def outlines_(req: Request, task: Outlines):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.outlines(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Generated Title !")

@router.post('/outlines_generated', dependencies=[Depends(JWTBearer())])
def outlines_generated_(req: Request, task: OutlinesGen):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    result = completion.outlines_generated(content= task.get('content'))

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Generated Title !")

@router.post('/article', dependencies=[Depends(JWTBearer())])
def article_(req: Request, task: CreateArticle):

    # Get the user
    user = get_auth_user(req)

    # Convert to json
    task = jsonable_encoder(task)
    tag = task.get('tag')
    
    
    # Completion Object
    completion = Completion( model= task.get('model') , tag= tag)
    completion.set_params( **task.get('inference_parameters') )

    # Complete Task
    ##Todo - Add openai response validation for success
    title = task.get('content')
    intro = task.get('content2')
    outlines = task.get('content3')
    result = completion.article(content= title, content2= intro, content3= outlines)

    # Prepare response payload
    input_data = task.copy()
    del input_data['tag']
    del input_data['inference_parameters']

    ret, msg = create_user_generation(username= user['username'], input_data= input_data, generation= result, application= 'rephrase', tag= tag)
    if not ret:
        return ErrorResponseModel(error= msg, code= 405, message= msg)

    input_data['generation'] = result

    return ResponseModel(input_data, "Generated Article !")