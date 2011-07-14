Quick start
===========

1. First thing first, read the documentation at http://developers.musixmatch.com/documentation .
2. Get an api key by signing up at http://developers.musixmatch.com/mmplans .
3. Install the musixmatch package
4. Run the python prompt

>>> import musixmatch
>>> apikey = '<your-apikey>'
>>> chart = musixmatch.ws.track.chart.get(country='it', apikey=apikey)
>>> print chart

It's that simple. Last, you can brows this documentation and have fun with the other modules.

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
   the response message format to query for
musixmatch_apiversion
   the api version to use in queryes

