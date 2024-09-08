from openai import AsyncOpenAI
from config import settings


class IA:

  def __init__(self):
    self.client = AsyncOpenAI(api_key=settings.api_key)
    self.model = settings.net_model
  
  async def autoGen(self, prompt,json=False):
    if(json):
      response = await self.client.chat.completions.create(
        model=self.model,
        temperature=int(settings.temperature)/10,
        messages=[
          {"role": "system", "content": "Eres un consultor experto experto en subvenciones para poyectos tecnológicos y de medioambiente"},
          {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
      )
    else:
      response = await self.client.chat.completions.create(
        model=self.model,
        temperature=int(settings.temperature)/10,
        messages=[
          {"role": "system", "content": "Eres un consultor experto experto en subvenciones para poyectos tecnológicos y de medioambiente"},
          {"role": "user", "content": prompt}
        ],
      )
    return response.choices[0].message.content

