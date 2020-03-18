# SeaTease
A software emulator for the `python-seabreeze` : Python module for Ocean Optics spectrometers



# Installing (Development)
Clone this repository, then create a virtual environment and install:
```bash
 $ python3 -m venv venv
 $ source venv/bin/activate
 (venv) $ python3 setup.py install
```
## Using `venv` in Jupyter Lab
```bash
 (venv) $ pip3 install ipykernel
 (venv) $ python3 -m ipykernel install --user --name=venv
```
This should make a `venv` kernel available in jupyter lab. To remove the kernel:
```bash
 (venv) $ jupyter kernelspec uninstall venv
 ```
# Development
For development, clone this directory, then have fun! Pro-tip: setup a python
virtual environment in the main directory:
```bash
 $ python3 -m venv venv
 $ source venv/bin/activate
```
## Installing
```bash
 (venv) $ python3 setup.py install
```

## Creating source packages
```bash
 (venv) $ python3 setup.py sdist bdist_wheel 
```

## Uploading to PyPI
```bash
 (venv) $ python3 -m twine upload dist/*
```

See: [https://packaging.python.org/tutorials/packaging-projects/]

# Acknowledgements
The authors would like to thank [Andreas Poehlmann](https://github.com/ap--) for creating the original `python-seabreeze` package, which this library emulates in software. His package has been indispensable to our [research](http://sites.science.oregonstate.edu/~ostroveo/publications/index.html).
