import json

from varint import *


class MCPacketBase:
    def __init__(self):
        self.Name = ''
        self.PacketID = 0xff
        self.BoundTo = ''


# Handshake状态
# 1/1
class HandShakeState(MCPacketBase):
    def __init__(self):
        MCPacketBase.__init__(self)
        self.state = "HandShake"


class Handshake(HandShakeState):
    def __init__(self, ver: int, addr: str, port: int, state: int):
        HandShakeState.__init__(self)
        self.ProtocolVersion = ver
        self.ServerAddress = addr
        self.ServerPort = port
        self.NextState = state
        self.PacketID = 0x00
        self.BoundTo = 'S'

    def send(self, sk):
        data = b''
        data += self.PacketID.to_bytes(1, 'big')
        data += varint(self.ProtocolVersion)
        data += MCString(self.ServerAddress)
        data += self.ServerPort.to_bytes(2, 'big')
        data += varint(self.NextState)
        packet = varint(len(data)) + data
        sk.send(packet)


# Status状态
# 4/4
class StatusState(MCPacketBase):
    def __init__(self):
        MCPacketBase.__init__(self)
        self.state = "Status"


class StatusRequest(StatusState):
    def __init__(self):
        self.PacketID = 0x00
        self.BoundTo = 'S'

    def send(self, sk):
        sk.send(b'\x01\x00')


class StatusResponse(StatusState):
    def __init__(self, data: bytes):
        if data[0] != 0x00:
            raise ValueError("packet ID 不对应")
        self.PacketID = data[0]
        data = data[1:]
        i = 0
        while data[i] >= 128:
            i += 1
        length = (de_varint(data[:i + 1]))
        data = data[i + 1:]
        if len(data) != length:
            raise ValueError("字符串长度不对应")
        self.Response = json.loads(data)

    def __repr__(self):
        data = ""
        data += f"Version: {self.Response['version']['name']}"
        try:
            data += f"\nDescription: {self.Response['description']['text']}"
        except KeyError:
            data += "Description: Unknown"

        data += f"\nPlayers: {self.Response['players']['online']}/{self.Response['players']['max']}"
        return data


class Ping(StatusState):
    def __init__(self, payload=123456):
        self.BoundTo = 'S'
        self.PacketID = 0x01
        self.Payload = payload

    def send(self, sk):
        data = b''
        data += b'\x09\x01'
        data += self.Payload.to_bytes(8, "big")
        sk.send(data)


class Pong(StatusState):
    def __init__(self, data: bytes):
        if data[0] != 0x01:
            raise ValueError("packet ID 不对应")
        self.PacketID = data[0]
        data = data[1:]
        if len(data) != 8:
            raise ValueError("字符串长度不对应")
        self.Payload = int.from_bytes(data, byteorder='big')


