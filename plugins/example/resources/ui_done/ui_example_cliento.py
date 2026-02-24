# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'example_cliento.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_sound_cliento(object):
    def setupUi(self, sound_cliento):
        if not sound_cliento.objectName():
            sound_cliento.setObjectName(u"sound_cliento")
        sound_cliento.resize(785, 580)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sound_cliento.sizePolicy().hasHeightForWidth())
        sound_cliento.setSizePolicy(sizePolicy)
        sound_cliento.setMinimumSize(QSize(785, 580))
        sound_cliento.setMaximumSize(QSize(785, 580))
        self.verticalLayout = QVBoxLayout(sound_cliento)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sound_frame = QFrame(sound_cliento)
        self.sound_frame.setObjectName(u"sound_frame")
        self.sound_frame.setEnabled(True)
        sizePolicy.setHeightForWidth(self.sound_frame.sizePolicy().hasHeightForWidth())
        self.sound_frame.setSizePolicy(sizePolicy)
        self.sound_frame.setMinimumSize(QSize(760, 560))
        self.sound_frame.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(5)
        self.sound_frame.setFont(font)
        self.sound_frame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.sound_frame.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.sound_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sound_frame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.sound_frame.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        self.sound_frame.setFrameShape(QFrame.Shape.Panel)
        self.sound_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.sound_frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.sound_frame)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)

        self.verticalLayout.addWidget(self.sound_frame)


        self.retranslateUi(sound_cliento)

        QMetaObject.connectSlotsByName(sound_cliento)
    # setupUi

    def retranslateUi(self, sound_cliento):
        pass
    # retranslateUi

