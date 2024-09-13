# SocketCat
Client and service implementation of socket communication based on Python asyncio

# TODO
1. CLI
2. Multiple Encryption Methods Support


### Documuments
[Packet Definition](docs/SocketCat_schematics.pdf)

 
[Full Document](docs/doc.md)

## Quick Start
### Setup enviroment

**Using Conda**

python version >= 3.11
```shell
conda install aioconsole pytest pyetest-asyncio pycryptodome
```
or create a new virtual enviroment:
```shell
conda create --name SocketCat python=3.11 aioconsole pytest pytest-asyncio pycryptodome
```

**Using Pip**
```shell
pip install aioconsole pytest pytest-asyncio pycryptodome
```

**Build & use package**
Prepare [poetry >= 1.8](https://python-poetry.org/)

And run:  
``` shell
poetry install
```
To build package:  
``` shell
poetry build
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
> Yay, you ran our software perfectly, great job!