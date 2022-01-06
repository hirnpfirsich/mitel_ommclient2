# Mitel OMMClient2

Another attempt for a client library to the Mitel OM Application XML Interface.

## Quicksart

Just some examples to give you an idea what this does.

```
import mitel_ommclient2

# Connect to your OMM
c = mitel_ommclient2.OMMClient2("omm.local", "admin", "admin")

# Use built in methods for common actions
c.ping()

# Create custom messages
r = c.session.request(mitel_ommclient2.messages.Ping(timeStamp=2342))

# Craft your own request, if it is not implemented yet
r = c.session.request(mitel_ommclient2.messages.DictRequest("Ping", {"timeStamp": 2342}))
```

Consult class documentation for more in depth examples and options.
