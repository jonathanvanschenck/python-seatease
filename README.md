# SeaTease
A software emulator for the [`python-seabreeze`](https://github.com/ap--/python-seabreeze) : Python module for Ocean Optics spectrometers.

The purpose of this library is to create an all-software emulator of the `python-seabreeze`
library, so that developers (like the authors) who wish create packages which utilize
seabreeze need not have a physical spectrometer on-hand to test their software.

Currently only parts of the `seabreeze.cseabreeze` backend and parts of the
`seabreeze.spectrometers` modules are emulated (here as `seatease.cseatease` and
`seatease.spectrometers` respectively), but more functionality is planned in
later versions. Additionally, the emulator currently assumes only a single USB2000-like
spectrometer is connected (though this can be changed, see `seatease.cseatease._SeaTeaseAPI`).

This USB2000-like device is treated like it is constantly measuring a 500nm spectral feature
with constant photon flux, so changing the integration time will change the peak's appearent
number of counts.

# Installing
To install the current stable version:
```bash
 $ pip3 install seatease
```

# Basic Use
It is highly advised that one references the [`python-seabreeze`](https://github.com/ap--/python-seabreeze)
documentatation, as many of the quirks of `seatease` are intended so as to mimic the
actual `python-seabreeze` package.

Also see the examples folder for slightly more details.

## Frontend functionality
The main frontend functionality provided is the `seatease.spectrometers.Spectrometer`
class, which hosts all the main calls to the underlying (emulated) hardware device,
instances can be created three ways:
```python
# Get any spectrometer
spec = seatease.spectrometers.Spectrometer.from_first_available()

# Get a specific spectrometer
spec = seatease.spectrometers.Spectrometer.from_serial_number("your-serial-number")

# List the devices, and instantiate one of them
dev_list = seatease.spectrometers.list_devices()
print(dev_list) # Prints list of available devices
spec = seatease.spectrometers.Spectrometer(dev_list[0])
```
With the spectrometer instance, the exposed methods allow retrival of emulated
hardware attributes:
```python
# Print wavelengths
print(spec.wavelengths())

# Set integration time
spec.integration_time_micros(10*1000) # 10 ms

# Print intensities
print(spec.intensities())
```
Have fun!

## Backend functionality
Again, the [Backend API](https://python-seabreeze.readthedocs.io/en/latest/backend_api.html)
for the `seabreeze.cseabreeze` package is helpful in understanding the following:

### `SeaTeaseDevice`
The main backend functionality provided is the `seatease.cseatease.SeaTeaseDevice`
class, which hosts all the main calls to the underlying (emulated) hardware device.
However, it cannot (or rather, should not when trying to faithfully emulate `seabreeze`)
be instantiated directly, but rather the instances are instantiated when the module is 
imported, and a reference to these instances are kept in the `seatease.cseatease.SeaTeaseAPI`
instances. So, to actually get a `SeaTeaseDevice` instance:
```python
dev_list = sb.cseatease.SeaTeaseAPI.list_devices()
print(dev_list) # Prints available devices
dev = dev_list[0]
```

### `.f` Functionality
All the features of the device are stored as attributes of the `dev.f`, for example:
```python
# Get wavelengths
dev.f.spectrometer.get_wavelengths()

# Set integration time
dev.f.spectrometer.set_integration_time_micros(100*1000) # 100 ms

# Get intensities
dev.f.spectrometer.get_intensities()
```

### `.features` Functionality
Alternatively, the same attributes are exposed in dictionary form in `dev.features`
```python
# Get wavelengths
dev.features["spectrometer"][0].get_wavelengths()

# Set integration time
dev.features["spectrometer"][0].set_integration_time_micros(100*1000) # 100 ms

# Get intensities
dev.features["spectrometer"][0].get_intensities()
```

# Development
We are happy for any contributions from others! In particular, those with experience
using other Ocean Optics spectrometers (besides just the USB2000) with `python-seabreeze`
who can shed light on the expected features and functionality from those devices.
Also, just fleshing out the rest of the backend API.

For development, clone this directory, setup a python
virtual environment in the main directory and install:
```bash
 $ python3 -m venv venv
 $ source venv/bin/activate
 (venv) $ python3 setup.py install
```
After making changes to the source, re-run that last line to re-install.

## Using `venv` in Jupyter Lab
If you want to use jupyter lab to edit and test, add the venv kernel to jupyter's local
files so that you can run the .ipynb files:
```bash
 (venv) $ pip3 install ipykernel
 (venv) $ python3 -m ipykernel install --user --name=venv
```
To remove the kernel when you are done:
```bash
 (venv) $ jupyter kernelspec uninstall venv
```

## PyPI
Create the source files and upload:
```bash
 (venv) $ python3 setup.py sdist bdist_wheel 
 (venv) $ python3 -m twine upload dist/*
```
See: [here](https://packaging.python.org/tutorials/packaging-projects/) for more details.

# Acknowledgements
The authors would like to thank [Andreas Poehlmann](https://github.com/ap--) and collaborators for creating the original `python-seabreeze` package, which this library emulates in software. His package has been indispensable to our [research](http://sites.science.oregonstate.edu/~ostroveo/publications/index.html).

The authors would also like to thank Caylee Van Schenck for the excellent pun after which this
library is named.