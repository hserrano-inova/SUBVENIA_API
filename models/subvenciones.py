#https://pypi.org/project/pydantic-mongo/

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import  PydanticObjectId
from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List
import os


class ContextField(BaseModel):
  descripcion: str = ""
  criterio: str = ""

class FasesDate(BaseModel):
  nfase: str = ""
  estado:str = ""
  fecha: str = ""
  observaciones: str = ""

class SubvencionGeneral(BaseModel):
    id: Optional[PydanticObjectId] = None
    actualizada: datetime = datetime.now()
    estado: str = ""
    beneficiarios: ContextField = ContextField()
    objetivo: ContextField = ContextField()
    inversion_inovacion: ContextField = ContextField()
    conceptos_financiables: ContextField = ContextField()
    consorcio: ContextField = ContextField()
    observaciones: str = ""
    enlace:str = ""

class Subvencion(SubvencionGeneral):
    nsubvencion: str = ""
    fechas: Optional[List[FasesDate]] = [FasesDate()]
    organismo: str = ""
    ambito: str = ""
    tipo_ayuda: str = ""
    concurrencia: str = ""
    minimis: int = 0
    presupuesto_minimo: int = 0
    presupuesto_maximo: int = 0
    areas: str = ""

class SubvencionList(BaseModel):
    id: Optional[PydanticObjectId]
    nsubvencion: str = ""
    organismo: str = ""
    ambito: str = ""
    actualizada: datetime = datetime.now()
    estado: str = ""
    

class Project(SubvencionGeneral):
    id_empresa: str = ""
    nombre_proyecto:str = ""
    fecha_limite: datetime = datetime.now()
    madurez: str = ""

class ProjectList(BaseModel):
    id: Optional[PydanticObjectId]
    nombre_proyecto:str = ""
    fecha_limite: datetime = datetime.now()
    madurez: str = ""