from fastapi.responses import HTMLResponse
from server.utils.templates import html_home

from server.routes.user import router as userRouter
from server.routes.completions_openai import router as completionsOpenaiRouter
from server.routes.completions_huggingface import router as completeWithHuggingFace

from server.routes.utilities.text.grade import router as gradeRouter

from .utils.middlewares import ChangeResponseMiddleware
from config import settings

import logging

format = "%(levelname)s:%(funcName)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=format)

def createApp():
    app = FastAPI(
                    title= settings.PROJECT_NAME,
                    description=settings.PROJECT_DESCRIPTION,
                    version= settings.PROJECT_VERSION,
                    contact={"email": settings.ADMIN_EMAIL},
                    termsOfService= settings.TERMS_OF_SERVICE,
                    host= settings.SERVER_HOST,
                    basePath= settings.API_V1_STR
                )
    
    app.add_middleware(ChangeResponseMiddleware)

    # add cors
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(userRouter, tags=["Users"], prefix= settings.API_V1_STR)
    app.include_router(completionsOpenaiRouter, tags=["Generate with OpenAI"], prefix= settings.API_V1_STR)
    app.include_router(completeWithHuggingFace, tags=["Generate with Hugging Face"], prefix= settings.API_V1_STR)
    app.include_router(gradeRouter, tags=["Grading"], prefix= settings.API_V1_STR)

    return app

app = createApp()

# controller routes
@app.get("/")
def get():
    return HTMLResponse(html_home)
