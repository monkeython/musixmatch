from setuptools import setup
import sys
import os

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

name = 'musixmatch'
pkg = __import__(name)
author, email = pkg.__author__.rsplit(' ', 1)
email = email.strip('<>')

url='http://src.monkeython.org/'
version = pkg.__version__
classifiers = pkg.__classifiers__
readme = open(os.path.join(wd, 'docs', 'README.txt'),'r').readlines()
description = readme[0]
long_description = '\n'.join(readme[2:])

setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    url='%s/doc/%s' % (url, name),
    description=description,
    long_description=long_description,
    download_url='%s/eggs/%s' % (url, name),
    classifiers=classifiers,
    packages=[name],
    test_suite='tests.suite')

