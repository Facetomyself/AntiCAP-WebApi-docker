import os
import jwt
import AntiCAP
import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


def get_required_env(name: str, *, allow_empty: bool = False) -> str:
    value = os.getenv(name, "")
    if value or allow_empty:
        return value
    raise RuntimeError(f"Missing required environment variable: {name}")


SECRET_KEY = get_required_env("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 * 60 * 24 * 60  # 60天
VALID_USERNAME = get_required_env("DEFAULT_USERNAME")
VALID_PASSWORD = get_required_env("DEFAULT_PASSWORD")
APP_PORT = int(os.getenv("PORT", os.getenv("UVICORN_PORT", "8000")))

description = """
* 通过Http协议 跨语言调用AntiCAP

<img src="https://img.shields.io/badge/GitHub-ffffff"></a> <a href="https://github.com/81NewArk/AntiCAP-WebApi"> <img src="https://img.shields.io/github/stars/81NewArk/AntiCAP-WebApi?style=social">

"""

app = FastAPI(
    title="AntiCAP - WebApi",
    description=description,
    version="1.1.1-docker",
    docs_url=None,
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - 开发者文档",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/swagger/swagger-ui-bundle.js",
        swagger_css_url="/swagger/swagger-ui.css",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ModelImageIn(BaseModel):
    img_base64: str
    math_model_path: Optional[str] = None
    detectionIcon_model_path: Optional[str] = None
    detectionText_model_path: Optional[str] = None


class ModelOrderImageIn(BaseModel):
    order_img_base64: str
    target_img_base64: str
    detectionIcon_model_path: Optional[str] = None
    detectionText_model_path: Optional[str] = None
    sim_onnx_model_path: Optional[str] = None


class SliderImageIn(BaseModel):
    target_base64: str
    background_base64: str


class CompareImageIn(BaseModel):
    img1_base64: str
    img2_base64: str
    sim_onnx_model_path: Optional[str] = None


class DoubleRotateIn(BaseModel):
    inside_base64: str
    outside_base64: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
Atc = AntiCAP.Handler(show_banner=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now_utc = datetime.now(timezone.utc)
    expire = now_utc + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


@app.get("/health", summary="健康检查", tags=["公共"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/models", summary="获取可用模型列表", tags=["模型管理"])
async def get_available_models(current_user: str = Depends(get_current_user)):
    models_dir = os.path.join(os.getcwd(), "Models")
    if not os.path.exists(models_dir):
        return {"models": [], "message": "Models directory not found"}

    model_files = []
    for filename in os.listdir(models_dir):
        filepath = os.path.join(models_dir, filename)
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            model_files.append({
                "name": filename,
                "path": filepath,
                "size": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2)
            })
    return {"models": model_files, "total": len(model_files), "models_dir": models_dir}


@app.post("/api/login", summary="登录获取JWT", tags=["公共"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != VALID_USERNAME or form_data.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/tokens/verification", summary="验证JWT", tags=["公共"])
async def verify_token_endpoint(current_user: str = Depends(get_current_user)):
    return {"username": current_user}


@app.post("/api/ocr", summary="返回字符串", tags=["OCR识别"])
async def ocr(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    return {"result": Atc.OCR(data.img_base64)}


@app.post("/api/math", summary="返回计算结果", tags=["计算识别"])
async def math(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Math(data.img_base64, math_model_path=data.math_model_path) if data.math_model_path else Atc.Math(data.img_base64)
    return {"result": result}


@app.post("/api/detection/icon", summary="检测图标,返回坐标", tags=["目标检测"])
async def detection_icon(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Detection_Icon(data.img_base64, detectionIcon_model_path=data.detectionIcon_model_path) if data.detectionIcon_model_path else Atc.Detection_Icon(data.img_base64)
    return {"result": result}


@app.post("/api/detection/text", summary="侦测文字,返回坐标", tags=["目标检测"])
async def detection_text(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Detection_Text(data.img_base64, detectionText_model_path=data.detectionText_model_path) if data.detectionText_model_path else Atc.Detection_Text(data.img_base64)
    return {"result": result}


@app.post("/api/detection/icon/order", summary="按序返回图标的坐标", tags=["目标检测"])
async def detection_icon_order(data: ModelOrderImageIn, current_user: str = Depends(get_current_user)):
    if data.detectionIcon_model_path and data.sim_onnx_model_path:
        result = Atc.ClickIcon_Order(order_img_base64=data.order_img_base64, target_img_base64=data.target_img_base64, detectionIcon_model_path=data.detectionIcon_model_path, sim_onnx_model_path=data.sim_onnx_model_path)
    else:
        result = Atc.ClickIcon_Order(order_img_base64=data.order_img_base64, target_img_base64=data.target_img_base64)
    return {"result": result}


@app.post("/api/detection/text/order", summary="按序返回文字的坐标", tags=["目标检测"])
async def detection_text_order(data: ModelOrderImageIn, current_user: str = Depends(get_current_user)):
    if data.detectionText_model_path and data.sim_onnx_model_path:
        result = Atc.ClickText_Order(order_img_base64=data.order_img_base64, target_img_base64=data.target_img_base64, detectionText_model_path=data.detectionText_model_path, sim_onnx_model_path=data.sim_onnx_model_path)
    else:
        result = Atc.ClickText_Order(order_img_base64=data.order_img_base64, target_img_base64=data.target_img_base64)
    return {"result": result}


@app.post("/api/slider/match", summary="缺口滑块,返回坐标", tags=["滑块验证码，OpenCV算法"])
async def slider_match(data: SliderImageIn, current_user: str = Depends(get_current_user)):
    return {"result": Atc.Slider_Match(target_base64=data.target_base64, background_base64=data.background_base64)}


@app.post("/api/slider/comparison", summary="阴影滑块,返回坐标", tags=["滑块验证码，OpenCV算法"])
async def slider_comparison(data: SliderImageIn, current_user: str = Depends(get_current_user)):
    return {"result": Atc.Slider_Comparison(target_base64=data.target_base64, background_base64=data.background_base64)}


@app.post("/api/compare/similarity", summary="对比图片相似度", tags=["图片对比，孪生神经经网络模型"])
async def compare_similarity(data: CompareImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.compare_image_similarity(image1_base64=data.img1_base64, image2_base64=data.img2_base64, sim_onnx_model_path=data.sim_onnx_model_path) if data.sim_onnx_model_path else Atc.compare_image_similarity(image1_base64=data.img1_base64, image2_base64=data.img2_base64)
    return {"result": float(result)}


@app.post("/api/rotate/double/rotate", summary="双图旋转验证码", tags=["旋转验证码，OpenCV算法"])
async def double_rotate(data: DoubleRotateIn, current_user: str = Depends(get_current_user)):
    return {"result": Atc.Double_Rotate(inside_base64=data.inside_base64, outside_base64=data.outside_base64)}


app.mount("/swagger", StaticFiles(directory="static/swagger"), name="swagger")
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == '__main__':
    print("Starting AntiCAP-WebApi...")
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT, access_log=True)
