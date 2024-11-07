import os
from fastapi import APIRouter, UploadFile, File
from models.note import Note
from pathlib import Path
from config.db import conn
from bson import ObjectId
from schema.note import noteEntity, notesEntity
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

note = APIRouter()

templates = Jinja2Templates(directory="templates")

notes_collection = conn.note.notes

UPLOAD_FOLDER = "uploads/images"
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = notes_collection.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id":doc["_id"],
            "title":doc["title"],
            "desc":doc["desc"],
            "important":doc["important"],
            "image":doc["image"]
        })
    return templates.TemplateResponse(
        request=request, name="index.html", context={"newDocs":newDocs},
    )

@note.post("/")
async def create_item(request: Request, image: UploadFile = File(...)):
    print("hello prayag")
    form = await request.form()
    print(form)
    formDict = dict(form)
    formDict["important"] = formDict.get("important") == "on"
     # Save the image file to the images folder
    image_path = f"{UPLOAD_FOLDER}/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    formDict["image_path"] = image_path

    # Convert form data to NoteData model
    note_data = Note(**formDict)

    inserted_note = notes_collection.insert_one(note)
    print(inserted_note)
    return {"Success": True}