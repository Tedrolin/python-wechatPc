from setuptools import setup, find_packages
import pathlib
import re

WORK_DIR = pathlib.Path(__file__).parent

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = ""
exec(open('wechatPc/__version__.py').read())


setup(
    name="wechatPc",
    version=__version__,
    description='Framework for WeChat hooks',
    author='tedrolin',
    author_email="undefined@example.com",
    url="https://github.com/tedrolin/python-wechatPc",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires='>=3.7',
    keywords=["wechatPc", ],
    install_requires=[
        "websockets",
        "pydantic"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent"
    ]
)