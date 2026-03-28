# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tune_cliento.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QProgressBar,
    QSizePolicy, QSlider, QToolButton, QVBoxLayout,
    QWidget)

class Ui_tune_cliento(object):
    def setupUi(self, tune_cliento):
        if not tune_cliento.objectName():
            tune_cliento.setObjectName(u"tune_cliento")
        tune_cliento.resize(785, 580)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(tune_cliento.sizePolicy().hasHeightForWidth())
        tune_cliento.setSizePolicy(sizePolicy)
        tune_cliento.setMinimumSize(QSize(785, 580))
        tune_cliento.setMaximumSize(QSize(785, 580))
        self.verticalLayout = QVBoxLayout(tune_cliento)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.tune_frame = QFrame(tune_cliento)
        self.tune_frame.setObjectName(u"tune_frame")
        self.tune_frame.setEnabled(True)
        sizePolicy.setHeightForWidth(self.tune_frame.sizePolicy().hasHeightForWidth())
        self.tune_frame.setSizePolicy(sizePolicy)
        self.tune_frame.setMinimumSize(QSize(760, 560))
        self.tune_frame.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(5)
        self.tune_frame.setFont(font)
        self.tune_frame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.tune_frame.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.tune_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tune_frame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.tune_frame.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        self.tune_frame.setFrameShape(QFrame.Shape.Panel)
        self.tune_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.tune_frame.setLineWidth(1)
        self.gridLayout = QGridLayout(self.tune_frame)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.volume_frame = QFrame(self.tune_frame)
        self.volume_frame.setObjectName(u"volume_frame")
        self.volume_frame.setMinimumSize(QSize(390, 540))
        self.volume_frame.setMaximumSize(QSize(390, 540))
        self.volume_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.volume_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.volume_frame)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.mic_frame = QFrame(self.volume_frame)
        self.mic_frame.setObjectName(u"mic_frame")
        self.mic_frame.setMinimumSize(QSize(120, 0))
        self.mic_frame.setMaximumSize(QSize(120, 16777215))
        self.mic_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mic_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.mic_frame)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.mic_top_frame = QFrame(self.mic_frame)
        self.mic_top_frame.setObjectName(u"mic_top_frame")
        self.mic_top_frame.setMinimumSize(QSize(105, 0))
        self.mic_top_frame.setMaximumSize(QSize(105, 140))
        self.mic_top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mic_top_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.mic_top_frame)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.mic_lable = QLabel(self.mic_top_frame)
        self.mic_lable.setObjectName(u"mic_lable")
        self.mic_lable.setMinimumSize(QSize(85, 25))
        self.mic_lable.setMaximumSize(QSize(85, 25))
        font1 = QFont()
        font1.setPointSize(10)
        self.mic_lable.setFont(font1)
        self.mic_lable.setFrameShape(QFrame.Shape.Panel)
        self.mic_lable.setTextFormat(Qt.TextFormat.RichText)
        self.mic_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.mic_lable, 0, Qt.AlignmentFlag.AlignHCenter)

        self.mic_level_pBar = QProgressBar(self.mic_top_frame)
        self.mic_level_pBar.setObjectName(u"mic_level_pBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mic_level_pBar.sizePolicy().hasHeightForWidth())
        self.mic_level_pBar.setSizePolicy(sizePolicy1)
        self.mic_level_pBar.setMinimumSize(QSize(30, 80))
        self.mic_level_pBar.setMaximumSize(QSize(30, 80))
        self.mic_level_pBar.setValue(24)
        self.mic_level_pBar.setTextVisible(True)
        self.mic_level_pBar.setOrientation(Qt.Orientation.Vertical)

        self.verticalLayout_5.addWidget(self.mic_level_pBar, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_6.addWidget(self.mic_top_frame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.mic_bottom_frame = QFrame(self.mic_frame)
        self.mic_bottom_frame.setObjectName(u"mic_bottom_frame")
        self.mic_bottom_frame.setMinimumSize(QSize(105, 365))
        self.mic_bottom_frame.setMaximumSize(QSize(105, 365))
        self.mic_bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mic_bottom_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mic_bottom_frame)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.mic_volume_slider = QSlider(self.mic_bottom_frame)
        self.mic_volume_slider.setObjectName(u"mic_volume_slider")
        self.mic_volume_slider.setMinimumSize(QSize(50, 0))
        self.mic_volume_slider.setMaximumSize(QSize(50, 16777215))
        self.mic_volume_slider.setMaximum(100)
        self.mic_volume_slider.setTracking(True)
        self.mic_volume_slider.setOrientation(Qt.Orientation.Vertical)
        self.mic_volume_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.mic_volume_slider.setTickInterval(0)

        self.verticalLayout_2.addWidget(self.mic_volume_slider, 0, Qt.AlignmentFlag.AlignHCenter)

        self.mic_mute_toolB = QToolButton(self.mic_bottom_frame)
        self.mic_mute_toolB.setObjectName(u"mic_mute_toolB")
        self.mic_mute_toolB.setMinimumSize(QSize(70, 70))
        self.mic_mute_toolB.setMaximumSize(QSize(70, 70))
        self.mic_mute_toolB.setIconSize(QSize(70, 70))
        self.mic_mute_toolB.setCheckable(True)

        self.verticalLayout_2.addWidget(self.mic_mute_toolB, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_6.addWidget(self.mic_bottom_frame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_6.setStretch(0, 3)
        self.verticalLayout_6.setStretch(1, 9)

        self.horizontalLayout_4.addWidget(self.mic_frame)

        self.sound_frame_2 = QFrame(self.volume_frame)
        self.sound_frame_2.setObjectName(u"sound_frame_2")
        self.sound_frame_2.setMinimumSize(QSize(120, 0))
        self.sound_frame_2.setMaximumSize(QSize(120, 16777215))
        self.sound_frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.sound_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.sound_frame_2)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.sound_top_frame = QFrame(self.sound_frame_2)
        self.sound_top_frame.setObjectName(u"sound_top_frame")
        self.sound_top_frame.setMinimumSize(QSize(105, 0))
        self.sound_top_frame.setMaximumSize(QSize(105, 140))
        self.sound_top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sound_top_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.sound_top_frame)
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(5, 5, 5, 5)
        self.sound_lable = QLabel(self.sound_top_frame)
        self.sound_lable.setObjectName(u"sound_lable")
        self.sound_lable.setMinimumSize(QSize(85, 25))
        self.sound_lable.setMaximumSize(QSize(85, 25))
        self.sound_lable.setFont(font1)
        self.sound_lable.setFrameShape(QFrame.Shape.Panel)
        self.sound_lable.setTextFormat(Qt.TextFormat.RichText)
        self.sound_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.sound_lable, 0, Qt.AlignmentFlag.AlignHCenter)

        self.sound_bar_frame = QHBoxLayout()
        self.sound_bar_frame.setSpacing(0)
        self.sound_bar_frame.setObjectName(u"sound_bar_frame")
        self.sound_bar_frame.setContentsMargins(0, 0, 0, 0)
        self.sound_level_01_pBar = QProgressBar(self.sound_top_frame)
        self.sound_level_01_pBar.setObjectName(u"sound_level_01_pBar")
        sizePolicy1.setHeightForWidth(self.sound_level_01_pBar.sizePolicy().hasHeightForWidth())
        self.sound_level_01_pBar.setSizePolicy(sizePolicy1)
        self.sound_level_01_pBar.setMinimumSize(QSize(30, 80))
        self.sound_level_01_pBar.setMaximumSize(QSize(30, 80))
        self.sound_level_01_pBar.setValue(24)
        self.sound_level_01_pBar.setOrientation(Qt.Orientation.Vertical)

        self.sound_bar_frame.addWidget(self.sound_level_01_pBar)

        self.sound_level_02_pBar = QProgressBar(self.sound_top_frame)
        self.sound_level_02_pBar.setObjectName(u"sound_level_02_pBar")
        sizePolicy1.setHeightForWidth(self.sound_level_02_pBar.sizePolicy().hasHeightForWidth())
        self.sound_level_02_pBar.setSizePolicy(sizePolicy1)
        self.sound_level_02_pBar.setMinimumSize(QSize(30, 80))
        self.sound_level_02_pBar.setMaximumSize(QSize(30, 80))
        self.sound_level_02_pBar.setValue(24)
        self.sound_level_02_pBar.setOrientation(Qt.Orientation.Vertical)

        self.sound_bar_frame.addWidget(self.sound_level_02_pBar)


        self.verticalLayout_8.addLayout(self.sound_bar_frame)


        self.verticalLayout_3.addWidget(self.sound_top_frame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.sound_bottom_frame = QFrame(self.sound_frame_2)
        self.sound_bottom_frame.setObjectName(u"sound_bottom_frame")
        self.sound_bottom_frame.setMinimumSize(QSize(105, 365))
        self.sound_bottom_frame.setMaximumSize(QSize(105, 365))
        self.sound_bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sound_bottom_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.sound_bottom_frame)
        self.verticalLayout_9.setSpacing(15)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(10, 10, 10, 10)
        self.sound_volume_slider = QSlider(self.sound_bottom_frame)
        self.sound_volume_slider.setObjectName(u"sound_volume_slider")
        self.sound_volume_slider.setMinimumSize(QSize(50, 0))
        self.sound_volume_slider.setMaximumSize(QSize(50, 16777215))
        self.sound_volume_slider.setMaximum(100)
        self.sound_volume_slider.setOrientation(Qt.Orientation.Vertical)
        self.sound_volume_slider.setTickPosition(QSlider.TickPosition.TicksAbove)

        self.verticalLayout_9.addWidget(self.sound_volume_slider, 0, Qt.AlignmentFlag.AlignHCenter)

        self.sound_mute_toolB = QToolButton(self.sound_bottom_frame)
        self.sound_mute_toolB.setObjectName(u"sound_mute_toolB")
        self.sound_mute_toolB.setMinimumSize(QSize(70, 70))
        self.sound_mute_toolB.setMaximumSize(QSize(70, 70))
        self.sound_mute_toolB.setIconSize(QSize(70, 70))
        self.sound_mute_toolB.setCheckable(True)

        self.verticalLayout_9.addWidget(self.sound_mute_toolB, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_3.addWidget(self.sound_bottom_frame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_3.setStretch(0, 3)
        self.verticalLayout_3.setStretch(1, 9)

        self.horizontalLayout_4.addWidget(self.sound_frame_2)

        self.other_frame = QFrame(self.volume_frame)
        self.other_frame.setObjectName(u"other_frame")
        self.other_frame.setMinimumSize(QSize(120, 0))
        self.other_frame.setMaximumSize(QSize(120, 16777215))
        self.other_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.other_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.other_frame)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.other_top_frame = QFrame(self.other_frame)
        self.other_top_frame.setObjectName(u"other_top_frame")
        self.other_top_frame.setMinimumSize(QSize(105, 0))
        self.other_top_frame.setMaximumSize(QSize(105, 140))
        self.other_top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.other_top_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.other_top_frame)
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 5, 5, 5)
        self.other_lable = QLabel(self.other_top_frame)
        self.other_lable.setObjectName(u"other_lable")
        self.other_lable.setMinimumSize(QSize(85, 25))
        self.other_lable.setMaximumSize(QSize(85, 25))
        self.other_lable.setFont(font1)
        self.other_lable.setFrameShape(QFrame.Shape.Panel)
        self.other_lable.setTextFormat(Qt.TextFormat.RichText)
        self.other_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.other_lable, 0, Qt.AlignmentFlag.AlignHCenter)

        self.other_level_pBar = QProgressBar(self.other_top_frame)
        self.other_level_pBar.setObjectName(u"other_level_pBar")
        sizePolicy1.setHeightForWidth(self.other_level_pBar.sizePolicy().hasHeightForWidth())
        self.other_level_pBar.setSizePolicy(sizePolicy1)
        self.other_level_pBar.setMinimumSize(QSize(30, 80))
        self.other_level_pBar.setMaximumSize(QSize(30, 80))
        self.other_level_pBar.setValue(24)
        self.other_level_pBar.setOrientation(Qt.Orientation.Vertical)

        self.verticalLayout_10.addWidget(self.other_level_pBar, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_4.addWidget(self.other_top_frame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.other_bottom_frame = QFrame(self.other_frame)
        self.other_bottom_frame.setObjectName(u"other_bottom_frame")
        self.other_bottom_frame.setMinimumSize(QSize(105, 365))
        self.other_bottom_frame.setMaximumSize(QSize(105, 365))
        self.other_bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.other_bottom_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.other_bottom_frame)
        self.verticalLayout_11.setSpacing(15)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(10, 10, 10, 10)
        self.other_volume_slider = QSlider(self.other_bottom_frame)
        self.other_volume_slider.setObjectName(u"other_volume_slider")
        self.other_volume_slider.setMinimumSize(QSize(50, 0))
        self.other_volume_slider.setMaximumSize(QSize(50, 16777215))
        self.other_volume_slider.setMaximum(100)
        self.other_volume_slider.setOrientation(Qt.Orientation.Vertical)
        self.other_volume_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.other_volume_slider.setTickInterval(10)

        self.verticalLayout_11.addWidget(self.other_volume_slider, 0, Qt.AlignmentFlag.AlignHCenter)

        self.other_mute_toolB = QToolButton(self.other_bottom_frame)
        self.other_mute_toolB.setObjectName(u"other_mute_toolB")
        self.other_mute_toolB.setMinimumSize(QSize(70, 70))
        self.other_mute_toolB.setMaximumSize(QSize(70, 70))
        self.other_mute_toolB.setIconSize(QSize(70, 70))
        self.other_mute_toolB.setCheckable(True)

        self.verticalLayout_11.addWidget(self.other_mute_toolB, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_4.addWidget(self.other_bottom_frame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_4.setStretch(0, 3)
        self.verticalLayout_4.setStretch(1, 9)

        self.horizontalLayout_4.addWidget(self.other_frame)


        self.gridLayout.addWidget(self.volume_frame, 0, 0, 2, 1)

        self.eq_frame = QFrame(self.tune_frame)
        self.eq_frame.setObjectName(u"eq_frame")
        self.eq_frame.setMinimumSize(QSize(350, 140))
        self.eq_frame.setMaximumSize(QSize(350, 140))
        self.eq_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.eq_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.eq_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.equalaizer_qFrame = QFrame(self.eq_frame)
        self.equalaizer_qFrame.setObjectName(u"equalaizer_qFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.equalaizer_qFrame.sizePolicy().hasHeightForWidth())
        self.equalaizer_qFrame.setSizePolicy(sizePolicy2)
        self.equalaizer_qFrame.setMinimumSize(QSize(310, 110))
        self.equalaizer_qFrame.setMaximumSize(QSize(310, 110))
        self.equalaizer_qFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.equalaizer_qFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.equalaizer_qFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.eq_01_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_01_pBar.setObjectName(u"eq_01_pBar")
        sizePolicy1.setHeightForWidth(self.eq_01_pBar.sizePolicy().hasHeightForWidth())
        self.eq_01_pBar.setSizePolicy(sizePolicy1)
        self.eq_01_pBar.setMinimumSize(QSize(20, 0))
        self.eq_01_pBar.setValue(24)
        self.eq_01_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_01_pBar)

        self.eq_02_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_02_pBar.setObjectName(u"eq_02_pBar")
        sizePolicy1.setHeightForWidth(self.eq_02_pBar.sizePolicy().hasHeightForWidth())
        self.eq_02_pBar.setSizePolicy(sizePolicy1)
        self.eq_02_pBar.setMinimumSize(QSize(20, 0))
        self.eq_02_pBar.setValue(24)
        self.eq_02_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_02_pBar)

        self.eq_03_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_03_pBar.setObjectName(u"eq_03_pBar")
        sizePolicy1.setHeightForWidth(self.eq_03_pBar.sizePolicy().hasHeightForWidth())
        self.eq_03_pBar.setSizePolicy(sizePolicy1)
        self.eq_03_pBar.setMinimumSize(QSize(20, 0))
        self.eq_03_pBar.setValue(24)
        self.eq_03_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_03_pBar)

        self.eq_04_Bar = QProgressBar(self.equalaizer_qFrame)
        self.eq_04_Bar.setObjectName(u"eq_04_Bar")
        sizePolicy1.setHeightForWidth(self.eq_04_Bar.sizePolicy().hasHeightForWidth())
        self.eq_04_Bar.setSizePolicy(sizePolicy1)
        self.eq_04_Bar.setMinimumSize(QSize(20, 0))
        self.eq_04_Bar.setValue(24)
        self.eq_04_Bar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_04_Bar)

        self.eq_05_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_05_pBar.setObjectName(u"eq_05_pBar")
        sizePolicy1.setHeightForWidth(self.eq_05_pBar.sizePolicy().hasHeightForWidth())
        self.eq_05_pBar.setSizePolicy(sizePolicy1)
        self.eq_05_pBar.setMinimumSize(QSize(20, 0))
        self.eq_05_pBar.setValue(24)
        self.eq_05_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_05_pBar)

        self.eq_06_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_06_pBar.setObjectName(u"eq_06_pBar")
        sizePolicy1.setHeightForWidth(self.eq_06_pBar.sizePolicy().hasHeightForWidth())
        self.eq_06_pBar.setSizePolicy(sizePolicy1)
        self.eq_06_pBar.setMinimumSize(QSize(20, 0))
        self.eq_06_pBar.setValue(24)
        self.eq_06_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_06_pBar)

        self.eq_07_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_07_pBar.setObjectName(u"eq_07_pBar")
        sizePolicy1.setHeightForWidth(self.eq_07_pBar.sizePolicy().hasHeightForWidth())
        self.eq_07_pBar.setSizePolicy(sizePolicy1)
        self.eq_07_pBar.setMinimumSize(QSize(20, 0))
        self.eq_07_pBar.setValue(24)
        self.eq_07_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_07_pBar)

        self.eq_08_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_08_pBar.setObjectName(u"eq_08_pBar")
        sizePolicy1.setHeightForWidth(self.eq_08_pBar.sizePolicy().hasHeightForWidth())
        self.eq_08_pBar.setSizePolicy(sizePolicy1)
        self.eq_08_pBar.setMinimumSize(QSize(20, 0))
        self.eq_08_pBar.setValue(24)
        self.eq_08_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_08_pBar)

        self.eq_09_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_09_pBar.setObjectName(u"eq_09_pBar")
        sizePolicy1.setHeightForWidth(self.eq_09_pBar.sizePolicy().hasHeightForWidth())
        self.eq_09_pBar.setSizePolicy(sizePolicy1)
        self.eq_09_pBar.setMinimumSize(QSize(20, 0))
        self.eq_09_pBar.setValue(24)
        self.eq_09_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_09_pBar)

        self.eq_10_pBar = QProgressBar(self.equalaizer_qFrame)
        self.eq_10_pBar.setObjectName(u"eq_10_pBar")
        sizePolicy1.setHeightForWidth(self.eq_10_pBar.sizePolicy().hasHeightForWidth())
        self.eq_10_pBar.setSizePolicy(sizePolicy1)
        self.eq_10_pBar.setMinimumSize(QSize(20, 0))
        self.eq_10_pBar.setValue(24)
        self.eq_10_pBar.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.eq_10_pBar)


        self.gridLayout_2.addWidget(self.equalaizer_qFrame, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.eq_frame, 0, 1, 1, 1)

        self.audio_device_frame = QFrame(self.tune_frame)
        self.audio_device_frame.setObjectName(u"audio_device_frame")
        self.audio_device_frame.setMinimumSize(QSize(350, 390))
        self.audio_device_frame.setMaximumSize(QSize(350, 390))
        self.audio_device_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.audio_device_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.audio_device_frame)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.audio_device_groupB = QGroupBox(self.audio_device_frame)
        self.audio_device_groupB.setObjectName(u"audio_device_groupB")
        self.audio_device_groupB.setFont(font1)
        self.verticalLayout_15 = QVBoxLayout(self.audio_device_groupB)
        self.verticalLayout_15.setSpacing(5)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(5, 5, 5, 5)
        self.audio_device_01_groupB = QFrame(self.audio_device_groupB)
        self.audio_device_01_groupB.setObjectName(u"audio_device_01_groupB")
        self.horizontalLayout_21 = QHBoxLayout(self.audio_device_01_groupB)
        self.horizontalLayout_21.setSpacing(5)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(5, 5, 5, 5)
        self.audiD_01_label = QLabel(self.audio_device_01_groupB)
        self.audiD_01_label.setObjectName(u"audiD_01_label")
        self.audiD_01_label.setFont(font1)
        self.audiD_01_label.setLineWidth(0)

        self.horizontalLayout_21.addWidget(self.audiD_01_label, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.audiD_01_lineE = QLineEdit(self.audio_device_01_groupB)
        self.audiD_01_lineE.setObjectName(u"audiD_01_lineE")
        self.audiD_01_lineE.setMinimumSize(QSize(0, 30))
        self.audiD_01_lineE.setReadOnly(True)

        self.horizontalLayout_21.addWidget(self.audiD_01_lineE)

        self.audiD_01_toolB = QToolButton(self.audio_device_01_groupB)
        self.audiD_01_toolB.setObjectName(u"audiD_01_toolB")
        sizePolicy2.setHeightForWidth(self.audiD_01_toolB.sizePolicy().hasHeightForWidth())
        self.audiD_01_toolB.setSizePolicy(sizePolicy2)
        self.audiD_01_toolB.setMinimumSize(QSize(40, 40))
        self.audiD_01_toolB.setMaximumSize(QSize(40, 40))
        self.audiD_01_toolB.setIconSize(QSize(32, 32))

        self.horizontalLayout_21.addWidget(self.audiD_01_toolB, 0, Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_21.setStretch(0, 1)
        self.horizontalLayout_21.setStretch(1, 5)
        self.horizontalLayout_21.setStretch(2, 1)

        self.verticalLayout_15.addWidget(self.audio_device_01_groupB)

        self.audio_device_02_groupB = QGroupBox(self.audio_device_groupB)
        self.audio_device_02_groupB.setObjectName(u"audio_device_02_groupB")
        self.horizontalLayout_22 = QHBoxLayout(self.audio_device_02_groupB)
        self.horizontalLayout_22.setSpacing(5)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(5, 5, 5, 5)
        self.audiD_02_label = QLabel(self.audio_device_02_groupB)
        self.audiD_02_label.setObjectName(u"audiD_02_label")
        self.audiD_02_label.setFont(font1)
        self.audiD_02_label.setLineWidth(0)

        self.horizontalLayout_22.addWidget(self.audiD_02_label, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.audiD_02_lineE = QLineEdit(self.audio_device_02_groupB)
        self.audiD_02_lineE.setObjectName(u"audiD_02_lineE")
        self.audiD_02_lineE.setMinimumSize(QSize(0, 30))
        self.audiD_02_lineE.setReadOnly(True)

        self.horizontalLayout_22.addWidget(self.audiD_02_lineE)

        self.audiD_02_toolB = QToolButton(self.audio_device_02_groupB)
        self.audiD_02_toolB.setObjectName(u"audiD_02_toolB")
        sizePolicy2.setHeightForWidth(self.audiD_02_toolB.sizePolicy().hasHeightForWidth())
        self.audiD_02_toolB.setSizePolicy(sizePolicy2)
        self.audiD_02_toolB.setMinimumSize(QSize(40, 40))
        self.audiD_02_toolB.setMaximumSize(QSize(40, 40))
        self.audiD_02_toolB.setIconSize(QSize(32, 32))

        self.horizontalLayout_22.addWidget(self.audiD_02_toolB, 0, Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_22.setStretch(0, 1)
        self.horizontalLayout_22.setStretch(1, 5)
        self.horizontalLayout_22.setStretch(2, 1)

        self.verticalLayout_15.addWidget(self.audio_device_02_groupB)

        self.bluetooth_device_groupB = QGroupBox(self.audio_device_groupB)
        self.bluetooth_device_groupB.setObjectName(u"bluetooth_device_groupB")
        self.horizontalLayout_23 = QHBoxLayout(self.bluetooth_device_groupB)
        self.horizontalLayout_23.setSpacing(5)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(5, 5, 5, 5)
        self.bt_audiD_label = QLabel(self.bluetooth_device_groupB)
        self.bt_audiD_label.setObjectName(u"bt_audiD_label")
        self.bt_audiD_label.setFont(font1)
        self.bt_audiD_label.setLineWidth(0)

        self.horizontalLayout_23.addWidget(self.bt_audiD_label, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.bt_audiD_lineE = QLineEdit(self.bluetooth_device_groupB)
        self.bt_audiD_lineE.setObjectName(u"bt_audiD_lineE")
        self.bt_audiD_lineE.setMinimumSize(QSize(0, 30))
        self.bt_audiD_lineE.setReadOnly(True)

        self.horizontalLayout_23.addWidget(self.bt_audiD_lineE)

        self.bt_audiD_toolB = QToolButton(self.bluetooth_device_groupB)
        self.bt_audiD_toolB.setObjectName(u"bt_audiD_toolB")
        sizePolicy2.setHeightForWidth(self.bt_audiD_toolB.sizePolicy().hasHeightForWidth())
        self.bt_audiD_toolB.setSizePolicy(sizePolicy2)
        self.bt_audiD_toolB.setMinimumSize(QSize(40, 40))
        self.bt_audiD_toolB.setMaximumSize(QSize(40, 40))
        self.bt_audiD_toolB.setIconSize(QSize(32, 32))

        self.horizontalLayout_23.addWidget(self.bt_audiD_toolB, 0, Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_23.setStretch(0, 1)
        self.horizontalLayout_23.setStretch(1, 5)
        self.horizontalLayout_23.setStretch(2, 1)

        self.verticalLayout_15.addWidget(self.bluetooth_device_groupB)

        self.mic_01_groupB = QGroupBox(self.audio_device_groupB)
        self.mic_01_groupB.setObjectName(u"mic_01_groupB")
        self.horizontalLayout_24 = QHBoxLayout(self.mic_01_groupB)
        self.horizontalLayout_24.setSpacing(5)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(5, 5, 5, 5)
        self.mic_01_label = QLabel(self.mic_01_groupB)
        self.mic_01_label.setObjectName(u"mic_01_label")
        self.mic_01_label.setFont(font1)
        self.mic_01_label.setLineWidth(0)

        self.horizontalLayout_24.addWidget(self.mic_01_label, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.mic_01_lineE = QLineEdit(self.mic_01_groupB)
        self.mic_01_lineE.setObjectName(u"mic_01_lineE")
        self.mic_01_lineE.setMinimumSize(QSize(0, 30))
        self.mic_01_lineE.setReadOnly(True)

        self.horizontalLayout_24.addWidget(self.mic_01_lineE)

        self.mic_01_toolB = QToolButton(self.mic_01_groupB)
        self.mic_01_toolB.setObjectName(u"mic_01_toolB")
        sizePolicy2.setHeightForWidth(self.mic_01_toolB.sizePolicy().hasHeightForWidth())
        self.mic_01_toolB.setSizePolicy(sizePolicy2)
        self.mic_01_toolB.setMinimumSize(QSize(40, 40))
        self.mic_01_toolB.setMaximumSize(QSize(40, 40))
        self.mic_01_toolB.setIconSize(QSize(32, 32))

        self.horizontalLayout_24.addWidget(self.mic_01_toolB, 0, Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_24.setStretch(0, 1)
        self.horizontalLayout_24.setStretch(1, 5)
        self.horizontalLayout_24.setStretch(2, 1)

        self.verticalLayout_15.addWidget(self.mic_01_groupB)


        self.gridLayout_3.addWidget(self.audio_device_groupB, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.audio_device_frame, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.tune_frame)


        self.retranslateUi(tune_cliento)

        QMetaObject.connectSlotsByName(tune_cliento)
    # setupUi

    def retranslateUi(self, tune_cliento):
        self.mic_lable.setText(QCoreApplication.translate("tune_cliento", u"Microphone", None))
        self.mic_mute_toolB.setText(QCoreApplication.translate("tune_cliento", u"...", None))
        self.sound_lable.setText(QCoreApplication.translate("tune_cliento", u"Sound", None))
        self.sound_mute_toolB.setText(QCoreApplication.translate("tune_cliento", u"...", None))
        self.other_lable.setText(QCoreApplication.translate("tune_cliento", u"Other", None))
        self.other_mute_toolB.setText(QCoreApplication.translate("tune_cliento", u"...", None))
        self.audio_device_groupB.setTitle(QCoreApplication.translate("tune_cliento", u"Device Output", None))
        self.audiD_01_label.setText(QCoreApplication.translate("tune_cliento", u"#1", None))
        self.audiD_01_toolB.setText("")
        self.audiD_02_label.setText(QCoreApplication.translate("tune_cliento", u"#2", None))
        self.audiD_02_toolB.setText("")
        self.bt_audiD_label.setText(QCoreApplication.translate("tune_cliento", u"BT", None))
        self.bt_audiD_toolB.setText("")
        self.mic_01_label.setText(QCoreApplication.translate("tune_cliento", u"Mic", None))
        self.mic_01_toolB.setText("")
        pass
    # retranslateUi

