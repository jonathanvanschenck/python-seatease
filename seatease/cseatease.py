"""Module seatease.cseatease

Intended to emulate `seabreeze.cseabreeze`. This provides
the backend API for the seatease spectrometer classes. 
Either, one can use the base front end API (`seatease.spectrometers.Spectrometer`),
or one can directly use this backend API.

See the `seabreeze.cseabreeze` documentation for more
details.

Example ::

    import seatease.cseateast.SeaTeaseAPI as lib
    
    # Lists available devices
    print(lib.list_devices())
    
    # Get the first device
    dev = lib.list_devices()[0]
    
    # use .f to access device features:
    dev.f.spectrometer.get_wavelengths()
    
    # use .features to access device features
    dev.features['spectrometer'][0].get_wavelengths()
    
"""

# TODO
#  - Add the rest of the `SeaBreezeFeature` classes
#  - Implemenent all the other methods . . .
#  - Add additional spectrometer types (USB4000, etc)
#  - Add functionality to mimic other spectra

import numpy as np
from time import sleep

class _SeaTeaseAPI:
    """Class for `seatease.cseatease._SeaTeaseAPI`
    
    Intended to emulate the `seabreeze.cseabreeze.SeaBreezeAPI` module.
    To mimic the hardware behavior (where only a single instance of 
    each device can exist), this class is used to create a single
    `SeaTeaseAPI` object, which can then be imported by other files.
    This object has a defined number of emulated devices instantiated,
    which when other programs reference them, it will properly raise
    `SeaTeaseError('Device already open')` errors if the requested
    device is being used by another thread.
    
    For testing other configurations of spectrometers, override
    the `SeaTeaseAPI = _SeaTeaseAPI.one_usb2000()` code in this 
    module to instantiate however many devices of whatever type
    you desire.
    
    :param dev_list: A list of `SeaTeaseDevice` instances which are
                     to emulate the spectrometers currently "plugged in"
    """
    def __init__(self, dev_list):
        self.__spectrometers = dev_list
        
    @classmethod
    def one_usb2000(cls):
        return cls([SeaTeaseDevice("1")])
    
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
    """Class for `seatease.cseatease.SeaTeaseDevice`
    
    Intended to emulate `seabreeze.cseabreeze.SeaBreezeDevice`. See
    that documentation for more details. Currently, there is only
    support for a USB2000-like device, more devices are to be 
    added in future versions.
    
    :param serial_number: String representing the serial number of 
                            the spectrometer device.
    """
    def __init__(self, serial_number = "1"):
        self.__serial_number = serial_number
        self.__connected = False
        self.__f = f()
        self.__features = {k:[self.__f.__getattribute__(k)] for k in self.__f._attr}
    
    # IDEA:
    #  - Add a set of classmethods which will instantiate different kinds of 
    #     spectrometer types: e.g. SeaTeaseDevice.from_usb2000("1"),
    #     SeaTeaseDevice.from_usb4000("1"), etc. 
    #     To do so, it might be better to als add class methods to f
    #     (f.from_usb2000(), ... ) and then have a single class method
    #     here like SeaTeaseDevice.from_device_type("usb2000")
    
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
    """The `seatease.cseatease.SeaTeaseDevice` features class
    
    This class emulates the features 'attribute' of the 
    `seabreeze.cseabreeze.SeaBreezeDevice` instance, which
    allows '.f' API calls to the backend seabreeze library.
    See `python-seabreeze` backend documentation for details.
    
    Currently, this class only emulates a USB2000-like
    spectrometer, further emulation is projected for the future.
    """
    _attr = ["spectrometer","eeprom"]
    def __init__(self):
        self.spectrometer = SeaTeaseSpectrometerFeature()
        self.eeprom = SeaTeaseEEPROMFeature()
        

class SeaTeaseFeature:
    """Base `seatease.cseatease.SeaTeaseFeature` class
    """
    # As far as I can tell, this class in seabreeze doesn't
    #  do anything other than be inhereted from...
    pass

#class SeaTeaseRawUSBBusAccessFeature(SeaTeaseFeature):
#    def __init__(self):
#        pass
#    def raw_usb_read(self, endpoint, buffer_length):
#        raise NotImplementedError("TODO")
#    def raw_usb_write(self, data, endpoint):
#        raise NotImplementedError("TODO")

        
class SeaTeaseSpectrometerFeature(SeaTeaseFeature):
    """The `seatease.cseatease.SeaTeaseSpectrometerFeature` class
    
    This class emulates the spectrometer features of a seabreeze
    device. See the `seabreeze.cseabreeze.SeaBreezeSpectrometerFeature`
    documentations for details.
    
    Current emulation only supports a USB2000-like spectrometer,
    which has a 4096 pixel ccd, ranges from ~300-1000nm and has 
    a max count of ~4000. Further emulation is projected in future
    versions.
    
    The spectra that this device 'measures' is a single peak at 500nm
    with a FWHM of ~ 40nm (think PL from a quantum dot, or something).
    The intensities are scaled by the integration time and noise is 
    added to roughly match what I have seen on my actual USB2000 device.
    """
    def __init__(self):
        # Values based roughly on a USB2000 device
        self.__it = 100*1000 # us (100ms)
        self.__itmin = 3*1000 # us (3ms)
        self.__itmax = 20*1000*1000 # us (20s)
        self.__w = np.linspace(300.0,1000.0,4096)
        # IDEA:
        #   Add functionality to create a 'spectrum' function
        self.__i = np.exp(-(self.__w-500)**2/20)/100
        self.__imax = 4000.0
    
    # Is it overkill to double encapsulate the IT?
    @property
    def _it(self):
        return self.__it
    @_it.setter
    def _it(self,it):
        # Clip the integration time based on the min/max
        self.__it = int(np.clip(it, self.__itmin, self.__itmax))
    
    def get_electric_dark_pixel_indices(self):
        # No dark pixel functionality
        return []
    
    def get_integration_time_micros_limits(self):
        return self.__itmin, self.__itmax
        
    def get_intensities(self):
        # Have processor sleep to mimic measurement
        sleep(self._it*1e-6)
        # Scale signal based on IT
        signal = self.__i * self._it
        # This noise looks right-ish
        noise = np.random.uniform(0,10,size=4096)
        # Clip results to mimic ccd flooding
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
    """The `seatease.cseatease.SeaTeaseEEPROMFeature` class
    
    This class emulates the spectrometer features of a seabreeze
    device. See the `seabreeze.cseabreeze.SeaBreezeEEPROMFeature`
    documentations for details.
    
    """
    def __init__(self):
        pass    
    def eeprom_read_slot(self, slot_number, strip_zero_bytes):
        raise NotImplementedError("TODO")
    
    

class SeaTeaseError(Exception):
    """Base `SeaTeaseError`
    
    This is the main exception class which is raised for
    all errors resulting from hardward calls.
    """
    pass
    
    
SeaTeaseAPI = _SeaTeaseAPI.one_usb2000()

__all__ = ['SeateaseAPI']