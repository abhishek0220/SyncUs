import socketio
from SyncUs.Schemas.message import BroadcastSchema
from SyncUs.utils.dataops import inMemDataBase

sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio)


@sio.on("connect")
def connect(sid, env):
    print(f"{sid} connected to websocket")


@sio.on("joined")
async def joined(sid, msg):
    access_token = msg
    inMemDataBase.addSid(sid, access_token)
    broadcastMsg = BroadcastSchema(msg="", sent_id=sid)
    print(f"{sid} joined")
    await sio.emit("userJoined", broadcastMsg.json())


@sio.on("message")
async def broadcast(sid, msg):
    print(f"{sid} sent msg to all")
    broadcastMsg = BroadcastSchema(msg=msg, sent_id=sid)
    await sio.emit("sendMessage", broadcastMsg.json())


@sio.on("disconnect")
async def disconnect(sid):
    broadcastMsg = BroadcastSchema(msg="", sent_id=sid)
    inMemDataBase.removeSid(sid)
    print(f"{sid} leaved")
    await sio.emit("leave", broadcastMsg.json())
