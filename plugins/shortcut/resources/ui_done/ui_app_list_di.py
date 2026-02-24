# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_list_di.ui'
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
    QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_app_list_qW(object):
    def setupUi(self, app_list_qW):
        if not app_list_qW.objectName():
            app_list_qW.setObjectName(u"app_list_qW")
        app_list_qW.resize(350, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(app_list_qW.sizePolicy().hasHeightForWidth())
        app_list_qW.setSizePolicy(sizePolicy)
        app_list_qW.setMinimumSize(QSize(350, 600))
        app_list_qW.setMaximumSize(QSize(350, 600))
        app_list_qW.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.gridLayout = QGridLayout(app_list_qW)
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_frame = QFrame(app_list_qW)
        self.main_frame.setObjectName(u"main_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main_frame.sizePolicy().hasHeightForWidth())
        self.main_frame.setSizePolicy(sizePolicy1)
        self.main_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_2 = QGridLayout(self.main_frame)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.app_list_groupB = QGroupBox(self.main_frame)
        self.app_list_groupB.setObjectName(u"app_list_groupB")
        sizePolicy1.setHeightForWidth(self.app_list_groupB.sizePolicy().hasHeightForWidth())
        self.app_list_groupB.setSizePolicy(sizePolicy1)
        self.app_list_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.app_list_groupB)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.search_layout = QHBoxLayout()
        self.search_layout.setSpacing(5)
        self.search_layout.setObjectName(u"search_layout")
        self.search_layout.setContentsMargins(5, 5, 5, 5)
        self.search_lineE = QLineEdit(self.app_list_groupB)
        self.search_lineE.setObjectName(u"search_lineE")
        sizePolicy1.setHeightForWidth(self.search_lineE.sizePolicy().hasHeightForWidth())
        self.search_lineE.setSizePolicy(sizePolicy1)

        self.search_layout.addWidget(self.search_lineE)

        self.search_toolB = QToolButton(self.app_list_groupB)
        self.search_toolB.setObjectName(u"search_toolB")
        sizePolicy1.setHeightForWidth(self.search_toolB.sizePolicy().hasHeightForWidth())
        self.search_toolB.setSizePolicy(sizePolicy1)
        self.search_toolB.setIconSize(QSize(64, 64))

        self.search_layout.addWidget(self.search_toolB)

        self.search_layout.setStretch(0, 8)
        self.search_layout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.search_layout)

        self.list_layout = QHBoxLayout()
        self.list_layout.setSpacing(5)
        self.list_layout.setObjectName(u"list_layout")
        self.list_layout.setContentsMargins(5, 5, 5, 5)
        self.app_listW = QListWidget(self.app_list_groupB)
        self.app_listW.setObjectName(u"app_listW")
        sizePolicy1.setHeightForWidth(self.app_listW.sizePolicy().hasHeightForWidth())
        self.app_listW.setSizePolicy(sizePolicy1)
        self.app_listW.setIconSize(QSize(64, 64))

        self.list_layout.addWidget(self.app_listW)


        self.verticalLayout.addLayout(self.list_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.select_toolB = QToolButton(self.app_list_groupB)
        self.select_toolB.setObjectName(u"select_toolB")
        sizePolicy1.setHeightForWidth(self.select_toolB.sizePolicy().hasHeightForWidth())
        self.select_toolB.setSizePolicy(sizePolicy1)

        self.button_layout.addWidget(self.select_toolB)

        self.cancel_toolB = QToolButton(self.app_list_groupB)
        self.cancel_toolB.setObjectName(u"cancel_toolB")
        sizePolicy1.setHeightForWidth(self.cancel_toolB.sizePolicy().hasHeightForWidth())
        self.cancel_toolB.setSizePolicy(sizePolicy1)

        self.button_layout.addWidget(self.cancel_toolB)


        self.verticalLayout.addLayout(self.button_layout)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 12)
        self.verticalLayout.setStretch(2, 1)

        self.gridLayout_2.addWidget(self.app_list_groupB, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.main_frame, 0, 0, 1, 1)


        self.retranslateUi(app_list_qW)

        QMetaObject.connectSlotsByName(app_list_qW)
    # setupUi

    def retranslateUi(self, app_list_qW):
        app_list_qW.setWindowTitle(QCoreApplication.translate("app_list_qW", u"Select app", None))
        self.app_list_groupB.setTitle(QCoreApplication.translate("app_list_qW", u"App List", None))
        self.search_lineE.setInputMask("")
        self.search_lineE.setPlaceholderText(QCoreApplication.translate("app_list_qW", u"Search", None))
        self.search_toolB.setText(QCoreApplication.translate("app_list_qW", u"...", None))
        self.select_toolB.setText(QCoreApplication.translate("app_list_qW", u"Select", None))
        self.cancel_toolB.setText(QCoreApplication.translate("app_list_qW", u"\u0421ancel", None))
    # retranslateUi

