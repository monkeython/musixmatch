CHANGES
=======

0.9
   * Deprecated **musixmatch_apiversion** environment variable in favour of
     **musixmatch_wslocation**. This will let developers to set up different api
     location and setup a testing environment.
   * **apikey** and **format** positional arguments in api.Method now take
     precedence over keyword arguments.
   * Added support for XML response messages.

0.8
   * API interface with JSON response support.
   * Low level objects library built around JSON response messages.
