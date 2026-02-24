from ctypes import POINTER, cast

import comtypes
import pythoncom
from comtypes import CLSCTX_ALL
from pycaw.constants import CLSID_MMDeviceEnumerator
from pycaw.pycaw import (AudioUtilities, EDataFlow, IAudioEndpointVolume,
                         IMMDeviceEnumerator)

# Инициализируем COM-библиотеку один раз при импорте модуля
pythoncom.CoInitialize()


class AudioController:
    """
    Класс для управления громкостью конкретного приложения (процесса).
    Находит и кэширует аудиосессию при создании для высокой производительности.
    """
    def __init__(self, process_name):
        self.process_name = process_name
        self.audio_interface = None
        self._find_session()

    def _find_session(self):
        """Находит и кэширует аудиосессию для указанного процесса."""
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == self.process_name:
                self.audio_interface = session.SimpleAudioVolume
                print(f"Аудиосессия для '{self.process_name}' найдена.")
                break # Нашли, выходим из цикла
        if not self.audio_interface:
            print(f"Предупреждение: Аудиосессия для '{self.process_name}' не найдена.")

    def get_volume(self):
        """Возвращает текущую громкость процесса (от 0.0 до 1.0)."""
        if self.audio_interface:
            return self.audio_interface.GetMasterVolume()
        return None

    def set_volume(self, level):
        """
        Устанавливает громкость для процесса.
        :param level: Уровень громкости от 0.0 (тихо) до 1.0 (макс).
        """
        if self.audio_interface:
            volume_level = min(1.0, max(0.0, level))
            self.audio_interface.SetMasterVolume(volume_level, None)

    def decrease_volume(self, amount):
        """
        Уменьшает громкость на указанное значение.
        :param amount: Значение от 0.0 до 1.0, на которое нужно уменьшить громкость.
        """
        if self.audio_interface:
            current_volume = self.audio_interface.GetMasterVolume()
            new_volume = max(0.0, current_volume - amount)
            self.audio_interface.SetMasterVolume(new_volume, None)

    def increase_volume(self, amount):
        """
        Увеличивает громкость на указанное значение.
        :param amount: Значение от 0.0 до 1.0, на которое нужно увеличить громкость.
        """
        if self.audio_interface:
            current_volume = self.audio_interface.GetMasterVolume()
            new_volume = min(1.0, current_volume + amount)
            self.audio_interface.SetMasterVolume(new_volume, None)


def muteAndUnMute(process, value):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == process:
            if value == "Toggle":
                value = 0 if volume.GetMute() == 1 else 1
            elif value == "Mute":
                value = 1
            elif value == "Unmute":
                value = 0
            volume.SetMute(value, None)


def volumeChanger(process, action, value):
    if process == "Master Volume":
        if action == "Set":
            setMasterVolume(value)
        else:
            value = +value if action == "Increase" else -value
            setMasterVolume(100 if (master_vol := getMasterVolume() + value) and master_vol > 100 else master_vol)
    elif action == "Set":
        AudioController(str(process)).set_volume((int(value)*0.01))
    elif action == "Increase":
        AudioController(str(process)).increase_volume((int(value)*0.01))

    elif action == "Decrease":
        AudioController(str(process)).decrease_volume((int(value)*0.01))


def setMasterVolume(Vol):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    scalarVolume = int(Vol) / 100
    volume.SetMasterVolumeLevelScalar(scalarVolume, None)

def getMasterVolume() -> int:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    # Get the volume range and current volume level
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume_percent = int(round(volume.GetMasterVolumeLevelScalar() * 100))

    return volume_percent

def getDeviceObject(device_id, direction="Output"):
    deviceEnumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER)
    
    if deviceEnumerator is None: return None

    flow = EDataFlow.eCapture.value
    if direction.lower() == "output":
        flow = EDataFlow.eRender.value

    devices = deviceEnumerator.EnumAudioEndpoints(flow, 1)

    for dev in devices:
        if dev.GetId() == device_id:
            return dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    
    return None
    
def setDeviceVolume(device_id, direction, volume_level):
    if device_id == "default":
        if direction.lower() == "output":
            device = AudioUtilities.GetSpeakers()
        else:
            device = AudioUtilities.GetMicrophone()
        device_object = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    else:
        device_object = getDeviceObject(device_id, direction)

    if device_object:
        volume = cast(device_object, POINTER(IAudioEndpointVolume))
        scalar_volume = float(volume_level) / 100
        volume.SetMasterVolumeLevelScalar(scalar_volume, None)


def get_process_id(name):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == name:
            return session.Process.pid
    return None
