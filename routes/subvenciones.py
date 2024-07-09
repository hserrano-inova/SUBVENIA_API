from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from db import get_db
from datetime import datetime
from models.subvenciones import Subvencion, SubvencionList
from models.users import User
from auth import get_current_user
from pydantic_mongo import  PydanticObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def getSubvencion(idl):
    if(idl!='0'):
        db = get_db()
        subvencion = db.subvenciones.find_one({"id": idl})
        if subvencion:
            return Subvencion(**subvencion)
        else:
            raise HTTPException(status_code=404, detail="Licitación no encontrada")
    else:
        return Subvencion() 
    
@router.get("/subvenciones/", response_model=List[SubvencionList], tags=["Subvenciones"])
async def read_subvenciones(current_user: User = Depends(get_current_user)):
    db = get_db()
    subvenciones = db.subvenciones.find({},{"_id":0})
    return [SubvencionList(**subvencion) for subvencion in subvenciones]

@router.get("/subvenciones/{id}", response_model=Subvencion , tags=["Subvenciones"])
async def read_subvencion(id: str, current_user: User = Depends(get_current_user)):
    return getSubvencion(id)

@router.post("/subvenciones/", tags=["Subvenciones"])
async def create_subvencion(subvencion: Subvencion, current_user: User = Depends(get_current_user)):
    db = get_db()
    subvencion_dict = subvencion.dict()
    subvencion_dict["id"] = str(PydanticObjectId())
    result = db.subvenciones.insert_one(subvencion_dict)

    if result:
        return {"msg": str(result.inserted_id)}
    raise HTTPException(status_code=404, detail="Error al guardae licitacion")

@router.put("/subvenciones/{id}", tags=["Subvenciones"])
async def update_subvencion(id: str, subvencion: Subvencion, current_user: User = Depends(get_current_user)):
    db = get_db()
    subvencion_dict = subvencion.dict()
    updated_subvencion = db.subvenciones.update_one(
        {"id": id},
        {"$set": subvencion_dict}
    )
    if updated_subvencion:
        return {"msg": updated_subvencion.modified_count}

    raise HTTPException(status_code=404, detail="Licitación no encontrada")
    # print(licitacion.dict(), id)
    # return "OK"

@router.delete("/subvenciones/{id}",  status_code=status.HTTP_204_NO_CONTENT, tags=["Subvenciones"])
async def delete_licitacion(id: str, current_user: User = Depends(get_current_user)):
    db = get_db()
    result = db.subvenciones.delete_one({"id": id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Licitación no encontrada")
    else:
        return {"msg":result.deleted_count }