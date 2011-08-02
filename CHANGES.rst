Changes
=======

0.9
   * Added support for XML response messages.
   * Deprecated **musixmatch_apiversion** environment variable in favour of
     **musixmatch_wslocation**. This will let developers to setup different api
     location and a testing environment. (musicae-ipsum under construction)
   * **apikey** and **format** in api.Method are now lookedup as follow:

     1. Positional arguments.
     2. Package wide variables.
     3. Operating system environment.

     Keyword arguments are not considered any more.
0.8
   * API interface with JSON response support.
   * Low level objects library built around JSON response messages.
