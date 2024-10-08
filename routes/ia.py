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
import json
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
  subvenciones = list(db.subvenciones.find({"estado":"Abierta"},{"_id":0}).limit(3))
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
              "objetivo": 1,
              "inversion_inovacion": 1,
              "conceptos_financiables": 1,
              "consorcio": 1,
              "empresa_info": 1            # Mostrar la información de la empresa unida
          }
      }
  ]
  result = list(db.projects.aggregate(pipeline))

  if len(result) > 0:
    project = result[0]
    empresa = project['empresa_info'][0]
    #print(result[0])
    for subvencion in subvenciones:
      try:
        # prompt=f"""
        #   {subvencion['beneficiarios']}
        #   {subvencion['objetivo']}
        #   {subvencion['inversion_inovacion']}
        #   {subvencion['conceptos_financiables']}
        #   {subvencion['consorcio']}
        #   {subvencion["ambito"]}
        #   {subvencion["tipo_ayuda"]}
        #   {subvencion["concurrencia"]}
        #   {subvencion["minimis"]}
        #   {subvencion["presupuesto_minimo"]}
        #   {subvencion["presupuesto_maximo"]}
        #   {subvencion["areas"]}

        #   {project['beneficiarios']}
        #   {project['objetivo']}
        #   {project['inversion_inovacion']}
        #   {project['conceptos_financiables']}
        #   {project['consorcio']}

        #   {empresa["tipo"]}
        #   {empresa["sector"]}
        #   {empresa["cnae_cod"]}
        #   {empresa["nempleados"]}          
        #   {empresa["facturacion"]}          
        #   {empresa["minimis"]}         
        #   {empresa["tags"]}
        #   {empresa["observaciones"]}
        #   {empresa["descripcion"]}    
        # """
        prompt=f"""
          Eres un consultor experto tecnología, energía y medioambiente.
          Tu labor es evaluar si una subvencion encaja con el perfil de la empresa y proyecto.

          Primero debes comprobar si los beneficiarios que pueden acceder a la subvencion encajan con el perfil de la empresa:
          <beneficiarios>
          Estos son los beneficiarios de la subvencion:
          {subvencion['beneficiarios']}
          Este es tipo de empresa es {empresa["tipo"]}
          </beneficiarios> 
          Si no se cumple el perfil de la empresa vete directamente al apartado <response>

          Segundo, debes comprobar si el objetivo de la subvencion encaja con el perfil de la empresa:
          <objetivo>
          Este es el objetivo de la subvencion:
          {subvencion['objetivo']}

          La empresa se describe de la siguiente manera:
          {empresa["descripcion"]}
          {empresa["tags"]}
          </objetivo>
          Si no se cumple el perfil de la empresa vete directamente al apartado <response>

          <reponse>
          Finalemnte devuelve un JSON con el nombre de cada apartado cada apartado en el que se responda en el campo "respuesta" si se cumple ture o false y un campo llamado "argumento" que argumente cada una de las respueestas
          </reponse>
        """
        
        iaresult = await assistant.autoGen(prompt,True)

        rdict ={
          "nsub":subvencion['nsubvencion'],
          "response": json.loads(iaresult)
        }

        await websocket.send_text(json.dumps(rdict))
        #await websocket.send_text(iaresult)
        #await asyncio.sleep(5)

      except WebSocketDisconnect:
        return "ws disconnect"
      except Exception as e:
        await websocket.close()
  else:
    await websocket.send_text("No se han encontrado datos")
  await websocket.close()