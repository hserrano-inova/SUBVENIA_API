from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from db import get_db
from datetime import datetime
from models.evaluaciones import Evaluacion, EvaluacionList
from models.users import User
from auth import get_current_user
from pydantic_mongo import  PydanticObjectId
from config import settings
from openai import AsyncOpenAI, OpenAI

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

client = AsyncOpenAI(
  api_key=settings.openai_api_key
)

@router.get("/evaluaciones/{idprj}", response_model=List[EvaluacionList], tags=["Evaluaciones"])
async def read_empresa(idprj: str, current_user: User = Depends(get_current_user)):
    db = get_db()
    evaluaciones = db.evaluaciones.find({"id_project": idprj},{"_id":0})
    return [EvaluacionList(**ev) for ev in evaluaciones]


@router.get("/evaluacion/{idev}", response_model=Evaluacion, tags=["Evaluaciones"])
async def read_empresa(idev: str, current_user: User = Depends(get_current_user)):
    db = get_db()
    evaluacion = db.evaluaciones.find({"id": idev},{"_id":0})
    return EvaluacionList(**evaluacion)