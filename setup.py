from setuptools import setup, find_packages

setup(
    name='usb_cannon',
    version='0.1.0',
    author='Shawn Crosby',
    author_email='scrosby@salesforce.com',
    packages=find_packages(),
    license='Keep it real',
    description='Controls my usb nerf cannon',
    long_description=open('README.md').read(),
)