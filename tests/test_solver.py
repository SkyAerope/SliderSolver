"""
SliderSolver 核心功能测试
"""

import os
import pytest
from slider_solver import SliderSolver


# 获取测试图片路径
TEST_DIR = os.path.dirname(__file__)
TEST_IMAGES_DIR = os.path.join(TEST_DIR, 'test_images')


class TestSliderSolver:
    """测试 SliderSolver 类的功能"""
    
    def test_detect_distance_case1(self):
        """测试用例1：bg1 + t1 组合"""
        bg_path = os.path.join(TEST_IMAGES_DIR, 'bg1.png')
        slider_path = os.path.join(TEST_IMAGES_DIR, 't1.png')
        
        # 确保测试文件存在
        assert os.path.exists(bg_path), f"背景图不存在: {bg_path}"
        assert os.path.exists(slider_path), f"滑块图不存在: {slider_path}"
        
        # 创建求解器并计算距离
        solver = SliderSolver(bg_path, slider_path)
        distance = solver.detect_distance()
        
        # 验证结果
        assert isinstance(distance, int), "返回值应该是整数"
        assert distance > 0, "距离应该大于0"
        assert distance < 500, "距离应该在合理范围内"
        
        print(f"测试用例1 - 检测到的距离: {distance}px")
    
    def test_detect_distance_case2(self):
        """测试用例2：bg2 + t2 组合"""
        bg_path = os.path.join(TEST_IMAGES_DIR, 'bg2.png')
        slider_path = os.path.join(TEST_IMAGES_DIR, 't2.png')
        
        # 确保测试文件存在
        assert os.path.exists(bg_path), f"背景图不存在: {bg_path}"
        assert os.path.exists(slider_path), f"滑块图不存在: {slider_path}"
        
        # 创建求解器并计算距离
        solver = SliderSolver(bg_path, slider_path)
        distance = solver.detect_distance()
        
        # 验证结果
        assert isinstance(distance, int), "返回值应该是整数"
        assert distance > 0, "距离应该大于0"
        assert distance < 500, "距离应该在合理范围内"
        
        print(f"测试用例2 - 检测到的距离: {distance}px")
    
    def test_draw_line_default_path(self):
        """测试绘制标记线功能（默认保存路径）"""
        bg_path = os.path.join(TEST_IMAGES_DIR, 'bg1.png')
        slider_path = os.path.join(TEST_IMAGES_DIR, 't1.png')
        
        solver = SliderSolver(bg_path, slider_path)
        distance = solver.detect_distance()
        
        # 绘制标记线
        result_path = solver.draw_line(distance, bg_path)
        
        # 验证结果文件
        assert result_path is not None, "应该返回结果路径"
        assert os.path.exists(result_path), f"结果图片应该被创建: {result_path}"
        assert result_path.endswith('_result.png'), "结果文件名应该包含 _result"
        
        print(f"标记图片已保存: {result_path}")
        
        # 清理测试生成的文件
        if os.path.exists(result_path):
            os.remove(result_path)
    
    def test_draw_line_custom_path(self):
        """测试绘制标记线功能（自定义保存路径）"""
        bg_path = os.path.join(TEST_IMAGES_DIR, 'bg1.png')
        slider_path = os.path.join(TEST_IMAGES_DIR, 't1.png')
        custom_output = os.path.join(TEST_IMAGES_DIR, 'test_custom_output.png')
        
        solver = SliderSolver(bg_path, slider_path)
        distance = solver.detect_distance()
        
        # 绘制标记线到自定义路径
        result_path = solver.draw_line(distance, bg_path, custom_output)
        
        # 验证结果
        assert result_path == custom_output, "应该返回自定义路径"
        assert os.path.exists(result_path), f"结果图片应该被创建: {result_path}"
        
        print(f"标记图片已保存到自定义路径: {result_path}")
        
        # 清理测试生成的文件
        if os.path.exists(result_path):
            os.remove(result_path)
    
    def test_invalid_image_path(self):
        """测试无效图片路径的处理"""
        with pytest.raises(Exception):
            solver = SliderSolver('nonexistent_bg.png', 'nonexistent_slider.png')
            solver.detect_distance()
    
    def test_initialization(self):
        """测试初始化参数"""
        bg_path = os.path.join(TEST_IMAGES_DIR, 'bg1.png')
        slider_path = os.path.join(TEST_IMAGES_DIR, 't1.png')
        
        solver = SliderSolver(bg_path, slider_path)
        
        assert solver.bg_img_path == bg_path, "背景图路径应该被正确保存"
        assert solver.front_img_path == slider_path, "滑块图路径应该被正确保存"


def test_all_combinations():
    """测试所有可能的图片组合"""
    backgrounds = ['bg1.png', 'bg2.png']
    sliders = ['t1.png', 't2.png']
    
    results = []
    
    for bg in backgrounds:
        for slider in sliders:
            bg_path = os.path.join(TEST_IMAGES_DIR, bg)
            slider_path = os.path.join(TEST_IMAGES_DIR, slider)
            
            if os.path.exists(bg_path) and os.path.exists(slider_path):
                solver = SliderSolver(bg_path, slider_path)
                distance = solver.detect_distance()
                results.append({
                    'background': bg,
                    'slider': slider,
                    'distance': distance
                })
                print(f"{bg} + {slider} -> 距离: {distance}px")
    
    # 至少应该成功测试一个组合
    assert len(results) > 0, "应该至少有一个成功的测试"
    
    return results


if __name__ == '__main__':
    # 运行所有测试
    pytest.main([__file__, '-v', '-s'])
