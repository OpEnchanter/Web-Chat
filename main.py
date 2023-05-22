import asyncio
import socket
import websockets


def boot():
  hostname = socket.gethostname()
  ip = socket.gethostbyname(hostname)
  print(f"Server is being run on: {ip}")


def parseConnectionData(data):
  # ip|username|serverId|Server Password|Message
  return data.split("|")


class chatServer():

  def __init__(self, serverId, password):
    print(f"Server {serverId} started")
    self.serverId = serverId
    self.password = password
    self.msglog = []

  async def handle_connection(self, websocket, path):
    async for data in websocket:
      print(f"Data: {data}")
      parsed_data = parseConnectionData(data)
      print(f"Parsed Data: {parsed_data}")
      if int(
          parsed_data[2]) == self.serverId and parsed_data[3] == self.password:
        self.msglog.append(f"{parsed_data[1]}: {parsed_data[4]}§")
        await websocket.send('\n'.join(self.msglog))

  async def run(self):
    async with websockets.serve(self.handle_connection, "127.0.0.1", 80):
      print("Started on port 80")
      await asyncio.Future()  # Keeps the server running indefinitely


boot()

cs1 = chatServer(0, "")

asyncio.run(cs1.run())
