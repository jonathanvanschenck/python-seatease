"""Module `seatease.spectrometers`

This module emulates the `seabreeze.spectrometers` module. This provides
the frontend API for the seatease spectrometer classes. 
Either, one can use this frontend API,
or one can directly use this backend API (`seatease.cseatease`).

Primarially, this library wraps the backend API, so check there
for more details.

Example Usage::

    dev_list = seatease.spectrometers.list_devices()
    
    spec = seatease.spectrometers.Spectrometer(dev_list[0])
    # Or: spec = seatease.spectrometers.Spectrometer.from_first_available()
    
    spec.integration_time_micros(3*1000) # sets IT to 3ms
    spec.intensities() # Returns fake spectra

    # Same as above, but at higher counts
    spec.integration_time_micros(100*1000) # sets IT to 100ms
    spec.intensities() # Returns fake spectra
    
    # Returns SeaTeaseError, device already open
    spec2 = seatease.spectrometers.Spectrometer(dev_list[0])
    
    # Does NOT return SeaTeaseError
    spec.close()
    spec2 = seatease.spectrometers.Spectrometer(dev_list[0])

"""

import numpy as np

# Pick cseatease as the backend
import seatease.cseatease as _lib

def list_devices():
    """List all available devices
    
    Returns
    -------
    val : list of `seatease.cseatease.SeaTeaseDevice`
        A list of the currently active SeaTeaseDevice
        instances. Note, some of these devices might
        already be open on another thread.
    """
    return _lib.SeaTeaseAPI.list_devices()

class Spectrometer:
    """Class for `seatease.spectrometers.Spectrometer`
    
    This class emulates the `seabreeze.spectrometers.Spectrometer`
    class. See that documentation for details. Primarially, this 
    is a frontend wrapper for the backend API, which exposes common
    calls (for a `seatease.cseatease.SeaTeaseDevice` instance: 
    `dev.f.spectrometer.get_wavelengths()`) more compactly (here 
    `dev.wavelengths()`).
    
    :param device: A `seatease.cseatease.SeaTeaseDevice` instance 
                    which will be wrapped. Typically, this is gotten
                    from `seatease.spectrometers.list_devices()`.
    
    Example Usage::
        
        spec = seatease.spectrometers.Spectrometer.from_first_available()
        
        print(spec.model) # Prints USB2000-esk
        
        spec.integration_time_micros(3*1000) # sets IT to 3ms
        spec.intensities() # Returns fake spectra
        
        # Same as above, but at higher counts
        spec.integration_time_micros(100*1000) # sets IT to 100ms
        spec.intensities() # Returns fake spectra
        
        # Returns SeaTeaseError (only one device is created by default)
        spec2 = seatease.spectrometers.Spectrometer.from_first_available()
        
        # Must be called before device can be re-instantiated
        spec.close()
        
        # Does NOT return SeaTeaseError
        spec2 = seatease.spectrometers.Spectrometer.from_first_available()
        
    """
    
    # Save a reference to the backend
    _backend = _lib

    def __init__(self, device):
        if not isinstance(device, self._backend.SeaTeaseDevice):
            raise TypeError("device has to be a `SeaTeaseDevice`")
        self._dev = device
        self.open()  # always open the device here to allow caching values
        self._wavelengths = self.f.spectrometer.get_wavelengths()
        

    @classmethod
    def from_first_available(cls):
        # Only open a closed device
        for dev in list_devices():
            if not dev.is_open:
                return cls(dev)
        else:
            raise cls._backend.SeaTeaseError("No unopened device found.")


    @classmethod
    def from_serial_number(cls, serial=None):
        if serial is None:  # pick first spectrometer
            return cls.from_first_available()

        for dev in list_devices():
            if dev.serial_number == str(serial):
                if dev.is_open:
                    raise cls._backend.SeaTeaseError("Device already opened.")
                else:
                    return cls(dev)
        else:
            raise cls._backend.SeaTeaseError("No device attached with serial number '%s'." % serial)


    def wavelengths(self):
        return self._wavelengths


    def intensities(self, correct_dark_counts=False, correct_nonlinearity=False):
        # No dark_counts or non_linearity support currently
        if correct_dark_counts:
            raise self._backend.SeaTeaseError("This device does not support dark count correction.")
        if correct_nonlinearity:
            raise self._backend.SeaTeaseError("This device does not support nonlinearity correction.")
        return self.f.spectrometer.get_intensities()


    @property
    def max_intensity(self):
        return self.f.spectrometer.get_maximum_intensity()

    def spectrum(self, correct_dark_counts=False, correct_nonlinearity=False):
        return np.vstack((self._wavelengths,
                          self.intensities(correct_dark_counts, correct_nonlinearity)))


    def integration_time_micros(self, integration_time_micros):
        itl = self.integration_time_micros_limits
        if int(np.clip(integration_time_micros,*itl)) != int(integration_time_micros):
            raise self._backend.SeaTeaseError(
                    "Requested integration time ({0} us) outside limits: ({1} us, {2} us)".format(
                        integration_time_micros,
                        *itl
                    )
                )
        return self.f.spectrometer.set_integration_time_micros(integration_time_micros)

    @property
    def integration_time_micros_limits(self):
        return self.f.spectrometer.get_integration_time_micros_limits()

    def trigger_mode(self, mode):
        self.f.spectrometer.set_trigger_mode(mode)

    @property
    def serial_number(self):
        return self._dev.serial_number

    @property
    def model(self):
        return self._dev.model

    @property
    def pixels(self):
        return self.f.spectrometer._spectrum_length

    @property
    def features(self):
        # Expose backend features attribute
        return self._dev.features

    @property
    def f(self):
        # Expose backend '.f' functionality
        return self._dev.f

    def open(self):
        self._dev.open()

    def close(self):
        self._dev.close()
    
    def __repr__(self):
        return "<Spectralmeter %s:%s>" % (self.model, self.serial_number)

    
__all__ = ['list_devices','Spectrometer']