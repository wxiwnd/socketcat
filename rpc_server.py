import os
from rpc import SocketCatRPC

trustid = os.getenv("TRUST_ID")

def TestFunction(*args, **kwargs):
    print("Test: args = {}, kwargs = {}".format(args, kwargs))
    return "TestFunction called"


main_server = SocketCatRPC('0.0.0.0', 20049, trustid)
main_server.add_function(TestFunction)

main_server.start()