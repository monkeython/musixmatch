Quick start
===========

1. First thing first, read the documentation at http://developers.musixmatch.com .
2. Get an api key by signing up at http://developers.musixmatch.com/mmplans .
3. Install the musixmatch package
4. Run the python prompt

>>> import musixmatch
>>> apikey = '<your-apikey>'
>>> try:
...     chart = musixmatch.ws.track.chart.get(country='it', apikey=apikey)
... except musixmatch.api.Error, e:
...     pass

It's that simple. Last, you can brows this documentation and have fun with the other modules.

Building / Installing
=====================

You can just use setup.py to build and install python-musixmatch::

   prompt $ python setup.py bdist_egg

Once built, you can use easy_install on the python egg.

Documentation
=============
You can read documentation online_, or generate your own local copy using
`Sphinx`_ trough the setup.py::

   prompt $ python setup.py build_sphinx

.. _Sphinx: http://sphinx.pocoo.org
.. _online: http://projects.monkeython.com/musixmatch/python-musixmatch/html/index.html

Unit testing
============
python-musixmatch comes with some essential unit testing. If you set up
**musixmatch_apikey** environment variable, and have internet connection, you
can also run some tests on API calls::

   prompt $ python setup.py test

Caching support
===============

Applications using python-musixmatch may take advantage of standard
urllib support for **http_proxy**, so they can just set up the proper
environment variable:

http_proxy
   the complete HTTP proxy URL to use in queries.

Considering all the available HTTP proxy solutions, I'm reluctant to implement
a further caching support. Though i can consider serialization support.

Environment variables
=====================

python-musixmatch takes advantage of operating system environment to get
**apikey**, **format** and api **version** values to use in API calls:

musixmatch_apikey
   the apikey value to use in query strings
musixmatch_format
   the response message format. For example: json
musixmatch_wslocation
   the webservice base url. For example: http://api.musixmatch.com/ws/1.1
musixmatch_apiversion
   the api version to use in queryes. For example: 1.1. Use of
   **musixmatch_apiversion** was deprecated in favour of
   **musixmatch_wslocation**.

