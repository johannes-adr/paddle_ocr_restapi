from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import shutil

app = FastAPI()

# Load PaddleOCR once at startup
ocr = PaddleOCR(use_angle_cls=True, lang='de')  # Set lang as needed

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    with open("temp_image.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ocr.ocr("temp_image.jpg", cls=True)
    parsed_result = []
    for line in result[0]:
        text = line[1][0]
        confidence = line[1][1]
        box = line[0]
        parsed_result.append({"text": text, "confidence": confidence, "box": box})

    return JSONResponse(content={"results": parsed_result})
