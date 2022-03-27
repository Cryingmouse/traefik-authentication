from __future__ import unicode_literals

import io
import os
import re

from setuptools import setup, find_packages

__author__ = 'Jay Xu'


def version():
    desc = get_long_description()
    ret = re.findall(r'VERSION: (.*)', desc)[0]
    return ret.strip()


def here(filename=None):
    ret = os.path.abspath(os.path.dirname(__file__))
    if filename is not None:
        ret = os.path.join(ret, filename)
    return ret


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n\n')
    buf = []
    for filename in filenames:
        with io.open(here(filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


def get_description():
    return 'Python Authentication Module for DXN.'


def get_long_description():
    filename = 'README.md'
    return read(filename)


setup(
    name='dsm_auth',
    version=version(),
    packages=find_packages(),
    author='Jay Xu',
    author_email='jay.xu@lenovonetapp.com',
    maintainer='',
    maintainer_email='',
    url='',
    description=get_description(),
    license='Apache Software License',
    keywords=['DXN', 'Authentication'],
    include_package_data=True,

    platforms=['any'],
    long_description=get_long_description(),
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt')
)
