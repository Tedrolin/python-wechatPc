# Installation
1. Install this package from source
```
pip3 install -U git+https://github.com/tedrolin/python-wechatPc
```
2. (For developers) Examples
```python
import asyncio
import threading

from wechatPc import *
from wechatPc.models.websocket import *

w = WechatPc("ws://127.0.0.1:5678")
c = w.register_client("test")

@c.add_handler(OPCODE_WECHAT_QRCODE)
async def on_qr_code(msg: dict):
    print(msg)

@c.add_handler(OPCODE_MESSAGE_RECEIVE)
async def on_message_receive(msg: dict):
    print(msg['body'])
    await c.send_text("test123", f"I've received your message: {msg['body']}")

async def call_qr():
    await c.open()

loop = asyncio.new_event_loop()
loop.run_until_complete(w.connect())
loop.run_until_complete(asyncio.wait([w.run(), call_qr()]))
```
Notice: All the API calls are asynchronous, meaning that these API calls won't block the main thread. If you want to retrieve the results, please add handler for specific opcode.