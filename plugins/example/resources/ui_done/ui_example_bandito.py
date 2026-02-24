# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'example_bandito.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
    QWidget)

class Ui_sound_bandito(object):
    def setupUi(self, sound_bandito):
        if not sound_bandito.objectName():
            sound_bandito.setObjectName(u"sound_bandito")
        sound_bandito.setWindowModality(Qt.WindowModality.NonModal)
        sound_bandito.resize(900, 680)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sound_bandito.sizePolicy().hasHeightForWidth())
        sound_bandito.setSizePolicy(sizePolicy)
        sound_bandito.setMinimumSize(QSize(900, 680))
        sound_bandito.setMaximumSize(QSize(900, 680))
        sound_bandito.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        sound_bandito.setWindowOpacity(1.000000000000000)
        self.sound_frame = QFrame(sound_bandito)
        self.sound_frame.setObjectName(u"sound_frame")
        self.sound_frame.setGeometry(QRect(0, 0, 900, 680))
        self.sound_frame.setMinimumSize(QSize(900, 680))
        self.sound_frame.setMaximumSize(QSize(980, 680))
        self.sound_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sound_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.sound_frame)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)

        self.retranslateUi(sound_bandito)

        QMetaObject.connectSlotsByName(sound_bandito)
    # setupUi

    def retranslateUi(self, sound_bandito):
        pass
    # retranslateUi

