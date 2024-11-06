from fastapi import APIRouter
from models.note import Note
from config.db import conn
from schema.note import noteEntity, notesEntity
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

note = APIRouter()

templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id":doc["_id"],
            "title":doc["title"],
            "desc":doc["desc"],
            "important":doc["important"]
        })
    return templates.TemplateResponse(
        request=request, name="index.html", context={"newDocs":newDocs},
    )

@note.post("/")
async def create_item(request: Request):
    print("hello prayag")
    form = await request.form()
    print(form)
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    print("After the data is")
    print(formDict)
    inserted_note = conn.note.notes.insert_one(formDict)
    print(inserted_note)
    return {"Success": True}