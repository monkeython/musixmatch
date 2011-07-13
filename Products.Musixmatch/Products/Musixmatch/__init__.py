__author__ = "Luca De Vitis <dewhiskeys@gmail.com>"
__copyright__ = "2011, %s " % __author__
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License'
    'Operating System :: OS Independent',
    "Framework :: Plone",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

__all__ = ['content']

import os
here = os.path.dirname(__file__)
with open(os.path.join(here, 'version.txt'),'r') as version:
    __version__ = version.read()
with open(os.path.join(here, 'README.txt'),'r') as description:
    __description__ = description.read()
with open(os.path.join(here, 'LICENSE.txt'), 'r') as license:
    __license__ = """
   Copyright (C) %s ::

%s""" % (__copyright__, '\n'.join([ ' ' * 6 + line for line in license]))
del os, here

__docformat__ = 'restructuredtext en'

__doc__ = """
:abstract: %s
:version: %s
:author: %s
:address: Via San Donato 10, 40127 Bologna (BO), Italy
:organization: Monkeython
:contact: http://src.monkeython.org
:date: 2011-06-15
:copyright: %s
""" % (__description__.split('\n\n',1)[1], __version__, __author__, __license__)

PRODUCT = 'Musixmatch'
GLOBALS = globals()
SKINS = 'skins'

def initialize(self, context=None):
    from Products.CMFCore.DirectoryView import registerDirectory
    from Products.CMFCore import utils
    from Products.Archetypes.atapi import process_types
    from Products.Archetypes import listTypes
    try:
        from Products.CMFCore.permissions import setDefaultRoles
    except ImportError:
        from Products.CMFCore.CMFCorePermissions import setDefaultRoles


    registerDirectory(SKINS, GLOBALS)

    # kick content registration
    from Products.Musixmatch import content, tools

    # register archetypes content with the machinery
    content_types, constructors, fti = \
        process_types(listTypes(PRODUCT), PRODUCT)

    utils.ContentInit(
        '%s content' % PRODUCT,
        content_types = content_types,
        permission = "Add portal content",
        extra_constructors = constructors,
        fti = fti).initialize(self)

    utils.ToolInit(
        '%s tools' % PRODUCT,
        tools = [tools.proxy.MusixmatchProxy],
        icon='skins/musixmatch_images/tool.gif').initialize(self)
