from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import shutil
from PIL import Image
from typing import List
import uuid
from .model import ImageTagger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

images_dir = "/app/images"
os.makedirs(images_dir, exist_ok=True)

app.mount("/images", StaticFiles(directory=images_dir), name="images")

tagger = ImageTagger()

@app.get("/")
async def root():
    return {"message": "图片库AI打标签服务正在运行"}

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只支持图片文件")
    
    try:
        # 生成唯一文件名
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"{images_dir}/{unique_filename}"
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        tags = await tagger.generate_tags(file_path)
        
        return {
            "status": "success",
            "filename": unique_filename,
            "tags": tags,
            "image_url": f"/images/{unique_filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理图片时出错: {str(e)}")

@app.get("/api/images/{filename}/tags")
async def get_image_tags(filename: str):
    file_path = f"{images_dir}/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="图片不存在")
    
    try:
        tags = await tagger.generate_tags(file_path)
        return {"filename": filename, "tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成标签时出错: {str(e)}")

@app.get("/api/images/list")
async def list_images():
    if not os.path.exists(images_dir):
        return {"images": []}
    
    images = []
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            images.append({
                "filename": filename,
                "url": f"/images/{filename}"
            })
    
    return {"images": images}
