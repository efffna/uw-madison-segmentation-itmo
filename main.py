from bdb import set_trace
from tools import Segmentation
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
import aiofiles
from typing import List

PATH_OUT = 'temp/out.png'
PATH_GIF = 'temp/1.gif'

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

img = Segmentation()


#@app.post("/upload_files")
#async def create_upload_files(files: List[UploadFile]):
#    print(files)
#    #return {"filenames": [file.filename for file in files]}


@app.post("/upload_files")
async def upload_files(files: UploadFile = File(...)):
    print("___")
    for file in files:
        print(file)
 



@app.get("/get_mask")
def get_img():    
    return FileResponse(PATH_OUT)