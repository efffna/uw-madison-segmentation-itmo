from tools import Segmentation
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from typing import List
import os


PATH_OUT = 'out.gif'


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],allow_headers=["*"])
img = Segmentation()


@app.post("/upload_files")
async def upload(files: List[UploadFile] = File(...)):
    count = 0
    for img_remove in [i for i in os.listdir('temp') if i.endswith('.png')]:
        os.remove('temp/'+img_remove)
    for file in files :
        contents = await file.read()
        img.preprocessing(contents)
        img.get_predict()
        os.rename('temp/out.png', f'temp/out{count}.png')
        count += 1
    img.gif_create()

    
@app.get("/get_mask")
def get_img():    
    return FileResponse(PATH_OUT)
