from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChartView
from PyQt5.QtMultimediaWidgets import QVideoWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1409, 1146)
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QLabel {
                color: #cdd6f4;
            }
            QGroupBox {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 8px;
                margin-top: 1ex;
                font-size: 14px;
                color: #cdd6f4;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #89b4fa;
            }
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
            QPushButton:pressed {
                background-color: #313244;
            }
            QTabWidget::pane {
                border: 2px solid #45475a;
                border-radius: 8px;
                background-color: #313244;
            }
            QTabBar::tab {
                background-color: #45475a;
                color: #cdd6f4;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 5px 10px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QTabBar::tab:hover:!selected {
                background-color: #585b70;
            }
            QProgressBar {
                border: 2px solid #45475a;
                border-radius: 5px;
                text-align: center;
                background-color: #313244;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 3px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #45475a;
                height: 8px;
                background: #313244;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #89b4fa;
                border: none;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #b4befe;
            }
            QPlainTextEdit {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 5px;
                padding: 5px;
                selection-background-color: #585b70;
            }
            QCheckBox {
                color: #cdd6f4;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #45475a;
            }
            QCheckBox::indicator:unchecked {
                background-color: #313244;
            }
            QCheckBox::indicator:checked {
                background-color: #89b4fa;
                image: url(check.png);
            }
        """)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.author_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.author_label_2.setMaximumSize(QtCore.QSize(16777215, 70))
        self.author_label_2.setMinimumSize(QtCore.QSize(800, 70))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.author_label_2.setFont(font)
        self.author_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.author_label_2.setObjectName("author_label_2")
        self.author_label_2.setStyleSheet("""
            QLabel {
                color: #89b4fa;
                font-size: 32px;
                font-weight: bold;
                padding: 15px 30px;
                margin: 40px;
                background-color: #313244;
                border-radius: 15px;
                border: 2px solid #45475a;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
        """)
        self.verticalLayout_3.addWidget(self.author_label_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.author_label = QtWidgets.QLabel(self.centralwidget)
        self.author_label.setMinimumSize(QtCore.QSize(200, 25))
        self.author_label.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.author_label.setFont(font)
        self.author_label.setStyleSheet("""
            QLabel {
                color: #f5c2e7;
                font-size: 14px;
                padding: 30px;
                background-color: #313244;
                border-radius: 16px;
                border: 1px solid #45475a;
            }
        """)
        self.author_label.setAlignment(QtCore.Qt.AlignCenter)
        self.author_label.setObjectName("author_label")
        self.horizontalLayout_7.addWidget(self.author_label)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setMinimumSize(QtCore.QSize(350, 600))
        self.groupBox.setMaximumSize(QtCore.QSize(1300, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.input_media_tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.input_media_tabWidget.setObjectName("input_media_tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.input_video_widget = QVideoWidget(self.tab)
        self.input_video_widget.setMinimumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.input_video_widget.setFont(font)
        self.input_video_widget.setObjectName("input_video_widget")
        self.horizontalLayout_8.addWidget(self.input_video_widget)
        self.input_media_tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.input_real_time_label = QtWidgets.QLabel(self.tab_2)
        self.input_real_time_label.setObjectName("input_real_time_label")
        self.horizontalLayout_9.addWidget(self.input_real_time_label)
        self.input_media_tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.input_media_tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("""
            QLabel {
                color: #89b4fa;
                font-weight: bold;
                padding: 5px;
                background-color: #313244;
                border-radius: 5px;
            }
        """)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.predict_progressBar = QtWidgets.QProgressBar(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.predict_progressBar.setFont(font)
        self.predict_progressBar.setStyleSheet("QProgressBar{\n"
                                               "border:2px solid grey;\n"
                                               "border-radius:5px;\n"
                                               "text-align: center;\n"
                                               "}\n"
                                               "\n"
                                               "\n"
                                               "QProgressBar::chunk {\n"
                                               "background-color:#CD96CD;\n"
                                               "width:10px;\n"
                                               "margin:0.5px;\n"
                                               "}")
        self.predict_progressBar.setMinimum(0)
        self.predict_progressBar.setProperty("value", 19)
        self.predict_progressBar.setObjectName("predict_progressBar")
        self.horizontalLayout_2.addWidget(self.predict_progressBar)
        self.fps_label = QtWidgets.QLabel(self.groupBox)
        self.fps_label.setMinimumSize(QtCore.QSize(0, 0))
        self.fps_label.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.fps_label.setFont(font)
        self.fps_label.setStyleSheet("""
            QLabel {
                color: #f9e2af;
                font-weight: bold;
            }
        """)
        self.fps_label.setObjectName("fps_label")
        self.horizontalLayout_2.addWidget(self.fps_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem1)
        self.weight_label = QtWidgets.QLabel(self.groupBox)
        self.weight_label.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(True)
        font.setWeight(75)
        self.weight_label.setFont(font)
        self.weight_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.weight_label.setStyleSheet("""
            QLabel {
                color: #f5c2e7;
                font-weight: bold;
                padding: 5px;
            }
        """)
        self.weight_label.setAlignment(QtCore.Qt.AlignCenter)
        self.weight_label.setObjectName("weight_label")
        self.horizontalLayout_13.addWidget(self.weight_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem2)
        self.real_time_checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.real_time_checkBox.setMinimumSize(QtCore.QSize(0, 25))
        self.real_time_checkBox.setMaximumSize(QtCore.QSize(130, 16777215))
        self.real_time_checkBox.setObjectName("real_time_checkBox")
        self.horizontalLayout_13.addWidget(self.real_time_checkBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.import_media_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.import_media_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.import_media_pushButton.setFont(font)
        self.import_media_pushButton.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:pressed {
                background-color: #74c7ec;
            }
        """)
        self.import_media_pushButton.setObjectName("import_media_pushButton")
        self.horizontalLayout.addWidget(self.import_media_pushButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.start_predict_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.start_predict_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.start_predict_pushButton.setFont(font)
        self.start_predict_pushButton.setStyleSheet("""
            QPushButton {
                background-color: #a6e3a1;
                color: #1e1e2e;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #94e2d5;
            }
            QPushButton:pressed {
                background-color: #89dceb;
            }
        """)
        self.start_predict_pushButton.setObjectName("start_predict_pushButton")
        self.horizontalLayout.addWidget(self.start_predict_pushButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_2.setMinimumSize(QtCore.QSize(500, 600))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.output_media_tabWidget = QtWidgets.QTabWidget(self.groupBox_2)
        self.output_media_tabWidget.setObjectName("output_media_tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.output_video_widget = QVideoWidget(self.tab_3)
        self.output_video_widget.setMinimumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.output_video_widget.setFont(font)
        self.output_video_widget.setObjectName("output_video_widget")
        self.horizontalLayout_10.addWidget(self.output_video_widget)
        self.output_media_tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.output_real_time_label = QtWidgets.QLabel(self.tab_4)
        self.output_real_time_label.setObjectName("output_real_time_label")
        self.horizontalLayout_11.addWidget(self.output_real_time_label)
        self.output_media_tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_2.addWidget(self.output_media_tabWidget)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem7)
        self.open_predict_file_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.open_predict_file_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.open_predict_file_pushButton.setFont(font)
        self.open_predict_file_pushButton.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #1e1e2e;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fab387;
            }
            QPushButton:pressed {
                background-color: #f5c2e7;
            }
        """)
        self.open_predict_file_pushButton.setObjectName("open_predict_file_pushButton")
        self.horizontalLayout_12.addWidget(self.open_predict_file_pushButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.verticalLayout_3.addWidget(self.splitter)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.video_horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.video_horizontalSlider.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.video_horizontalSlider.setFont(font)
        self.video_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.video_horizontalSlider.setObjectName("video_horizontalSlider")
        self.horizontalLayout_4.addWidget(self.video_horizontalSlider)
        self.video_percent_label = QtWidgets.QLabel(self.centralwidget)
        self.video_percent_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.video_percent_label.setFont(font)
        self.video_percent_label.setObjectName("video_percent_label")
        self.horizontalLayout_4.addWidget(self.video_percent_label)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem11 = QtWidgets.QSpacerItem(40, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem11)
        self.play_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.play_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.play_pushButton.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.play_pushButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/PeterH/.designer/backup/icon/play.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.play_pushButton.setIcon(icon)
        self.play_pushButton.setObjectName("play_pushButton")
        self.horizontalLayout_3.addWidget(self.play_pushButton)
        self.pause_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pause_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.pause_pushButton.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.pause_pushButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/PeterH/.designer/backup/icon/pause.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pause_pushButton.setIcon(icon1)
        self.pause_pushButton.setObjectName("pause_pushButton")
        self.horizontalLayout_3.addWidget(self.pause_pushButton)
        spacerItem12 = QtWidgets.QSpacerItem(40, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem12)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.predict_info_plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_3)
        self.predict_info_plainTextEdit.setMinimumSize(QtCore.QSize(0, 160))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.predict_info_plainTextEdit.setFont(font)
        self.predict_info_plainTextEdit.setStyleSheet("""
            QPlainTextEdit {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.predict_info_plainTextEdit.setObjectName("predict_info_plainTextEdit")
        self.horizontalLayout_6.addWidget(self.predict_info_plainTextEdit)
        self.horizontalLayout_5.addWidget(self.groupBox_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1409, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.input_media_tabWidget.setCurrentIndex(0)
        self.output_media_tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "安全帽检测系统"))
        self.author_label_2.setText(_translate("MainWindow", "工地安全帽检测系统"))
        self.author_label.setText(_translate("MainWindow", "Product by: Hzy"))
        self.groupBox.setTitle(_translate("MainWindow", "输入视频"))
        self.input_media_tabWidget.setTabText(self.input_media_tabWidget.indexOf(self.tab), _translate("MainWindow", "结果"))
        self.input_real_time_label.setText(_translate("MainWindow", "HinGwenWoong"))
        self.input_media_tabWidget.setTabText(self.input_media_tabWidget.indexOf(self.tab_2), _translate("MainWindow", "实时推理"))
        self.label.setText(_translate("MainWindow", "  处理进度:  "))
        self.fps_label.setText(_translate("MainWindow", "(FPS)"))
        self.weight_label.setText(_translate("MainWindow", "模型路径:"))
        self.real_time_checkBox.setText(_translate("MainWindow", "实时检测"))
        self.import_media_pushButton.setStatusTip(_translate("MainWindow", "导入视频进行检测"))
        self.import_media_pushButton.setText(_translate("MainWindow", "导入"))
        self.start_predict_pushButton.setStatusTip(_translate("MainWindow", "开始检测视频"))
        self.start_predict_pushButton.setText(_translate("MainWindow", "检测"))
        self.groupBox_2.setTitle(_translate("MainWindow", "检测结果"))
        self.output_media_tabWidget.setTabText(self.output_media_tabWidget.indexOf(self.tab_3), _translate("MainWindow", "结果"))
        self.output_real_time_label.setText(_translate("MainWindow", "HinGwenWoong"))
        self.output_media_tabWidget.setTabText(self.output_media_tabWidget.indexOf(self.tab_4), _translate("MainWindow", "实时推理"))
        self.open_predict_file_pushButton.setText(_translate("MainWindow", "打开文件夹"))
        self.video_percent_label.setText(_translate("MainWindow", "0 %"))
        self.play_pushButton.setText(_translate("MainWindow", "播放"))
        self.pause_pushButton.setText(_translate("MainWindow", "暂停"))
        self.groupBox_3.setTitle(_translate("MainWindow", "检测信息:"))


