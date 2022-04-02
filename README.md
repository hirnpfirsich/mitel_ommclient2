# Mitel OMMClient2

Another attempt for a modern client library to the Mitel OM Application XML Interface.

## Quicksart

Just some examples to give you an idea what this does.

```
import mitel_ommclient2

# Connect to your OMM
c = mitel_ommclient2.OMMClient2("omm.local", "admin", "admin")

# Use built in methods for common actions
c.ping()

# Create custom messages
r = c.connection.request(mitel_ommclient2.messages.Ping(timeStamp=2342))
```

Consult class documentation for more in depth examples and options.

## Attribution

This software is inspired by `python-mitel` by Thomas and n-st.
