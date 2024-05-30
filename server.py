import os
from socketcat import SocketCatServer


trustid = 'very_trust_id'

main_server = SocketCatServer('0.0.0.0', 20049, trustid)
main_server.start()