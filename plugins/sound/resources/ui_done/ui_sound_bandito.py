# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sound_bandito.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

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
        self.audio_device_frame = QFrame(self.sound_frame)
        self.audio_device_frame.setObjectName(u"audio_device_frame")
        self.audio_device_frame.setGeometry(QRect(570, 257, 320, 390))
        self.audio_device_frame.setMinimumSize(QSize(320, 390))
        self.audio_device_frame.setMaximumSize(QSize(320, 390))
        self.audio_device_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.audio_device_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.audio_device_frame)
        self.formLayout.setObjectName(u"formLayout")
        self.audio_device_groupB = QGroupBox(self.audio_device_frame)
        self.audio_device_groupB.setObjectName(u"audio_device_groupB")
        self.audio_device_groupB.setMinimumSize(QSize(300, 370))
        self.audio_device_groupB.setMaximumSize(QSize(300, 400))
        font = QFont()
        font.setPointSize(10)
        self.audio_device_groupB.setFont(font)
        self.audio_device_groupB.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.audio_device_groupB.setFlat(False)
        self.audio_device_groupB.setCheckable(False)
        self.verticalLayout_7 = QVBoxLayout(self.audio_device_groupB)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.audio_device_01_groupB = QGroupBox(self.audio_device_groupB)
        self.audio_device_01_groupB.setObjectName(u"audio_device_01_groupB")
        self.audio_device_01_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_2 = QHBoxLayout(self.audio_device_01_groupB)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 10)
        self.audiD_01_comboB = QComboBox(self.audio_device_01_groupB)
        self.audiD_01_comboB.setObjectName(u"audiD_01_comboB")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.audiD_01_comboB.sizePolicy().hasHeightForWidth())
        self.audiD_01_comboB.setSizePolicy(sizePolicy1)
        self.audiD_01_comboB.setMinimumSize(QSize(100, 30))
        self.audiD_01_comboB.setFont(font)

        self.horizontalLayout_2.addWidget(self.audiD_01_comboB)


        self.verticalLayout_7.addWidget(self.audio_device_01_groupB)

        self.audio_device_02_groupB = QGroupBox(self.audio_device_groupB)
        self.audio_device_02_groupB.setObjectName(u"audio_device_02_groupB")
        self.audio_device_02_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_3 = QHBoxLayout(self.audio_device_02_groupB)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 10)
        self.audiD_02_comboB = QComboBox(self.audio_device_02_groupB)
        self.audiD_02_comboB.setObjectName(u"audiD_02_comboB")
        sizePolicy1.setHeightForWidth(self.audiD_02_comboB.sizePolicy().hasHeightForWidth())
        self.audiD_02_comboB.setSizePolicy(sizePolicy1)
        self.audiD_02_comboB.setMinimumSize(QSize(100, 30))
        self.audiD_02_comboB.setFont(font)

        self.horizontalLayout_3.addWidget(self.audiD_02_comboB)


        self.verticalLayout_7.addWidget(self.audio_device_02_groupB)

        self.bluetooth_device_groupB = QGroupBox(self.audio_device_groupB)
        self.bluetooth_device_groupB.setObjectName(u"bluetooth_device_groupB")
        self.bluetooth_device_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_5 = QHBoxLayout(self.bluetooth_device_groupB)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, 5, 5, 10)
        self.bt_audiD_comboB = QComboBox(self.bluetooth_device_groupB)
        self.bt_audiD_comboB.setObjectName(u"bt_audiD_comboB")
        sizePolicy1.setHeightForWidth(self.bt_audiD_comboB.sizePolicy().hasHeightForWidth())
        self.bt_audiD_comboB.setSizePolicy(sizePolicy1)
        self.bt_audiD_comboB.setMinimumSize(QSize(100, 30))
        self.bt_audiD_comboB.setFont(font)

        self.horizontalLayout_5.addWidget(self.bt_audiD_comboB)


        self.verticalLayout_7.addWidget(self.bluetooth_device_groupB)

        self.mic_01_groupB = QGroupBox(self.audio_device_groupB)
        self.mic_01_groupB.setObjectName(u"mic_01_groupB")
        self.mic_01_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_4 = QHBoxLayout(self.mic_01_groupB)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 10)
        self.mic_01_comboB = QComboBox(self.mic_01_groupB)
        self.mic_01_comboB.setObjectName(u"mic_01_comboB")
        sizePolicy1.setHeightForWidth(self.mic_01_comboB.sizePolicy().hasHeightForWidth())
        self.mic_01_comboB.setSizePolicy(sizePolicy1)
        self.mic_01_comboB.setMinimumSize(QSize(100, 30))
        self.mic_01_comboB.setFont(font)

        self.horizontalLayout_4.addWidget(self.mic_01_comboB)


        self.verticalLayout_7.addWidget(self.mic_01_groupB)

        self.outpu_device_save_toolB = QToolButton(self.audio_device_groupB)
        self.outpu_device_save_toolB.setObjectName(u"outpu_device_save_toolB")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.outpu_device_save_toolB.sizePolicy().hasHeightForWidth())
        self.outpu_device_save_toolB.setSizePolicy(sizePolicy2)
        self.outpu_device_save_toolB.setMinimumSize(QSize(50, 50))
        self.outpu_device_save_toolB.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_7.addWidget(self.outpu_device_save_toolB)


        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.audio_device_groupB)


        self.retranslateUi(sound_bandito)

        QMetaObject.connectSlotsByName(sound_bandito)
    # setupUi

    def retranslateUi(self, sound_bandito):
        self.audio_device_groupB.setTitle(QCoreApplication.translate("sound_bandito", u"Device Output", None))
        self.audio_device_01_groupB.setTitle(QCoreApplication.translate("sound_bandito", u"Audio device #1", None))
        self.audio_device_02_groupB.setTitle(QCoreApplication.translate("sound_bandito", u"Audio device #2", None))
        self.bluetooth_device_groupB.setTitle(QCoreApplication.translate("sound_bandito", u"Bluetooch device", None))
        self.mic_01_groupB.setTitle(QCoreApplication.translate("sound_bandito", u"Mic #1", None))
        self.outpu_device_save_toolB.setText(QCoreApplication.translate("sound_bandito", u"Save", None))
        pass
    # retranslateUi

