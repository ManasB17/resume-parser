import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from extract_resume_info import driver
# from extract_text import extract_text_from_resume
from pydantic import BaseModel
import aiofiles

#define fastapi
app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File()):
    contents = await file.read()
    print("Type", contents)
    out_file_path = './data/resume/test.pdf'
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
        
    value = driver(file_path=out_file_path)
    return {"Filename": file.filename} 

@app.post("/display")
async def display_outcome(file: UploadFile = File()):
    contents = await file.read()
    contents = await file.read()
    value = driver(file_path=contents)
    return value

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
