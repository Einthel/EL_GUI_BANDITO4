import comtypes
from pycaw.pycaw import AudioUtilities, DEVICE_STATE, EDataFlow
from pycaw.constants import CLSID_MMDeviceEnumerator
from pycaw.pycaw import IMMDeviceEnumerator
from . import policyconfig as pc

class MyAudioUtilities:
    @staticmethod
    def getAllDevices(direction, State=DEVICE_STATE.ACTIVE.value):
        """Возвращает словарь {Имя: ID} всех активных устройств."""
        devices = {}
        comtypes.CoInitialize()
        try:
            deviceEnumerator = comtypes.CoCreateInstance(
                CLSID_MMDeviceEnumerator,
                IMMDeviceEnumerator,
                comtypes.CLSCTX_INPROC_SERVER)
            
            flow = EDataFlow.eCapture.value if direction.lower() == "input" else EDataFlow.eRender.value
            collection = deviceEnumerator.EnumAudioEndpoints(flow, State)
            count = collection.GetCount()
            
            for i in range(count):
                dev = collection.Item(i)
                if dev:
                    createDev = AudioUtilities.CreateDevice(dev)
                    devices[createDev.FriendlyName] = createDev.id
        finally:
            comtypes.CoUninitialize()
        return devices

def switchOutput(deviceId, role):
    """Устанавливает устройство по умолчанию по его системному ID."""
    comtypes.CoInitialize()
    try:
        policy_config = comtypes.CoCreateInstance(
            pc.CLSID_PolicyConfigClient,
            pc.IPolicyConfig,
            comtypes.CLSCTX_ALL
        )
        policy_config.SetDefaultEndpoint(deviceId, role)
    finally:
        comtypes.CoUninitialize()
