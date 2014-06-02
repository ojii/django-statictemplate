#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from statictemplate import __version__


INSTALL_REQUIRES = [
    'django>=1.2',
]

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development',
]

setup(
    name='django-statictemplate',
    version=__version__,
    description=('This project aims at providing a compromise between dynamic '
        'error pages for Django (that use template tags etc and therefore '
        'potentially error too) and having to write static error pages by hand.'),
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
