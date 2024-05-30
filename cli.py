import argparse
import os

from socketcat import SocketCatServer
from client import connect

def start_server(address, port, trust_id):
    print(f"Starting server at {address}:{port}")
    main_server = SocketCatServer(address, port, trust_id)
    main_server.start()

def start_client(address, port, trust_id):
    print(f"Starting client at {address}:{port}")
    connect(address, port, trust_id)

def main():
    parser = argparse.ArgumentParser(description='SocketCat CLI')
    parser.add_argument('-s', '--server', action='store_true', help='Start as server')
    parser.add_argument('-c', '--client', action='store_true', help='Start as client')
    parser.add_argument('-a', '--address', default='localhost', help='Address to listen/connect')
    parser.add_argument('-p', '--port', type=int, default=20049, help='Port to listen/connect')
    parser.add_argument('-t', '--trust_id', default=os.getenv("TRUST_ID"), help='Trust ID for authentication')

    args = parser.parse_args()

    if args.server and args.client:
        print("Error: Only one of --server or --client can be specified.")
        return

    if args.server:
        start_server(args.address, args.port, args.trust_id)
    elif args.client:
        start_client(args.address, args.port, args.trust_id)
    else:
        print("Error: Either --server or --client must be specified.")

if __name__ == '__main__':
    main()