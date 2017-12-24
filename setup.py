from setuptools import setup, find_packages

setup(
    name = "Clickpecker",
    version = "0.1",
    packages = find_packages("clickpecker"),
    package_dir = {"":"clickpecker"},

    install_requires = [
        "bitstring==3.1.5",
        "fuzzywuzzy==0.15.1",
        "numpy==1.13.1",
        "opencv.python==3.3.0.10",
        "Pilow==4.2.1",
        "requests==2.18.4",
        "tesserocr==2.2.2"
    ],

)
