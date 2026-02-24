import asyncio
from bleak import BleakScanner, BleakClient

class BluetoothManager:
    """Менеджер для работы с Bluetooth устройствами через Bleak."""

    def __init__(self):
        self._loop = asyncio.new_event_loop()

    async def _get_address_by_name(self, device_name: str):
        """Поиск MAC-адреса устройства по его FriendlyName."""
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name == device_name:
                return d.address
        return None

    async def _connect_async(self, device_name: str) -> bool:
        """Асинхронная попытка подключения к устройству."""
        address = await self._get_address_by_name(device_name)
        if not address:
            print(f"[BluetoothManager] Device '{device_name}' not found during scan.")
            return False
        
        try:
            async with BleakClient(address, timeout=10.0) as client:
                is_connected = await client.connect()
                print(f"[BluetoothManager] Connection to {device_name} ({address}): {is_connected}")
                return is_connected
        except Exception as e:
            print(f"[BluetoothManager] Error connecting to {device_name}: {e}")
            return False

        try:
            import threading
            result = [[]]
            thread = threading.Thread(target=_run_get_paired, args=(result,))
            thread.start()
            thread.join(timeout=10.0)
            return result[0]
        except Exception as e:
            print(f"[BluetoothManager] Get paired devices error: {e}")
            return []

    def connect_device(self, device_name: str) -> bool:
        """Синхронная обертка для подключения устройства."""
        try:
            # Запуск асинхронной задачи в отдельном цикле событий
            return self._loop.run_until_complete(self._connect_async(device_name))
        except Exception as e:
            print(f"[BluetoothManager] Loop error: {e}")
            return False

    async def _get_paired_async(self):
        """Получение списка сопряженных устройств (через сканнер)."""
        devices = await BleakScanner.discover()
        return [d.name for d in devices if d.name]

    def get_paired_devices(self):
        """Синхронная обертка для получения списка устройств."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    res_list[0] = loop.run_until_complete(self._get_paired_async())
                finally:
                    loop.close()
            except Exception as e:
                print(f"[BluetoothManager] Get paired devices thread error: {e}")
                res_list[0] = []
