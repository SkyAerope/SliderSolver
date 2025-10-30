# SliderSolver

![Tests](https://github.com/SkyAerope/SliderSolver/workflows/Run%20Tests/badge.svg)
![PyPI](https://img.shields.io/pypi/v/slider-solver-cv)
![Python](https://img.shields.io/pypi/pyversions/slider-solver-cv)
![License](https://img.shields.io/github/license/SkyAerope/SliderSolver)

一个用于识别滑块验证码缺口位置的 Python 包。通过图像处理技术，自动识别缺口在背景图中的位置，并返回缺口左边缘到背景图左边缘的距离。

## 功能特点

- 🎯 精准定位：使用 OpenCV 模板匹配算法精确识别缺口位置
- 🖼️ 边缘检测：基于 Canny 边缘检测提高匹配准确率
- 📊 可视化结果：自动在背景图上标记识别位置
- 🚀 简单易用：仅需两行代码即可完成识别

## 安装

### 从源码安装

```bash
git clone https://github.com/SkyAerope/SliderSolver.git
cd SliderSolver
pip install -e .
```

### 使用 pip 安装

```bash
pip install slider-solver-cv
```

## 依赖

- Python >= 3.9
- opencv-python >= 4.5.0
- numpy >= 1.19.0
- pillow >= 8.0.0

## 使用方法

### 基本用法

```python
from slider_solver import SliderSolver

# 创建求解器实例
solver = SliderSolver(
    bg_img_path='path/to/background.png',    # 背景图路径
    front_img_path='path/to/slider.png'      # 缺口图路径
)

# 计算缺口位置
distance = solver.detect_distance()
print(f'缺口位置: {distance}px')
```

### 带可视化的完整示例

```python
from slider_solver import SliderSolver
import os

def solve_slider_captcha():
    # 图片路径
    bg_img = 'images/background.png'
    slider_img = 'images/slider.png'
  
    # 检查文件是否存在
    if not os.path.exists(bg_img) or not os.path.exists(slider_img):
        print("错误：图片文件不存在")
        return
  
    # 创建求解器
    solver = SliderSolver(bg_img, slider_img)
  
    # 计算位置
    distance = solver.detect_distance()
    print(f'✅ 识别成功！缺口位置在 x = {distance}px')
  
    # 可选：绘制标记线并保存结果图片
    result_path = solver.draw_line(distance, bg_img)
    print(f'📁 结果图片已保存到: {result_path}')
  
    return distance

if __name__ == '__main__':
    solve_slider_captcha()
```

### 自定义保存路径

```python
from slider_solver import SliderSolver

solver = SliderSolver('background.png', 'slider.png')
distance = solver.detect_distance()

# 指定自定义的保存路径
result_path = solver.draw_line(
    x=distance,
    bg_img_path='background.png',
    target_path='output/marked_result.png'  # 可选，不指定则自动生成
)
print(f'结果保存到: {result_path}')
```

## API 说明

### SliderSolver 类

#### `__init__(bg_img_path, front_img_path)`

初始化求解器。

**参数：**

- `bg_img_path` (str): 背景图片的文件路径
- `front_img_path` (str): 缺口图片的文件路径

#### `detect_distance()`

检测缺口在背景图中的 x 坐标位置。

**返回值：**

- `int`: 缺口距离左边界的像素距离

**示例：**

```python
solver = SliderSolver('bg.png', 'slider.png')
distance = solver.detect_distance()  # 返回如: 120
```

#### `draw_line(x, bg_img_path, target_path=None)`

在背景图上绘制红色竖线标记位置。

**参数：**

- `x` (int): 竖线的 x 坐标
- `bg_img_path` (str): 背景图片路径
- `target_path` (str, 可选): 结果图片保存路径，不指定则自动生成（添加 `_result` 后缀）

**返回值：**

- `str`: 保存的结果图片路径

**示例：**

```python
result_path = solver.draw_line(120, 'bg.png')  # 自动保存为 bg_result.png
# 或指定路径
result_path = solver.draw_line(120, 'bg.png', 'output/marked.png')
```

## 工作原理

1. **读取图片**：加载背景图和缺口图
2. **预处理**：去除缺口图的透明边界
3. **灰度转换**：将图片转换为灰度图
4. **边缘检测**：使用 Canny 算法检测边缘
5. **模板匹配**：使用 TM_CCOEFF_NORMED 方法进行匹配
6. **返回结果**：返回匹配到的 x 坐标
7. **可选可视化**：调用 `draw_line()` 方法绘制标记线

## 项目结构

```
SliderSolver/
├── src/
│   └── slider_solver/
│       ├── __init__.py      # 包初始化文件
│       └── solver.py        # 核心实现
├── tests/                   # 测试目录
│   ├── __init__.py         # 测试包初始化
│   ├── test_solver.py      # 单元测试
│   └── test_images/        # 测试图片
│       ├── bg1.png         # 测试背景图1
│       ├── bg2.png         # 测试背景图2
│       ├── t1.png          # 测试滑块图1
│       └── t2.png          # 测试滑块图2
├── setup.py                # 安装配置（传统方式）
├── pyproject.toml         # 现代 Python 包配置
├── requirements.txt       # 依赖列表
├── README.md             # 使用文档
├── LICENSE               # 许可证
└── .gitignore           # Git 忽略规则
```

## 开发与测试

### 安装开发依赖

```bash
# 安装所有依赖（包括测试工具）
pip install -r requirements.txt
```

### 运行测试

`tests/test_images`中含有示例图片，可以用于测试目的

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_solver.py::TestSliderSolver::test_detect_distance_case1 -v

# 显示详细输出
pytest tests/ -v -s
```

### 测试覆盖的功能

- ✅ 基本的距离检测功能
- ✅ 多组图片组合测试
- ✅ 默认路径的标记线绘制
- ✅ 自定义路径的标记线绘制
- ✅ 无效路径的错误处理
- ✅ 初始化参数验证

## 许可证

本项目采用 Apache-2.0 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

- GitHub: [@SkyAerope](https://github.com/SkyAerope)
