Message Usage Manual
====================

The API consists of three main message types: request, response and event. They
are represented by :class:`mitel_ommclient2.messages.Request`, :class:`mitel_ommclient2.messages.Response`
and events aren't supported yet.

There are several subclasses for each messages type, but they are just just overlays
to provide a conveinient interface to message content using attributes.

Each message provides three attributes that define the central interfaces:

  * name
  * attrs
  * childs

Using messages
--------------

Just choose one of several message classes of :module:`mitel_ommclient2.messages`
and hand it over to :func:`mitel_ommclient2.client.OMMClient2.request` or
:func:`mitel_ommclient2.connection.Connection.request`.

.. code-block:: python

    import time

    my_time = int(time.time())

    request = mitel_ommclient2.messages.Ping(timeStamp=my_time)
    r = c.request(request)

    ping = r.timeStamp - my_time

Crafting your own messages
--------------------------

It some cases your message class isn't implemented yet. Then you can craft the
message yourself.

.. code-block:: python

    import time

    my_time = int(time.time())

    request = mitel_ommclient2.messages.Request("Ping")
    request.attrs = {
      "timeStamp": my_time,
    }
    r = c.request(request)

    ping = r.attrs["timeStamp"] - my_time
