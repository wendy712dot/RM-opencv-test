# RM-opencv-test

本程序对几个视觉实验进行复现，主要包括
1. 颜色分割实验
2. 多边形检测实验
3. Tag识别（位姿解算）

## 开发环境
1. 基于 python版opencv 编写
2. 需下载 OpenCV-Python 和 opencv-contrib-python

## 项目结构
```text
PythonProject/  
├── 📄 task1.py                        
| 
├── 📄 task2.py
| 
├── 📄 task2-extra-test.py
| 
├── 📄 task2-extra.py
| 
├── 📄 task3-calibration.py
| 
├── 📄 task3.py
| 
├── 📄 img-out.png
| 
├── 📄 ubuntu-opencv.png
| 
├── 📁 resources/                  # 实验中用到的（处理的）图片及视频  
│    ├── bed_pic.png
│    ├── initial_image.png
│    ├── test.png
│    └── testVideo.mp4  
│ 
└── 📁 my_photos/                   # 实验三拍摄的用于标定相机的模块  
```

## 如何使用源代码
1. 克隆或下载本仓库到本地。
2. 确保你已经安装了Python和OpenCV库。
3. 按照下文指引运行相应的Python脚本，查看图像或视频处理效果。

### 实验一
本程序对颜色进行分割，通过滑条实时观测 hsv 变化对二值化图像变化的影响，可以确定所需颜色的 hsv 取值范围。
记录取值范围并键入 q 退出，在源代码中将取值修改为记录值，再运行程序，即可得到分割后的图像。

### 实验二
运行程序即可得到处理结果
#### 选做题
使用视频testVideo，检测视频中地面上的黄色虚线。
先运行 task2-extra-test.py 确定所需颜色的 hsv 范围，具体方法与实验一相同。
将上述运行结果写入 task2-extra.py ，再运行，即可看到处理后的视频。

### 实验三
准备一个标定版，运行 task3-calibration.py 拍摄约20张照片，尽量使标定板占据图片大部分。
拍摄的图片会被存在文件夹 my_photos 中，覆盖文件夹中原有的图片。
然后用matlab对进行标定，得到相机内参，并写入 task3.py 中的 cameraMatrix 和 distCoeffs。
按照你所要解算的物体的实际大小更改 objectPoints 。
再运行task3，即可调用电脑摄像头，实时解算物体位姿



