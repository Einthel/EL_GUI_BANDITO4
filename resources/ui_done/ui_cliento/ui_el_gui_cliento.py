# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'el_gui_cliento.ui'
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
    QHBoxLayout, QLCDNumber, QLineEdit, QMainWindow,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_El_GUI_CLIENTO(object):
    def setupUi(self, El_GUI_CLIENTO):
        if not El_GUI_CLIENTO.objectName():
            El_GUI_CLIENTO.setObjectName(u"El_GUI_CLIENTO")
        El_GUI_CLIENTO.resize(1024, 600)
        El_GUI_CLIENTO.setMinimumSize(QSize(1024, 600))
        El_GUI_CLIENTO.setMaximumSize(QSize(1024, 600))
        El_GUI_CLIENTO.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.centralwidget = QWidget(El_GUI_CLIENTO)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1024, 600))
        self.centralwidget.setMaximumSize(QSize(1024, 600))
        self.centralwidget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.Main_widget = QWidget(self.centralwidget)
        self.Main_widget.setObjectName(u"Main_widget")
        self.Main_widget.setGeometry(QRect(0, 0, 1024, 600))
        self.Main_widget.setMinimumSize(QSize(1024, 600))
        self.Main_widget.setMaximumSize(QSize(1024, 600))
        self.horizontalLayout = QHBoxLayout(self.Main_widget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.left_frame = QFrame(self.Main_widget)
        self.left_frame.setObjectName(u"left_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(sizePolicy)
        self.left_frame.setMinimumSize(QSize(210, 580))
        self.left_frame.setMaximumSize(QSize(210, 580))
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.left_frame)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.time_gBox = QGroupBox(self.left_frame)
        self.time_gBox.setObjectName(u"time_gBox")
        self.time_gBox.setMinimumSize(QSize(190, 370))
        self.time_gBox.setMaximumSize(QSize(190, 370))
        self.time_gBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.time_gBox)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.Time_gBox = QGroupBox(self.time_gBox)
        self.Time_gBox.setObjectName(u"Time_gBox")
        self.Time_gBox.setMinimumSize(QSize(170, 0))
        self.Time_gBox.setMaximumSize(QSize(170, 90))
        self.Time_gBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_10 = QHBoxLayout(self.Time_gBox)
        self.horizontalLayout_10.setSpacing(5)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 5, 5, 5)
        self.HH = QHBoxLayout()
        self.HH.setObjectName(u"HH")
        self.HH_lcdN = QLCDNumber(self.Time_gBox)
        self.HH_lcdN.setObjectName(u"HH_lcdN")
        self.HH_lcdN.setMinimumSize(QSize(75, 75))
        self.HH_lcdN.setMaximumSize(QSize(75, 75))
        self.HH_lcdN.setFrameShape(QFrame.Shape.Panel)
        self.HH_lcdN.setFrameShadow(QFrame.Shadow.Raised)
        self.HH_lcdN.setSmallDecimalPoint(False)
        self.HH_lcdN.setDigitCount(2)
        self.HH_lcdN.setMode(QLCDNumber.Mode.Dec)
        self.HH_lcdN.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)

        self.HH.addWidget(self.HH_lcdN)


        self.horizontalLayout_10.addLayout(self.HH)

        self.MM = QHBoxLayout()
        self.MM.setObjectName(u"MM")
        self.MM_lcdN = QLCDNumber(self.Time_gBox)
        self.MM_lcdN.setObjectName(u"MM_lcdN")
        self.MM_lcdN.setMinimumSize(QSize(75, 75))
        self.MM_lcdN.setMaximumSize(QSize(75, 75))
        self.MM_lcdN.setFrameShape(QFrame.Shape.Panel)
        self.MM_lcdN.setFrameShadow(QFrame.Shadow.Raised)
        self.MM_lcdN.setSmallDecimalPoint(False)
        self.MM_lcdN.setDigitCount(2)
        self.MM_lcdN.setMode(QLCDNumber.Mode.Dec)
        self.MM_lcdN.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)

        self.MM.addWidget(self.MM_lcdN)


        self.horizontalLayout_10.addLayout(self.MM)


        self.verticalLayout_3.addWidget(self.Time_gBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.settings_toolB_3 = QToolButton(self.time_gBox)
        self.settings_toolB_3.setObjectName(u"settings_toolB_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.settings_toolB_3.sizePolicy().hasHeightForWidth())
        self.settings_toolB_3.setSizePolicy(sizePolicy1)
        self.settings_toolB_3.setMinimumSize(QSize(170, 35))
        self.settings_toolB_3.setMaximumSize(QSize(170, 35))

        self.verticalLayout_3.addWidget(self.settings_toolB_3, 0, Qt.AlignmentFlag.AlignHCenter)

        self.settings_toolB_1 = QToolButton(self.time_gBox)
        self.settings_toolB_1.setObjectName(u"settings_toolB_1")
        sizePolicy1.setHeightForWidth(self.settings_toolB_1.sizePolicy().hasHeightForWidth())
        self.settings_toolB_1.setSizePolicy(sizePolicy1)
        self.settings_toolB_1.setMinimumSize(QSize(170, 35))
        self.settings_toolB_1.setMaximumSize(QSize(170, 35))

        self.verticalLayout_3.addWidget(self.settings_toolB_1, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout.addWidget(self.time_gBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.stat_sett_gBox = QGroupBox(self.left_frame)
        self.stat_sett_gBox.setObjectName(u"stat_sett_gBox")
        self.stat_sett_gBox.setMinimumSize(QSize(190, 190))
        self.stat_sett_gBox.setMaximumSize(QSize(190, 190))
        self.stat_sett_gBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stat_sett_gBox.setFlat(False)
        self.stat_sett_gBox.setCheckable(False)
        self.gridLayout = QGridLayout(self.stat_sett_gBox)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.network_stat_line = QLineEdit(self.stat_sett_gBox)
        self.network_stat_line.setObjectName(u"network_stat_line")
        sizePolicy1.setHeightForWidth(self.network_stat_line.sizePolicy().hasHeightForWidth())
        self.network_stat_line.setSizePolicy(sizePolicy1)
        self.network_stat_line.setMinimumSize(QSize(170, 35))
        self.network_stat_line.setMaximumSize(QSize(170, 35))
        self.network_stat_line.setFrame(True)
        self.network_stat_line.setReadOnly(True)

        self.gridLayout.addWidget(self.network_stat_line, 1, 0, 1, 1)

        self.settings_toolB = QToolButton(self.stat_sett_gBox)
        self.settings_toolB.setObjectName(u"settings_toolB")
        sizePolicy1.setHeightForWidth(self.settings_toolB.sizePolicy().hasHeightForWidth())
        self.settings_toolB.setSizePolicy(sizePolicy1)
        self.settings_toolB.setMinimumSize(QSize(170, 35))
        self.settings_toolB.setMaximumSize(QSize(170, 35))

        self.gridLayout.addWidget(self.settings_toolB, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.stat_sett_gBox, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout.addWidget(self.left_frame)

        self.right_frame = QFrame(self.Main_widget)
        self.right_frame.setObjectName(u"right_frame")
        sizePolicy.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        self.right_frame.setSizePolicy(sizePolicy)
        self.right_frame.setMinimumSize(QSize(800, 580))
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.right_frame)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.toolB_null_5 = QToolButton(self.right_frame)
        self.toolB_null_5.setObjectName(u"toolB_null_5")

        self.verticalLayout_2.addWidget(self.toolB_null_5)

        self.toolB_null_6 = QToolButton(self.right_frame)
        self.toolB_null_6.setObjectName(u"toolB_null_6")

        self.verticalLayout_2.addWidget(self.toolB_null_6)

        self.toolB_null_7 = QToolButton(self.right_frame)
        self.toolB_null_7.setObjectName(u"toolB_null_7")

        self.verticalLayout_2.addWidget(self.toolB_null_7)

        self.toolB_null_8 = QToolButton(self.right_frame)
        self.toolB_null_8.setObjectName(u"toolB_null_8")

        self.verticalLayout_2.addWidget(self.toolB_null_8)

        self.toolB_null_4 = QToolButton(self.right_frame)
        self.toolB_null_4.setObjectName(u"toolB_null_4")

        self.verticalLayout_2.addWidget(self.toolB_null_4)

        self.toolB_null_3 = QToolButton(self.right_frame)
        self.toolB_null_3.setObjectName(u"toolB_null_3")

        self.verticalLayout_2.addWidget(self.toolB_null_3)

        self.toolB_null_2 = QToolButton(self.right_frame)
        self.toolB_null_2.setObjectName(u"toolB_null_2")

        self.verticalLayout_2.addWidget(self.toolB_null_2)

        self.toolB_null_1 = QToolButton(self.right_frame)
        self.toolB_null_1.setObjectName(u"toolB_null_1")

        self.verticalLayout_2.addWidget(self.toolB_null_1)


        self.horizontalLayout.addWidget(self.right_frame)

        El_GUI_CLIENTO.setCentralWidget(self.centralwidget)

        self.retranslateUi(El_GUI_CLIENTO)

        QMetaObject.connectSlotsByName(El_GUI_CLIENTO)
    # setupUi

    def retranslateUi(self, El_GUI_CLIENTO):
        El_GUI_CLIENTO.setWindowTitle(QCoreApplication.translate("El_GUI_CLIENTO", u"el_gui_cliento v.0.0.1", None))
        self.time_gBox.setTitle(QCoreApplication.translate("El_GUI_CLIENTO", u"el_gui_cliento", None))
        self.Time_gBox.setTitle("")
        self.settings_toolB_3.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"Settings", None))
        self.settings_toolB_1.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"Settings", None))
        self.stat_sett_gBox.setTitle(QCoreApplication.translate("El_GUI_CLIENTO", u"Status", None))
        self.settings_toolB.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"Settings", None))
        self.toolB_null_5.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
        self.toolB_null_6.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
        self.toolB_null_7.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
        self.toolB_null_8.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
        self.toolB_null_4.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
        self.toolB_null_3.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
        self.toolB_null_2.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
        self.toolB_null_1.setText(QCoreApplication.translate("El_GUI_CLIENTO", u"...", None))
    # retranslateUi

