# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'el_gui_bandito.ui'
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
    QHBoxLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_El_GUI_BANDITO(object):
    def setupUi(self, El_GUI_BANDITO):
        if not El_GUI_BANDITO.objectName():
            El_GUI_BANDITO.setObjectName(u"El_GUI_BANDITO")
        El_GUI_BANDITO.resize(1140, 700)
        self.centralwidget = QWidget(El_GUI_BANDITO)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Main_widget = QWidget(self.centralwidget)
        self.Main_widget.setObjectName(u"Main_widget")
        self.Main_widget.setGeometry(QRect(0, 0, 1130, 690))
        self.Main_widget.setMaximumSize(QSize(16777215, 700))
        self.left_frame = QFrame(self.Main_widget)
        self.left_frame.setObjectName(u"left_frame")
        self.left_frame.setGeometry(QRect(10, 10, 210, 680))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(sizePolicy)
        self.left_frame.setMinimumSize(QSize(210, 680))
        self.left_frame.setMaximumSize(QSize(210, 680))
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.left_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.main_gBox = QGroupBox(self.left_frame)
        self.main_gBox.setObjectName(u"main_gBox")
        self.main_gBox.setMinimumSize(QSize(200, 470))
        self.main_gBox.setMaximumSize(QSize(190, 470))
        self.main_gBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2 = QVBoxLayout(self.main_gBox)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.plugin_frame_1 = QFrame(self.main_gBox)
        self.plugin_frame_1.setObjectName(u"plugin_frame_1")
        self.plugin_frame_1.setMinimumSize(QSize(180, 84))
        self.plugin_frame_1.setMaximumSize(QSize(180, 84))
        self.plugin_frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.plugin_frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.plugin_frame_1)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.plugin_led_1 = QLineEdit(self.plugin_frame_1)
        self.plugin_led_1.setObjectName(u"plugin_led_1")
        self.plugin_led_1.setMinimumSize(QSize(160, 30))
        self.plugin_led_1.setMaximumSize(QSize(160, 16777215))
        self.plugin_led_1.setReadOnly(True)

        self.gridLayout_2.addWidget(self.plugin_led_1, 0, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.switch_push_1 = QPushButton(self.plugin_frame_1)
        self.switch_push_1.setObjectName(u"switch_push_1")
        sizePolicy.setHeightForWidth(self.switch_push_1.sizePolicy().hasHeightForWidth())
        self.switch_push_1.setSizePolicy(sizePolicy)
        self.switch_push_1.setMinimumSize(QSize(30, 30))
        self.switch_push_1.setMaximumSize(QSize(30, 30))
        self.switch_push_1.setStyleSheet(u"")
        self.switch_push_1.setCheckable(True)

        self.gridLayout_2.addWidget(self.switch_push_1, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_add_toolB_1 = QToolButton(self.plugin_frame_1)
        self.plugin_add_toolB_1.setObjectName(u"plugin_add_toolB_1")
        self.plugin_add_toolB_1.setMinimumSize(QSize(30, 30))
        self.plugin_add_toolB_1.setMaximumSize(QSize(30, 30))
        self.plugin_add_toolB_1.setIconSize(QSize(128, 128))

        self.gridLayout_2.addWidget(self.plugin_add_toolB_1, 1, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_reload_toolB_1 = QToolButton(self.plugin_frame_1)
        self.plugin_reload_toolB_1.setObjectName(u"plugin_reload_toolB_1")
        self.plugin_reload_toolB_1.setMinimumSize(QSize(30, 30))
        self.plugin_reload_toolB_1.setMaximumSize(QSize(30, 30))
        self.plugin_reload_toolB_1.setIconSize(QSize(128, 128))

        self.gridLayout_2.addWidget(self.plugin_reload_toolB_1, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_delete_toolB_1 = QToolButton(self.plugin_frame_1)
        self.plugin_delete_toolB_1.setObjectName(u"plugin_delete_toolB_1")
        self.plugin_delete_toolB_1.setMinimumSize(QSize(30, 30))
        self.plugin_delete_toolB_1.setMaximumSize(QSize(30, 30))
        self.plugin_delete_toolB_1.setIconSize(QSize(128, 128))

        self.gridLayout_2.addWidget(self.plugin_delete_toolB_1, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addWidget(self.plugin_frame_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_frame_2 = QFrame(self.main_gBox)
        self.plugin_frame_2.setObjectName(u"plugin_frame_2")
        self.plugin_frame_2.setMinimumSize(QSize(180, 84))
        self.plugin_frame_2.setMaximumSize(QSize(180, 84))
        self.plugin_frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.plugin_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.plugin_frame_2)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.plugin_led_2 = QLineEdit(self.plugin_frame_2)
        self.plugin_led_2.setObjectName(u"plugin_led_2")
        self.plugin_led_2.setMinimumSize(QSize(160, 30))
        self.plugin_led_2.setMaximumSize(QSize(160, 16777215))
        self.plugin_led_2.setReadOnly(True)

        self.gridLayout_3.addWidget(self.plugin_led_2, 0, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.switch_push_2 = QPushButton(self.plugin_frame_2)
        self.switch_push_2.setObjectName(u"switch_push_2")
        sizePolicy.setHeightForWidth(self.switch_push_2.sizePolicy().hasHeightForWidth())
        self.switch_push_2.setSizePolicy(sizePolicy)
        self.switch_push_2.setMinimumSize(QSize(30, 30))
        self.switch_push_2.setMaximumSize(QSize(30, 30))
        self.switch_push_2.setStyleSheet(u"")
        self.switch_push_2.setCheckable(True)

        self.gridLayout_3.addWidget(self.switch_push_2, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_add_toolB_2 = QToolButton(self.plugin_frame_2)
        self.plugin_add_toolB_2.setObjectName(u"plugin_add_toolB_2")
        self.plugin_add_toolB_2.setMinimumSize(QSize(30, 30))
        self.plugin_add_toolB_2.setMaximumSize(QSize(30, 30))
        self.plugin_add_toolB_2.setIconSize(QSize(128, 128))

        self.gridLayout_3.addWidget(self.plugin_add_toolB_2, 1, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_reload_toolB_2 = QToolButton(self.plugin_frame_2)
        self.plugin_reload_toolB_2.setObjectName(u"plugin_reload_toolB_2")
        self.plugin_reload_toolB_2.setMinimumSize(QSize(30, 30))
        self.plugin_reload_toolB_2.setMaximumSize(QSize(30, 30))
        self.plugin_reload_toolB_2.setIconSize(QSize(128, 128))

        self.gridLayout_3.addWidget(self.plugin_reload_toolB_2, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_delete_toolB_2 = QToolButton(self.plugin_frame_2)
        self.plugin_delete_toolB_2.setObjectName(u"plugin_delete_toolB_2")
        self.plugin_delete_toolB_2.setMinimumSize(QSize(30, 30))
        self.plugin_delete_toolB_2.setMaximumSize(QSize(30, 30))
        self.plugin_delete_toolB_2.setIconSize(QSize(128, 128))

        self.gridLayout_3.addWidget(self.plugin_delete_toolB_2, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addWidget(self.plugin_frame_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_frame_3 = QFrame(self.main_gBox)
        self.plugin_frame_3.setObjectName(u"plugin_frame_3")
        self.plugin_frame_3.setMinimumSize(QSize(180, 84))
        self.plugin_frame_3.setMaximumSize(QSize(180, 84))
        self.plugin_frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.plugin_frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.plugin_frame_3)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        self.plugin_led_3 = QLineEdit(self.plugin_frame_3)
        self.plugin_led_3.setObjectName(u"plugin_led_3")
        self.plugin_led_3.setMinimumSize(QSize(160, 30))
        self.plugin_led_3.setMaximumSize(QSize(160, 16777215))
        self.plugin_led_3.setReadOnly(True)

        self.gridLayout_4.addWidget(self.plugin_led_3, 0, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.switch_push_3 = QPushButton(self.plugin_frame_3)
        self.switch_push_3.setObjectName(u"switch_push_3")
        sizePolicy.setHeightForWidth(self.switch_push_3.sizePolicy().hasHeightForWidth())
        self.switch_push_3.setSizePolicy(sizePolicy)
        self.switch_push_3.setMinimumSize(QSize(30, 30))
        self.switch_push_3.setMaximumSize(QSize(30, 30))
        self.switch_push_3.setStyleSheet(u"")
        self.switch_push_3.setCheckable(True)

        self.gridLayout_4.addWidget(self.switch_push_3, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_add_toolB_3 = QToolButton(self.plugin_frame_3)
        self.plugin_add_toolB_3.setObjectName(u"plugin_add_toolB_3")
        self.plugin_add_toolB_3.setMinimumSize(QSize(30, 30))
        self.plugin_add_toolB_3.setMaximumSize(QSize(30, 30))
        self.plugin_add_toolB_3.setIconSize(QSize(128, 128))

        self.gridLayout_4.addWidget(self.plugin_add_toolB_3, 1, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_reload_toolB_3 = QToolButton(self.plugin_frame_3)
        self.plugin_reload_toolB_3.setObjectName(u"plugin_reload_toolB_3")
        self.plugin_reload_toolB_3.setMinimumSize(QSize(30, 30))
        self.plugin_reload_toolB_3.setMaximumSize(QSize(30, 30))
        self.plugin_reload_toolB_3.setIconSize(QSize(128, 128))

        self.gridLayout_4.addWidget(self.plugin_reload_toolB_3, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_delete_toolB_3 = QToolButton(self.plugin_frame_3)
        self.plugin_delete_toolB_3.setObjectName(u"plugin_delete_toolB_3")
        self.plugin_delete_toolB_3.setMinimumSize(QSize(30, 30))
        self.plugin_delete_toolB_3.setMaximumSize(QSize(30, 30))
        self.plugin_delete_toolB_3.setIconSize(QSize(128, 128))

        self.gridLayout_4.addWidget(self.plugin_delete_toolB_3, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addWidget(self.plugin_frame_3, 0, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_frame_4 = QFrame(self.main_gBox)
        self.plugin_frame_4.setObjectName(u"plugin_frame_4")
        self.plugin_frame_4.setMinimumSize(QSize(180, 84))
        self.plugin_frame_4.setMaximumSize(QSize(180, 84))
        self.plugin_frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.plugin_frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.plugin_frame_4)
        self.gridLayout_5.setSpacing(5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.plugin_led_4 = QLineEdit(self.plugin_frame_4)
        self.plugin_led_4.setObjectName(u"plugin_led_4")
        self.plugin_led_4.setMinimumSize(QSize(160, 30))
        self.plugin_led_4.setMaximumSize(QSize(160, 16777215))
        self.plugin_led_4.setReadOnly(True)

        self.gridLayout_5.addWidget(self.plugin_led_4, 0, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.switch_push_4 = QPushButton(self.plugin_frame_4)
        self.switch_push_4.setObjectName(u"switch_push_4")
        sizePolicy.setHeightForWidth(self.switch_push_4.sizePolicy().hasHeightForWidth())
        self.switch_push_4.setSizePolicy(sizePolicy)
        self.switch_push_4.setMinimumSize(QSize(30, 30))
        self.switch_push_4.setMaximumSize(QSize(30, 30))
        self.switch_push_4.setStyleSheet(u"")
        self.switch_push_4.setCheckable(True)

        self.gridLayout_5.addWidget(self.switch_push_4, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_add_toolB_4 = QToolButton(self.plugin_frame_4)
        self.plugin_add_toolB_4.setObjectName(u"plugin_add_toolB_4")
        self.plugin_add_toolB_4.setMinimumSize(QSize(30, 30))
        self.plugin_add_toolB_4.setMaximumSize(QSize(30, 30))
        self.plugin_add_toolB_4.setIconSize(QSize(128, 128))

        self.gridLayout_5.addWidget(self.plugin_add_toolB_4, 1, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_reload_toolB_4 = QToolButton(self.plugin_frame_4)
        self.plugin_reload_toolB_4.setObjectName(u"plugin_reload_toolB_4")
        self.plugin_reload_toolB_4.setMinimumSize(QSize(30, 30))
        self.plugin_reload_toolB_4.setMaximumSize(QSize(30, 30))
        self.plugin_reload_toolB_4.setIconSize(QSize(128, 128))

        self.gridLayout_5.addWidget(self.plugin_reload_toolB_4, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_delete_toolB_4 = QToolButton(self.plugin_frame_4)
        self.plugin_delete_toolB_4.setObjectName(u"plugin_delete_toolB_4")
        self.plugin_delete_toolB_4.setMinimumSize(QSize(30, 30))
        self.plugin_delete_toolB_4.setMaximumSize(QSize(30, 30))
        self.plugin_delete_toolB_4.setIconSize(QSize(128, 128))

        self.gridLayout_5.addWidget(self.plugin_delete_toolB_4, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addWidget(self.plugin_frame_4, 0, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_frame_5 = QFrame(self.main_gBox)
        self.plugin_frame_5.setObjectName(u"plugin_frame_5")
        self.plugin_frame_5.setMinimumSize(QSize(180, 84))
        self.plugin_frame_5.setMaximumSize(QSize(180, 84))
        self.plugin_frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.plugin_frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.plugin_frame_5)
        self.gridLayout_6.setSpacing(5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(5, 5, 5, 5)
        self.plugin_led_5 = QLineEdit(self.plugin_frame_5)
        self.plugin_led_5.setObjectName(u"plugin_led_5")
        self.plugin_led_5.setMinimumSize(QSize(160, 30))
        self.plugin_led_5.setMaximumSize(QSize(160, 16777215))
        self.plugin_led_5.setReadOnly(True)

        self.gridLayout_6.addWidget(self.plugin_led_5, 0, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.switch_push_5 = QPushButton(self.plugin_frame_5)
        self.switch_push_5.setObjectName(u"switch_push_5")
        sizePolicy.setHeightForWidth(self.switch_push_5.sizePolicy().hasHeightForWidth())
        self.switch_push_5.setSizePolicy(sizePolicy)
        self.switch_push_5.setMinimumSize(QSize(30, 30))
        self.switch_push_5.setMaximumSize(QSize(30, 30))
        self.switch_push_5.setStyleSheet(u"")
        self.switch_push_5.setCheckable(True)

        self.gridLayout_6.addWidget(self.switch_push_5, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_add_toolB_5 = QToolButton(self.plugin_frame_5)
        self.plugin_add_toolB_5.setObjectName(u"plugin_add_toolB_5")
        self.plugin_add_toolB_5.setMinimumSize(QSize(30, 30))
        self.plugin_add_toolB_5.setMaximumSize(QSize(30, 30))
        self.plugin_add_toolB_5.setIconSize(QSize(128, 128))

        self.gridLayout_6.addWidget(self.plugin_add_toolB_5, 1, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_reload_toolB_5 = QToolButton(self.plugin_frame_5)
        self.plugin_reload_toolB_5.setObjectName(u"plugin_reload_toolB_5")
        self.plugin_reload_toolB_5.setMinimumSize(QSize(30, 30))
        self.plugin_reload_toolB_5.setMaximumSize(QSize(30, 30))
        self.plugin_reload_toolB_5.setIconSize(QSize(128, 128))

        self.gridLayout_6.addWidget(self.plugin_reload_toolB_5, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.plugin_delete_toolB_5 = QToolButton(self.plugin_frame_5)
        self.plugin_delete_toolB_5.setObjectName(u"plugin_delete_toolB_5")
        self.plugin_delete_toolB_5.setMinimumSize(QSize(30, 30))
        self.plugin_delete_toolB_5.setMaximumSize(QSize(30, 30))
        self.plugin_delete_toolB_5.setIconSize(QSize(128, 128))

        self.gridLayout_6.addWidget(self.plugin_delete_toolB_5, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addWidget(self.plugin_frame_5, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout.addWidget(self.main_gBox)

        self.settings_gBox = QGroupBox(self.left_frame)
        self.settings_gBox.setObjectName(u"settings_gBox")
        self.settings_gBox.setMinimumSize(QSize(200, 200))
        self.settings_gBox.setMaximumSize(QSize(200, 200))
        self.settings_gBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.settings_gBox.setFlat(False)
        self.settings_gBox.setCheckable(False)
        self.gridLayout = QGridLayout(self.settings_gBox)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.plugin_toolB = QToolButton(self.settings_gBox)
        self.plugin_toolB.setObjectName(u"plugin_toolB")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plugin_toolB.sizePolicy().hasHeightForWidth())
        self.plugin_toolB.setSizePolicy(sizePolicy1)
        self.plugin_toolB.setMinimumSize(QSize(180, 35))
        self.plugin_toolB.setMaximumSize(QSize(170, 35))

        self.gridLayout.addWidget(self.plugin_toolB, 2, 0, 1, 1)

        self.network_stat_line = QLineEdit(self.settings_gBox)
        self.network_stat_line.setObjectName(u"network_stat_line")
        sizePolicy1.setHeightForWidth(self.network_stat_line.sizePolicy().hasHeightForWidth())
        self.network_stat_line.setSizePolicy(sizePolicy1)
        self.network_stat_line.setMinimumSize(QSize(180, 35))
        self.network_stat_line.setMaximumSize(QSize(170, 35))
        self.network_stat_line.setFrame(True)
        self.network_stat_line.setReadOnly(True)

        self.gridLayout.addWidget(self.network_stat_line, 0, 0, 1, 1)

        self.settings_toolB = QToolButton(self.settings_gBox)
        self.settings_toolB.setObjectName(u"settings_toolB")
        sizePolicy1.setHeightForWidth(self.settings_toolB.sizePolicy().hasHeightForWidth())
        self.settings_toolB.setSizePolicy(sizePolicy1)
        self.settings_toolB.setMinimumSize(QSize(180, 35))
        self.settings_toolB.setMaximumSize(QSize(170, 35))

        self.gridLayout.addWidget(self.settings_toolB, 1, 0, 1, 1)

        self.null_Layout = QHBoxLayout()
        self.null_Layout.setSpacing(10)
        self.null_Layout.setObjectName(u"null_Layout")
        self.null_toolB_1 = QToolButton(self.settings_gBox)
        self.null_toolB_1.setObjectName(u"null_toolB_1")
        sizePolicy1.setHeightForWidth(self.null_toolB_1.sizePolicy().hasHeightForWidth())
        self.null_toolB_1.setSizePolicy(sizePolicy1)
        self.null_toolB_1.setMinimumSize(QSize(85, 35))
        self.null_toolB_1.setMaximumSize(QSize(80, 35))

        self.null_Layout.addWidget(self.null_toolB_1)

        self.null_toolB_2 = QToolButton(self.settings_gBox)
        self.null_toolB_2.setObjectName(u"null_toolB_2")
        sizePolicy1.setHeightForWidth(self.null_toolB_2.sizePolicy().hasHeightForWidth())
        self.null_toolB_2.setSizePolicy(sizePolicy1)
        self.null_toolB_2.setMinimumSize(QSize(85, 35))
        self.null_toolB_2.setMaximumSize(QSize(80, 35))

        self.null_Layout.addWidget(self.null_toolB_2)


        self.gridLayout.addLayout(self.null_Layout, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.settings_gBox)

        self.right_frame = QFrame(self.Main_widget)
        self.right_frame.setObjectName(u"right_frame")
        self.right_frame.setGeometry(QRect(230, 10, 900, 680))
        sizePolicy.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        self.right_frame.setSizePolicy(sizePolicy)
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Shadow.Raised)
        El_GUI_BANDITO.setCentralWidget(self.centralwidget)

        self.retranslateUi(El_GUI_BANDITO)

        QMetaObject.connectSlotsByName(El_GUI_BANDITO)
    # setupUi

    def retranslateUi(self, El_GUI_BANDITO):
        El_GUI_BANDITO.setWindowTitle(QCoreApplication.translate("El_GUI_BANDITO", u"el_gui_bandito v.0.0.5", None))
        self.main_gBox.setTitle(QCoreApplication.translate("El_GUI_BANDITO", u"el_gui_bandito", None))
        self.switch_push_1.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_add_toolB_1.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Add Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_add_toolB_1.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_reload_toolB_1.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Reload Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_reload_toolB_1.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_delete_toolB_1.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Delete plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_delete_toolB_1.setText("")
        self.switch_push_2.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_add_toolB_2.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Add Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_add_toolB_2.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_reload_toolB_2.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Reload Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_reload_toolB_2.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_delete_toolB_2.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Delete plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_delete_toolB_2.setText("")
        self.switch_push_3.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_add_toolB_3.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Add Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_add_toolB_3.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_reload_toolB_3.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Reload Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_reload_toolB_3.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_delete_toolB_3.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Delete plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_delete_toolB_3.setText("")
        self.switch_push_4.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_add_toolB_4.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Add Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_add_toolB_4.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_reload_toolB_4.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Reload Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_reload_toolB_4.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_delete_toolB_4.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Delete plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_delete_toolB_4.setText("")
        self.switch_push_5.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_add_toolB_5.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Add Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_add_toolB_5.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_reload_toolB_5.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Reload Plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_reload_toolB_5.setText("")
#if QT_CONFIG(tooltip)
        self.plugin_delete_toolB_5.setToolTip(QCoreApplication.translate("El_GUI_BANDITO", u"Delete plugin", None))
#endif // QT_CONFIG(tooltip)
        self.plugin_delete_toolB_5.setText("")
        self.settings_gBox.setTitle(QCoreApplication.translate("El_GUI_BANDITO", u"Status", None))
        self.plugin_toolB.setText(QCoreApplication.translate("El_GUI_BANDITO", u"Plugin Manager", None))
        self.settings_toolB.setText(QCoreApplication.translate("El_GUI_BANDITO", u"Settings", None))
        self.null_toolB_1.setText(QCoreApplication.translate("El_GUI_BANDITO", u"null_button", None))
        self.null_toolB_2.setText(QCoreApplication.translate("El_GUI_BANDITO", u"null_button", None))
    # retranslateUi

