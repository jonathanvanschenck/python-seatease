import numpy as np

import seatease.cseatease as _lib

SeaTeaseError = _lib.SeaTeaseError
SeaTeaseDevice = _lib.SeaTeaseDevice


def list_devices():
    return _lib.SeaTeaseAPI.list_devices()

class Spectrometer:
    _backend = _lib

    def __init__(self, device):
        if not isinstance(device, self._backend.SeaTeaseDevice):
            raise TypeError("device has to be a `SeaTeaseDevice`")
        self._dev = device
        self.open()  # always open the device here to allow caching values
        self._wavelengths = self.f.spectrometer.get_wavelengths()


    @classmethod
    def from_first_available(cls):
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
                    "Requested integration time ({0} us) outside limits: ({1} us,{2} us)".format(
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
        return self._dev.features

    @property
    def f(self):
        return self._dev.f

    def open(self):
        self._dev.open()

    def close(self):
        self._dev.close()
    
    def __repr__(self):
        return "<Spectralmeter %s:%s>" % (self.model, self.serial_number)
