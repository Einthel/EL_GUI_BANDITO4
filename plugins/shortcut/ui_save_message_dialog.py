# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'save_message_dialog.ui'
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
    QLabel, QSizePolicy, QToolButton, QVBoxLayout,
    QWidget)

class Ui_save_message_dialog(object):
    def setupUi(self, save_message_dialog):
        if not save_message_dialog.objectName():
            save_message_dialog.setObjectName(u"save_message_dialog")
        save_message_dialog.resize(270, 140)
        save_message_dialog.setModal(False)
        self.dialog_layout = QVBoxLayout(save_message_dialog)
        self.dialog_layout.setSpacing(5)
        self.dialog_layout.setObjectName(u"dialog_layout")
        self.dialog_layout.setContentsMargins(5, 5, 5, 5)
        self.save_groupB = QGroupBox(save_message_dialog)
        self.save_groupB.setObjectName(u"save_groupB")
        self.save_groupB.setFlat(False)
        self.verticalLayout = QVBoxLayout(self.save_groupB)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.questions_lable = QLabel(self.save_groupB)
        self.questions_lable.setObjectName(u"questions_lable")
        font = QFont()
        font.setPointSize(12)
        self.questions_lable.setFont(font)
        self.questions_lable.setLineWidth(2)
        self.questions_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.questions_lable)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.button_layout.setObjectName(u"button_layout")
        self.save_toolB = QToolButton(self.save_groupB)
        self.save_toolB.setObjectName(u"save_toolB")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_toolB.sizePolicy().hasHeightForWidth())
        self.save_toolB.setSizePolicy(sizePolicy)
        self.save_toolB.setMaximumSize(QSize(100, 30))

        self.button_layout.addWidget(self.save_toolB)

        self.cancle_toolB = QToolButton(self.save_groupB)
        self.cancle_toolB.setObjectName(u"cancle_toolB")
        sizePolicy.setHeightForWidth(self.cancle_toolB.sizePolicy().hasHeightForWidth())
        self.cancle_toolB.setSizePolicy(sizePolicy)
        self.cancle_toolB.setMaximumSize(QSize(100, 30))

        self.button_layout.addWidget(self.cancle_toolB)


        self.verticalLayout.addLayout(self.button_layout)


        self.dialog_layout.addWidget(self.save_groupB)


        self.retranslateUi(save_message_dialog)

        QMetaObject.connectSlotsByName(save_message_dialog)
    # setupUi

    def retranslateUi(self, save_message_dialog):
        save_message_dialog.setWindowTitle(QCoreApplication.translate("save_message_dialog", u"message", None))
        self.save_groupB.setTitle("")
        self.questions_lable.setText(QCoreApplication.translate("save_message_dialog", u"questions", None))
        self.save_toolB.setText(QCoreApplication.translate("save_message_dialog", u"yes", None))
        self.cancle_toolB.setText(QCoreApplication.translate("save_message_dialog", u"no", None))
    # retranslateUi

