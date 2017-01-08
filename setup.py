# coding: utf-8

from setuptools import setup

setup(
    name="ifv",
    packages=["ifv"],
    version="0.1.1",
    description="a simple common api client framework",
    url="https://github.com/MrLYC/IFV",
    author="MrLYC",
    author_email="imyikong@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords=["api", "client", "framework"],
    extras_require={
        "extend": ["requests>=2.7.0"],
    },
)
