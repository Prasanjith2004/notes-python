import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson.objectid import ObjectId

app = FastAPI()

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["notes_app"]
collection = db["notes"]

# Home page (Read)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    notes = [{"id": str(note["_id"]), "text": note["text"]} for note in collection.find()]
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

# Create note (form)
@app.post("/add")
async def add_note_form(note: str = Form(...)):
    collection.insert_one({"text": note})
    return RedirectResponse("/", status_code=303)

# Update note (form)
@app.post("/update/{note_id}")
async def update_note(note_id: str, note: str = Form(...)):
    collection.update_one({"_id": ObjectId(note_id)}, {"$set": {"text": note}})
    return RedirectResponse("/", status_code=303)

# Delete note
@app.get("/delete/{note_id}")
async def delete_note(note_id: str):
    collection.delete_one({"_id": ObjectId(note_id)})
    return RedirectResponse("/", status_code=303)

# API: Get all notes
@app.get("/api/notes")
async def get_notes():
    notes = [{"id": str(note["_id"]), "text": note["text"]} for note in collection.find()]
    return {"notes": notes}

# API: Create note
@app.post("/api/notes")
async def add_note_api(note: str):
    result = collection.insert_one({"text": note})
    return {"message": "Note added", "id": str(result.inserted_id)}

# API: Update note
@app.put("/api/notes/{note_id}")
async def update_note_api(note_id: str, note: str):
    collection.update_one({"_id": ObjectId(note_id)}, {"$set": {"text": note}})
    return {"message": "Note updated", "id": note_id}

# API: Delete note
@app.delete("/api/notes/{note_id}")
async def delete_note_api(note_id: str):
    collection.delete_one({"_id": ObjectId(note_id)})
    return {"message": "Note deleted", "id": note_id}
