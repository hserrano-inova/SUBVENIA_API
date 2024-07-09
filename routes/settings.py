from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from db import get_db
from datetime import datetime
from models.subvenciones import SubvencionGeneral
from models.users import User
from auth import get_current_user
from pydantic_mongo import  PydanticObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/criterios", response_model=SubvencionGeneral, tags=["criterios"], description="Get subvenciones by id")
async def get_criteria():
  db = get_db()
  resp = db.settings.find_one({'criteria': {'$exists': True}},{'_id': 0})
  if(resp is not None):
    return SubvencionGeneral(**resp['criteria'])
  else:
    return SubvencionGeneral()

@router.post("/criterios", response_model=str, tags=["criterios"], description="Create subvenciones")
async def update_criteria(criteria: SubvencionGeneral):
  db = get_db()
  resp = db.settings.update_one(
    {'criteria': {'$exists': True}}, 
        {"$set": {'criteria': criteria.model_dump()}},upsert=True
  )
  return "OK"

@router.get("/getsettings", tags=["Settings"], description="Get subvenciones by id")
async def get_settings():
  db = get_db()
  resp = db.settings.find_one(
        {'tipo_empresa': {'$exists': True}},
        {'_id': 0}
    )
  if(resp is not None):
    return resp
  else:
    raise HTTPException(status_code=404, detail="Settings not found")