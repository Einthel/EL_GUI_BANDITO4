import os
import time
from PySide6.QtCore import QThread, Signal


class AudioStatusListener(QThread):
    """Универсальный поток для прослушивания изменения статуса аудиоустройства (mute и volume)."""
    status_changed = Signal(dict)  # {'mute': bool, 'volume': int}

    def __init__(self, audio_manager, device_name, is_input=False, interval=1.0):
        super().__init__()
        self.audio_manager = audio_manager
        self.device_name = device_name
        self.is_input = is_input
        self.interval = interval
        self.running = True
        self._last_state = {'mute': None, 'volume': None}

    def run(self):
        import pythoncom
        pythoncom.CoInitialize()
        try:
            while self.running:
                if not self.device_name:
                    time.sleep(self.interval)
                    continue

                # Получаем актуальные данные
                if self.is_input:
                    mute = self.audio_manager.is_mic_muted(self.device_name)
                else:
                    mute = self.audio_manager.is_sound_muted(self.device_name)
                
                volume = self.audio_manager.get_device_volume(self.device_name)
                
                current_state = {'mute': mute, 'volume': volume}
                
                if self._last_state['mute'] is None:
                    self._last_state = current_state.copy()
                elif current_state != self._last_state:
                    self._last_state = current_state.copy()
                    self.status_changed.emit(current_state)

                time.sleep(self.interval)
        finally:
            pythoncom.CoUninitialize()

    def stop(self):
        self.running = False
        self.wait()


class TnAudioManager:
    """Обертка над системным аудио-менеджером для Tune."""

    def __init__(self):
        self._output_devices: list[str] = []
        self._input_devices: list[str] = []
        self._mic_listener: AudioStatusListener | None = None
        self._sound_listener: AudioStatusListener | None = None

    def __del__(self):
        self.stop_mic_listening()
        self.stop_sound_listening()

    def start_mic_listening(self, device_name: str, callback) -> bool:
        """Запустить прослушивание статуса микрофона."""
        self.stop_mic_listening()
        if not device_name:
            return False
            
        self._mic_listener = AudioStatusListener(self, device_name, is_input=True)
        self._mic_listener.status_changed.connect(callback)
        self._mic_listener.start()
        return True

    def stop_mic_listening(self):
        """Остановить прослушивание."""
        if self._mic_listener:
            self._mic_listener.stop()
            self._mic_listener = None

    def start_sound_listening(self, device_name: str, callback) -> bool:
        """Запустить прослушивание статуса звука."""
        self.stop_sound_listening()
        if not device_name:
            return False
            
        self._sound_listener = AudioStatusListener(self, device_name, is_input=False)
        self._sound_listener.status_changed.connect(callback)
        self._sound_listener.start()
        return True

    def stop_sound_listening(self):
        """Остановить прослушивание."""
        if self._sound_listener:
            self._sound_listener.stop()
            self._sound_listener = None

    def refresh_output_devices(self) -> list[str]:
        """Получить список устройств вывода и залогировать их."""
        devices: list[str] = []
        default_name: str | None = None

        try:
            from libs.audio_manager import audioSwitch as switcher
            devices_map = switcher.MyAudioUtilities.getAllDevices("output")
            devices = list(devices_map.keys())

            # Пытаемся определить текущее устройство по умолчанию
            try:
                import pythoncom
                pythoncom.CoInitialize()
                try:
                    from pycaw.pycaw import AudioUtilities
                    default_endpoint = AudioUtilities.GetSpeakers()
                    if default_endpoint is not None:
                        device_obj = AudioUtilities.CreateDevice(default_endpoint)
                        default_name = device_obj.FriendlyName
                finally:
                    try:
                        pythoncom.CoUninitialize()
                    except Exception:
                        pass
            except Exception:
                pass

            if default_name and default_name in devices:
                devices.remove(default_name)
                devices.insert(0, default_name)

        except Exception as e:
            print(f"[TuneBandito] AudioManager error while listing outputs: {e}")

        self._output_devices = devices
        return devices

    def refresh_input_devices(self) -> list[str]:
        """Получить список устройств ввода (микрофоны)."""
        devices: list[str] = []
        try:
            from libs.audio_manager import audioSwitch as switcher
            devices_map = switcher.MyAudioUtilities.getAllDevices("input")
            devices = list(devices_map.keys())
        except Exception as e:
            print(f"[TuneBandito] AudioManager error while listing inputs: {e}")

        self._input_devices = devices
        return devices

    def get_cached_output_devices(self) -> list[str]:
        """Вернуть последний закешированный список устройств вывода."""
        return list(self._output_devices)

    def get_cached_input_devices(self) -> list[str]:
        """Вернуть последний закешированный список устройств ввода."""
        return list(self._input_devices)

    def set_default_output_device(self, device_name: str) -> bool:
        """Сделать указанное устройство системным устройством вывода по умолчанию."""
        if not device_name:
            print("[TuneBandito] set_default_output_device: empty device name, skipping.")
            return False

        try:
            import pythoncom
            pythoncom.CoInitialize()
            try:
                from libs.audio_manager import audioSwitch as switcher
                all_devices = switcher.MyAudioUtilities.getAllDevices("output")
                device_id = all_devices.get(device_name)
                if not device_id:
                    print(f"[TuneBandito] Device '{device_name}' not found among active outputs.")
                    return False

                # Устанавливаем выбранное устройство по умолчанию для всех ролей
                switcher.switchOutput(device_id, switcher.pc.ERole.eConsole)
                switcher.switchOutput(device_id, switcher.pc.ERole.eMultimedia)
                switcher.switchOutput(device_id, switcher.pc.ERole.eCommunications)
                print(f"[TuneBandito] Default output device set to: {device_name}")
                return True
            except Exception as e:
                print(f"[TuneBandito] Error while switching default output device: {e}")
                return False
            finally:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass
        except Exception as e:
            print(f"[TuneBandito] Python COM initialization error: {e}")
            return False

    def set_mute_mic(self, device_name: str, mute: bool) -> bool:
        """Включить/выключить звук для указанного микрофона."""
        return self._set_device_mute(device_name, mute)

    def is_mic_muted(self, device_name: str) -> bool:
        """Проверить, выключен ли звук у микрофона."""
        return self._is_device_muted(device_name)

    def set_mute_sound(self, device_name: str, mute: bool) -> bool:
        """Включить/выключить звук для указанного устройства вывода."""
        return self._set_device_mute(device_name, mute)

    def is_sound_muted(self, device_name: str) -> bool:
        """Проверить, выключен ли звук у устройства вывода."""
        return self._is_device_muted(device_name)

    def get_device_volume(self, device_name: str) -> int:
        """Получить текущий уровень громкости устройства (0-100)."""
        return self._get_device_volume(device_name)

    def set_device_volume(self, device_name: str, volume: int) -> bool:
        """Установить уровень громкости устройства (0-100)."""
        return self._set_device_volume(device_name, volume)

    def _set_device_mute(self, device_name: str, mute: bool) -> bool:
        """Внутренний метод для установки mute на устройстве."""
        if not device_name:
            return False
        try:
            import pythoncom
            pythoncom.CoInitialize()
            try:
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                devices = AudioUtilities.GetAllDevices()
                for device in devices:
                    if device.FriendlyName == device_name:
                        target = getattr(device, "_dev", None)
                        if target is None:
                            target = getattr(device, "device", device)
                            
                        if hasattr(target, "Activate"):
                            interface = target.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                            volume = interface.QueryInterface(IAudioEndpointVolume)
                            volume.SetMute(1 if mute else 0, None)
                            return True
            finally:
                pythoncom.CoUninitialize()
        except Exception as e:
            print(f"[Tn] Mute device error: {e}")
        return False

    def _is_device_muted(self, device_name: str) -> bool:
        """Внутренний метод для проверки mute на устройстве."""
        if not device_name:
            return False
        try:
            import pythoncom
            pythoncom.CoInitialize()
            try:
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                devices = AudioUtilities.GetAllDevices()
                for device in devices:
                    if device.FriendlyName == device_name:
                        target = getattr(device, "_dev", None)
                        if target is None:
                            target = getattr(device, "device", device)
                            
                        if hasattr(target, "Activate"):
                            interface = target.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                            volume = interface.QueryInterface(IAudioEndpointVolume)
                            return bool(volume.GetMute())
            finally:
                pythoncom.CoUninitialize()
        except Exception:
            pass
        return False

    def _get_device_volume(self, device_name: str) -> int:
        """Внутренний метод для получения громкости (0-100)."""
        if not device_name:
            return 0
        try:
            import pythoncom
            pythoncom.CoInitialize()
            try:
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                devices = AudioUtilities.GetAllDevices()
                for device in devices:
                    if device.FriendlyName == device_name:
                        target = getattr(device, "_dev", None)
                        if target is None:
                            target = getattr(device, "device", device)
                            
                        if hasattr(target, "Activate"):
                            interface = target.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                            volume_interface = interface.QueryInterface(IAudioEndpointVolume)
                            current_volume = volume_interface.GetMasterVolumeLevelScalar()
                            return int(round(current_volume * 100))
            finally:
                pythoncom.CoUninitialize()
        except Exception:
            pass
        return 0

    def _set_device_volume(self, device_name: str, volume: int) -> bool:
        """Внутренний метод для установки громкости (0-100)."""
        if not device_name:
            return False
        try:
            import pythoncom
            pythoncom.CoInitialize()
            try:
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                devices = AudioUtilities.GetAllDevices()
                for device in devices:
                    if device.FriendlyName == device_name:
                        target = getattr(device, "_dev", None)
                        if target is None:
                            target = getattr(device, "device", device)
                            
                        if hasattr(target, "Activate"):
                            interface = target.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                            volume_interface = interface.QueryInterface(IAudioEndpointVolume)
                            volume_interface.SetMasterVolumeLevelScalar(volume / 100.0, None)
                            return True
            finally:
                pythoncom.CoUninitialize()
        except Exception as e:
            print(f"[Tn] Set volume error: {e}")
        return False

