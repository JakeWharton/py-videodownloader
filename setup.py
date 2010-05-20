#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='videodownloader',
    version='2.0.0',

    author='Jake Wharton',
    author_email='jakewharton@gmail.com',
    url='http://github.com/JakeWharton/py-videodownloader',
    license='Apache License, Version 2.0',

    description='Python module and script for downloading video source files from the major online streaming sites (YouTube, Vimeo, etc.)',
    long_description='Python module and script for downloading video source files from the major online streaming sites (YouTube, Vimeo, etc.)',
    keywords='youtube vimeo download streaming video save',

    packages=find_packages(),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities',
    ],

    entry_points = {
        'console_scripts': [
            'videodownloader = videodownloader.main:main',
        ],
    },
)
