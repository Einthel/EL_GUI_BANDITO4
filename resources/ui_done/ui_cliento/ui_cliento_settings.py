# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cliento_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Setting_cliento_widget(object):
    def setupUi(self, Setting_cliento_widget):
        if not Setting_cliento_widget.objectName():
            Setting_cliento_widget.setObjectName(u"Setting_cliento_widget")
        Setting_cliento_widget.setWindowModality(Qt.WindowModality.NonModal)
        Setting_cliento_widget.resize(350, 300)
        Setting_cliento_widget.setMinimumSize(QSize(350, 300))
        Setting_cliento_widget.setMaximumSize(QSize(350, 300))
        Setting_cliento_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.gridLayout = QGridLayout(Setting_cliento_widget)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.frm_settings = QFrame(Setting_cliento_widget)
        self.frm_settings.setObjectName(u"frm_settings")
        self.frm_settings.setMinimumSize(QSize(340, 290))
        self.frm_settings.setMaximumSize(QSize(340, 290))
        self.frm_settings.setFrameShape(QFrame.Shape.StyledPanel)
        self.frm_settings.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frm_settings)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.edit_line_layout = QHBoxLayout()
        self.edit_line_layout.setSpacing(5)
        self.edit_line_layout.setObjectName(u"edit_line_layout")
        self.edit_line_layout.setContentsMargins(0, 0, 0, 0)
        self.lable_layout = QVBoxLayout()
        self.lable_layout.setSpacing(5)
        self.lable_layout.setObjectName(u"lable_layout")
        self.lable_layout.setContentsMargins(5, 5, 5, 5)
        self.ip_source_label = QLabel(self.frm_settings)
        self.ip_source_label.setObjectName(u"ip_source_label")
        self.ip_source_label.setMinimumSize(QSize(0, 30))
        self.ip_source_label.setMaximumSize(QSize(16777215, 30))

        self.lable_layout.addWidget(self.ip_source_label)

        self.ip_destination_label = QLabel(self.frm_settings)
        self.ip_destination_label.setObjectName(u"ip_destination_label")
        self.ip_destination_label.setMinimumSize(QSize(0, 30))
        self.ip_destination_label.setMaximumSize(QSize(16777215, 30))

        self.lable_layout.addWidget(self.ip_destination_label)

        self.port_label = QLabel(self.frm_settings)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setMinimumSize(QSize(0, 30))
        self.port_label.setMaximumSize(QSize(16777215, 30))

        self.lable_layout.addWidget(self.port_label)


        self.edit_line_layout.addLayout(self.lable_layout)

        self.txtEd_layout = QVBoxLayout()
        self.txtEd_layout.setSpacing(5)
        self.txtEd_layout.setObjectName(u"txtEd_layout")
        self.txtEd_layout.setContentsMargins(5, 5, 5, 5)
        self.ip_source_lineE = QLineEdit(self.frm_settings)
        self.ip_source_lineE.setObjectName(u"ip_source_lineE")
        self.ip_source_lineE.setMinimumSize(QSize(220, 30))
        self.ip_source_lineE.setMaximumSize(QSize(220, 30))
        self.ip_source_lineE.setReadOnly(False)

        self.txtEd_layout.addWidget(self.ip_source_lineE)

        self.ip_destination_lineE = QLineEdit(self.frm_settings)
        self.ip_destination_lineE.setObjectName(u"ip_destination_lineE")
        self.ip_destination_lineE.setMinimumSize(QSize(220, 30))
        self.ip_destination_lineE.setMaximumSize(QSize(220, 30))

        self.txtEd_layout.addWidget(self.ip_destination_lineE)

        self.port_lineE = QLineEdit(self.frm_settings)
        self.port_lineE.setObjectName(u"port_lineE")
        self.port_lineE.setMinimumSize(QSize(220, 30))
        self.port_lineE.setMaximumSize(QSize(220, 30))

        self.txtEd_layout.addWidget(self.port_lineE)


        self.edit_line_layout.addLayout(self.txtEd_layout)

        self.edit_line_layout.setStretch(0, 3)
        self.edit_line_layout.setStretch(1, 10)

        self.verticalLayout.addLayout(self.edit_line_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(5, 0, 0, 0)
        self.connect_toolB = QToolButton(self.frm_settings)
        self.connect_toolB.setObjectName(u"connect_toolB")
        self.connect_toolB.setMinimumSize(QSize(70, 30))
        self.connect_toolB.setMaximumSize(QSize(60, 30))

        self.button_layout.addWidget(self.connect_toolB)

        self.disconnect_toolB = QToolButton(self.frm_settings)
        self.disconnect_toolB.setObjectName(u"disconnect_toolB")
        self.disconnect_toolB.setMinimumSize(QSize(70, 30))
        self.disconnect_toolB.setMaximumSize(QSize(60, 30))

        self.button_layout.addWidget(self.disconnect_toolB)

        self.save_toolB = QToolButton(self.frm_settings)
        self.save_toolB.setObjectName(u"save_toolB")
        self.save_toolB.setMinimumSize(QSize(70, 30))
        self.save_toolB.setMaximumSize(QSize(60, 30))

        self.button_layout.addWidget(self.save_toolB)

        self.ping_toolB = QToolButton(self.frm_settings)
        self.ping_toolB.setObjectName(u"ping_toolB")
        self.ping_toolB.setMinimumSize(QSize(70, 30))
        self.ping_toolB.setMaximumSize(QSize(60, 30))

        self.button_layout.addWidget(self.ping_toolB)


        self.verticalLayout.addLayout(self.button_layout)

        self.status_light = QHBoxLayout()
        self.status_light.setSpacing(5)
        self.status_light.setObjectName(u"status_light")
        self.signal_frame = QFrame(self.frm_settings)
        self.signal_frame.setObjectName(u"signal_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signal_frame.sizePolicy().hasHeightForWidth())
        self.signal_frame.setSizePolicy(sizePolicy)
        self.signal_frame.setMinimumSize(QSize(35, 35))
        self.signal_frame.setMaximumSize(QSize(35, 35))
        self.signal_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.signal_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.status_light.addWidget(self.signal_frame)

        self.status_lineE = QLineEdit(self.frm_settings)
        self.status_lineE.setObjectName(u"status_lineE")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.status_lineE.sizePolicy().hasHeightForWidth())
        self.status_lineE.setSizePolicy(sizePolicy1)
        self.status_lineE.setMinimumSize(QSize(270, 35))
        self.status_lineE.setMaximumSize(QSize(270, 35))
        self.status_lineE.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.status_lineE.setReadOnly(True)

        self.status_light.addWidget(self.status_lineE)


        self.verticalLayout.addLayout(self.status_light)

        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)

        self.gridLayout.addWidget(self.frm_settings, 0, 0, 1, 1)


        self.retranslateUi(Setting_cliento_widget)

        QMetaObject.connectSlotsByName(Setting_cliento_widget)
    # setupUi

    def retranslateUi(self, Setting_cliento_widget):
        Setting_cliento_widget.setWindowTitle(QCoreApplication.translate("Setting_cliento_widget", u"Settings", None))
        self.ip_source_label.setText(QCoreApplication.translate("Setting_cliento_widget", u"IP Source:", None))
        self.ip_destination_label.setText(QCoreApplication.translate("Setting_cliento_widget", u"IP Destination:", None))
        self.port_label.setText(QCoreApplication.translate("Setting_cliento_widget", u"Port:", None))
        self.connect_toolB.setText(QCoreApplication.translate("Setting_cliento_widget", u"Connect", None))
        self.disconnect_toolB.setText(QCoreApplication.translate("Setting_cliento_widget", u"Disconnect", None))
        self.save_toolB.setText(QCoreApplication.translate("Setting_cliento_widget", u"Save", None))
        self.ping_toolB.setText(QCoreApplication.translate("Setting_cliento_widget", u"Ping", None))
    # retranslateUi

