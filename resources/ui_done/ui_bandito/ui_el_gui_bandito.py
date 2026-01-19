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
    QLineEdit, QMainWindow, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

class Ui_El_GUI_BANDITO(object):
    def setupUi(self, El_GUI_BANDITO):
        if not El_GUI_BANDITO.objectName():
            El_GUI_BANDITO.setObjectName(u"El_GUI_BANDITO")
        El_GUI_BANDITO.resize(1280, 720)
        self.centralwidget = QWidget(El_GUI_BANDITO)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Main_widget = QWidget(self.centralwidget)
        self.Main_widget.setObjectName(u"Main_widget")
        self.Main_widget.setGeometry(QRect(0, 0, 1280, 720))
        self.left_frame = QFrame(self.Main_widget)
        self.left_frame.setObjectName(u"left_frame")
        self.left_frame.setGeometry(QRect(5, 10, 210, 700))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(sizePolicy)
        self.left_frame.setMinimumSize(QSize(210, 700))
        self.left_frame.setMaximumSize(QSize(210, 700))
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.left_frame)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.null_gBox = QGroupBox(self.left_frame)
        self.null_gBox.setObjectName(u"null_gBox")
        self.null_gBox.setMinimumSize(QSize(190, 0))
        self.null_gBox.setMaximumSize(QSize(190, 16777215))
        self.null_gBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.null_gBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.null_toolB_4 = QToolButton(self.null_gBox)
        self.null_toolB_4.setObjectName(u"null_toolB_4")
        self.null_toolB_4.setMaximumSize(QSize(170, 30))

        self.verticalLayout_3.addWidget(self.null_toolB_4)

        self.null_toolB_3 = QToolButton(self.null_gBox)
        self.null_toolB_3.setObjectName(u"null_toolB_3")
        self.null_toolB_3.setMaximumSize(QSize(170, 30))

        self.verticalLayout_3.addWidget(self.null_toolB_3)

        self.setting_toolB = QToolButton(self.null_gBox)
        self.setting_toolB.setObjectName(u"setting_toolB")
        self.setting_toolB.setMaximumSize(QSize(170, 30))

        self.verticalLayout_3.addWidget(self.setting_toolB)

        self.line_status_2 = QLineEdit(self.null_gBox)
        self.line_status_2.setObjectName(u"line_status_2")
        self.line_status_2.setMaximumSize(QSize(170, 30))

        self.verticalLayout_3.addWidget(self.line_status_2)


        self.verticalLayout.addWidget(self.null_gBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.settings_gBox = QGroupBox(self.left_frame)
        self.settings_gBox.setObjectName(u"settings_gBox")
        self.settings_gBox.setMinimumSize(QSize(190, 200))
        self.settings_gBox.setMaximumSize(QSize(190, 200))
        self.settings_gBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.settings_gBox.setFlat(False)
        self.settings_gBox.setCheckable(False)
        self.gridLayout = QGridLayout(self.settings_gBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.null_toolB_1 = QToolButton(self.settings_gBox)
        self.null_toolB_1.setObjectName(u"null_toolB_1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.null_toolB_1.sizePolicy().hasHeightForWidth())
        self.null_toolB_1.setSizePolicy(sizePolicy1)
        self.null_toolB_1.setMinimumSize(QSize(170, 35))
        self.null_toolB_1.setMaximumSize(QSize(170, 35))

        self.gridLayout.addWidget(self.null_toolB_1, 0, 0, 1, 1)

        self.null_toolB_2 = QToolButton(self.settings_gBox)
        self.null_toolB_2.setObjectName(u"null_toolB_2")
        sizePolicy1.setHeightForWidth(self.null_toolB_2.sizePolicy().hasHeightForWidth())
        self.null_toolB_2.setSizePolicy(sizePolicy1)
        self.null_toolB_2.setMinimumSize(QSize(170, 35))
        self.null_toolB_2.setMaximumSize(QSize(170, 35))

        self.gridLayout.addWidget(self.null_toolB_2, 1, 0, 1, 1)

        self.settings_toolB = QToolButton(self.settings_gBox)
        self.settings_toolB.setObjectName(u"settings_toolB")
        sizePolicy1.setHeightForWidth(self.settings_toolB.sizePolicy().hasHeightForWidth())
        self.settings_toolB.setSizePolicy(sizePolicy1)
        self.settings_toolB.setMinimumSize(QSize(170, 35))
        self.settings_toolB.setMaximumSize(QSize(170, 35))

        self.gridLayout.addWidget(self.settings_toolB, 2, 0, 1, 1)

        self.network_stat_line = QLineEdit(self.settings_gBox)
        self.network_stat_line.setObjectName(u"network_stat_line")
        sizePolicy1.setHeightForWidth(self.network_stat_line.sizePolicy().hasHeightForWidth())
        self.network_stat_line.setSizePolicy(sizePolicy1)
        self.network_stat_line.setMinimumSize(QSize(170, 35))
        self.network_stat_line.setMaximumSize(QSize(170, 35))
        self.network_stat_line.setFrame(True)
        self.network_stat_line.setReadOnly(True)

        self.gridLayout.addWidget(self.network_stat_line, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.settings_gBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.right_frame = QFrame(self.Main_widget)
        self.right_frame.setObjectName(u"right_frame")
        self.right_frame.setGeometry(QRect(224, 10, 1040, 700))
        sizePolicy.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        self.right_frame.setSizePolicy(sizePolicy)
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.toolButton_8 = QToolButton(self.right_frame)
        self.toolButton_8.setObjectName(u"toolButton_8")
        self.toolButton_8.setGeometry(QRect(6, 303, 21, 22))
        self.toolButton_5 = QToolButton(self.right_frame)
        self.toolButton_5.setObjectName(u"toolButton_5")
        self.toolButton_5.setGeometry(QRect(6, 60, 21, 22))
        self.toolButton_7 = QToolButton(self.right_frame)
        self.toolButton_7.setObjectName(u"toolButton_7")
        self.toolButton_7.setGeometry(QRect(6, 222, 21, 22))
        self.toolButton_6 = QToolButton(self.right_frame)
        self.toolButton_6.setObjectName(u"toolButton_6")
        self.toolButton_6.setGeometry(QRect(6, 141, 21, 22))
        self.toolButton = QToolButton(self.right_frame)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(6, 627, 21, 22))
        self.toolButton_2 = QToolButton(self.right_frame)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setGeometry(QRect(6, 546, 21, 22))
        self.toolButton_3 = QToolButton(self.right_frame)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setGeometry(QRect(6, 465, 21, 22))
        self.toolButton_4 = QToolButton(self.right_frame)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setGeometry(QRect(6, 384, 21, 22))
        El_GUI_BANDITO.setCentralWidget(self.centralwidget)

        self.retranslateUi(El_GUI_BANDITO)

        QMetaObject.connectSlotsByName(El_GUI_BANDITO)
    # setupUi

    def retranslateUi(self, El_GUI_BANDITO):
        El_GUI_BANDITO.setWindowTitle(QCoreApplication.translate("El_GUI_BANDITO", u"el_gui_bandito v.0.0.1", None))
        self.null_gBox.setTitle(QCoreApplication.translate("El_GUI_BANDITO", u"el_gui_comrado", None))
        self.null_toolB_4.setText(QCoreApplication.translate("El_GUI_BANDITO", u"Settings", None))
        self.null_toolB_3.setText(QCoreApplication.translate("El_GUI_BANDITO", u"null_button", None))
        self.setting_toolB.setText(QCoreApplication.translate("El_GUI_BANDITO", u"Settings", None))
        self.settings_gBox.setTitle(QCoreApplication.translate("El_GUI_BANDITO", u"Status", None))
        self.null_toolB_1.setText(QCoreApplication.translate("El_GUI_BANDITO", u"null_button", None))
        self.null_toolB_2.setText(QCoreApplication.translate("El_GUI_BANDITO", u"null_button", None))
        self.settings_toolB.setText(QCoreApplication.translate("El_GUI_BANDITO", u"Settings", None))
        self.toolButton_8.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
        self.toolButton_5.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
        self.toolButton_7.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
        self.toolButton_6.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
        self.toolButton.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
        self.toolButton_2.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
        self.toolButton_3.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
        self.toolButton_4.setText(QCoreApplication.translate("El_GUI_BANDITO", u"...", None))
    # retranslateUi

