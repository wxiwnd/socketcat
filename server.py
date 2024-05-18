import os
from socketcat import SocketCatServer


trustid = os.getenv("TRUST_ID")

main_server = SocketCatServer('0.0.0.0', 20049, trustid)
main_server.start()