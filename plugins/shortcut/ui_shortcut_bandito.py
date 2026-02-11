# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shortcut_bandito.ui'
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QSizePolicy, QToolButton,
    QWidget)

class Ui_stream_bandito(object):
    def setupUi(self, stream_bandito):
        if not stream_bandito.objectName():
            stream_bandito.setObjectName(u"stream_bandito")
        stream_bandito.setWindowModality(Qt.WindowModality.NonModal)
        stream_bandito.resize(900, 680)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(stream_bandito.sizePolicy().hasHeightForWidth())
        stream_bandito.setSizePolicy(sizePolicy)
        stream_bandito.setMinimumSize(QSize(900, 680))
        stream_bandito.setMaximumSize(QSize(900, 680))
        stream_bandito.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        stream_bandito.setWindowOpacity(1.000000000000000)
        self.pressMe_toolB = QToolButton(stream_bandito)
        self.pressMe_toolB.setObjectName(u"pressMe_toolB")
        self.pressMe_toolB.setGeometry(QRect(90, 140, 141, 71))
        self.lineEdit = QLineEdit(stream_bandito)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(90, 250, 151, 71))
        self.lineEdit.setReadOnly(True)

        self.retranslateUi(stream_bandito)

        QMetaObject.connectSlotsByName(stream_bandito)
    # setupUi

    def retranslateUi(self, stream_bandito):
        self.pressMe_toolB.setText(QCoreApplication.translate("stream_bandito", u"...", None))
        pass
    # retranslateUi

