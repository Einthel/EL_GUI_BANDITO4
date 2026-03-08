import os


class TnAudioManager:
    """Обертка над системным аудио-менеджером для Tune."""

    def __init__(self):
        self._output_devices: list[str] = []

    def refresh_output_devices(self) -> list[str]:
        """Получить список устройств вывода и залогировать их."""
        devices: list[str] = []
        default_name: str | None = None

        try:
            # Логика заимствована из sound_example.SoundCore.get_all_devices
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

            print(f"[Tn] Output devices count: {len(devices)}")
        except Exception as e:
            # Важно не ронять плагин, даже если подсистема звука не готова
            print(f"[TuneBandito] AudioManager error while listing outputs: {e}")

        self._output_devices = devices
        return devices

    def get_cached_output_devices(self) -> list[str]:
        """Вернуть последний закешированный список устройств."""
        return list(self._output_devices)

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

