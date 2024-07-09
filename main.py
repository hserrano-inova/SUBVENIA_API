from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes import router
from config import settings
#from fastapi.staticfiles import StaticFiles


app = FastAPI(
  title="SUBVEN-IA",
  timeout_keep_alive=100,
  docs_url='/docs'if not settings.production else None,
  #redoc_url='/redoc'if not settings.production else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(router)