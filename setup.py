import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seatease",
    version="0.3",
    author="Jonathan D B Van Schenck",
    author_email="vanschej@oregonstate.edu",
    description="A software emulator for the `python-seabreeze` package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanvanschenck/seatease",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires = ['numpy'],
    install_requires = ['numpy']
)
