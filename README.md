# fast-api-tutorial

- Install the packages required like:
	  fastapi, pymongo, jinja2
	  
- Create a server with the help of fastapi as like this:
	  from typing import Union
	  from fastapi import FastAPI
	  from routes.note import note
	  from fastapi.staticfiles import StaticFiles
	  app = FastAPI()
	  app.include_router(note)
	  app.mount("/static", StaticFiles(directory="static"), name="static") 
	  
- Connect to the mongodb database :
		from pymongo import MongoClient
		MONGO_URI = "mongodb://localhost:27017/notes"
		conn = MongoClient(MONGO_URI)
		
- Render the template files using jinja2:
	  templates = Jinja2Templates(directory="templates")
	  
- With the help of router perform the post and get requests:
	  @note.get("/", response_class=HTMLResponse)
	  async def read_item(request: Request):
	  docs = conn.notes.notes.find({})
	  return templates.TemplateResponse(
	  request=request, name="index.html", context={"newDocs":newDocs},)