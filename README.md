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
# Web界面: http://localhost:6688
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

## 📋 待完成事项

### 🔧 技术优化
- [ ] 修复HTML/CSS加载问题
- [ ] 优化前端界面样式
- [ ] 添加更多验证码类型支持
- [ ] 实现模型热更新机制

### 🚀 功能增强
- [ ] 实现模型可替换功能
- [ ] 添加批量处理接口
- [ ] 支持自定义识别模型
- [ ] 添加识别结果缓存
- [ ] 实现识别历史记录

### 📦 部署优化
- [ ] 优化Docker镜像大小
- [ ] 添加多架构镜像构建
- [ ] 实现负载均衡配置
- [ ] 添加日志收集系统

### 🔒 安全加固
- [ ] 添加API限流机制
- [ ] 实现用户权限管理
- [ ] 添加HTTPS支持
- [ ] 敏感信息加密存储

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

## 📄 使用说明

本项目支持本地、局域网、公网部署。早期版本使用教程：[B站视频](https://www.bilibili.com/video/BV1xYGgz9ENE)

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

**⭐ 如果喜欢这个项目，请给我们一个Star！**

</div>




