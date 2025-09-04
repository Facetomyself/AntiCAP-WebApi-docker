<div align="center">

# AntiCAP-WebApi

**基于FastAPI的验证码识别WebAPI服务**

[![Docker](https://img.shields.io/badge/Docker-支持-blue)](https://www.docker.com/)
[![ARM64](https://img.shields.io/badge/ARM64-支持-green)](https://en.wikipedia.org/wiki/ARM_architecture)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

*通过Http协议跨语言调用AntiCAP，实现自动化验证码识别*

<img src="https://img.shields.io/badge/GitHub-ffffff"></a> <a href="https://github.com/81NewArk/AntiCAP-WebApi"> <img src="https://img.shields.io/github/stars/81NewArk/AntiCAP-WebApi?style=social">

</div>

## 🌍 环境要求

- **Python**: >= 3.8 (64-bit)
- **推荐版本**: Python 3.10.6 (pyjwt库兼容性更好)
- **操作系统**: 支持Windows、Linux、macOS
- **架构**: 支持x86_64和ARM64

```bash
# Windows Python下载地址
https://registry.npmmirror.com/-/binary/python/3.10.6/python-3.10.6-amd64.exe
```

## 🚀 快速开始

### 🐳 Docker部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/81NewArk/AntiCAP-WebApi
cd AntiCAP-WebApi

# 2. 构建并启动Docker容器
docker-compose up -d

# 3. 访问服务
# Web界面: http://localhost:6688/login
# API文档: http://localhost:6688/docs
# 健康检查: http://localhost:6688/health
```

**Docker特性：**
- ✅ 支持x86_64和ARM64架构
- ✅ 开箱即用，无需手动安装依赖
- ✅ 自动健康检查和重启
- ✅ 安全隔离，非root用户运行
- ✅ 端口映射到6688

### 📁 本地安装

```bash
# 1. 克隆项目
git clone https://github.com/81NewArk/AntiCAP-WebApi
cd AntiCAP-WebApi

# 2. 安装依赖（推荐使用清华源）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 运行项目
python main.py

# 4. 首次运行需要设置账号密码和端口（默认6688）
# 账号密码会保存到.env文件中，可随时修改
```

### ⚡ 性能优化

项目支持以下性能优化配置：

```bash
# 环境变量配置
export UVICORN_WORKERS=4          # Worker进程数量
export UVICORN_HOST=0.0.0.0       # 监听地址
export UVICORN_PORT=6688          # 监听端口
export DEFAULT_USERNAME=admin     # 默认用户名
export DEFAULT_PASSWORD=password  # 默认密码
```

### 🔧 Docker Compose配置

```yaml
version: '3.8'
services:
  anticap-webapi:
    build: .
    ports:
      - "6688:8000"
    environment:
      - UVICORN_WORKERS=4
      - DEFAULT_USERNAME=admin
      - DEFAULT_PASSWORD=password
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## ✨ 功能特性

### 🎯 验证码识别类型
- ✅ **OCR文字识别** - 通用文字识别
- ✅ **数学计算识别** - 数学验证码识别
- ✅ **图标检测** - 目标图标定位
- ✅ **文字检测** - 文字区域定位
- ✅ **滑块验证码** - 缺口/阴影滑块识别
- ✅ **旋转验证码** - 双图旋转验证码

### 🔧 技术特性
- 🚀 **高性能**: 基于FastAPI异步框架
- 🐳 **容器化**: 完整的Docker支持
- 🔒 **安全认证**: JWT令牌认证
- 📊 **健康监控**: 内置健康检查端点
- 🌐 **跨平台**: 支持多种操作系统和架构
- 📚 **自动文档**: Swagger UI API文档

## 📖 API文档

启动服务后访问以下地址：

- **Web界面**: http://localhost:6688
- **API文档**: http://localhost:6688/docs
- **健康检查**: http://localhost:6688/health

### 🔐 认证方式

所有API接口都需要JWT认证：

```bash
# 1. 获取访问令牌
POST /api/login
{
  "username": "your_username",
  "password": "your_password"
}

# 2. 使用令牌调用API
Authorization: Bearer your_token_here
```

### 📁 模型管理

#### 获取可用模型列表
```bash
GET /api/models
Authorization: Bearer your_token_here
```

#### 使用自定义模型
在API请求中指定模型路径：

```bash
POST /api/math
{
  "img_base64": "your_image_base64",
  "math_model_path": "/app/Models/[Math]Detection_model.pt"
}
```

支持的模型参数：
- `math_model_path`: 数学识别模型 (.pt文件)
- `detectionIcon_model_path`: 图标检测模型 (.pt文件)
- `detectionText_model_path`: 文字检测模型 (.pt文件)
- `sim_onnx_model_path`: 相似度比较模型 (.onnx文件)

#### 默认模型文件
项目已包含以下预训练模型：
- `[Math]Detection_model.pt` - 数学验证码识别
- `[Icon]Detection_model.pt` - 图标检测
- `[Text]Detection_model.pt` - 文字检测
- `[Text]Siamese_model.onnx` - 文字相似度比较
- `[OCR]Ddddocr.onnx` - OCR文字识别

## 📋 使用示例

### 🐍 Python调用示例

```python
import requests
import base64

# 1. 获取访问令牌
def get_token():
    response = requests.post(
        "http://localhost:6688/api/login",
        data={
            "username": "admin",
            "password": "password"
        }
    )
    return response.json()["access_token"]

# 2. OCR文字识别
def ocr_recognition(image_path, token):
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        "http://localhost:6688/api/ocr",
        json={"img_base64": img_base64},
        headers=headers
    )
    return response.json()

# 3. 数学验证码识别
def math_recognition(image_path, token, custom_model=None):
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    data = {"img_base64": img_base64}
    if custom_model:
        data["math_model_path"] = custom_model

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        "http://localhost:6688/api/math",
        json=data,
        headers=headers
    )
    return response.json()

# 使用示例
if __name__ == "__main__":
    token = get_token()
    result = ocr_recognition("captcha.png", token)
    print("OCR结果:", result)
```

### 🌐 JavaScript调用示例

```javascript
// 1. 获取访问令牌
async function getToken() {
    const response = await fetch('http://localhost:6688/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'username=admin&password=password'
    });
    const data = await response.json();
    return data.access_token;
}

// 2. 上传图片进行识别
async function recognizeCaptcha(imageFile, token) {
    const formData = new FormData();
    formData.append('img_base64', await fileToBase64(imageFile));

    const response = await fetch('http://localhost:6688/api/ocr', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            img_base64: await fileToBase64(imageFile)
        })
    });

    return await response.json();
}

// 辅助函数：文件转Base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            // 移除data:image/...;base64,前缀
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = error => reject(error);
    });
}
```

### 🐚 cURL命令示例

```bash
# 1. 获取访问令牌
TOKEN=$(curl -X POST "http://localhost:6688/api/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password" \
  | jq -r '.access_token')

# 2. OCR识别
curl -X POST "http://localhost:6688/api/ocr" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"img_base64": "your_base64_image_data"}'

# 3. 使用自定义模型
curl -X POST "http://localhost:6688/api/math" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "img_base64": "your_base64_image_data",
    "math_model_path": "/app/Models/[Math]Detection_model.pt"
  }'
```

## 🏗️ 项目架构

```
AntiCAP-WebApi/
├── 📁 Models/                    # AI模型文件目录
│   ├── [Math]Detection_model.pt     # 数学验证码识别模型
│   ├── [Icon]Detection_model.pt     # 图标检测模型
│   ├── [Text]Detection_model.pt     # 文字检测模型
│   ├── [Text]Siamese_model.onnx     # 相似度比较模型
│   └── [OCR]Ddddocr.onnx           # OCR文字识别模型
├── 📁 static/                   # 静态文件目录
│   ├── index.html               # Web界面
│   ├── _next/                   # Next.js静态资源
│   └── favicon.ico              # 网站图标
├── 🐳 Dockerfile               # Docker构建文件
├── 🐳 docker-compose.yml       # Docker编排配置
├── 📋 requirements.txt         # Python依赖
├── 🔐 main.py                  # FastAPI主应用
└── 📖 README.md               # 项目文档
```

### 🔧 故障排除

#### 常见问题

**1. Docker构建失败**
```bash
# 清理Docker缓存
docker system prune -f

# 重新构建
docker-compose build --no-cache
```

**2. 端口占用**
```bash
# 检查端口占用
netstat -tlnp | grep 6688

# 修改端口映射
# 编辑 docker-compose.yml 中的端口配置
```

**3. 模型文件缺失**
```bash
# 检查Models目录
ls -la Models/

# 重新下载模型文件
# 或者使用默认模型
```

**4. 认证失败**
```bash
# 检查环境变量
docker exec anticap-webapi env | grep DEFAULT

# 重置.env文件
rm .env && docker-compose restart
```

**5. ARM64架构兼容性**
```bash
# 检查系统架构
uname -m

# 使用兼容的Docker镜像
# 项目已支持ARM64架构，无需额外配置
```

#### 性能调优

```bash
# 增加Worker数量
export UVICORN_WORKERS=8

# 调整内存限制
# 编辑 docker-compose.yml 中的内存配置

# 启用Gunicorn预加载
# 在Dockerfile中添加 --preload 参数
```

## 📋 待完成事项

### 🔧 技术优化
- [x] 修复HTML/CSS加载问题
- [ ] 优化前端界面样式
- [ ] 添加更多验证码类型支持
- [ ] 实现模型热更新机制

### 🚀 功能增强
- [x] 实现模型可替换功能
- [ ] 添加批量处理接口
- [ ] 支持自定义识别模型
- [ ] 添加识别结果缓存
- [ ] 实现识别历史记录

### 📦 部署优化
- [ ] 优化Docker镜像大小
- [ ] 添加多架构镜像构建
- [ ] 实现负载均衡配置
- [ ] 添加日志收集系统

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置

```bash
# 1. Fork项目
# 2. 克隆到本地
git clone https://github.com/your-username/AntiCAP-WebApi.git
cd AntiCAP-WebApi

# 3. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 4. 安装开发依赖
pip install -r requirements.txt

# 5. 运行项目
python main.py
```


## 📄 更新日志

### v1.0.6 (最新)
- ✅ **实现模型可替换功能** - 支持运行时切换AI模型
- ✅ **完善Docker支持** - 优化ARM64架构兼容性
- ✅ **添加健康监控** - 内置健康检查端点

### v1.0.5
- 🔧 基础FastAPI框架搭建
- 🐳 初步Docker容器化
- 📚 基础API文档生成

## 🔗 相关链接

- **项目主页**: https://github.com/81NewArk/AntiCAP-WebApi
- **AntiCAP原项目**: https://github.com/81NewArk/AntiCAP
- **FastAPI文档**: https://fastapi.tiangolo.com/
- **Docker文档**: https://docs.docker.com/

## 📜 许可证

本项目采用 **MIT License** 开源协议。

```
MIT License

Copyright (c) 2025 AntiCAP-WebApi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 💬 交流反馈

### 🐧 QQ交流群
<div align="center">
<img src="https://free.picui.cn/free/2025/07/04/6867f1907d1a0.png" alt="QQGroup" width="200" height="200">
</div>

## 🙏 支持项目

如果这个项目对你有帮助，欢迎赞助！

<div align="center">
<img src="https://free.picui.cn/free/2025/07/04/6867efd0bd67e.png" alt="Ali" width="200" height="200">
<img src="https://free.picui.cn/free/2025/07/04/6867efd0d7cbb.png" alt="Wx" width="200" height="200">
</div>

---

<div align="center">

## 🎉 项目状态

**⭐ 生产就绪 - 支持Docker一键部署**

**🚀 全架构兼容 - x86_64 & ARM64**

**🔒 安全可靠 - JWT认证 + 健康监控**

**📚 文档完善 - 中英文完整文档**

---

**⭐ 如果喜欢这个项目，请给我们一个Star！**

</div>




