from PIL import Image
from typing import List, Dict
import random

class ImageTagger:
    def __init__(self):
        self.labels = [
            "人物", "风景", "动物", "建筑", "食物", "交通工具", "植物", "天空",
            "水", "山", "城市", "自然", "室内", "室外", "艺术", "运动",
            "科技", "时尚", "抽象", "黑白", "彩色", "夜景", "日景"
        ]
    
    async def generate_tags(self, image_path: str) -> List[str]:
        try:
            image = Image.open(image_path).convert("RGB")
            tags = await self._analyze_image(image)
            return tags
        except:
            return ["未知"]
    
    async def _analyze_image(self, image: Image.Image) -> List[str]:
        tags = []
        width, height = image.size
        aspect_ratio = width / height
        
        if width > 1920 or height > 1080:
            tags.append("高清")
        
        if aspect_ratio > 1.5:
            tags.append("横屏")
        elif aspect_ratio < 0.67:
            tags.append("竖屏")
        else:
            tags.append("方形")
        
        colors = image.getcolors(maxcolors=256*256*256)
        if colors:
            dominant_color = max(colors, key=lambda x: x[0])
            color_value = dominant_color[1]
            
            if isinstance(color_value, tuple) and len(color_value) >= 3:
                r, g, b = color_value[:3]
                
                if r > 200 and g > 200 and b > 200:
                    tags.append("明亮")
                elif r < 50 and g < 50 and b < 50:
                    tags.append("暗色")
                
                if r > g and r > b:
                    tags.append("红色调")
                elif g > r and g > b:
                    tags.append("绿色调")
                elif b > r and b > g:
                    tags.append("蓝色调")
        
        tags.extend(["图片", "内容"])
        random_tags = random.sample(self.labels, min(3, len(self.labels)))
        tags.extend(random_tags)
        
        return list(set(tags))
    
    def get_available_labels(self) -> List[str]:
        return self.labels.copy()
    
    async def batch_generate_tags(self, image_paths: List[str]) -> Dict[str, List[str]]:
        results = {}
        
        for image_path in image_paths:
            try:
                tags = await self.generate_tags(image_path)
                filename = image_path.split("/")[-1]
                results[filename] = tags
            except:
                filename = image_path.split("/")[-1]
                results[filename] = ["处理失败"]
        
        return results
