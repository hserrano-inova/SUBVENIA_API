#https://pypi.org/project/pydantic-mongo/

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import  PydanticObjectId
from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List
import os


class Evaluacion(BaseModel):
  id: Optional[PydanticObjectId] = PydanticObjectId()
  actualizada:datetime = datetime.now()
  cif: str = ""
  rsocial: str = ""
  acronimo:str = "" 
  tipo: str = ""
  sector: str = ""
  cnae_cod:str = ""
  nempleados: int = 0
  facturacion: int = 0
  minimis: int = 0
  tags: str = ""
  observaciones: str = ""
  descripcion: str = ""

class EvaluacionList(BaseModel):
    id: Optional[PydanticObjectId]
    cif: str = ""
    rsocial: str = ""
    acronimo:str = "" 
    tipo: str = ""
    sector: str = ""