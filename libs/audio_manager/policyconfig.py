import ctypes
import comtypes
from ctypes import HRESULT, POINTER
from ctypes.wintypes import BOOL, LPCWSTR
from comtypes import COMMETHOD, GUID

# Константы для Windows PolicyConfig
IID_IPolicyConfig = GUID('{f8679f50-850a-41cf-9c72-430f290290c8}')
CLSID_PolicyConfigClient = GUID('{870af99c-171d-4f9e-af0d-e63df40c2bc9}')

class ERole:
    eConsole = 0
    eMultimedia = 1
    eCommunications = 2

class IPolicyConfig(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IPolicyConfig
    _methods_ = (
        COMMETHOD([], HRESULT, 'GetMixFormat', (['in'], LPCWSTR, 'pwstrDeviceId'), (['out'], POINTER(ctypes.c_void_p), 'pFormat')),
        COMMETHOD([], HRESULT, 'GetDeviceFormat', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], BOOL, 'bDefault'), (['out'], POINTER(ctypes.c_void_p), 'pFormat')),
        COMMETHOD([], HRESULT, 'ResetDeviceFormat', (['in'], LPCWSTR, 'pwstrDeviceId')),
        COMMETHOD([], HRESULT, 'SetDeviceFormat', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], ctypes.c_void_p, 'pEndpointFormat'), (['in'], ctypes.c_void_p, 'pMixFormat')),
        COMMETHOD([], HRESULT, 'GetProcessingPeriod', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], BOOL, 'bDefault'), (['out'], POINTER(ctypes.c_longlong), 'hnsDefaultDevicePeriod'), (['out'], POINTER(ctypes.c_longlong), 'hnsMinimumDevicePeriod')),
        COMMETHOD([], HRESULT, 'SetProcessingPeriod', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], POINTER(ctypes.c_longlong), 'hnsDevicePeriod')),
        COMMETHOD([], HRESULT, 'GetShareMode', (['in'], LPCWSTR, 'pwstrDeviceId'), (['out'], POINTER(ctypes.c_void_p), 'pMode')),
        COMMETHOD([], HRESULT, 'SetShareMode', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], POINTER(ctypes.c_void_p), 'pMode')),
        COMMETHOD([], HRESULT, 'GetPropertyValue', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], POINTER(ctypes.c_void_p), 'key'), (['out'], POINTER(ctypes.c_void_p), 'pValue')),
        COMMETHOD([], HRESULT, 'SetPropertyValue', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], POINTER(ctypes.c_void_p), 'key'), (['in'], POINTER(ctypes.c_void_p), 'pValue')),
        COMMETHOD([], HRESULT, 'SetDefaultEndpoint', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], ctypes.c_int, 'ERole')),
        COMMETHOD([], HRESULT, 'SetEndpointVisibility', (['in'], LPCWSTR, 'pwstrDeviceId'), (['in'], BOOL, 'bVisible')),
    )
