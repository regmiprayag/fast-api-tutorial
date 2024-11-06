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
            "note":doc["note"]
        })
    return templates.TemplateResponse(
        request=request, name="index.html", context={"newDocs":newDocs},
    )