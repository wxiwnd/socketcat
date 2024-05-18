import json
from packet import DataPacket
from socketcat import SocketCatServer


class SocketCatRPC(SocketCatServer):
    def __init__(self, addr: str, port: int, trustid):
        super().__init__(addr, port, trustid)
        self.functions = {}

    def add_function(self, fnptr, name=None):
        if name is None:
            name = fnptr.__name__
        
        self.functions[name] = fnptr

    async def _handle_data(self):
        data = await self.read_and_unpack()
        if (data == -1): return data

        print(f'Receive data: {data!r}')

        jsondata = json.loads(data.decode('utf-8'))
        func_name = jsondata.get('func_name', '')
        func_args = jsondata.get('func_args', None)
        func_kwargs = jsondata.get('func_kwargs', None)

        if (func_name in self.functions):
            status = '200'
            ret = self.functions[func_name](*func_args, **func_kwargs)
        
        else:
            status = '404'
            ret = 'Invalid function call'
        
        ret_data = {"status" : status, "ret" : ret}
        ret_json = json.dumps(ret_data)

        ret_packet = DataPacket(self.trustid, ret_json.encode()).pack()
        self.writer.write(ret_packet)
        await self.writer.drain()

        print(f'Response: {ret_data!r}')

        return 0
