#!/usr/bin/env python

from setuptools import setup

setup(
    name='docker-volume-service',
    version='1.0.5',
    description='Docker Volume Service for Cloud Foundry',
    author='Dennis Mueller',
    author_email='dmueller@evoila.de',
    url='evoila.de',
    license='Apache-2.0',
    setup_requires=['setuptools>=17.1'],
    install_requires=['paho-mqtt==1.1'],
    packages=['docker_volume_service'],
    entry_points={
        'console_scripts': ['dvs = '
                            'docker_volume_service.executer:main']
        },
)
