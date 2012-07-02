#!/usr/bin/env python
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from setuptools import setup, find_packages
import os

execfile(os.path.join('dupinanny', 'version.py'))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name=PACKAGE,
    version=VERSION,
    description='Dupinanny',
    long_description=read('README'),
    author='Timothee Besset',
    url=WEBSITE,
    download_url=DOWNLOAD,
    packages=find_packages(),
    package_data={
        'dupinanny': ['config.cfg.sample'],
        },
    scripts=['dupinanny/dupinanny.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Archiving :: Backup',
        ],
    license=LICENSE,
    install_requires=[],
    extras_require={},
    zip_safe=False,
)
