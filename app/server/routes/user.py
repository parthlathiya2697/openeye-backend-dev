from config import config

from fastapi import APIRouter, status, HTTPException, Depends

from server.models.user import User
from server.controllers.user import get_users, get_user, create_user, update_user, delete_user, authenticate_user

from server.utils.auth_handler import signJWT
from server.utils.auth_bearer import JWTBearer

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = config.get("settings", "ACCESS_TOKEN_EXPIRE_MINUTES")


@router.get('/user', status_code=200)
def get_users_():
    ret, msg = get_users()
    if not ret:
        raise HTTPException(status_code=400, detail= msg)

    return {"data": ret, "status": 200, "message": msg}

@router.get('/user/{username}', status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_user_(username: str):
    
    ret, msg = get_user(username)
    if not ret:
        raise HTTPException(status_code=400, detail= msg)

    return {"data": ret, "status": 200, "message": msg}

@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=Token)
def create_user_(user: User):

    # Check user exists in db
    ret, msg = create_user(user)
    if not ret:
        raise HTTPException(status_code=400, detail= msg)

    return Token(access_token= signJWT( ret.username ), token_type= 'JWT')

@router.put('/user/{username}', status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_user_(username: str, user: User):

    # Get existing user
    ret, msg = update_user(username, user)
    if not ret:
        raise HTTPException(status_code=400, detail= msg)

    return {"status": 200, "message": msg}

@router.delete('/user/{username}', dependencies=[Depends(JWTBearer())])
def delete_user_(username: str):

    # Get existing user
    ret, msg = delete_user(username)
    if not ret:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= msg)

    return {"data": ret, "status": 200, "message": msg}

@router.post("/login", response_model=Token)
def login_(login: Login):
    ret, msg = authenticate_user(login.username, login.password)
    if not ret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return Token(access_token= signJWT( ret.username ), token_type= 'JWT')

@router.post('/logout', dependencies=[Depends(JWTBearer())])
def logout_():
    return {"Msg": "Logout Success"}

@router.get("/auth", dependencies=[Depends(JWTBearer())])
def auth():
    return {"Msg": "Auth Success"}
