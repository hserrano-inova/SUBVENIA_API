from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from db import get_db
from datetime import datetime
from models.ia import Completion
from models.users import User
from auth import get_current_user
from pydantic_mongo import  PydanticObjectId

from ia import IA

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

assistant = IA()

@router.post("/autogen/", tags=["IA"])
async def ia_generate(completion: Completion, current_user: User = Depends(get_current_user)):
  data = completion.dict()
  try:
    result = await assistant.autoGen(data['prompt'])
    return result
  except Exception as e:
    print(e)
    return {"msg": "Error al generar la respuesta"}
    # db = get_db()
    # empresa_dict = empresa.dict()
    # empresa_dict["id"] = str(PydanticObjectId())
    # result = db.empresas.insert_one(empresa_dict)

    # if result:
    #     return {"msg": str(result.inserted_id)}
    # raise HTTPException(status_code=404, detail="Error al guardae licitacion")
