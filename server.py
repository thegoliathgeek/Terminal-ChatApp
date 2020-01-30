import asyncio
from aiohttp import web
import socketio
from json import dumps

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

@sio.event
async def join_chat(sid,message):
    print()
    print(message.get('name', sid) + ' joined to {}'.format(message['room']))
    sio.enter_room(sid, message['room'])

@sio.event
async def exit_chat(sid,message):
    sio.leave_room(sid, message['room'])

@sio.event
async def send_chat_room(sid, message):
        await sio.emit('get_message', {'message': message['message'], 'from': message['name']}, room=message['room'])

@sio.event
async def connect(sid, environ):
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')


if __name__ == '__main__':
    web.run_app(app)