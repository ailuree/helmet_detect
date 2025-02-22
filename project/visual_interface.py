import os
import time
import sys
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal, QUrl, pyqtSlot, QTimer, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, 
    QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap
import torch
from UI.main_window import Ui_MainWindow
from detect_visual import YOLOPredict
from utils.datasets import img_formats
import numpy as np
import cv2

CODE_VER = "V2.0"
PREDICT_SHOW_TAB_INDEX = 0
REAL_TIME_PREDICT_TAB_INDEX = 1

class PredictDataHandlerThread(QThread):
    """
    打印信息的线程
    """
    predict_message_trigger = pyqtSignal(str)

    def __init__(self, predict_model):
        super(PredictDataHandlerThread, self).__init__()
        self.running = False
        self.predict_model = predict_model

    def __del__(self):
        self.running = False

    def run(self):
        self.running = True
        over_time = 0
        while self.running:
            if self.predict_model.predict_info != "":
                self.predict_message_trigger.emit(self.predict_model.predict_info)
                self.predict_model.predict_info = ""
                over_time = 0
            time.sleep(0.01)
            over_time += 1

            if over_time > 100000:
                self.running = False

class PredictHandlerThread(QThread):
    """
    进行模型推理的线程
    """
    update_ui_signal = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, input_player, output_player, out_file_path, weight_path,
                 predict_info_plain_text_edit, predict_progress_bar, fps_label,
                 button_dict, input_tab, output_tab, input_image_label, output_image_label,
                 real_time_show_predict_flag):
        super(PredictHandlerThread, self).__init__()
        self.running = False

        '''加载模型'''
        self.predict_model = YOLOPredict(weight_path, out_file_path)
        self.output_predict_file = ""
        self.parameter_source = ''
        self.out_file_path = out_file_path

        # 传入的QT插件
        self.input_player = input_player
        self.output_player = output_player
        self.predict_info_plainTextEdit = predict_info_plain_text_edit
        self.predict_progressBar = predict_progress_bar
        self.fps_label = fps_label
        self.button_dict = button_dict
        self.input_tab = input_tab
        self.output_tab = output_tab
        self.input_image_label = input_image_label
        self.output_image_label = output_image_label

        # 是否实时显示推理图片
        self.real_time_show_predict_flag = real_time_show_predict_flag

        # 创建显示进程
        self.predict_data_handler_thread = PredictDataHandlerThread(self.predict_model)
        self.predict_data_handler_thread.predict_message_trigger.connect(self.add_messages)

        # 保存主应用程序实例的引用
        self.app = QApplication.instance()

        # 连接信号到槽函数
        self.update_ui_signal.connect(self.update_ui)

    def __del__(self):
        self.running = False

    @pyqtSlot(np.ndarray, np.ndarray)
    def update_ui(self, input_image, output_image):
        """更新UI的槽函数"""
        try:
            if self.input_image_label and self.output_image_label:
                # 确保在主线程中更新UI
                if QThread.currentThread() != QApplication.instance().thread():
                    # 如果不在主线程，使用信号槽机制
                    self.update_ui_signal.emit(input_image, output_image)
                    return
                    
                # 显示图像
                YOLOPredict.show_real_time_image(self.input_image_label, input_image)
                YOLOPredict.show_real_time_image(self.output_image_label, output_image)
                
                # 处理事件，保持UI响应
                QApplication.processEvents()
                
        except Exception as e:
            print(f"Error updating UI: {str(e)}")

    def run(self):
        try:
            self.predict_data_handler_thread.start()
            
            self.predict_progressBar.setValue(0)
            for item, button in self.button_dict.items():
                button.setEnabled(False)
                
            image_flag = os.path.splitext(self.parameter_source)[-1].lower() in img_formats
            qt_input = None
            qt_output = None

            if not image_flag and self.real_time_show_predict_flag:
                qt_input = self.input_image_label
                qt_output = self.output_image_label
                if self.app:
                    self.app.processEvents()
                self.input_tab.setCurrentIndex(REAL_TIME_PREDICT_TAB_INDEX)
                self.output_tab.setCurrentIndex(REAL_TIME_PREDICT_TAB_INDEX)
                
            with torch.no_grad():
                try:
                    # 确保输出目录存在
                    os.makedirs(self.out_file_path, exist_ok=True)
                    
                    # 如果是图片，复制到处理目录
                    if image_flag:
                        # 创建临时处理目录
                        process_dir = os.path.join(self.out_file_path, 'temp_process')
                        os.makedirs(process_dir, exist_ok=True)
                        
                        # 复制原始图片到处理目录
                        base_name = os.path.basename(self.parameter_source)
                        temp_path = os.path.join(process_dir, base_name)
                        import shutil
                        shutil.copy2(self.parameter_source, temp_path)
                        
                        # 使用临时路径进行检测
                        output_dir = self.predict_model.detect(
                            temp_path,
                            qt_input=qt_input,
                            qt_output=qt_output,
                            update_ui_signal=self.update_ui_signal
                        )
                    else:
                        output_dir = self.predict_model.detect(
                            self.parameter_source,
                            qt_input=qt_input,
                            qt_output=qt_output,
                            update_ui_signal=self.update_ui_signal
                        )
                    
                    # 对于图片，找到实际保存的检测结果文件
                    if image_flag:
                        predict_dir = os.path.join(output_dir, 'predict')
                        if not os.path.exists(predict_dir):
                            raise Exception(f"检测结果目录不存在: {predict_dir}")
                            
                        base_name = os.path.basename(self.parameter_source)
                        self.output_predict_file = os.path.join(predict_dir, base_name)
                        
                        if not os.path.exists(self.output_predict_file):
                            # 尝试在输出目录中查找结果文件
                            files = os.listdir(predict_dir)
                            if files:
                                self.output_predict_file = os.path.join(predict_dir, files[0])
                            else:
                                raise Exception("未找到检测结果文件")
                    else:
                        self.output_predict_file = output_dir
                        
                except Exception as e:
                    print(f"Detection error: {str(e)}")
                    self.predict_info_plainTextEdit.appendPlainText(f"检测错误: {str(e)}")
                    return
                    
            if self.output_predict_file and os.path.exists(self.output_predict_file):
                if image_flag:
                    # 处理图片
                    try:
                        # 读取原始图片和检测结果图片
                        input_image = cv2.imread(str(self.parameter_source))
                        output_image = cv2.imread(str(self.output_predict_file))
                        
                        if input_image is None or output_image is None:
                            raise Exception("无法读取图片文件")
                        
                        # 显示图片
                        self.input_tab.setCurrentIndex(REAL_TIME_PREDICT_TAB_INDEX)
                        self.output_tab.setCurrentIndex(REAL_TIME_PREDICT_TAB_INDEX)
                        YOLOPredict.show_real_time_image(self.input_image_label, input_image)
                        YOLOPredict.show_real_time_image(self.output_image_label, output_image)
                        
                        # 保存检测结果到单独的文件夹
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        save_dir = os.path.join(self.out_file_path, 'image_results')
                        os.makedirs(save_dir, exist_ok=True)
                        
                        # 生成保存文件名
                        base_name = os.path.basename(self.parameter_source)
                        name, ext = os.path.splitext(base_name)
                        save_path = os.path.join(save_dir, f"{name}_detected_{timestamp}{ext}")
                        
                        # 保存检测结果图片
                        if not cv2.imwrite(save_path, output_image):
                            raise Exception(f"无法保存图片到: {save_path}")
                        
                        print(f"检测结果已保存至: {save_path}")
                        self.predict_info_plainTextEdit.appendPlainText(f"检测结果已保存至: {save_path}")
                        
                        # 更新进度条
                        self.predict_progressBar.setValue(100)
                        
                        # 清理临时文件
                        try:
                            temp_dir = os.path.join(self.out_file_path, 'temp_process')
                            if os.path.exists(temp_dir):
                                shutil.rmtree(temp_dir)
                        except Exception as e:
                            print(f"清理临时文件失败: {str(e)}")
                        
                    except Exception as e:
                        print(f"Error processing image: {str(e)}")
                        self.predict_info_plainTextEdit.appendPlainText(f"图片处理错误: {str(e)}")
                else:
                    # 处理视频
                    self.input_player.setMedia(QMediaContent(QUrl.fromLocalFile(str(self.parameter_source))))
                    self.input_player.pause()

                    self.output_player.setMedia(QMediaContent(QUrl.fromLocalFile(str(self.output_predict_file))))
                    self.output_player.pause()

                    # tab 设置显示第一栏
                    self.input_tab.setCurrentIndex(PREDICT_SHOW_TAB_INDEX)
                    self.output_tab.setCurrentIndex(PREDICT_SHOW_TAB_INDEX)

                # 启用按钮
                for item, button in self.button_dict.items():
                    if image_flag and item in ['play_pushButton', 'pause_pushButton']:
                        continue
                    button.setEnabled(True)
            else:
                error_msg = f"检测结果文件不存在: {self.output_predict_file}"
                print(error_msg)
                self.predict_info_plainTextEdit.appendPlainText(error_msg)
                
                # 检查目录结构
                if image_flag:
                    predict_dir = os.path.join(output_dir, 'predict')
                    if os.path.exists(predict_dir):
                        files = os.listdir(predict_dir)
                        debug_msg = f"predict目录中的文件: {files}"
                        print(debug_msg)
                        self.predict_info_plainTextEdit.appendPlainText(debug_msg)

        except Exception as e:
            error_msg = f"严重错误: {str(e)}"
            print(error_msg)
            self.predict_info_plainTextEdit.appendPlainText(error_msg)
            import traceback
            traceback.print_exc()

    @pyqtSlot(str)
    def add_messages(self, message):
        if message != "":
            self.predict_info_plainTextEdit.appendPlainText(message)

            if ":" not in message:
                # 跳过无用字符
                return

            split_message = message.split(" ")

            # 设置进度条
            if "video" in message:
                percent = split_message[2][1:-1].split("/")  # 提取图片的序号
                value = int((int(percent[0]) / int(percent[1])) * 100)
                value = value if (int(percent[1]) - int(percent[0])) > 2 else 100
                self.predict_progressBar.setValue(value)
            else:
                self.predict_progressBar.setValue(100)

            # 设置 FPS
            second_count = 1 / float(split_message[-1][1:-2])
            self.fps_label.setText(f"--> {second_count:.1f} FPS")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, weight_path, out_file_path, real_time_show_predict_flag: bool, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("建筑工地安全帽检测系统 " + CODE_VER)
        self.showMaximized()

        '''按键绑定'''
        # 输入媒体
        self.import_media_pushButton.clicked.connect(self.import_media)  # 导入
        self.start_predict_pushButton.clicked.connect(self.predict_button_click)  # 开始推理
        # 输出媒体
        self.open_predict_file_pushButton.clicked.connect(self.open_file_in_browser)  # 文件中显示推理视频
        # 下方
        self.play_pushButton.clicked.connect(self.play_pause_button_click)  # 播放
        self.pause_pushButton.clicked.connect(self.play_pause_button_click)  # 暂停
        self.button_dict = dict()
        self.button_dict.update({
            "import_media_pushButton": self.import_media_pushButton,
            "start_predict_pushButton": self.start_predict_pushButton,
            "open_predict_file_pushButton": self.open_predict_file_pushButton,
            "play_pushButton": self.play_pushButton,
            "pause_pushButton": self.pause_pushButton,
            "real_time_checkBox": self.real_time_checkBox
        })

        '''媒体流绑定输出'''
        self.input_player = QMediaPlayer()  # 媒体输入的widget
        self.input_player.setVideoOutput(self.input_video_widget)
        self.input_player.positionChanged.connect(self.change_slide_bar)  # 播放进度条

        self.output_player = QMediaPlayer()  # 媒体输出的widget
        self.output_player.setVideoOutput(self.output_video_widget)

        # 播放时长, 以 input 的时长为准
        self.video_length = 0
        self.out_file_path = out_file_path
        
        # 推理使用另外一线程
        self.predict_handler_thread = PredictHandlerThread(
            self.input_player,
            self.output_player,
            self.out_file_path,
            weight_path,
            self.predict_info_plainTextEdit,
            self.predict_progressBar,
            self.fps_label,
            self.button_dict,
            self.input_media_tabWidget,
            self.output_media_tabWidget,
            self.input_real_time_label,
            self.output_real_time_label,
            real_time_show_predict_flag
        )
        self.weight_label.setText(f" 使用模型: {Path(weight_path[0]).name}")
        
        # 界面美化
        self.gen_better_gui()

        self.media_source = ""  # 推理媒体的路径
        self.predict_progressBar.setValue(0)  # 进度条归零

        '''check box 绑定'''
        self.real_time_checkBox.stateChanged.connect(self.real_time_checkbox_state_changed)
        self.real_time_checkBox.setChecked(real_time_show_predict_flag)
        self.real_time_check_state = self.real_time_checkBox.isChecked()

        # 设置标签的大小策略
        self.input_real_time_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.output_real_time_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        
        # 设置标签的最小大小
        self.input_real_time_label.setMinimumSize(320, 240)
        self.output_real_time_label.setMinimumSize(320, 240)
        
        # 设置对齐方式
        self.input_real_time_label.setAlignment(Qt.AlignCenter)
        self.output_real_time_label.setAlignment(Qt.AlignCenter)

        # 忽略QTextBlock和QTextCursor警告
        try:
            from PyQt5.QtCore import QMetaType
            QMetaType.type("QTextBlock")
            QMetaType.type("QTextCursor")
        except:
            pass  # 如果注册失败，忽略警告

    def gen_better_gui(self):
        """
        美化界面
        """
        # Play 按钮
        play_icon = QIcon()
        play_icon.addPixmap(QPixmap("./UI/icon/play.png"), QIcon.Normal, QIcon.Off)
        self.play_pushButton.setIcon(play_icon)

        # Pause 按钮
        pause_icon = QIcon()
        pause_icon.addPixmap(QPixmap("./UI/icon/pause.png"), QIcon.Normal, QIcon.Off)
        self.pause_pushButton.setIcon(pause_icon)

        # 隐藏 tab 标题栏
        self.input_media_tabWidget.tabBar().hide()
        self.output_media_tabWidget.tabBar().hide()
        # tab 设置显示第一栏
        self.input_media_tabWidget.setCurrentIndex(PREDICT_SHOW_TAB_INDEX)
        self.output_media_tabWidget.setCurrentIndex(PREDICT_SHOW_TAB_INDEX)

        # 设置显示图片的 label 为黑色背景
        self.input_real_time_label.setStyleSheet("QLabel{background:black}")
        self.output_real_time_label.setStyleSheet("QLabel{background:black}")

    def real_time_checkbox_state_changed(self):
        """
        切换是否实时显示推理图片
        :return:
        """
        self.real_time_check_state = self.real_time_checkBox.isChecked()
        self.predict_handler_thread.real_time_show_predict_flag = self.real_time_check_state

    def import_media(self):
        """
        导入媒体文件
        """
        try:
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("Media files (*.mp4 *.avi *.jpg *.jpeg *.png *.bmp);;All files (*.*)")
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                if not selected_files:
                    return
                    
                self.media_source = selected_files[0]
                if not os.path.exists(self.media_source):
                    print(f"文件不存在: {self.media_source}")
                    return

                # 检查是否是图片
                is_image = os.path.splitext(self.media_source)[1].lower() in img_formats
                if is_image:
                    try:
                        # 读取并显示原始图片
                        input_image = cv2.imread(self.media_source)
                        if input_image is None:
                            raise Exception(f"无法读取图片: {self.media_source}")
                        
                        # 显示原始图片
                        self.input_media_tabWidget.setCurrentIndex(REAL_TIME_PREDICT_TAB_INDEX)
                        YOLOPredict.show_real_time_image(self.input_real_time_label, input_image)
                    except Exception as e:
                        print(f"Error loading image: {str(e)}")
                        return
                else:
                    # 处理视频
                    self.input_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.media_source)))
                    self.input_player.pause()
                    self.input_media_tabWidget.setCurrentIndex(PREDICT_SHOW_TAB_INDEX)

                # 将路径传递给检测线程
                self.predict_handler_thread.parameter_source = self.media_source

                # 设置按钮状态
                for item, button in self.button_dict.items():
                    if is_image and item in ['play_pushButton', 'pause_pushButton']:
                        button.setEnabled(False)
                    else:
                        button.setEnabled(True)
                
        except Exception as e:
            print(f"Error importing media: {str(e)}")

    def predict_button_click(self):
        """
        推理按钮
        :return:
        """
        # 启动线程去调用
        self.predict_handler_thread.start()

    def change_slide_bar(self, position):
        """
        进度条移动
        :param position:
        :return:
        """
        self.video_length = self.input_player.duration() + 0.1
        self.video_horizontalSlider.setValue(round((position / self.video_length) * 100))
        self.video_percent_label.setText(str(round((position / self.video_length) * 100, 2)) + '%')

    @pyqtSlot()
    def play_pause_button_click(self):
        """
        播放、暂停按钮回调事件
        :return:
        """
        name = self.sender().objectName()

        if self.media_source == "":
            return

        if name == "play_pushButton":
            print("play")
            self.input_player.play()
            self.output_player.play()

        elif name == "pause_pushButton":
            self.input_player.pause()
            self.output_player.pause()

    @pyqtSlot()
    def open_file_in_browser(self):
        os.system(f"start explorer {self.out_file_path}")

    @pyqtSlot()
    def closeEvent(self, *args, **kwargs):
        print("Close")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    weight_root = Path.cwd().joinpath("weights")
    if not weight_root.exists():
        raise FileNotFoundError("weights not found !!!")

    weight_file = [item for item in weight_root.iterdir() if item.suffix == ".pt"]
    weight_root = [str(weight_file[0])]  # 权重文件位置
    out_file_root = Path.cwd().joinpath(r'inference/output')
    out_file_root.parent.mkdir(exist_ok=True)
    out_file_root.mkdir(exist_ok=True)

    real_time_show_predict = True  # 是否实时显示推理图片，有可能导致卡顿，软件卡死

    main_window = MainWindow(weight_root, out_file_root, real_time_show_predict)

    # 设置窗口图标
    icon = QIcon()
    icon.addPixmap(QPixmap("./UI/icon/icon.ico"), QIcon.Normal, QIcon.Off)
    main_window.setWindowIcon(icon)

    main_window.show()
    sys.exit(app.exec_())
