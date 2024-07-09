#https://pypi.org/project/pydantic-mongo/

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import  PydanticObjectId
from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List
import os


class Localizacion(BaseModel):
  descripcion:str=""
  ciudad: str = ""
  provincia:int = 1
  direccion: str  = ""
  cp: str  = ""
  pcontacto:str=""
  tlf:str=""
  mail:str=""

class Empresa(BaseModel):
  id: Optional[PydanticObjectId] = PydanticObjectId()
  actualizada:datetime = datetime.now()
  cif: str = ""
  rsocial: str = ""
  acronimo:str = "" 
  tipo: str = ""
  sector: str = ""
  cnae_grupo:str = ""
  cnae_cod:str = ""
  pyme:bool = True
  nempleados: int = 0
  facturacion: int = 0
  minimis: int = 0
  tags: str = ""
  localizacion: List[Localizacion] = [Localizacion()]
  observaciones: str = ""
  descripcion: str = ""

class EmpresaList(BaseModel):
    id: Optional[PydanticObjectId]
    cif: str = ""
    rsocial: str = ""
    acronimo:str = "" 
    tipo: str = ""
    sector: str = ""