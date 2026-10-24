# SliderSolver

[![Tests](https://github.com/SkyAerope/SliderSolver/actions/workflows/test.yml/badge.svg)](https://github.com/SkyAerope/SliderSolver/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/slider-solver-cv.svg)](https://pypi.org/project/slider-solver-cv/)
[![Python Versions](https://img.shields.io/pypi/pyversions/slider-solver-cv.svg)](https://pypi.org/project/slider-solver-cv/)
[![License](https://img.shields.io/github/license/SkyAerope/SliderSolver.svg)](https://github.com/SkyAerope/SliderSolver/blob/main/LICENSE)

**SliderSolver**（PyPI 包名：`slider-solver-cv`）是一个轻量级的滑块验证码缺口位置识别库。基于 OpenCV 边缘检测与模板匹配算法，自动计算滑块缺口在背景图中的水平偏移距离（像素），并提供结果可视化调试支持。

---

## 核心特性

- **开箱即用**：无需训练深度学习模型，纯图像处理方案，零配置直接调用。
- **抗干扰预处理**：自动剥离滑块拼图的 Alpha 透明空白边距，通过 Canny 边缘算子削弱光照与色彩干扰。
- **可视化校验**：内置标注输出功能，可在背景图上直接绘制识别出的校准线，便于调试与验证。
- **轻量依赖**：仅依赖 `opencv-python`、`numpy` 与 `pillow`，支持 Python 3.9 ~ 3.14。

---

## 安装

通过 `pip` 安装稳定版：

```bash
pip install slider-solver-cv
```

或从源码以可编辑模式安装：

```bash
git clone https://github.com/SkyAerope/SliderSolver.git
cd SliderSolver
pip install -e .
```

---

## 快速开始

### 1. 计算缺口距离

```python
from slider_solver import SliderSolver

solver = SliderSolver(
    bg_img_path="path/to/background.png",
    tile_img_path="path/to/slider.png",
)

distance = solver.detect_distance()
print(f"Horizontal offset: {distance}px")
```

### 2. 生成可视化标记图

在调用 `detect_distance()` 完成识别后，可调用 `save_marked()` 将计算出的缺口位置以红线标记在背景图上并保存：

```python
from slider_solver import SliderSolver

solver = SliderSolver(
    bg_img_path="path/to/background.png",
    tile_img_path="path/to/slider.png",
)

distance = solver.detect_distance()
output_path = solver.save_marked("path/to/marked_result.png")
print(f"Offset: {distance}px, marked image saved to: {output_path}")
```

---

## API 参考

### `SliderSolver(bg_img_path, tile_img_path)`

构造滑块求解器实例。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `bg_img_path` | `str` | 带缺口的背景图片文件路径 |
| `tile_img_path` | `str` | 滑块拼图图片文件路径（支持带 Alpha 通道的 PNG） |

### 方法

| 方法签名 | 返回类型 | 说明 |
| :--- | :--- | :--- |
| `detect_distance()` | `int` | 计算并缓存缺口距离背景图左边缘的水平像素坐标（`x` 轴偏移量）。 |
| `save_marked(path)` | `str` | 复用 `detect_distance()` 的计算结果，在背景图对应 `x` 坐标处绘制纵向标记线并保存至 `path`。若调用前未执行 `detect_distance()`，将抛出 `RuntimeError`。 |

---

## 算法流程

`SliderSolver` 采用经典的计算机视觉流水线定位缺口，具体步骤如下：

1. **图像加载**：以 `IMREAD_UNCHANGED` 模式读取背景图与滑块图，完整保留通道信息。
2. **透明边界裁剪**：若滑块图包含 Alpha 通道（4 通道 RGBA），提取非透明像素掩码并计算外接矩形（Bounding Box），裁除四周多余的透明边距。
3. **灰度化与边缘提取**：将背景图与裁剪后的滑块图转换为灰度图，并使用 Canny 算子（阈值 `50` / `150`）提取轮廓边缘特征。
4. **归一化相关匹配**：使用 `cv2.TM_CCOEFF_NORMED`（归一化相关系数匹配法）在背景边缘图中检索最佳匹配位置，计算最终水平偏移坐标。

---

## 开发与测试

本项目使用 `pytest` 进行单元测试，`tests/test_images/` 目录下提供了用于验证的标准测试样本。

```bash
# 1. 安装运行与测试依赖
pip install -r requirements.txt

# 2. 以可编辑模式安装当前包
pip install -e .

# 3. 执行测试套件
pytest tests/ -v
```

---

## 许可证

本项目基于 [Apache-2.0 License](LICENSE) 开源。
