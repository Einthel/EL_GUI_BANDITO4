import os
from PySide6.QtWidgets import QWidget
from resources.ui_done.ui_music_cliento import Ui_Form

class MusicClientoPlugin(QWidget, Ui_Form):
    def __init__(self, socket_client=None, plugin_path=None):
        super().__init__()
        self.socket_client = socket_client
        self.plugin_path = plugin_path
        self.setupUi(self)
