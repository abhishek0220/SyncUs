import socketio
from SyncUs.Schemas.message import BroadcastSchema
from SyncUs.utils.dataops import inMemDataBase

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio)


@sio.on("connect")
def connect(sid, env):
    print(f"{sid} connected to websocket")


@sio.on("joined")
async def joined(sid, msg):
    try:
        access_token = msg
        inMemDataBase.addSid(sid, access_token)
        broadcastMsg = BroadcastSchema(msg="", sent_id=sid)
        broadcastMsg.msg = f"{broadcastMsg.sent_from.display_name} joined the channel"
        print(f"{sid} joined")
    except Exception as e:
        print(e)
        await sio.emit("leave", "", room=sid)
        await sio.disconnect(sid)
    else:
        await sio.emit("system", broadcastMsg.json())


@sio.on("message")
async def broadcast(sid, msg):
    print(f"{sid} sent msg to all")
    broadcastMsg = BroadcastSchema(msg=msg, sent_id=sid)
    await sio.emit("sendMessage", broadcastMsg.json())


@sio.on("disconnect")
async def disconnect(sid):
    try:
        broadcastMsg = BroadcastSchema(msg="", sent_id=sid)
        broadcastMsg.msg = f"{broadcastMsg.sent_from.display_name} disconnected from channel"
        inMemDataBase.removeSid(sid)
    except Exception as e:
        print("user not exist")
    else:
        await sio.emit("system", broadcastMsg.json())
    print(f"{sid} leaved")
