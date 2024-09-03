from openai import AsyncOpenAI
from config import settings
from db import get_db

class IA:

  def __init__(self):
    self.client = AsyncOpenAI(api_key=settings.api_key)
    self.model = settings.net_model
  

  async def autoGen(self, prompt):
    response = await self.client.chat.completions.create(
      model=self.model,
      temperature=int(settings.temperature)/10,
      messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
  
  async def subSniff(self):
    # db = get_db()
    # empresa_dict = empresa.dict()
    # empresa_dict["id"] = str(PydanticObjectId())
    # result = db.empresas.insert_one(empresa_dict)
  
    # response = await self.client.chat.completions.create(
    #   model=self.model,
    #   temperature=int(settings.temperature)/10,
    #   messages=[{"role": "user", "content": ""}],
    # )
    # return response.choices[0].message.content
    return "OK"