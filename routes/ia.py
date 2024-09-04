from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from typing import List
from db import get_db
from datetime import datetime
from auth import get_current_user
from models.ia import Completion
from models.users import User
from models.proyectos import Proyecto
from models.subvenciones import SubvencionList
from pydantic_mongo import  PydanticObjectId

from ia import IA
import asyncio


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

@router.websocket("/peval")
async def ia_subsniff( websocket: WebSocket):
  await websocket.accept()
  db = get_db()
  subvenciones = list(db.subvenciones.find({},{"_id":0}).limit(4))
  for s in subvenciones:
    try:
      await websocket.send_text(f"subvencion: {s['nsubvencion']}")
      await asyncio.sleep(5)

    except WebSocketDisconnect:
      return "ws disconnect"
    except Exception as e:
      return e
  await websocket.close()
  
  # try:
  #   db = get_db()
  #   subvenciones = list(db.subvenciones.find({},{"_id":0}))

  #   await asyncio.sleep(5)
  #   # sub=[SubvencionList(**subvencion) for subvencion in subvenciones]
  #   # for s in sub:
  #   #   aresult = await assistant.autoGen("")
  #   #   return "OK"
  # except Exception as e:
  #   print(e)
  #   return {"msg": "Error al generar la respuesta"}