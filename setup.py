#!/usr/bin/env python

from setuptools import setup
import os.path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setupconf = dict(
    name = 'flask_bundle',
    version = '0.3',
    license = 'BSD',
    url = 'https://github.com/Deepwalker/flask_bundle/',
    author = 'Svarga team, Deepwalker',
    author_email = 'krivushinme@gmail.com',
    description = ('Class based tool that behaves like blueprints'),
    long_description = read('README.rst'),
    keywords = 'flask bundle',
    include_package_data = True,
    install_requires = ['Flask'],
    packages = ['flask_bundle'],
    download_url = 'git+git://github.com/Deepwalker/flask_bundle.git#egg=flask_bundle-dev',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )

if __name__ == '__main__':
    setup(**setupconf)
