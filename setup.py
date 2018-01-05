from setuptools import setup, find_packages

setup(
    name = "clickpecker",
    version = "0.1",
    packages = find_packages(exclude=["tests"]),

    install_requires = [
        "bitstring",
        "fuzzywuzzy",
        "numpy",
        "opencv-python",
        "Pillow>=5.0.0",
        "requests",
        "tesserocr",
        "packaging",
        "scikit-image"
    ],

)
