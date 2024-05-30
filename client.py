from socketcat import SocketCatClient
import asyncio
scc = SocketCatClient('127.0.0.1', 20049, 'very_trust_id')


scc.open_connection()
scc.interactive()

