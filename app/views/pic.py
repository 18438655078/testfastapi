import uuid
import os

from PIL import Image, ImageDraw, ImageFont

from fastapi import APIRouter, File, UploadFile, Form

from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse, FileResponse, HTMLResponse


router = APIRouter()


@router.post("/make")
async def make(
    font_size: int = Form(6),
    text: str = Form("我喜欢你"),
    file: UploadFile = File(...),
):
    if file.content_type[:5] != "image":
        return {"msg": "请上传图片文件！"}
    contents = await file.read()
    
    img_path = "./imgs/%s.png" % repr(uuid.uuid4())

    with open(img_path, 'wb') as f:
        f.write(contents)

    img_raw = Image.open(img_path)
    img_array = img_raw.load()

    img_new = Image.new("RGB", img_raw.size, (0, 0, 0))
    draw = ImageDraw.Draw(img_new)
    font = ImageFont.truetype('./imgs/SIMKAI.TTF', font_size)

    def character_generator(text):
        while True:
            for i in range(len(text)):
                yield text[i]

    ch_gen = character_generator(text)

    for y in range(0, img_raw.size[1], font_size):
        for x in range(0, img_raw.size[0], font_size):
            draw.text((x, y), next(ch_gen), font=font, fill=img_array[x, y], direction=None)

    img_new.convert('RGB').save(img_path)
    # 先创建文件，返回成功后删除；未找到流式文件方法
    async def rmf():
        os.remove(img_path)
    return FileResponse(img_path, background=rmf)



def generate_html_response():
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
    <div>
    <form action="/api/make" method="post" enctype ="multipart/form-data">
    输入背景文字：<br><input type="text" id="text" name="text" value="我喜欢你"><br><br>
    选择背景文字大小:<br><input type="number" id="channel_img" name="font_size" value=6><br><br>
    选择图片:<br>
    <input type="file" name="file"  multiple="multiple">
    <br>
    <input type="submit" onclick="setValue()" value="Submit image file">
    </form> 
    </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/html/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()
