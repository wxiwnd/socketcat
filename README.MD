# SocketCat
Client and service implementation of socket communication based on Python asyncio

Packet Defination See Doc/*.pdf

## Quick Start
### Setup enviroment

**Using Conda**

python version >= 3.8
```shell
conda install pytest pyetest-asyncio pycryptodome
```
or create a new virtual enviroment:
```shell
conda create --name SocketCat python=3.10 pytest pytest-asyncio pycryptodome
```

**Using Pip**
```shell
pip install pytest pycryptodome
```

### Start Test
1. Start Server:
```shell
TRUST_ID=<placeholder> python server.py
```
> Remember to change listen address and port if you like (in server.py).
 

> Note that server.py and socketcat.py is refactored version, you stiil can use legacy_server.py.

2. Start pytest

    At root folder:
```shell
cd test
TRUST_ID=<placeholder> pytest
```

### Test Screenshots:
Server Side:

<img src="https://s2.loli.net/2024/05/19/czJ8BT7REPuDpCg.png" alt=server width="70%">

Client Side:

<img src="https://s2.loli.net/2024/05/19/htMU1Qpoy5fCVNl.png" alt=client width="70%">

PyTest:

<img src="https://s2.loli.net/2024/05/19/lIH48kesBcOTmjh.png" alt=pytest width="70%">

<img src="https://s2.loli.net/2024/05/19/fBk3R8rZxHOIjun.png" alt=servertest width="70%">