# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tune_bandito.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_tune_bandito(object):
    def setupUi(self, tune_bandito):
        if not tune_bandito.objectName():
            tune_bandito.setObjectName(u"tune_bandito")
        tune_bandito.setWindowModality(Qt.WindowModality.NonModal)
        tune_bandito.resize(900, 680)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(tune_bandito.sizePolicy().hasHeightForWidth())
        tune_bandito.setSizePolicy(sizePolicy)
        tune_bandito.setMinimumSize(QSize(900, 680))
        tune_bandito.setMaximumSize(QSize(900, 680))
        tune_bandito.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        tune_bandito.setWindowOpacity(1.000000000000000)
        self.tune_frame = QFrame(tune_bandito)
        self.tune_frame.setObjectName(u"tune_frame")
        self.tune_frame.setGeometry(QRect(0, 0, 900, 680))
        self.tune_frame.setMinimumSize(QSize(900, 680))
        self.tune_frame.setMaximumSize(QSize(980, 680))
        self.tune_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.tune_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.audio_device_frame = QFrame(self.tune_frame)
        self.audio_device_frame.setObjectName(u"audio_device_frame")
        self.audio_device_frame.setGeometry(QRect(530, 280, 360, 390))
        self.audio_device_frame.setMinimumSize(QSize(360, 390))
        self.audio_device_frame.setMaximumSize(QSize(360, 390))
        self.audio_device_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.audio_device_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.audio_device_frame)
        self.formLayout.setObjectName(u"formLayout")
        self.audio_device_groupB = QGroupBox(self.audio_device_frame)
        self.audio_device_groupB.setObjectName(u"audio_device_groupB")
        self.audio_device_groupB.setMinimumSize(QSize(300, 370))
        self.audio_device_groupB.setMaximumSize(QSize(340, 400))
        font = QFont()
        font.setPointSize(10)
        self.audio_device_groupB.setFont(font)
        self.audio_device_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_device_groupB.setFlat(False)
        self.audio_device_groupB.setCheckable(False)
        self.verticalLayout_7 = QVBoxLayout(self.audio_device_groupB)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.audio_device_01_groupB = QGroupBox(self.audio_device_groupB)
        self.audio_device_01_groupB.setObjectName(u"audio_device_01_groupB")
        self.audio_device_01_groupB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_2 = QHBoxLayout(self.audio_device_01_groupB)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 10)
        self.label = QLabel(self.audio_device_01_groupB)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.audiD_01_comboB = QComboBox(self.audio_device_01_groupB)
        self.audiD_01_comboB.setObjectName(u"audiD_01_comboB")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.audiD_01_comboB.sizePolicy().hasHeightForWidth())
        self.audiD_01_comboB.setSizePolicy(sizePolicy1)
        self.audiD_01_comboB.setMinimumSize(QSize(100, 40))
        self.audiD_01_comboB.setMaximumSize(QSize(250, 16777215))
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
        self.label_2 = QLabel(self.audio_device_02_groupB)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.audiD_02_comboB = QComboBox(self.audio_device_02_groupB)
        self.audiD_02_comboB.setObjectName(u"audiD_02_comboB")
        sizePolicy1.setHeightForWidth(self.audiD_02_comboB.sizePolicy().hasHeightForWidth())
        self.audiD_02_comboB.setSizePolicy(sizePolicy1)
        self.audiD_02_comboB.setMinimumSize(QSize(100, 40))
        self.audiD_02_comboB.setMaximumSize(QSize(250, 16777215))
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
        self.label_3 = QLabel(self.bluetooth_device_groupB)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.bt_audiD_comboB = QComboBox(self.bluetooth_device_groupB)
        self.bt_audiD_comboB.setObjectName(u"bt_audiD_comboB")
        sizePolicy1.setHeightForWidth(self.bt_audiD_comboB.sizePolicy().hasHeightForWidth())
        self.bt_audiD_comboB.setSizePolicy(sizePolicy1)
        self.bt_audiD_comboB.setMinimumSize(QSize(100, 40))
        self.bt_audiD_comboB.setMaximumSize(QSize(250, 16777215))
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
        self.label_4 = QLabel(self.mic_01_groupB)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.mic_01_comboB = QComboBox(self.mic_01_groupB)
        self.mic_01_comboB.setObjectName(u"mic_01_comboB")
        sizePolicy1.setHeightForWidth(self.mic_01_comboB.sizePolicy().hasHeightForWidth())
        self.mic_01_comboB.setSizePolicy(sizePolicy1)
        self.mic_01_comboB.setMinimumSize(QSize(100, 40))
        self.mic_01_comboB.setMaximumSize(QSize(250, 16777215))
        self.mic_01_comboB.setFont(font)

        self.horizontalLayout_4.addWidget(self.mic_01_comboB)


        self.verticalLayout_7.addWidget(self.mic_01_groupB)

        self.output_device_save_toolB = QToolButton(self.audio_device_groupB)
        self.output_device_save_toolB.setObjectName(u"output_device_save_toolB")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.output_device_save_toolB.sizePolicy().hasHeightForWidth())
        self.output_device_save_toolB.setSizePolicy(sizePolicy2)
        self.output_device_save_toolB.setMinimumSize(QSize(50, 30))
        self.output_device_save_toolB.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_7.addWidget(self.output_device_save_toolB)


        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.audio_device_groupB)

        self.test_mute_toolB = QToolButton(self.tune_frame)
        self.test_mute_toolB.setObjectName(u"test_mute_toolB")
        self.test_mute_toolB.setGeometry(QRect(110, 570, 51, 41))
        self.test_mute_sound_toolB = QToolButton(self.tune_frame)
        self.test_mute_sound_toolB.setObjectName(u"test_mute_sound_toolB")
        self.test_mute_sound_toolB.setGeometry(QRect(210, 570, 51, 41))
        self.test_vol_plus_toolB = QToolButton(self.tune_frame)
        self.test_vol_plus_toolB.setObjectName(u"test_vol_plus_toolB")
        self.test_vol_plus_toolB.setGeometry(QRect(200, 480, 51, 41))
        self.test_vol_minus_toolB = QToolButton(self.tune_frame)
        self.test_vol_minus_toolB.setObjectName(u"test_vol_minus_toolB")
        self.test_vol_minus_toolB.setGeometry(QRect(280, 480, 51, 41))

        self.retranslateUi(tune_bandito)

        QMetaObject.connectSlotsByName(tune_bandito)
    # setupUi

    def retranslateUi(self, tune_bandito):
        self.audio_device_groupB.setTitle(QCoreApplication.translate("tune_bandito", u"Device Output", None))
        self.audio_device_01_groupB.setTitle("")
        self.label.setText(QCoreApplication.translate("tune_bandito", u"Audio #1", None))
        self.audio_device_02_groupB.setTitle("")
        self.label_2.setText(QCoreApplication.translate("tune_bandito", u"Audio #2", None))
        self.bluetooth_device_groupB.setTitle("")
        self.label_3.setText(QCoreApplication.translate("tune_bandito", u"BT Audio", None))
        self.mic_01_groupB.setTitle("")
        self.label_4.setText(QCoreApplication.translate("tune_bandito", u"Mic #1", None))
        self.output_device_save_toolB.setText(QCoreApplication.translate("tune_bandito", u"Save", None))
        self.test_mute_toolB.setText(QCoreApplication.translate("tune_bandito", u"Mute", None))
        self.test_mute_sound_toolB.setText(QCoreApplication.translate("tune_bandito", u"off_sound", None))
        self.test_vol_plus_toolB.setText(QCoreApplication.translate("tune_bandito", u"+", None))
        self.test_vol_minus_toolB.setText(QCoreApplication.translate("tune_bandito", u"-", None))
        pass
    # retranslateUi

