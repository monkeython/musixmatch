==========
api module
==========

.. automodule:: musixmatch.api
   :undoc-members:
   :members: version

   .. autoexception:: Error
      :show-inheritance:

   .. autoexception:: ResponseError
      :show-inheritance:

   .. autoexception:: ResponseMessageError
      :show-inheritance:

   .. autoclass:: ResponseStatusCode
      :show-inheritance:

   .. autoclass:: ResponseMessage
      :members: status_code

   .. autoclass:: JsonResponseMessage

   .. autoclass:: QueryString
      :members: items

   .. autoclass:: Method
      :undoc-members:

   .. autoclass:: Request
      :undoc-members:
      :members: query_string, api_method, getResponse, getResponseMessage

