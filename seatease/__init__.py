"""The SeaTease Module

This module emulates the behavior of the `python-seabreeze`
library when an Ocean Optics spectrometer is USB connected.
This library is intended to aid the development of `python-seabreeze`-
derived library, so that developers need not have physical access 
to spectrometer device during software development.

Many thanks to Andreas Poehlmann and collaborators for the development
of the `python-seabreeze` library.

"""
import seatease.cseatease
import seatease.spectrometers
