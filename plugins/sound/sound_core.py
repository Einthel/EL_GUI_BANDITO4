import os
import time
from PySide6.QtCore import QObject, Signal
try:
    from loguru import logger
    # Настройка лога
    log_path = os.path.join(os.path.dirname(__file__), "sound_debug.log")
    logger.add(log_path, rotation="10 MB", level="DEBUG", encoding="utf-8")
except ImportError:
    class DummyLogger:
        def debug(self, msg): print(f"DEBUG: {msg}")
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def success(self, msg): print(f"SUCCESS: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
    logger = DummyLogger()

_CORE_KEEP_ALIVE = []

class SoundCore(QObject):
    """Логика для плагина sound. Системные вызовы только на стороне Bandito."""
    
    # Сигналы для обновления UI
    volume_changed = Signal(str, int)  # device_name, volume
    mute_changed = Signal(str, bool)   # device_name, is_muted
    
    def __init__(self, socket_client=None):
        super().__init__()
        self.socket_client = socket_client
        self._last_action_time = 0
        self._cooldown = 0.5  # Задержка 500мс между COM-вызовами
        
        self.devices = {
            "mic": {"volume": 50, "muted": False},
            "sound": {"volume": 70, "muted": False},
            "other": {"volume": 30, "muted": False}
        }
        self._callbacks = {}

    def _can_do_action(self):
        """Проверка кулдауна для предотвращения ошибок COM VTable."""
        now = time.time()
        if now - self._last_action_time < self._cooldown:
            return False
        self._last_action_time = now
        return True

    def handle_system_mute_change(self, device_type, is_muted):
        """Обработка изменения Mute из системы (только сервер)."""
        if device_type in self.devices:
            if self.devices[device_type]["muted"] != is_muted:
                self.devices[device_type]["muted"] = is_muted
                self.mute_changed.emit(device_type, is_muted)

    def handle_system_volume_change(self, device_type, volume):
        """Обработка изменения громкости из системы (только сервер)."""
        if device_type in self.devices:
            if self.devices[device_type]["volume"] != volume:
                self.devices[device_type]["volume"] = volume
                self.volume_changed.emit(device_type, volume)

    def get_all_devices(self):
        """Список активных устройств вывода (только сервер)."""
        try:
            from libs.audio_manager import audioSwitch as switcher
            return list(switcher.MyAudioUtilities.getAllDevices("output").keys())
        except:
            return []

    def get_all_mic(self):
        """Список активных микрофонов (только сервер)."""
        try:
            from libs.audio_manager import audioSwitch as switcher
            return list(switcher.MyAudioUtilities.getAllDevices("input").keys())
        except:
            return []

    def set_device(self, device_name: str):
        """Установка устройства по умолчанию (только сервер)."""
        if not self._can_do_action(): return False
        try:
            import pythoncom
            pythoncom.CoInitialize()
            from libs.audio_manager import audioSwitch as switcher
            all_devices = switcher.MyAudioUtilities.getAllDevices("output")
            device_id = all_devices.get(device_name)
            if not device_id: return False
            switcher.switchOutput(device_id, switcher.pc.ERole.eConsole)
            switcher.switchOutput(device_id, switcher.pc.ERole.eMultimedia)
            switcher.switchOutput(device_id, switcher.pc.ERole.eCommunications)
            return True
        except:
            return False

    def set_volume(self, device, value):
        """Установка громкости."""
        if device in self.devices:
            self.devices[device]["volume"] = value
            self.volume_changed.emit(device, value)
            
            # Установка громкости в системе (только на сервере)
            try:
                import pythoncom
                pythoncom.CoInitialize()
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from ctypes import POINTER, cast
                from comtypes import CLSCTX_ALL
                
                sys_device = AudioUtilities.GetMicrophone() if device == "mic" else AudioUtilities.GetSpeakers()
                interface = sys_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                
                logger.debug(f"[SoundCore] Setting system volume: {device} -> {value}%")
                volume_interface.SetMasterVolumeLevelScalar(value / 100.0, None)
                
                # КРИТИЧЕСКИЙ МОМЕНТ: Сохраняем в ГЛОБАЛЬНЫЙ список
                global _CORE_KEEP_ALIVE
                _CORE_KEEP_ALIVE.append((sys_device, interface, volume_interface))
                
                # Ограничиваем размер списка, чтобы не было утечки памяти, но объекты жили долго
                if len(_CORE_KEEP_ALIVE) > 50:
                    _CORE_KEEP_ALIVE.pop(0)
                    
            except ImportError:
                # На клиенте (Android/iOS) библиотек pycaw/pythoncom нет, это нормально
                pass
            except Exception as e:
                logger.error(f"[SoundCore] System volume error: {e}")
            finally:
                try:
                    import pythoncom
                    pythoncom.CoUninitialize()
                except: pass

            # ПРЕДОТВРАЩЕНИЕ ПАДЕНИЙ: Проверка socket_client
            if self.socket_client and not isinstance(self.socket_client, str):
                try:
                    self.socket_client.send_command("SOUND_SET_VOLUME", {"device": device, "value": value})
                except Exception as e:
                    print(f"[SoundCore] Socket error in set_volume: {e}")

    def get_mute_state(self, device_type="sound"):
        """Текущее состояние Mute (только сервер)."""
        try:
            import pythoncom
            pythoncom.CoInitialize()
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            # ...
        except ImportError:
            return False
        except:
            return False
        finally:
            try:
                import pythoncom
                pythoncom.CoUninitialize()
            except: pass

    def get_system_volume(self, device_type="sound"):
        """Получение текущего уровня громкости в % (0-100)."""
        try:
            import pythoncom
            pythoncom.CoInitialize()
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            # ...
        except ImportError:
            return 0
        except:
            return 0
        finally:
            try:
                import pythoncom
                pythoncom.CoUninitialize()
            except: pass

    def set_mute(self, device, value):
        """Установка Mute (только сервер)."""
        if not self._can_do_action(): return
        if device in self.devices:
            self.devices[device]["muted"] = value
            self.mute_changed.emit(device, value)
            try:
                import pythoncom
                pythoncom.CoInitialize()
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from ctypes import POINTER, cast
                from comtypes import CLSCTX_ALL
                sys_device = AudioUtilities.GetMicrophone() if device == "mic" else AudioUtilities.GetSpeakers()
                interface = sys_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume.SetMute(int(value), None)
                
                # Сохраняем для стабильности
                global _CORE_KEEP_ALIVE
                _CORE_KEEP_ALIVE.append((sys_device, interface, volume))
                if len(_CORE_KEEP_ALIVE) > 50: _CORE_KEEP_ALIVE.pop(0)

            except ImportError:
                pass
            except Exception as e:
                logger.error(f"[SoundCore] Set mute error: {e}")
            finally:
                try:
                    import pythoncom
                    pythoncom.CoUninitialize()
                except: pass

    def toggle_mute(self, device):
        """Переключение Mute."""
        if device in self.devices:
            new_state = not self.devices[device]["muted"]
            self.update_mute_state(device, new_state)
            # ПРЕДОТВРАЩЕНИЕ ПАДЕНИЙ: Проверка socket_client
            if self.socket_client and not isinstance(self.socket_client, str):
                try:
                    self.socket_client.send_command("SOUND_TOGGLE_MUTE", {"device": device, "value": new_state})
                except Exception as e:
                    print(f"[SoundCore] Socket error in toggle_mute: {e}")

    def update_mute_state(self, device, value):
        """Обновление состояния без команд."""
        if device in self.devices:
            self.devices[device]["muted"] = value
            self.mute_changed.emit(device, value)

