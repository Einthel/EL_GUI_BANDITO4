# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'save_prefab_di.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

class Ui_save_prefab_di(object):
    def setupUi(self, save_prefab_di):
        if not save_prefab_di.objectName():
            save_prefab_di.setObjectName(u"save_prefab_di")
        save_prefab_di.resize(275, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(save_prefab_di.sizePolicy().hasHeightForWidth())
        save_prefab_di.setSizePolicy(sizePolicy)
        save_prefab_di.setMinimumSize(QSize(275, 150))
        save_prefab_di.setMaximumSize(QSize(275, 150))
        self.dialog_layout = QVBoxLayout(save_prefab_di)
        self.dialog_layout.setSpacing(5)
        self.dialog_layout.setObjectName(u"dialog_layout")
        self.dialog_layout.setContentsMargins(5, 5, 5, 5)
        self.save_groupB = QGroupBox(save_prefab_di)
        self.save_groupB.setObjectName(u"save_groupB")
        self.save_groupB.setMinimumSize(QSize(260, 125))
        self.save_groupB.setMaximumSize(QSize(270, 125))
        self.save_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.save_groupB)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.name_layout = QVBoxLayout()
        self.name_layout.setSpacing(5)
        self.name_layout.setObjectName(u"name_layout")
        self.name_layout.setContentsMargins(5, 5, 5, 5)
        self.enter_name_lable = QLabel(self.save_groupB)
        self.enter_name_lable.setObjectName(u"enter_name_lable")
        self.enter_name_lable.setMinimumSize(QSize(200, 30))
        font = QFont()
        font.setPointSize(12)
        self.enter_name_lable.setFont(font)
        self.enter_name_lable.setLineWidth(2)
        self.enter_name_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_layout.addWidget(self.enter_name_lable, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.namePrefab_lineE = QLineEdit(self.save_groupB)
        self.namePrefab_lineE.setObjectName(u"namePrefab_lineE")
        sizePolicy.setHeightForWidth(self.namePrefab_lineE.sizePolicy().hasHeightForWidth())
        self.namePrefab_lineE.setSizePolicy(sizePolicy)
        self.namePrefab_lineE.setMinimumSize(QSize(220, 30))
        self.namePrefab_lineE.setMaximumSize(QSize(220, 16777215))

        self.name_layout.addWidget(self.namePrefab_lineE, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout.addLayout(self.name_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.button_layout.setObjectName(u"button_layout")
        self.save_toolB = QToolButton(self.save_groupB)
        self.save_toolB.setObjectName(u"save_toolB")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.save_toolB.sizePolicy().hasHeightForWidth())
        self.save_toolB.setSizePolicy(sizePolicy1)
        self.save_toolB.setMinimumSize(QSize(80, 30))
        self.save_toolB.setMaximumSize(QSize(100, 30))

        self.button_layout.addWidget(self.save_toolB)

        self.cancle_toolB = QToolButton(self.save_groupB)
        self.cancle_toolB.setObjectName(u"cancle_toolB")
        sizePolicy1.setHeightForWidth(self.cancle_toolB.sizePolicy().hasHeightForWidth())
        self.cancle_toolB.setSizePolicy(sizePolicy1)
        self.cancle_toolB.setMinimumSize(QSize(80, 30))
        self.cancle_toolB.setMaximumSize(QSize(100, 30))

        self.button_layout.addWidget(self.cancle_toolB)


        self.verticalLayout.addLayout(self.button_layout)


        self.dialog_layout.addWidget(self.save_groupB, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.retranslateUi(save_prefab_di)

        QMetaObject.connectSlotsByName(save_prefab_di)
    # setupUi

    def retranslateUi(self, save_prefab_di):
        save_prefab_di.setWindowTitle(QCoreApplication.translate("save_prefab_di", u"message", None))
        self.save_groupB.setTitle("")
        self.enter_name_lable.setText(QCoreApplication.translate("save_prefab_di", u"enter_name_text", None))
        self.save_toolB.setText(QCoreApplication.translate("save_prefab_di", u"Save", None))
        self.cancle_toolB.setText(QCoreApplication.translate("save_prefab_di", u"Cancle", None))
    # retranslateUi

