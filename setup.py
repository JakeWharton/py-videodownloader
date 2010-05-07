#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='videodownloader',
    version='1.2.4',
    author='Jake Wharton',
    author_email='jakewharton@gmail.com',
    url='http://github.com/JakeWharton/py-videodownloader',
    download_url='http://github.com/JakeWharton/py-videodownloader/downloads',
    description='Python module and script for downloading video source files from the major online streaming sites (YouTube, Vimeo, etc.)',
    long_description='Python module and script for downloading video source files from the major online streaming sites (YouTube, Vimeo, etc.)',
    packages=find_packages(),
    keywords='youtube vimeo download streaming video save',
    license='Apache License, Version 2.0',
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
    scripts=[
        'videodownloader/videodownloader.py',
    ],
)
