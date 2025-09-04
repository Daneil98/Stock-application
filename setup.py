from setuptools import setup, Extension
import sys

def get_pybind_include():
    try:
        import pybind11
        return pybind11.get_include()
    except ImportError:
        return ""

ext_modules = [
    Extension(
        "trading_cpp",
        ["bindings.cpp"],
        include_dirs=[get_pybind_include(), "."],
        language="c++",
        extra_compile_args=["-O3"],
    ),
]

setup(
    name="trading_cpp",
    version="0.1",
    ext_modules=ext_modules,
    zip_safe=False,
    setup_requires=["pybind11>=2.6"],   # ensures pybind11 installs first
    install_requires=["pybind11>=2.6"],
)