# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'questions_di.ui'
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

class Ui_questions_di(object):
    def setupUi(self, questions_di):
        if not questions_di.objectName():
            questions_di.setObjectName(u"questions_di")
        questions_di.resize(270, 130)
        questions_di.setMinimumSize(QSize(270, 130))
        questions_di.setMaximumSize(QSize(270, 130))
        questions_di.setModal(False)
        self.dialog_layout = QVBoxLayout(questions_di)
        self.dialog_layout.setSpacing(5)
        self.dialog_layout.setObjectName(u"dialog_layout")
        self.dialog_layout.setContentsMargins(5, 5, 5, 5)
        self.q_groupB = QGroupBox(questions_di)
        self.q_groupB.setObjectName(u"q_groupB")
        self.q_groupB.setMinimumSize(QSize(260, 120))
        self.q_groupB.setMaximumSize(QSize(260, 120))
        self.q_groupB.setFlat(False)
        self.verticalLayout = QVBoxLayout(self.q_groupB)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.questions_lable = QLabel(self.q_groupB)
        self.questions_lable.setObjectName(u"questions_lable")
        self.questions_lable.setMinimumSize(QSize(200, 0))
        font = QFont()
        font.setPointSize(12)
        self.questions_lable.setFont(font)
        self.questions_lable.setLineWidth(2)
        self.questions_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.questions_lable)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.yes_toolB = QToolButton(self.q_groupB)
        self.yes_toolB.setObjectName(u"yes_toolB")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yes_toolB.sizePolicy().hasHeightForWidth())
        self.yes_toolB.setSizePolicy(sizePolicy)
        self.yes_toolB.setMaximumSize(QSize(100, 30))

        self.button_layout.addWidget(self.yes_toolB)

        self.no_toolB = QToolButton(self.q_groupB)
        self.no_toolB.setObjectName(u"no_toolB")
        sizePolicy.setHeightForWidth(self.no_toolB.sizePolicy().hasHeightForWidth())
        self.no_toolB.setSizePolicy(sizePolicy)
        self.no_toolB.setMaximumSize(QSize(100, 30))

        self.button_layout.addWidget(self.no_toolB)


        self.verticalLayout.addLayout(self.button_layout)


        self.dialog_layout.addWidget(self.q_groupB)


        self.retranslateUi(questions_di)

        QMetaObject.connectSlotsByName(questions_di)
    # setupUi

    def retranslateUi(self, questions_di):
        questions_di.setWindowTitle("")
        self.q_groupB.setTitle("")
        self.questions_lable.setText(QCoreApplication.translate("questions_di", u"questions", None))
        self.yes_toolB.setText(QCoreApplication.translate("questions_di", u"yes", None))
        self.no_toolB.setText(QCoreApplication.translate("questions_di", u"no", None))
    # retranslateUi

