# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_list.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QListWidget, QListWidgetItem, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

class Ui_plugin_list_qW(object):
    def setupUi(self, plugin_list_qW):
        if not plugin_list_qW.objectName():
            plugin_list_qW.setObjectName(u"plugin_list_qW")
        plugin_list_qW.resize(270, 250)
        plugin_list_qW.setMinimumSize(QSize(0, 0))
        plugin_list_qW.setMaximumSize(QSize(270, 450))
        plugin_list_qW.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame = QFrame(plugin_list_qW)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setGeometry(QRect(0, 0, 270, 251))
        self.main_frame.setMinimumSize(QSize(0, 0))
        self.main_frame.setMaximumSize(QSize(270, 16777215))
        self.main_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.main_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.plugin_list_groupB = QGroupBox(self.main_frame)
        self.plugin_list_groupB.setObjectName(u"plugin_list_groupB")
        self.plugin_list_groupB.setMaximumSize(QSize(270, 16777215))
        self.plugin_list_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.plugin_list_groupB)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.plugin_listW = QListWidget(self.plugin_list_groupB)
        self.plugin_listW.setObjectName(u"plugin_listW")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plugin_listW.sizePolicy().hasHeightForWidth())
        self.plugin_listW.setSizePolicy(sizePolicy)
        self.plugin_listW.setMinimumSize(QSize(170, 0))
        self.plugin_listW.setMaximumSize(QSize(240, 220))
        self.plugin_listW.setIconSize(QSize(64, 64))

        self.horizontalLayout.addWidget(self.plugin_listW)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.select_toolB = QToolButton(self.plugin_list_groupB)
        self.select_toolB.setObjectName(u"select_toolB")
        sizePolicy.setHeightForWidth(self.select_toolB.sizePolicy().hasHeightForWidth())
        self.select_toolB.setSizePolicy(sizePolicy)
        self.select_toolB.setMinimumSize(QSize(0, 30))
        self.select_toolB.setMaximumSize(QSize(140, 30))

        self.button_layout.addWidget(self.select_toolB)

        self.cancel_toolB = QToolButton(self.plugin_list_groupB)
        self.cancel_toolB.setObjectName(u"cancel_toolB")
        sizePolicy.setHeightForWidth(self.cancel_toolB.sizePolicy().hasHeightForWidth())
        self.cancel_toolB.setSizePolicy(sizePolicy)
        self.cancel_toolB.setMinimumSize(QSize(0, 30))
        self.cancel_toolB.setMaximumSize(QSize(140, 30))

        self.button_layout.addWidget(self.cancel_toolB)


        self.verticalLayout_3.addLayout(self.button_layout)


        self.horizontalLayout_2.addWidget(self.plugin_list_groupB, 0, Qt.AlignmentFlag.AlignHCenter)


        self.retranslateUi(plugin_list_qW)

        QMetaObject.connectSlotsByName(plugin_list_qW)
    # setupUi

    def retranslateUi(self, plugin_list_qW):
        plugin_list_qW.setWindowTitle(QCoreApplication.translate("plugin_list_qW", u"Add plugin...", None))
        self.plugin_list_groupB.setTitle(QCoreApplication.translate("plugin_list_qW", u"Plugin list", None))
        self.select_toolB.setText(QCoreApplication.translate("plugin_list_qW", u"Select", None))
        self.cancel_toolB.setText(QCoreApplication.translate("plugin_list_qW", u"\u0421ancel", None))
    # retranslateUi

