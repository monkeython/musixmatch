__author__ = "Luca De Vitis <luca@monkeython.com>"
__version__ = '0.9'
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries',
]
__all__ = [
    'ws', 'api', 'base',
    'artist', 'track', 'lyrics', 'subtitle', 'album'
]
__copyright__ = "2011, %s " % __author__
__license__ = """
   Copyright (C) %s

      This program is free software: you can redistribute it and/or modify
      it under the terms of the GNU General Public License as published by
      the Free Software Foundation, either version 3 of the License, or
      (at your option) any later version.

      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.

      You should have received a copy of the GNU General Public License
      along with this program.  If not, see <http://www.gnu.org/licenses/>.
""" % __copyright__

__docformat__ = 'restructuredtext en'

__doc__ = """
:abstract: Python interface to Musixmatch API
:version: %s
:author: %s
:address: Via San Donato 10, 40127 Bologna (BO), Italy
:organization: Monkeython
:contact: http://www.monkeython.com
:copyright: %s
""" % (__version__, __author__, __license__)

import os

apikey = os.environ.get('musixmatch_apikey', None)
format = os.environ.get('musixmatch_format', 'json')

import api
import ws
