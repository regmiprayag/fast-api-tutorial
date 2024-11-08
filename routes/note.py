import os
from fastapi import APIRouter, UploadFile, File
from models.note import Note
from pathlib import Path
from config.db import conn
from bson import ObjectId
import shutil
from schema.note import noteEntity, notesEntity
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

note = APIRouter()

templates = Jinja2Templates(directory="templates")

notes_collection = conn.note.notes

UPLOAD_FOLDER = "images"
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
     # Extract form data
    form = await request.form()
    form_data = dict(form)

    # Ensure images folder exists
    os.makedirs("images", exist_ok=True)

    # Generate a unique filename
    existing_files = os.listdir("images")
    img_count = sum(1 for f in existing_files if f.startswith("IMG-") and f.endswith(".png"))
    new_filename = f"IMG-{img_count + 1:04}.png"

    # Save the image to the images folder
    image_path = f"images/{new_filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Add the image path and filename to form data
    form_data["image_path"] = image_path  # Only the path, not the UploadFile object
    form_data["image_filename"] = new_filename  # Store the filename in database

    # Store in MongoDB (add some metadata for identification)
    form_data["_id"] = str(ObjectId())  # Create a unique ObjectId
    result = notes_collection.insert_one(form_data)

    # Return the response with file information and MongoDB insert ID
    return {"success": True, "data_id": str(result.inserted_id), "filename": new_filename}