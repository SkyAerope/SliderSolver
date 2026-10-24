"""
SliderSolver核心实现模块
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw


class SliderSolver:
    """
    滑块验证码求解器
    
    根据背景图和缺口图计算出滑块需要移动的距离
    """
    
    def __init__(self, bg_img_path, tile_img_path):
        """
        初始化求解器
        
        Args:
            bg_img_path: 背景图片路径
            tile_img_path: 缺口图片路径
        """
        self.bg_img_path = bg_img_path
        self.tile_img_path = tile_img_path
        self.distance = None

    def detect_distance(self):
        """
        检测缺口在背景图中与左边距的距离
        
        Returns:
            int: 缺口的x坐标
        """
        bg = cv2.imread(self.bg_img_path, cv2.IMREAD_UNCHANGED)
        tile = cv2.imread(self.tile_img_path, cv2.IMREAD_UNCHANGED)

        # 去掉透明边
        if tile.shape[2] == 4:
            alpha = tile[:, :, 3]
            mask = alpha > 0
            x, y, w, h = cv2.boundingRect(mask.astype(np.uint8))
            tile = tile[y:y+h, x:x+w, :3]

        # 转灰度 + 边缘检测
        bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        tile_gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
        bg_edge = cv2.Canny(bg_gray, 50, 150)
        tile_edge = cv2.Canny(tile_gray, 50, 150)

        # 模板匹配
        res = cv2.matchTemplate(bg_edge, tile_edge, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        start_x = max_loc[0]

        self.distance = int(start_x + 10)
        return self.distance

    def save_marked(self, path):
        """
        在背景图上标记识别到的缺口位置并保存结果图片

        复用 detect_distance() 的计算结果，调用前必须先执行 detect_distance()

        Args:
            path: 结果图片保存路径

        Returns:
            str: 保存的结果图片路径

        Raises:
            RuntimeError: 如果尚未调用 detect_distance() 计算距离
        """
        if self.distance is None:
            raise RuntimeError("请先调用 detect_distance() 计算缺口距离后再调用 save_marked()")

        x = self.distance
        bg_img_path = self.bg_img_path

        img = Image.open(bg_img_path)
        img_draw = ImageDraw.Draw(img)
        img_draw.line((x, 0, x, img.size[1]), fill='red', width=2)

        img.save(path)
        return path
