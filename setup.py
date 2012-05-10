#!/usr/bin/env python

from setuptools import setup
import os.path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setupconf = dict(
    name = 'flask_bundle',
    version = '0.1',
    license = 'BSD',
    url = 'https://github.com/Deepwalker/flask_bundle/',
    author = 'Svarga team, Deepwalker',
    author_email = 'krivushinme@gmail.com',
    description = ('Class based tool that behave like blueprints'),
    long_description = read('README.rst'),
    keywords = 'validatation form forms data schema',

    packages = ['trafaret'],

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        ],
    )

if __name__ == '__main__':
    setup(**setupconf)
