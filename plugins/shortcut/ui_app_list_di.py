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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QListWidget, QListWidgetItem, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

class Ui_app_list_qW(object):
    def setupUi(self, app_list_qW):
        if not app_list_qW.objectName():
            app_list_qW.setObjectName(u"app_list_qW")
        app_list_qW.resize(350, 650)
        app_list_qW.setMinimumSize(QSize(350, 650))
        app_list_qW.setMaximumSize(QSize(350, 650))
        app_list_qW.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame = QFrame(app_list_qW)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setGeometry(QRect(5, 5, 340, 640))
        self.main_frame.setMinimumSize(QSize(340, 640))
        self.main_frame.setMaximumSize(QSize(340, 640))
        self.main_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self._2 = QHBoxLayout(self.main_frame)
        self._2.setObjectName(u"_2")
        self._2.setContentsMargins(5, 5, 5, 5)
        self.app_list_groupB = QGroupBox(self.main_frame)
        self.app_list_groupB.setObjectName(u"app_list_groupB")
        self.app_list_groupB.setMinimumSize(QSize(330, 630))
        self.app_list_groupB.setMaximumSize(QSize(330, 630))
        self.app_list_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.app_list_groupB)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.app_listW = QListWidget(self.app_list_groupB)
        self.app_listW.setObjectName(u"app_listW")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.app_listW.sizePolicy().hasHeightForWidth())
        self.app_listW.setSizePolicy(sizePolicy)
        self.app_listW.setMaximumSize(QSize(320, 610))
        self.app_listW.setIconSize(QSize(64, 64))

        self.horizontalLayout.addWidget(self.app_listW)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.select_toolB = QToolButton(self.app_list_groupB)
        self.select_toolB.setObjectName(u"select_toolB")
        sizePolicy.setHeightForWidth(self.select_toolB.sizePolicy().hasHeightForWidth())
        self.select_toolB.setSizePolicy(sizePolicy)
        self.select_toolB.setMinimumSize(QSize(0, 30))
        self.select_toolB.setMaximumSize(QSize(140, 30))

        self.button_layout.addWidget(self.select_toolB)

        self.cancel_toolB = QToolButton(self.app_list_groupB)
        self.cancel_toolB.setObjectName(u"cancel_toolB")
        sizePolicy.setHeightForWidth(self.cancel_toolB.sizePolicy().hasHeightForWidth())
        self.cancel_toolB.setSizePolicy(sizePolicy)
        self.cancel_toolB.setMinimumSize(QSize(0, 30))
        self.cancel_toolB.setMaximumSize(QSize(140, 30))

        self.button_layout.addWidget(self.cancel_toolB)


        self.verticalLayout_3.addLayout(self.button_layout)

        self.verticalLayout_3.setStretch(0, 9)
        self.verticalLayout_3.setStretch(1, 1)

        self._2.addWidget(self.app_list_groupB, 0, Qt.AlignmentFlag.AlignHCenter)


        self.retranslateUi(app_list_qW)

        QMetaObject.connectSlotsByName(app_list_qW)
    # setupUi

    def retranslateUi(self, app_list_qW):
        app_list_qW.setWindowTitle(QCoreApplication.translate("app_list_qW", u"Select app", None))
        self.app_list_groupB.setTitle(QCoreApplication.translate("app_list_qW", u"App List", None))
        self.select_toolB.setText(QCoreApplication.translate("app_list_qW", u"Select", None))
        self.cancel_toolB.setText(QCoreApplication.translate("app_list_qW", u"\u0421ancel", None))
    # retranslateUi

