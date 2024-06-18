from socketcat import SocketCatClient

def connect(addr='127.0.0.1', port=20049, trustid='very_trust_id'):
    scc = SocketCatClient(addr, port, trustid)
    scc.open_connection()
    scc.interactive()

if __name__ == "__main__":
    connect()
