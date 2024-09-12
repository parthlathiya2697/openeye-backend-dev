import os
from app import config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import uvicorn

if __name__ == "__main__":

    uvicorn.run("server.app:app", host= os.getenv('FASTAPI_HOST'), port=int( os.getenv('FASTAPI_PORT') ), reload=True if os.getenv('ENV')=='dev' else False)