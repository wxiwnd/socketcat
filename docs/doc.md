# SocketCat Document

## socketcat.py
The main code of socketcat implement.

### class SocketCatServer
**Constructor Defination**
```python
def __init__(self, addr:str, port:int, trustid):
    self.reader = None
    self.writer = None
    self.trustid = trustid
    self.listen_addr:str = addr
    self.listen_port:int = port
```

**Create a SocketCatServer object:**

```python
from socketcat import SocketCatServer
trustid = "very_secret_str"
sc = SocketCatServer('0.0.0.0', 20049, trustid)
```

**Start()**

Start SocketCat Server. You can define multiple SocketCatServer Objects without start.

**read_and_unpack()**

Read the next packet from reader stream, then return the decrypt data.

If the next packet is a HelloPacket, it will return trustid. And if decrypt failed(it always means trustid not the same), return None.

Else if the packet is a DataPacket, it will return the decrypted data(Normally no decrypt failed).

Else if the data is not a valid packet, return None.

### Private Methods
Internal implementation details.

## packet.py
The main code of packet definiation and encryption.

**HelloPacket** & **DataPacket**

See [SchematicsPDF](./SocketCat_schematics.pdf)

**pack()**

pack the packet and encrypt.

Return a packet.

## utils.py
The main code of utils functions.

**decrypt()**
A static method, decrypt data.
```python
from utils import PacketUtils
trustid = "very_secret_str"
data_encrypt = <placeholder>
data = PacketUtils.decrypt(trustid, data_encrypt)
```

Normally this method should be called by SocketCatServer

# RPC

## rpc.py
### class SocketCatRPC

Inherited from SocketCatServer.

This is a jsonRPC.

**add_function()**

Add a function in RPCServer's known functions.

This function should be implemented in Code Context.

```python
def TestFunction(*args, **kwargs):
    print("Test: args = {}, kwargs = {}".format(args, kwargs))
    return "TestFunction called"

trustid = "very_secret_str"
main_server = SocketCatRPC('0.0.0.0', 20049, trustid)
main_server.add_function(TestFunction)
```