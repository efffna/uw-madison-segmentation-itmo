from tools import Segmentation
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response


PATH_OUT = 'temp/out.png'

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

img = Segmentation()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    img.preprocessing(contents)
    img.get_predict()


@app.get("/get_mask")
def get_img():    
    return FileResponse(PATH_OUT)