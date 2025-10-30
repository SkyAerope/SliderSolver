"""
slider_solver - 滑块验证码位置识别工具

根据背景图和缺口图计算滑块位置
"""

from setuptools import setup, find_packages

# 读取 README 文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取依赖
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="slider-solver",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个用于识别滑块验证码位置的Python包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SkyAerope/SliderSolver",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="slider captcha opencv computer-vision",
    project_urls={
        "Bug Reports": "https://github.com/SkyAerope/SliderSolver/issues",
        "Source": "https://github.com/SkyAerope/SliderSolver",
    },
)
