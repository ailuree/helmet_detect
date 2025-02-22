# 安全帽佩戴检测系统

本项目是一个基于深度学习的安全帽佩戴检测系统，可以实时检测人员是否正确佩戴安全帽，并对违规情况进行警告和记录。

## 主要功能

- **UI界面**：
  - 基于PyQt5开发，用QSS进行界面美化
  - 采用QtDesigner进行界面设计
  - 实时显示检测结果和警告信息

- **检测功能**：
  - 支持实时视频检测
  - 支持图片检测
  - 自动识别三类目标：人员(person)、头部(head)、安全帽(helmet)
  - 违规检测逻辑：检测到头部(head)即判定为未正确佩戴安全帽
  - 违规警告：使用红色边框突出显示违规情况
  - 自动抓取和保存违规关键帧
  - 支持检测结果的图片和视频保存

## 模型说明

- **训练数据集**：
  - 使用 [Safety-Helmet-Wearing-Dataset](https://github.com/njvisionpower/Safety-Helmet-Wearing-Dataset) 开源数据集
  - 数据集包含安全帽佩戴场景的标注数据
  - 训练轮次(epoch)：150

- **模型详情**：
  - 预训练模型：yolov5l.*pt*
  - 训练后模型：helmet_head_person_l.pt
  - 检测类别：helmet（安全帽）、head（头部）、person（人员）

## 项目结构

```
project/
├── visual_interface.py    # 主程序界面文件
├── detect_visual.py       # 检测可视化核心功能实现
├── detect.py              # 单张图片检测脚本
├── train.py               # 模型训练脚本
├── test.py                # 测试脚本
├── requirements.txt       # 项目依赖文件
│
├── UI/                    # UI相关文件目录
│   ├── main_window.py          # UI设计文件
│   └── icon/              # UI资源文件
│
├── models/                # 模型文件目录
│   └── yolo.py             # yolo模型文件
│
├── weights/          # 权重文件目录
│   └── helmet_head_person_l.pt   # 安全帽检测模型
│
├── utils/           # 工具函数目录
│   ├── datasets.py  # 数据集处理
│   └── custom_utils.py  # 自定义工具函数
│
├── data/            # 数据目录
│   ├── gen_data/   # 生成数据集
│   └── custom_data.yaml  # 自定义数据集
│
├── test-source/     # 测试资源目录
│
├── inference/       # 推理结果目录
│   └── output/      # 输出结果
│
└── dist/            # 打包发布目录
```