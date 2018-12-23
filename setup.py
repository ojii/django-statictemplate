#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from statictemplate import __version__


INSTALL_REQUIRES = [
    'django>=1.6',
]

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Framework :: Django :: 1.10',
    'Framework :: Django :: 1.11',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development',
]

setup(
    name='django-statictemplate',
    version=__version__,
    description=(
        'This project aims at providing a compromise between dynamic '
        'error pages for Django (that use template tags etc and therefore '
        'potentially error too) and having to write static error pages by hand.'
    ),
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    url='https://github.com/ojii/django-statictemplate',
    packages=[
        'statictemplate',
        'statictemplate.management',
        'statictemplate.management.commands'
    ],
    license='LICENSE',
    platforms=['OS Independent'],
    install_requires=INSTALL_REQUIRES,
)
