# 图片库AI打标签功能

基于FastAPI和AI模型的图片自动标签生成。

## 项目结构

```
/project
    /images               # 用于存储上传的图片
    /app
        __init__.py       # Python包初始化文件
        main.py           # FastAPI 服务代码
        model.py          # AI 模型代码
        requirements.txt  # 依赖文件
    Dockerfile
    docker-compose.yml
    README.md
```

## 功能特性

- 图片上传和存储
- AI自动标签生成
- RESTful API接口
- Docker容器化部署
- 异步处理支持
- 支持多种图片格式

## 使用步骤

### 方式1：使用Docker Compose（推荐）

1. 克隆项目到本地
2. 在项目根目录执行：

```bash
docker-compose up -d
```

3. 服务将在 http://localhost:8000 启动

### 方式2：本地开发

1. 安装Python依赖：

```bash
cd app
pip install -r requirements.txt
```

2. 启动服务：

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API接口

### 上传图片并获取标签

```http
POST /api/upload
Content-Type: multipart/form-data

file: [图片文件]
```

响应：
```json
{
    "status": "success",
    "filename": "unique-filename.jpg",
    "tags": ["人物", "室外", "明亮"],
    "image_url": "/images/unique-filename.jpg"
}
```

### 获取图片标签

```http
GET /api/images/{filename}/tags
```

响应：
```json
{
    "filename": "example.jpg",
    "tags": ["风景", "天空", "蓝色调"]
}
```

### 获取图片列表

```http
GET /api/images/list
```

响应：
```json
{
    "images": [
        {
            "filename": "example1.jpg",
            "url": "/images/example1.jpg"
        },
        {
            "filename": "example2.png",
            "url": "/images/example2.png"
        }
    ]
}
```

### 测试页面

项目根目录包含一个 `test.html` 文件，可以直接在浏览器中打开进行功能测试：

```bash
# 用浏览器打开测试页面
open test.html
```

## 配置说明

### 环境变量

- `PYTHONPATH`: Python模块搜索路径
- `PYTHONUNBUFFERED`: 禁用Python输出缓冲

### 支持的图片格式

- PNG
- JPEG/JPG
- GIF
- BMP
- WebP

## 扩展功能

### 集成更强大的AI模型

可以在 `model.py` 中集成其他模型，我这里列出了一些可能有用的：

1. **预训练的图像分类模型**：
   - ResNet
   - EfficientNet
   - Vision Transformer (ViT)

2. **多模态模型**：
   - CLIP
   - BLIP

3. **专用标签模型**：
   - 场景识别模型
   - 物体检测模型

## 开发说明

### 目录结构

- `app/main.py`: FastAPI应用主文件，包含API路由定义
- `app/model.py`: AI模型相关代码，包含标签生成逻辑
- `images/`: 图片存储目录
- `Dockerfile`: Docker镜像构建文件
- `docker-compose.yml`: Docker编排文件

### 开发模式

启动开发服务器：

```bash
cd app
uvicorn main:app --reload
```

## 部署

### 生产环境部署

1. 构建Docker镜像：

```bash
docker build -t image-tagger .
```

2. 运行容器：

```bash
docker run -d -p 8000:8000 -v ./images:/app/images image-tagger
```

## 许可证

MIT License

