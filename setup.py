from setuptools import setup, Extension

setup(
    name="trading_cpp",
    version="0.1.0",
    ext_modules=[
        Extension(
            "trading_cpp",
            sources=["trading_cpp.cpp"],  # adjust if needed
            language="c++",
        )
    ],
)
