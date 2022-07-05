from setuptools import find_packages
from setuptools import setup
import os

def read(fname: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mu_bot",
    version = read("VERSION"),
    packages = find_packages(),
    install_requires = read("requirements.txt").splitlines()
)