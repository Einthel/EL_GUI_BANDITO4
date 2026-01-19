# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bandito_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Setting_bandito_widget(object):
    def setupUi(self, Setting_bandito_widget):
        if not Setting_bandito_widget.objectName():
            Setting_bandito_widget.setObjectName(u"Setting_bandito_widget")
        Setting_bandito_widget.setWindowModality(Qt.WindowModality.NonModal)
        Setting_bandito_widget.resize(370, 320)
        Setting_bandito_widget.setMinimumSize(QSize(370, 320))
        Setting_bandito_widget.setMaximumSize(QSize(372, 320))
        Setting_bandito_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.gridLayout = QGridLayout(Setting_bandito_widget)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.settings_qFrame = QFrame(Setting_bandito_widget)
        self.settings_qFrame.setObjectName(u"settings_qFrame")
        self.settings_qFrame.setMinimumSize(QSize(0, 310))
        self.settings_qFrame.setMaximumSize(QSize(16777215, 310))
        self.settings_qFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.settings_qFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.settings_qFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ipSource = QHBoxLayout()
        self.ipSource.setSpacing(0)
        self.ipSource.setObjectName(u"ipSource")
        self.ip_label = QLabel(self.settings_qFrame)
        self.ip_label.setObjectName(u"ip_label")
        self.ip_label.setMinimumSize(QSize(60, 30))
        self.ip_label.setMaximumSize(QSize(60, 30))

        self.ipSource.addWidget(self.ip_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.ip_source_lineE = QLineEdit(self.settings_qFrame)
        self.ip_source_lineE.setObjectName(u"ip_source_lineE")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ip_source_lineE.sizePolicy().hasHeightForWidth())
        self.ip_source_lineE.setSizePolicy(sizePolicy)
        self.ip_source_lineE.setMinimumSize(QSize(230, 30))
        self.ip_source_lineE.setMaximumSize(QSize(230, 30))
        self.ip_source_lineE.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.ip_source_lineE.setReadOnly(False)

        self.ipSource.addWidget(self.ip_source_lineE)


        self.verticalLayout.addLayout(self.ipSource)

        self.ipDestination = QHBoxLayout()
        self.ipDestination.setSpacing(0)
        self.ipDestination.setObjectName(u"ipDestination")
        self.ip_destination_label = QLabel(self.settings_qFrame)
        self.ip_destination_label.setObjectName(u"ip_destination_label")
        self.ip_destination_label.setMinimumSize(QSize(75, 30))
        self.ip_destination_label.setMaximumSize(QSize(75, 30))

        self.ipDestination.addWidget(self.ip_destination_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.ip_destination_lineE = QLineEdit(self.settings_qFrame)
        self.ip_destination_lineE.setObjectName(u"ip_destination_lineE")
        sizePolicy.setHeightForWidth(self.ip_destination_lineE.sizePolicy().hasHeightForWidth())
        self.ip_destination_lineE.setSizePolicy(sizePolicy)
        self.ip_destination_lineE.setMinimumSize(QSize(230, 30))
        self.ip_destination_lineE.setMaximumSize(QSize(230, 30))

        self.ipDestination.addWidget(self.ip_destination_lineE)


        self.verticalLayout.addLayout(self.ipDestination)

        self.port = QHBoxLayout()
        self.port.setSpacing(0)
        self.port.setObjectName(u"port")
        self.port_label = QLabel(self.settings_qFrame)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setMinimumSize(QSize(60, 30))
        self.port_label.setMaximumSize(QSize(60, 30))

        self.port.addWidget(self.port_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.port_lineE = QLineEdit(self.settings_qFrame)
        self.port_lineE.setObjectName(u"port_lineE")
        sizePolicy.setHeightForWidth(self.port_lineE.sizePolicy().hasHeightForWidth())
        self.port_lineE.setSizePolicy(sizePolicy)
        self.port_lineE.setMinimumSize(QSize(230, 30))
        self.port_lineE.setMaximumSize(QSize(230, 30))

        self.port.addWidget(self.port_lineE)


        self.verticalLayout.addLayout(self.port)

        self.login = QHBoxLayout()
        self.login.setSpacing(0)
        self.login.setObjectName(u"login")
        self.login_label = QLabel(self.settings_qFrame)
        self.login_label.setObjectName(u"login_label")
        self.login_label.setMinimumSize(QSize(60, 30))
        self.login_label.setMaximumSize(QSize(60, 30))

        self.login.addWidget(self.login_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.login_lineE = QLineEdit(self.settings_qFrame)
        self.login_lineE.setObjectName(u"login_lineE")
        sizePolicy.setHeightForWidth(self.login_lineE.sizePolicy().hasHeightForWidth())
        self.login_lineE.setSizePolicy(sizePolicy)
        self.login_lineE.setMinimumSize(QSize(230, 30))
        self.login_lineE.setMaximumSize(QSize(230, 30))

        self.login.addWidget(self.login_lineE)


        self.verticalLayout.addLayout(self.login)

        self.password = QHBoxLayout()
        self.password.setSpacing(5)
        self.password.setObjectName(u"password")
        self.pass_label = QLabel(self.settings_qFrame)
        self.pass_label.setObjectName(u"pass_label")
        self.pass_label.setMinimumSize(QSize(60, 30))
        self.pass_label.setMaximumSize(QSize(60, 30))

        self.password.addWidget(self.pass_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.pass_lay = QHBoxLayout()
        self.pass_lay.setSpacing(5)
        self.pass_lay.setObjectName(u"pass_lay")
        self.pass_lineE = QLineEdit(self.settings_qFrame)
        self.pass_lineE.setObjectName(u"pass_lineE")
        sizePolicy.setHeightForWidth(self.pass_lineE.sizePolicy().hasHeightForWidth())
        self.pass_lineE.setSizePolicy(sizePolicy)
        self.pass_lineE.setMinimumSize(QSize(170, 30))
        self.pass_lineE.setMaximumSize(QSize(170, 30))

        self.pass_lay.addWidget(self.pass_lineE)

        self.show_pass_checkB = QCheckBox(self.settings_qFrame)
        self.show_pass_checkB.setObjectName(u"show_pass_checkB")
        self.show_pass_checkB.setMaximumSize(QSize(60, 16777215))

        self.pass_lay.addWidget(self.show_pass_checkB)


        self.password.addLayout(self.pass_lay)


        self.verticalLayout.addLayout(self.password)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.connect_toolB = QToolButton(self.settings_qFrame)
        self.connect_toolB.setObjectName(u"connect_toolB")
        self.connect_toolB.setMinimumSize(QSize(80, 30))
        self.connect_toolB.setMaximumSize(QSize(80, 30))

        self.button_layout.addWidget(self.connect_toolB)

        self.disconnect_toolB = QToolButton(self.settings_qFrame)
        self.disconnect_toolB.setObjectName(u"disconnect_toolB")
        self.disconnect_toolB.setMinimumSize(QSize(80, 30))
        self.disconnect_toolB.setMaximumSize(QSize(80, 30))

        self.button_layout.addWidget(self.disconnect_toolB)

        self.save_toolB = QToolButton(self.settings_qFrame)
        self.save_toolB.setObjectName(u"save_toolB")
        self.save_toolB.setMinimumSize(QSize(80, 30))
        self.save_toolB.setMaximumSize(QSize(80, 30))

        self.button_layout.addWidget(self.save_toolB)

        self.ping_toolB = QToolButton(self.settings_qFrame)
        self.ping_toolB.setObjectName(u"ping_toolB")
        self.ping_toolB.setMinimumSize(QSize(80, 30))
        self.ping_toolB.setMaximumSize(QSize(80, 30))

        self.button_layout.addWidget(self.ping_toolB)


        self.verticalLayout.addLayout(self.button_layout)

        self.status_light = QHBoxLayout()
        self.status_light.setSpacing(5)
        self.status_light.setObjectName(u"status_light")
        self.signal_frame = QFrame(self.settings_qFrame)
        self.signal_frame.setObjectName(u"signal_frame")
        self.signal_frame.setMinimumSize(QSize(35, 35))
        self.signal_frame.setMaximumSize(QSize(35, 35))
        self.signal_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.signal_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.status_light.addWidget(self.signal_frame)

        self.status_lineE = QLineEdit(self.settings_qFrame)
        self.status_lineE.setObjectName(u"status_lineE")
        sizePolicy.setHeightForWidth(self.status_lineE.sizePolicy().hasHeightForWidth())
        self.status_lineE.setSizePolicy(sizePolicy)
        self.status_lineE.setMinimumSize(QSize(300, 35))
        self.status_lineE.setMaximumSize(QSize(300, 35))
        self.status_lineE.setReadOnly(True)

        self.status_light.addWidget(self.status_lineE)


        self.verticalLayout.addLayout(self.status_light)


        self.gridLayout.addWidget(self.settings_qFrame, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop)


        self.retranslateUi(Setting_bandito_widget)

        QMetaObject.connectSlotsByName(Setting_bandito_widget)
    # setupUi

    def retranslateUi(self, Setting_bandito_widget):
        Setting_bandito_widget.setWindowTitle(QCoreApplication.translate("Setting_bandito_widget", u"Settings", None))
        self.ip_label.setText(QCoreApplication.translate("Setting_bandito_widget", u"IP Source:", None))
        self.ip_source_lineE.setInputMask("")
        self.ip_destination_label.setText(QCoreApplication.translate("Setting_bandito_widget", u"IP Destination:", None))
        self.port_label.setText(QCoreApplication.translate("Setting_bandito_widget", u"Port:", None))
        self.login_label.setText(QCoreApplication.translate("Setting_bandito_widget", u"Login:", None))
        self.pass_label.setText(QCoreApplication.translate("Setting_bandito_widget", u"Password:", None))
        self.show_pass_checkB.setText(QCoreApplication.translate("Setting_bandito_widget", u"Show", None))
        self.connect_toolB.setText(QCoreApplication.translate("Setting_bandito_widget", u"Connect", None))
        self.disconnect_toolB.setText(QCoreApplication.translate("Setting_bandito_widget", u"Disconnect", None))
        self.save_toolB.setText(QCoreApplication.translate("Setting_bandito_widget", u"Save", None))
        self.ping_toolB.setText(QCoreApplication.translate("Setting_bandito_widget", u"Ping", None))
    # retranslateUi

