# 阶段1：构建依赖
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LIBGL_ALWAYS_SOFTWARE=1 \
    MESA_GL_VERSION_OVERRIDE=3.3

# 安装系统依赖（根据项目需求调整）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev \
    libglib2.0-0 \
    libgomp1 \
    libegl-mesa0 \
    libglx-mesa0 \
    libosmesa6 \
    mesa-utils && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖（分层优化，利用Docker缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---
# 阶段2：生产镜像
FROM python:3.11-slim

# 补上缺失的 OpenGL/Mesa 运行时库
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 libgl1-mesa-dri libglapi-mesa libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 从builder阶段复制已安装的Python包
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制项目代码（通过.dockerignore过滤无关文件）
COPY . .

# 安全配置：使用非root用户
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# 环境变量
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 \
    LIBGL_ALWAYS_SOFTWARE=1 \
    MESA_GL_VERSION_OVERRIDE=3.3

# 暴露端口
EXPOSE 8000

# 健康检查端点
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# 启动命令（使用Uvicorn，单进程模式）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
