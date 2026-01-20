# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_manager.ui'
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
    QLineEdit, QListWidget, QListWidgetItem, QProgressBar,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_plugin_manager_qW(object):
    def setupUi(self, plugin_manager_qW):
        if not plugin_manager_qW.objectName():
            plugin_manager_qW.setObjectName(u"plugin_manager_qW")
        plugin_manager_qW.resize(470, 450)
        plugin_manager_qW.setMinimumSize(QSize(470, 450))
        plugin_manager_qW.setMaximumSize(QSize(470, 450))
        plugin_manager_qW.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame = QFrame(plugin_manager_qW)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setGeometry(QRect(0, 0, 470, 450))
        self.main_frame.setMinimumSize(QSize(470, 450))
        self.main_frame.setMaximumSize(QSize(470, 450))
        self.main_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.main_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(self.main_frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.plugin_listW = QListWidget(self.groupBox)
        self.plugin_listW.setObjectName(u"plugin_listW")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plugin_listW.sizePolicy().hasHeightForWidth())
        self.plugin_listW.setSizePolicy(sizePolicy)
        self.plugin_listW.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.plugin_listW)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(200, 0))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.browser_toolB = QToolButton(self.groupBox)
        self.browser_toolB.setObjectName(u"browser_toolB")
        sizePolicy.setHeightForWidth(self.browser_toolB.sizePolicy().hasHeightForWidth())
        self.browser_toolB.setSizePolicy(sizePolicy)
        self.browser_toolB.setMinimumSize(QSize(0, 30))
        self.browser_toolB.setMaximumSize(QSize(16777215, 30))

        self.button_layout.addWidget(self.browser_toolB)

        self.upload_plug_toolB = QToolButton(self.groupBox)
        self.upload_plug_toolB.setObjectName(u"upload_plug_toolB")
        sizePolicy.setHeightForWidth(self.upload_plug_toolB.sizePolicy().hasHeightForWidth())
        self.upload_plug_toolB.setSizePolicy(sizePolicy)
        self.upload_plug_toolB.setMinimumSize(QSize(0, 30))
        self.upload_plug_toolB.setMaximumSize(QSize(16777215, 30))

        self.button_layout.addWidget(self.upload_plug_toolB)

        self.delete_plug_toolB = QToolButton(self.groupBox)
        self.delete_plug_toolB.setObjectName(u"delete_plug_toolB")
        sizePolicy.setHeightForWidth(self.delete_plug_toolB.sizePolicy().hasHeightForWidth())
        self.delete_plug_toolB.setSizePolicy(sizePolicy)
        self.delete_plug_toolB.setMinimumSize(QSize(0, 30))
        self.delete_plug_toolB.setMaximumSize(QSize(16777215, 30))

        self.button_layout.addWidget(self.delete_plug_toolB)

        self.delete_plug_toolB_2 = QToolButton(self.groupBox)
        self.delete_plug_toolB_2.setObjectName(u"delete_plug_toolB_2")
        sizePolicy.setHeightForWidth(self.delete_plug_toolB_2.sizePolicy().hasHeightForWidth())
        self.delete_plug_toolB_2.setSizePolicy(sizePolicy)
        self.delete_plug_toolB_2.setMinimumSize(QSize(0, 30))
        self.delete_plug_toolB_2.setMaximumSize(QSize(16777215, 30))

        self.button_layout.addWidget(self.delete_plug_toolB_2)


        self.verticalLayout_3.addLayout(self.button_layout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.progressBar = QProgressBar(self.groupBox)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"/* QProgressBar {\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 5px;\n"
"    background-color: #1a1a1a;\n"
"    text-align: center;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"        stop:0 #00f2fe, stop:1 #4facfe); \n"
"    width: 20px;\n"
"    margin: 1px;\n"
"}\n"
"*/")
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.path_lineE = QLineEdit(self.groupBox)
        self.path_lineE.setObjectName(u"path_lineE")
        sizePolicy.setHeightForWidth(self.path_lineE.sizePolicy().hasHeightForWidth())
        self.path_lineE.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.path_lineE)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_3.setStretch(0, 8)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 2)

        self.horizontalLayout_2.addWidget(self.groupBox)


        self.retranslateUi(plugin_manager_qW)

        QMetaObject.connectSlotsByName(plugin_manager_qW)
    # setupUi

    def retranslateUi(self, plugin_manager_qW):
        plugin_manager_qW.setWindowTitle(QCoreApplication.translate("plugin_manager_qW", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("plugin_manager_qW", u"Manager Plugins", None))
        self.browser_toolB.setText(QCoreApplication.translate("plugin_manager_qW", u"Browse", None))
        self.upload_plug_toolB.setText(QCoreApplication.translate("plugin_manager_qW", u"Upload", None))
        self.delete_plug_toolB.setText(QCoreApplication.translate("plugin_manager_qW", u"Delete", None))
        self.delete_plug_toolB_2.setText(QCoreApplication.translate("plugin_manager_qW", u"Delete", None))
    # retranslateUi

