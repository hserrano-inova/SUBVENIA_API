from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from db import get_db
from datetime import datetime
from models.empresas import Empresa, EmpresaList
from models.users import User
from auth import get_current_user
from pydantic_mongo import  PydanticObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def getEmpresa(idl):
    if(idl!='0'):
        db = get_db()
        subvencion = db.empresas.find_one({"id": idl})
        if subvencion:
            return Empresa(**subvencion)
        else:
            raise HTTPException(status_code=404, detail="Licitación no encontrada")
    else:
        return Empresa() 
    
@router.get("/empresas/", response_model=List[EmpresaList], tags=["Empresas"])
async def read_empresas(current_user: User = Depends(get_current_user)):
    db = get_db()
    empresas = db.empresas.find({},{"_id":0})
    return [EmpresaList(**empresa) for empresa in empresas]

@router.get("/empresas/{id}", response_model=Empresa , tags=["Empresas"])
async def read_empresa(id: str, current_user: User = Depends(get_current_user)):
    return getEmpresa(id)

@router.post("/empresas/", tags=["Empresas"])
async def create_empresa(empresa: Empresa, current_user: User = Depends(get_current_user)):
    db = get_db()
    empresa_dict = empresa.dict()
    empresa_dict["id"] = str(PydanticObjectId())
    result = db.empresas.insert_one(empresa_dict)

    if result:
        return {"msg": str(result.inserted_id)}
    raise HTTPException(status_code=404, detail="Error al guardae licitacion")

@router.put("/empresas/{id}", tags=["Empresas"])
async def update_empresa(id: str, empresa: Empresa, current_user: User = Depends(get_current_user)):
    db = get_db()
    empresa_dict = empresa.dict()
    updated_empresa = db.empresas.update_one(
        {"id": id},
        {"$set": empresa_dict}
    )
    if updated_empresa:
        return {"msg": updated_empresa.modified_count}

    raise HTTPException(status_code=404, detail="Licitación no encontrada")
    # print(licitacion.dict(), id)
    # return "OK"

@router.delete("/empresas/{id}",  status_code=status.HTTP_204_NO_CONTENT, tags=["Empresas"])
async def delete_licitacion(id: str, current_user: User = Depends(get_current_user)):
    db = get_db()
    result = db.empresas.delete_one({"id": id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Licitación no encontrada")
    else:
        return {"msg":result.deleted_count }