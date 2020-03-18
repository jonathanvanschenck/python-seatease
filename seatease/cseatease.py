"""Module seatease.cseatease

Intended to emulate seabreeze.cseabreeze.
"""

# TODO
#  - Add the rest of the SeaBreezeFeature classes

import numpy as np
from time import sleep

class _SeaTeaseAPI:
    """Emulation of seabreeze.cseabreeze.SeaBreezeAPI module
    """
    def __init__(self, num_devices = 1):
        self.__spectrometers = [SeaTeaseDevice(str(i)) for i in range(1,num_devices+1)]
        
    def list_devices(self):
        return self.__spectrometers
    
    def aadd_rs232_device_location(self, device_type, bus_path, baudrate):
        raise NotImplementedError("TODO")
        
    def add_ipv4_device_location(self, device_type, ip_address, port):
        raise NotImplementedError("TODO")
        
    def initialize(self):
        raise NotImplementedError("TODO")
        
    def shutdown(self):
        pass
    
class SeaTeaseDevice:
    """Module for seatease.cseatease.SeaTeaseDevice
    Intended to emulate seabreeze.cseabreeze.SeaBreezeDevice
    """
    def __init__(self, serial_number = "1"):
        self.__serial_number = serial_number
        self.__connected = False
        self.__f = f()
        self.__features = {k:[self.__f.__getattribute__(k)] for k in self.__f._attr}
        
    def __repr__(self):
        return "<SeaTeaseDevice: {}>".format(self.__serial_number)
    
    @property
    def model(self):
        return "USB2000-esk"
    def get_model(self):
        return self.model
    
    @property
    def serial_number(self):
        return self.__serial_number
    def get_serial_number(self):
        return self.serial_number
    
    def close(self):
        self.__connected = False
        return None
    def open(self):
        self.__connected = True
        return None
    @property
    def is_open(self):
        return self.__connected
    
    @property
    def f(self):
        return self.__f
    @property
    def features(self):
        return self.__features
    
class f:
    _attr = ["spectrometer","eeprom"]
    def __init__(self):
        self.spectrometer = SeaTreezeSpectrometerFeature()
        self.eeprom = SeaTeaseEEPROMFeature()
        

class SeaTeaseFeature:
    pass

#class SeaTeaseRawUSBBusAccessFeature(SeaTeaseFeature):
#    def __init__(self):
#        pass
#    def raw_usb_read(self, endpoint, buffer_length):
#        raise NotImplementedError("TODO")
#    def raw_usb_write(self, data, endpoint):
#        raise NotImplementedError("TODO")

        
class SeaTreezeSpectrometerFeature(SeaTeaseFeature):
    def __init__(self):
        self.__it = 100*1000 # us (100ms)
        self.__itmin = 3*1000 # us (3ms)
        self.__itmax = 20*1000*1000 # us (20s)
        self.__w = np.linspace(300.0,1000.0,4096)
        self.__i = np.exp(-(self.__w-500)**2/20)/100
        self.__imax = 4000.0
        
    @property
    def _it(self):
        return self.__it
    @_it.setter
    def _it(self,it):
        self.__it = int(np.clip(it, self.__itmin, self.__itmax))
    
    def get_electric_dark_pixel_indices(self):
        return []
    
    def get_integration_time_micros_limits(self):
        return self.__itmin, self.__itmax
        
    def get_intensities(self):
        sleep(self._it*1e-6)
        signal = self.__i * self._it
        noise = np.random.uniform(0,10,size=4096)
        return np.clip(signal + noise + 100, 0, self.__imax) 
        
    def get_maximum_intensity(self):
        return self.__imax
        
    def get_wavelengths(self):
        return self.__w
        
    def set_integration_time_micros(self, integration_time_micros):
        self._it = integration_time_micros
        return None
    
    def set_trigger_mode(self, mode):
        raise NotImplementedError("TODO")
        
    
#class SeaTeasePixelBinningFeature(SeaTeaseFeature):
#    def __init__(self):
#        pass
#    @property
#    def binning_factor(self):
#        raise NotImplementedError("TODO")
#    @property
#    def default_binning_factor(self):
#        raise NotImplementedError("TODO")
#    def get_binning_factor(self):
#        raise NotImplementedError("TODO")
#    def get_default_binning_factor(self):
#        raise NotImplementedError("TODO")
#    def get_max_binning_factor(self):
#        raise NotImplementedError("TODO")
#    @property
#    def max_binning_factor(self):
#        raise NotImplementedError("TODO")
#    def set_binning_factor(self, factor):
#        raise NotImplementedError("TODO")
#    def set_default_binning_factor(self, factor):
#        raise NotImplementedError("TODO")
    
#class SeaTeaseThermoElectricFeature(SeaTeaseFeature):
#    def __init__(self):
#        pass
#    def enable_tec(self, state):
#        raise NotImplementedError("TODO")
#    def read_temperature_degrees_celsius(self):
#        raise NotImplementedError("TODO")
#    def set_temperature_setpoint_degrees_celsius(self, temperature):
#        raise NotImplementedError("TODO")
    
#class SeaTeaseIrradCalFeature(SeaTeaseFeature):
#    def __init__(self):
#        pass
#    def has_collection_area(self):
#        raise NotImplementedError("TODO")
#    def read_calibration(self):
#        raise NotImplementedError("TODO")
#    def read_collection_area(self):
#        raise NotImplementedError("TODO")
#    def write_calibration(self, calibration_array):
#        raise NotImplementedError("TODO")
#    def write_collection_area(self, area):
#        raise NotImplementedError("TODO")
    
#class SeaTeaseGPIOFeature(SeaTeaseFeature):
#    def __init__(self):
#        pass  
#    def get_egpio_available_modes(self, pin_number):
#        raise NotImplementedError("TODO")
#    def get_egpio_current_mode(self, pin_number):
#        raise NotImplementedError("TODO")
#    def get_egpio_output_vector_vector(self):
#        raise NotImplementedError("TODO")
#    def get_egpio_value(self, pin_number):
#        raise NotImplementedError("TODO")
#    def get_gpio_output_enable_vector(self):
#        raise NotImplementedError("TODO")
#    def get_gpio_value_vector(self):
#        raise NotImplementedError("TODO")
#    def get_number_of_egpio_pins(self):
#        raise NotImplementedError("TODO")
#    def get_number_of_gpio_pins(self):
#        raise NotImplementedError("TODO")
#    def set_egpio_mode(self, pin_number, mode, value):
#        raise NotImplementedError("TODO")
#    def set_egpio_output_vector(self, output_vector, bit_mask):
#        raise NotImplementedError("TODO")
#    def set_egpio_value(self, pin_number, value):
#        raise NotImplementedError("TODO")
#    def set_gpio_output_enable_vector(self, output_enable_vector, bit_mask):
#        raise NotImplementedError("TODO")
#    def set_gpio_value_vector(self, value_vector, bit_mask):
#        raise NotImplementedError("TODO")  
    
    
class SeaTeaseEEPROMFeature(SeaTeaseFeature):
    def __init__(self):
        pass    
    def eeprom_read_slot(self, slot_number, strip_zero_bytes):
        raise NotImplementedError("TODO")
    
    

class SeaTeaseError(Exception):
    pass
    
SeaTeaseAPI = _SeaTeaseAPI()

__all__ = ['SeateaseAPI']