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
├── 📄 ubuntu-opencv.png           # 虚拟机运行opencv界面截图
| 
├── 📁 resources/                  # 实验中用到的（处理的）图片及视频  
│    ├── bed_pic.png
│    ├── initial_image.png
│    ├── test.png
│    └── testVideo.mp4  
│ 
└── 📁 my_photos/                   # 实验三拍摄的用于标定相机的模块  
```

process/ 中为程序运行结果和部分ai对话记录

报名表也在这里面

attempts-for-tast3/ 中为 tag 识别实验的探索过程中的部分代码，这些代码没有实现目标，但是能部分反应我的思考过程。
由于文件大小受限，这里没有将这部分的录频放进来

Self_learning/ 是之前自己跟着网上的教程写的一些代码，比较基础

## 如何使用源代码
1. 克隆或下载本仓库到本地。
2. 确保你已经安装了Python和OpenCV库。
3. 按照下文指引运行相应的Python脚本，查看图像或视频处理效果。

### 实验一
本程序对颜色进行分割，通过滑条实时观测 hsv 变化对二值化图像变化的影响，可以确定所需颜色的 hsv 取值范围。
记录取值范围并键入 q 退出，在源代码中将取值修改为记录值，再运行程序，即可得到分割后的图像。
<img width="641" height="466" alt="img_out" src="https://github.com/user-attachments/assets/d7e0ee4d-156b-4ae3-9196-98c4ae3f0ba3" />


### 实验二
运行程序即可得到处理结果
<img width="1914" height="1145" alt="task2" src="https://github.com/user-attachments/assets/ff05e08a-f02a-43d6-9a4a-37781b869d93" />

#### 选做题
使用视频testVideo，检测视频中地面上的黄色虚线。
先运行 task2-extra-test.py 确定所需颜色的 hsv 范围，具体方法与实验一相同。
将上述运行结果写入 task2-extra.py ，再运行，即可看到处理后的视频。

https://github.com/user-attachments/assets/9e0a32ff-1d88-49af-87f0-3130d2b30326


### 实验三
准备一个标定版，运行 task3-calibration.py 拍摄约20张照片，尽量使标定板占据图片大部分。
拍摄的图片会被存在文件夹 my_photos 中，覆盖文件夹中原有的图片。
然后用matlab对进行标定，得到相机内参，并写入 task3.py 中的 cameraMatrix 和 distCoeffs。
按照你所要解算的物体的实际大小更改 objectPoints 。
再运行task3，即可调用电脑摄像头，实时解算物体位姿

由于视频太大，没法直接放到 readme 里，运行视频请看 process/task3.mp4


