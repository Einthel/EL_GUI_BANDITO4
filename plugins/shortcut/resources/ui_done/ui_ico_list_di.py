# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ico_list_di.ui'
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
    QHBoxLayout, QListView, QListWidget, QListWidgetItem,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_ico_list_qW(object):
    def setupUi(self, ico_list_qW):
        if not ico_list_qW.objectName():
            ico_list_qW.setObjectName(u"ico_list_qW")
        ico_list_qW.resize(400, 500)
        ico_list_qW.setMinimumSize(QSize(400, 500))
        ico_list_qW.setMaximumSize(QSize(400, 500))
        ico_list_qW.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.gridLayout_2 = QGridLayout(ico_list_qW)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(5)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.main_frame = QFrame(ico_list_qW)
        self.main_frame.setObjectName(u"main_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_frame.sizePolicy().hasHeightForWidth())
        self.main_frame.setSizePolicy(sizePolicy)
        self.main_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout = QGridLayout(self.main_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ico_list_groupB = QGroupBox(self.main_frame)
        self.ico_list_groupB.setObjectName(u"ico_list_groupB")
        sizePolicy.setHeightForWidth(self.ico_list_groupB.sizePolicy().hasHeightForWidth())
        self.ico_list_groupB.setSizePolicy(sizePolicy)
        self.ico_list_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.ico_list_groupB)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.ico_listW = QListWidget(self.ico_list_groupB)
        self.ico_listW.setObjectName(u"ico_listW")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ico_listW.sizePolicy().hasHeightForWidth())
        self.ico_listW.setSizePolicy(sizePolicy1)
        self.ico_listW.setIconSize(QSize(48, 48))
        self.ico_listW.setMovement(QListView.Movement.Static)
        self.ico_listW.setFlow(QListView.Flow.TopToBottom)
        self.ico_listW.setResizeMode(QListView.ResizeMode.Adjust)
        self.ico_listW.setSpacing(10)
        self.ico_listW.setGridSize(QSize(65, 85))
        self.ico_listW.setViewMode(QListView.ViewMode.IconMode)
        self.ico_listW.setModelColumn(0)

        self.horizontalLayout.addWidget(self.ico_listW)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.select_toolB = QToolButton(self.ico_list_groupB)
        self.select_toolB.setObjectName(u"select_toolB")
        sizePolicy1.setHeightForWidth(self.select_toolB.sizePolicy().hasHeightForWidth())
        self.select_toolB.setSizePolicy(sizePolicy1)

        self.button_layout.addWidget(self.select_toolB)

        self.cancel_toolB = QToolButton(self.ico_list_groupB)
        self.cancel_toolB.setObjectName(u"cancel_toolB")
        sizePolicy1.setHeightForWidth(self.cancel_toolB.sizePolicy().hasHeightForWidth())
        self.cancel_toolB.setSizePolicy(sizePolicy1)

        self.button_layout.addWidget(self.cancel_toolB)


        self.verticalLayout_3.addLayout(self.button_layout)

        self.verticalLayout_3.setStretch(0, 9)
        self.verticalLayout_3.setStretch(1, 1)

        self.gridLayout.addWidget(self.ico_list_groupB, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.main_frame, 0, 0, 1, 1)


        self.retranslateUi(ico_list_qW)

        self.ico_listW.setCurrentRow(-1)


        QMetaObject.connectSlotsByName(ico_list_qW)
    # setupUi

    def retranslateUi(self, ico_list_qW):
        ico_list_qW.setWindowTitle(QCoreApplication.translate("ico_list_qW", u"Select ico", None))
        self.ico_list_groupB.setTitle(QCoreApplication.translate("ico_list_qW", u"Ico List", None))
        self.select_toolB.setText(QCoreApplication.translate("ico_list_qW", u"Select", None))
        self.cancel_toolB.setText(QCoreApplication.translate("ico_list_qW", u"\u0421ancel", None))
    # retranslateUi

