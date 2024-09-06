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
#from pydantic_mongo import  PydanticObjectId
#from bson.objectid import ObjectId

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

@router.websocket("/ws/peval/")
async def ia_subsniff( websocket: WebSocket, prjid:str):
  await websocket.accept()
  db = get_db()
  subvenciones = list(db.subvenciones.find({},{"_id":0}).limit(1))
  pipeline = [
      {
        "$match": { "id": prjid }  # Asegúrate que el ID es de tipo ObjectId, si corresponde
      },
      {
          "$lookup": {
              "from": "empresas",          # Colección "empresas"
              "localField": "id_empresa",  # Campo en "proyectos"
              "foreignField": "id",       # Campo en "empresas"
              "as": "empresa_info"         # Nombre del campo donde se guardará la información de "empresas"
          }
      },
      {
          "$project": {
              "id": 1,
              "beneficiarios": 1,
              "objeticos": 1,
              "invercion_inovacion": 1,
              "conceptos_financiables": 1,
              "consorcio": 1,
              "empresa_info": 1            # Mostrar la información de la empresa unida
          }
      }
  ]

  # Ejecutar el pipeline
  result = list(db.projects.aggregate(pipeline))
  #chack result not empty
  if len(result) > 0:
    print(result[0])
    for s in subvenciones:
      try:
        #iaresult = await assistant.autoGen("")
        await websocket.send_text(f"subvencion: {s['nsubvencion']}")
        await asyncio.sleep(5)

      except WebSocketDisconnect:
        return "ws disconnect"
      except Exception as e:
        return e
  else:
    await websocket.send_text("No hay subvenciones")
  await websocket.close()