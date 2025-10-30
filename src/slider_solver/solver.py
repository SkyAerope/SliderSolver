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
    
    def __init__(self, bg_img_path, front_img_path):
        """
        初始化求解器
        
        Args:
            bg_img_path: 背景图片路径
            front_img_path: 缺口图片路径
        """
        self.bg_img_path = bg_img_path
        self.front_img_path = front_img_path

    def detect_distance(self):
        """
        检测缺口在背景图中与左边距的距离
        
        Returns:
            int: 缺口的x坐标
        """
        bg = cv2.imread(self.bg_img_path, cv2.IMREAD_UNCHANGED)
        tile = cv2.imread(self.front_img_path, cv2.IMREAD_UNCHANGED)

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

        # 绘制结果
        # self.draw_line(start_x + 10)
        return start_x + 10

    def draw_line(self, x, bg_img_path, target_path=None):
        """
        在背景图上绘制一条竖线，用于标记识别的缺口位置
        
        Args:
            x: 竖线的x坐标
        """
        img = Image.open(bg_img_path)
        img_draw = ImageDraw.Draw(img)
        img_draw.line((x, 0, x, img.size[1]), fill='red', width=2)
        
        # 保存到同目录下，文件名添加_result后缀
        if not target_path:
            if bg_img_path.endswith('.jpg'):
                target_path = bg_img_path.replace('.jpg', '_result.png')
            else:
                target_path = bg_img_path.replace('.png', '_result.png')

        img.save(target_path)
        # print(f'结果图片已保存到: {target_path}')
        return target_path
