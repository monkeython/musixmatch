from setuptools import setup
import sys
import os

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

name = 'musixmatch'
pkg = __import__(name)
author, email = pkg.__author__.rsplit(' ', 1)

with open(os.path.join(wd, 'README.rst'),'r') as readme:
    long_description = readme.read()

url = 'http://projects.monkeython.com/musixmatch',
egg = {
    'name': name,
    'version': pkg.__version__,
    'author': author,
    'author_email': email.strip('<>'),
    'url': url,
    'description': "Package to interface with the Musixmatch API",
    'long_description': long_description,
    'download_url': '%s/dists' % url,
    'classifiers': pkg.__classifiers__,
    'packages': [name],
    'include_package_data': True,
    'exclude_package_data': {name: ["*.rst", "docs", "tests"]},
    'test_suite': 'tests.suite'}

if __name__ == '__main__':
    setup(**egg)
