from copy import deepcopy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication

import torch.backends.cudnn as cudnn

from models.experimental import *
from utils.datasets import *
from utils.utils import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import time
from datetime import datetime
import cv2
from skimage.metrics import structural_similarity as ssim
from threading import Thread
from queue import Queue

class YOLOPredict(object):
    def __init__(self, weights, out_file_path):
        """
        YOLO 模型初始化
        :param weights: 权重路径
        :param out_file_path: 推理结果存放路径
        """

        '''模型参数'''
        self.agnostic_nms = False
        self.augment = False
        self.classes = None
        self.conf_thres = 0.4
        self.device = ''
        self.img_size = 640
        self.iou_thres = 0.5
        self.output = out_file_path
        self.save_txt = False
        self.update = False
        self.view_img = False
        self.weights = weights  # 权重文件路径，修改这里

        # 加载模型
        self.model, self.half, self.names, self.colors, self.device = self.load_model()
        self.predict_info = ""
        
        # 安全帽检测相关变量
        self.no_helmet_count = 0  # 当前帧未戴安全帽的人数
        self.warning_active = False
        self.warning_counter = 0
        self.last_warning_time = 0
        self.warning_cooldown = 0.5
        self.warning_frames = 0
        self.warning_duration = 50

        self.violation_save_dir = os.path.join(out_file_path, 'violations')
        os.makedirs(self.violation_save_dir, exist_ok=True)
        self.last_save_time = 0
        self.min_save_interval = 1.5  # 降低保存间隔到1.5秒
        self.last_saved_frame = None
        self.min_no_helmet_count = 1  # 最小未戴安全帽人数阈值
        
        # 添加连续违规检测相关参数
        self.violation_duration = 0  # 连续违规帧计数
        self.min_violation_duration = 10  # 最小连续违规帧数
        self.last_violation_time = 0  # 上次违规时间
        self.violation_cooldown = 5.0  # 违规场景冷却时间（秒）
        
        # 性能优化
        self.save_queue = Queue(maxsize=20)  # 增加队列大小
        self.save_thread = Thread(target=self._save_worker, daemon=True)
        self.save_thread.start()
        
        self.compare_size = (160, 120)          # 降采样参数 用于相似度比较的降采样尺寸

        self.save_video = True  # 是否保存视频
        self.video_save_dir = os.path.join(out_file_path, 'videos')
        os.makedirs(self.video_save_dir, exist_ok=True)
        self.vid_writer = None

    def load_model(self):

        imgsz = self.img_size
        weights = self.weights
        device = self.device
        # Initialize
        device = torch_utils.select_device(device)
        half = device.type != 'cpu'  # half precision only supported on CUDA
        # Load model
        model = attempt_load(weights, map_location=device)  # load FP32 model
        imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
        if half:
            model.half()  # to FP16
        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
        # Run inference
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
        return model, half, names, colors, device

    @staticmethod
    def show_real_time_image(image_label, img):
        """
        image_label 显示实时推理图片
        """
        try:
            if image_label is None or not isinstance(img, np.ndarray):
                return
            image_label_width = image_label.width()
            if image_label_width <= 0:
                return
            
            height = int(image_label.height())            # 计算调整后的高度，保持宽高比
            width = int(image_label_width)
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)            # 调整图像大小以适应标签
            
            if len(img.shape) == 3:               # 转换颜色空间
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            
            h, w, ch = img_rgb.shape               # 创建QImage
            bytes_per_line = ch * w
            image = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            pixmap = QPixmap.fromImage(image)        # 创建并设置QPixmap
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)     # 让图片填充整个label
            
        except Exception as e:
            print(f"Error in show_real_time_image: {str(e)}")

    def _save_worker(self):
        """
        后台保存线程
        """
        while True:
            try:
                save_data = self.save_queue.get()
                if save_data is None:
                    break
                    
                frame, filename = save_data
                cv2.imwrite(filename, frame)
            except Exception as e:
                print(f"Error in save worker: {str(e)}")
                continue

    def check_frame_similarity(self, current_frame):
        """
        快速检查帧相似度，放宽相似度判断标准
        """
        if self.last_saved_frame is None:
            return False
            
        current_small = cv2.resize(current_frame, self.compare_size)        # 降采样以加快比较速度
        last_small = cv2.resize(self.last_saved_frame, self.compare_size)
        
        current_gray = cv2.cvtColor(current_small, cv2.COLOR_BGR2GRAY)        # 转换为灰度图
        last_gray = cv2.cvtColor(last_small, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.absdiff(current_gray, last_gray)        # 使用MSE（均方误差）
        mse = np.mean(diff ** 2)
        
        return mse < 200  # 放宽MSE阈值

    def save_violation_frame(self, frame, no_helmet_count):
        """
        优化的违规关键帧保存逻辑
        """
        current_time = time.time()
        
        if no_helmet_count > 0:
            if current_time - self.last_violation_time < 1.0:  # 1秒内的连续违规
                self.violation_duration += 1
            else:
                self.violation_duration = 1
            self.last_violation_time = current_time
        else:
            self.violation_duration = 0
        
        if self.save_queue.full():
            return False
            
        # 关键帧保存策略：
        # 1. 刚开始违规时保存
        # 2. 违规持续一段时间后保存
        # 3. 违规人数发生变化时保存
        should_save = False
        
        # 情况1：新的违规场景
        if (current_time - self.last_save_time >= self.violation_cooldown and 
            no_helmet_count > 0):
            should_save = True
        
        # 情况2：持续违规到达阈值
        elif (self.violation_duration >= self.min_violation_duration and 
              current_time - self.last_save_time >= self.min_save_interval):
            should_save = True
        
        # 情况3：场景发生明显变化
        elif (current_time - self.last_save_time >= self.min_save_interval and 
              not self.check_frame_similarity(frame)):
            should_save = True
        
        if not should_save:
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 生成文件名
        duration_info = f"_duration_{self.violation_duration}" if self.violation_duration > 1 else ""
        filename = f"violation_{timestamp}_persons_{no_helmet_count}{duration_info}.jpg"
        save_path = os.path.join(self.violation_save_dir, filename)
        
        try:
            self.save_queue.put_nowait((frame.copy(), save_path))
            self.last_save_time = current_time
            self.last_saved_frame = frame.copy()
            return True
        except:
            return False

    def detect(self, source, save_img=False, qt_input=None, qt_output=None, update_ui_signal=None):
        """
        进行推理操作
        :param source: 推理素材
        :param save_img: 保存图片 flag
        :param qt_input: QT 输入窗口
        :param qt_output: QT 输出窗口
        :param update_ui_signal: 用于更新UI的信号
        :return:
        """
        try:
            out = self.output
            view_img = self.view_img
            save_txt = self.save_txt
            imgsz = self.img_size
            augment = self.augment
            conf_thres = self.conf_thres
            iou_thres = self.iou_thres
            cclasses = self.classes
            agnostic_nms = self.agnostic_nms

            os.makedirs(out, exist_ok=True)  # make new output folder
            show_count = 0
            t0 = time.time()
            vid_path, vid_writer = None, None

            # 设置数据加载器
            try:
                webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')
                if webcam:
                    view_img = True
                    cudnn.benchmark = True  # set True to speed up constant image size inference
                    dataset = LoadStreams(source, img_size=imgsz)
                else:
                    save_img = True
                    dataset = LoadImages(source, img_size=imgsz, visualize_flag=True)
            except Exception as e:
                print(f"Error loading dataset: {str(e)}")
                return

            # 处理每一帧
            for path, img, im0s, vid_cap, info_str in dataset:
                try:
                    # 保存原始图像
                    origin_image = deepcopy(im0s)

                    # 图像预处理
                    img = torch.from_numpy(img).to(self.device)
                    img = img.half() if self.half else img.float()
                    img /= 255.0
                    if img.ndimension() == 3:
                        img = img.unsqueeze(0)

                    # 推理
                    t1 = torch_utils.time_synchronized()
                    pred = self.model(img, augment)[0]
                    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=cclasses, agnostic=agnostic_nms)
                    t2 = torch_utils.time_synchronized()

                    # 处理检测结果
                    for i, det in enumerate(pred):
                        if webcam:
                            p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                        else:
                            p, s, im0 = path, '', im0s

                        save_path = str(Path(out) / Path(p).name)
                        txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
                        s += '%gx%g ' % img.shape[2:]
                        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]

                        if det is not None and len(det):
                            # 重新缩放边界框
                            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                            # 统计检测结果
                            person_count = head_count = helmet_count = 0
                            no_helmet_heads = []
                            try:
                                if det is not None and len(det):
                                    for c in det[:, -1].unique():
                                        try:
                                            n = (det[:, -1] == c).sum()
                                            class_idx = int(c)
                                            if class_idx >= len(self.names):
                                                continue
                                            
                                            s += '%g %ss, ' % (n, self.names[class_idx])
                                            if self.names[class_idx] == 'person':
                                                person_count = int(n)
                                            elif self.names[class_idx] == 'head':
                                                head_count = int(n)
                                                head_indices = (det[:, -1] == c).nonzero(as_tuple=False).squeeze(1)
                                                if len(head_indices.shape) == 0:
                                                    head_indices = head_indices.unsqueeze(0)
                                                for head_index in head_indices:
                                                    if head_index >= det.shape[0]:
                                                        continue
                                                    head_xyxy = det[head_index, :4]
                                                    has_helmet = False
                                                    for j in range(det.shape[0]):
                                                        if j < det.shape[0] and self.names[int(det[j, -1])] == 'helmet':
                                                            helmet_xyxy = det[j, :4]
                                                            if bbox_iou(head_xyxy, helmet_xyxy) > 0.5:
                                                                has_helmet = True
                                                                break
                                                    if not has_helmet:
                                                        no_helmet_heads.append(head_xyxy)
                                            elif self.names[class_idx] == 'helmet':
                                                helmet_count = int(n)
                                        except Exception as e:
                                            print(f"Error processing detection class {c}: {str(e)}")
                                            continue
                            except Exception as e:
                                print(f"Error processing detections: {str(e)}")

                            self.no_helmet_count = len(no_helmet_heads)
                            
                            current_time = time.time()
                            
                            # 警告逻辑
                            if self.no_helmet_count > 0:
                                if not self.warning_active and current_time - self.last_warning_time >= self.warning_cooldown:
                                    self.warning_active = True
                                    self.warning_frames = 0
                                    self.last_warning_time = current_time
                            else:
                                self.warning_active = False
                                self.warning_frames = 0
                            
                            # 处理警告显示
                            if self.warning_active and self.no_helmet_count > 0:
                                self.warning_frames += 1
                                if self.warning_frames >= self.warning_duration:
                                    self.warning_active = False
                                    self.warning_frames = 0
                                
                                warning_text = f"{self.no_helmet_count}人没有戴安全帽"
                                warning_text_en = f"{self.no_helmet_count} people not wearing helmets"
                                detail_text = f"检测到: {person_count}人 {head_count}头 {helmet_count}顶安全帽"
                                detail_text_en = f"Detected: {person_count} people {head_count} heads {helmet_count} helmets"

                                try:
                                    font_paths = [
                                        os.path.join(os.path.dirname(os.path.abspath(__file__)), "simhei.ttf"),
                                        "C:/Windows/Fonts/simhei.ttf",  # Windows
                                    ]
                                    
                                    font_path = None
                                    for path in font_paths:
                                        if os.path.exists(path):
                                            font_path = path
                                            break
                                            
                                    if font_path:
                                        img_pil = Image.fromarray(cv2.cvtColor(im0, cv2.COLOR_BGR2RGB))
                                        draw = ImageDraw.Draw(img_pil)
                                        
                                        main_font_size = 60  # 主要警告文字
                                        detail_font_size = 32  # 详细信息文字
                                        
                                        main_font = ImageFont.truetype(font_path, main_font_size)
                                        detail_font = ImageFont.truetype(font_path, detail_font_size)
                                        
                                        main_bbox = draw.textbbox((0, 0), warning_text, font=main_font)
                                        detail_bbox = draw.textbbox((0, 0), detail_text, font=detail_font)
                                        
                                        padding = 20  # 计算主警告背景
                                        main_bg_width = main_bbox[2] + padding * 2
                                        main_bg_height = main_font_size + padding * 2
                                        main_bg_x = (im0.shape[1] - main_bg_width) // 2
                                        main_bg_y = 20
                                        
                                        draw.rectangle([(main_bg_x, main_bg_y),           # 绘制主警告背景
                                                      (main_bg_x + main_bg_width, main_bg_y + main_bg_height)],
                                                     fill=(255, 0, 0))
                                        
                                        x_position = (im0.shape[1] - main_bbox[2]) // 2   # 绘制主警告文字
                                        draw.text((x_position, main_bg_y + padding), warning_text, 
                                                font=main_font, fill=(255, 255, 255))
                                        
                                        padding = 10     # 计算详细信息背景
                                        detail_bg_width = detail_bbox[2] + padding * 2
                                        detail_bg_height = detail_font_size + padding * 2
                                        detail_bg_x = 20  # 左上角x坐标
                                        detail_bg_y = 20  # 左上角y坐标

                                        draw.rectangle([(detail_bg_x, detail_bg_y),   
                                                      (detail_bg_x + detail_bg_width, detail_bg_y + detail_bg_height)], 
                                                     fill=(255, 255, 255)) # 绘制详细信息
                                        draw.text((detail_bg_x + padding, detail_bg_y + padding), detail_text, 
                                                font=detail_font, fill=(255, 0, 0))
                                        
                                        im0 = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)  # 转换回OpenCV格式
                                    else:
                                        # 如果找不到字体文件，直接按照错误处理
                                        print("Warning: Font file not found. Please install the font or check the path.")        
                                    cv2.rectangle(im0, (0, 0), (im0.shape[1], im0.shape[0]), (0, 0, 255), 5)  # 绘制警告大边框
                                except Exception as e:
                                    print(f"Error drawing warning: {str(e)}")

                            # 绘制检测框
                            for *xyxy, conf, cls in det:
                                if save_txt:
                                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                                    with open(txt_path + '.txt', 'a') as f:
                                        f.write(('%g ' * 5 + '\n') % (cls, *xywh))

                                if save_img or view_img:
                                    label = '%s %.2f' % (self.names[int(cls)], conf)
                                    plot_one_box(xyxy, im0, label=label, color=self.colors[int(cls)], line_thickness=3)

                        print('%sDone. (%.3fs)' % (s, t2 - t1))
                        self.predict_info = info_str + '%sDone. (%.3fs)' % (s, t2 - t1)

                        # 显示结果
                        if qt_input is not None and qt_output is not None and dataset.mode == 'video':
                            try:
                                video_count, vid_total = info_str.split(" ")[2][1:-1].split("/")
                                current_frame = int(video_count)
                                
                                fps = 1.0 / (t2 - t1)                                # 自适应帧率控制
                                target_fps = 30  # 降低目标帧率以减少负载
                                
                                if fps > target_fps:
                                    skip_frames = max(1, int(fps / target_fps))
                                    show_frame = (current_frame % skip_frames == 0)
                                else:
                                    show_frame = True
                                
                                if show_frame:
                                    try:
                                        if update_ui_signal is not None:
                                            update_ui_signal.emit(origin_image.copy(), im0.copy())
                                        else:
                                            self.show_real_time_image(qt_input, origin_image)
                                            self.show_real_time_image(qt_output, im0)
                                            QApplication.processEvents()
                                            
                                    except Exception as e:
                                        print(f"Error displaying frame: {str(e)}")
                                        continue
                                    
                            except Exception as e:
                                print(f"Error processing frame display: {str(e)}")
                                continue

                        # 在处理检测结果的部分添加关键帧保存逻辑
                        if self.no_helmet_count > 0:
                            save_success = self.save_violation_frame(im0.copy(), self.no_helmet_count)
                            if save_success:
                                print(f"Queued violation frame with {self.no_helmet_count} people without helmets")

                        # 处理检测结果
                        for i, det in enumerate(pred):
                            if webcam:
                                p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                            else:
                                p, s, im0 = path, '', im0s

                            # 设置保存路径
                            if dataset.mode == 'video':  # 视频模式
                                if self.save_video:
                                    if vid_path != save_path:  # 新视频
                                        vid_path = save_path
                                        if isinstance(vid_writer, cv2.VideoWriter):
                                            vid_writer.release()  # 释放之前的writer
                                        
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                        video_name = f"detection_{timestamp}.mp4"
                                        save_path = str(Path(self.video_save_dir) / video_name)
                                        
                                        if vid_cap:  # video
                                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                        else:  # stream
                                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                                        
                                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                                    vid_writer.write(im0)  # 保存视频帧
                            
                            # 在检测和绘制完成后再保存关键帧
                            if self.no_helmet_count > 0:
                                save_success = self.save_violation_frame(im0.copy(), self.no_helmet_count)
                                if save_success:
                                    print(f"Queued violation frame with {self.no_helmet_count} people without helmets")

                except Exception as e:
                    print(f"Error processing frame: {str(e)}")
                    continue

            # 清理视频写入器
            if isinstance(vid_writer, cv2.VideoWriter):
                vid_writer.release()

            if save_txt or save_img:
                print('Results saved to %s' % str(out))

        except Exception as e:
            print(f"Critical error in detect function: {str(e)}")
            import traceback
            traceback.print_exc()

        print('Done. (%.3fs)' % (time.time() - t0))
        self.predict_info = 'Done. (%.3fs)' % (time.time() - t0)

        return out


if __name__ == '__main__':
    print("This is not for run, may be you want to run 'detect.py' or 'visual_interface.py', pls check your file name. Thx ! ")
