from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from db import get_db
from datetime import datetime
from models.subvenciones import Project, ProjectList
from models.users import User
from auth import get_current_user
from pydantic_mongo import  PydanticObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def getProject(idl):
    if(idl!='0'):
        db = get_db()
        project = db.projects.find_one({"id": idl})
        if project:
            return Project(**project)
        else:
            raise HTTPException(status_code=404, detail="Licitación no encontrada")
    else:
        return Project() 
    
@router.get("/projects/", response_model=List[ProjectList], tags=["Projects"])
async def read_projects(current_user: User = Depends(get_current_user)):
    db = get_db()
    projects = db.projects.find({},{"_id":0})
    return [ProjectList(**prj) for prj in projects]

@router.get("/projects/{id}", response_model=Project , tags=["Projects"])
async def read_projects(id: str, current_user: User = Depends(get_current_user)):
    return getProject(id)

@router.get("/projectsemp/{id}", response_model=List[ProjectList], tags=["Projects"])
async def read_projects(id:str, current_user: User = Depends(get_current_user)):
    db = get_db()
    projects = db.projects.find({"id_empresa": id },{"_id":0})
    return [ProjectList(**prj) for prj in projects]

@router.post("/projects/", tags=["Projects"])
async def create_projects(prj: Project, current_user: User = Depends(get_current_user)):
    db = get_db()
    prj_dict = prj.dict()
    prj_dict["id"] = str(PydanticObjectId())
    result = db.projects.insert_one(prj_dict)

    if result:
        return {"msg": str(result.inserted_id)}
    raise HTTPException(status_code=404, detail="Error al guardae licitacion")

@router.put("/projects/{id}", tags=["Projects"])
async def update_projects(id: str, prj: Project, current_user: User = Depends(get_current_user)):
    db = get_db()
    prj_dict = prj.dict()
    updated_prj = db.projects.update_one(
        {"id": id},
        {"$set": prj_dict}
    )
    if updated_prj:
        return {"msg": updated_prj.modified_count}

    raise HTTPException(status_code=404, detail="Licitación no encontrada")
    # print(licitacion.dict(), id)
    # return "OK"

@router.delete("/projects/{id}",  status_code=status.HTTP_204_NO_CONTENT, tags=["Projects"])
async def delete_projects(id: str, current_user: User = Depends(get_current_user)):
    db = get_db()
    result = db.projects.delete_one({"id": id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Licitación no encontrada")
    else:
        return {"msg":result.deleted_count }