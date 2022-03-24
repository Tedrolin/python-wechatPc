import asyncio
import json
import logging
import traceback
from typing import List, Callable

import websockets
from websockets.client import WebSocketClientProtocol

from .models.websocket import *


class WechatPc:
    conn: Union[None, WebSocketClientProtocol]
    logger: logging.Logger = logging.getLogger('python.wechatPc')

    def __init__(self, url: str):
        self.clients = {}
        self.url = url
        self.conn = None
        self.rebindingQueue = asyncio.Queue()

    def register_client(self, wechat_id: str):
        obj = WechatPcClient(wechat_id, self)
        self.clients[wechat_id] = obj
        return obj

    async def connect(self):
        self.conn = await websockets.connect(self.url)

    async def run(self):
        while not self.conn.closed:
            response = await self.conn.recv()  # todo error handling
            try:
                event = json.loads(response)
                self.logger.debug(f'Received event: {event}')
                if 'opCode' in event and event['opCode'] == OPCODE_WECHAT_QRCODE and self.rebindingQueue.qsize() > 0:
                    old_wechat_id = self.rebindingQueue.get_nowait()
                    if 'wechatId' in event:
                        self.clients[old_wechat_id].wechat_id = event['wechatId']
                        self.clients[event['wechatId']] = self.clients[old_wechat_id]
                        del self.clients[old_wechat_id]
                if 'wechatId' in event and 'body' in event and event['wechatId'] in self.clients:
                    asyncio.get_running_loop().create_task(self.clients[event['wechatId']].event_handler(event))
                    # await self.clients[event['wechatId']].event_handler(event)
            except json.JSONDecodeError:
                continue
            except:
                traceback.print_exc()
                continue  # todo error handling


class WechatPcClient:
    def __init__(self, wechat_id: str, ws: WechatPc):
        self.wechat_id = wechat_id
        self.ws = ws
        self.handlers = {}
        self.logger: logging.Logger = logging.getLogger('python.wechatPcClient')

    def add_handler(self, event: Union[int, List[int]]):
        def wrapper(func: Callable):
            if not asyncio.iscoroutinefunction(func):
                raise Exception('Handler must be a coroutine function')
            nonlocal event
            if not isinstance(event, list):
                event = [event]
            for e in event:
                if e in self.handlers:
                    self.handlers[e].append(func)
                else:
                    self.handlers[e] = [func]
            return func
        return wrapper

    async def event_handler(self, event: dict):
        try:
            if 'opCode' in event and event['opCode'] in self.handlers:
                for h in self.handlers[event['opCode']]:
                    await h(event['body'])
        except:
            traceback.print_exc()  # todo error handling

    async def open(self):
        await self.ws.rebindingQueue.put(self.wechat_id)
        return await self.send(OpenWechatMsg(body={}))

    def close(self):
        return self.send(CloseWechatMsg())

    async def send(self, action: WebsocketMsg):
        action.wechatId = self.wechat_id
        self.logger.debug(action)
        if self.ws.conn and self.ws.conn.open:
            self.logger.debug(action.json())
            await self.ws.conn.send(action.json())

    def get_login_info(self):
        return self.send(GetLoginInfoMsg())

    def get_login_status(self):
        return self.send(GetLoginStatusMsg())

    def logout(self):
        return self.send(LogoutMsg())

    def send_text(self, wxid: str, content: str):
        return self.send(SendTextMsg(
            wechatId=self.wechat_id,
            body=SendTextBody(wxid=wxid, content=content)
        ))

    def send_image(self, wxid: str, image_url: str):
        return self.send(SendImageMsg(
            wechatId=self.wechat_id,
            body=SendImageBody(wxid=wxid, imageUrl=image_url)
        ))

    def send_file(self, wxid: str, file_url: str):
        return self.send(SendFileMsg(
            wechatId=self.wechat_id,
            body=SendFileBody(wxid=wxid, fileUrl=file_url)
        ))

    def send_card(self, wxid: str, xml: str):
        return self.send(SendCardMsg(
            wechatId=self.wechat_id,
            body=SendCardBody(wxid=wxid, xml=xml)
        ))

    def send_xml(self, xml_type: str, wxid: str, from_wxid: str, image_url: str, xml: str):
        return self.send(SendXmlMsg(
            wechatId=self.wechat_id,
            body=SendXmlBody(
                xmlType=xml_type,
                wxid=wxid,
                fromWxid=from_wxid,
                imageUrl=image_url,
                xml=xml
            )
        ))

    def add_friend(self, wxid: str, message: str):
        return self.send(FriendAddMsg(
            wechatId=self.wechat_id,
            body=FriendAddBody(wxid=wxid, message=message)
        ))

    def add_friend_v1(self, wxid: str, message: str):
        return self.send(FriendAddFromV1Msg(
            wechatId=self.wechat_id,
            body=FriendAddFromV1Body(wxid=wxid, message=message)
        ))

    def delete_friend(self, wxid: str):
        return self.send(FriendDeleteMsg(
            wechatId=self.wechat_id,
            body=FriendDeleteBody(wxid=wxid)
        ))

    def verify_friend(self, v1: str, v2: str):
        return self.send(FriendVerifyMsg(
            wechatId=self.wechat_id,
            body=FriendVerifyBody(v1=v1, v2=v2)
        ))

    def get_friend_list(self):
        return self.send(FriendListMsg(wechatId=self.wechat_id))

    def create_room(self, wxid1: str, wxid2: str):
        return self.send(RoomCreateMsg(
            wechatId=self.wechat_id,
            body=RoomCreateBody(wxid1=wxid1, wxid2=wxid2)
        ))

    def set_friend_remark(self, wxid: str, remark: str):
        return self.send(SetFriendRemarkMsg(
            wechatId=self.wechat_id,
            body=SetFriendRemarkBody(wxid=wxid, remark=remark)
        ))

    def edit_room_name(self, room_id: str, room_name: str):
        return self.send(EditRoomNameMsg(
            wechatId=self.wechat_id,
            body=EditRoomNameBody(roomId=room_id, roomName=room_name)
        ))

    def set_room_announcement(self, room_id: str, announcement: str):
        return self.send(SetRoomAnnouncementMsg(
            wechatId=self.wechat_id,
            body=SetRoomAnnouncementBody(roomId=room_id, announcement=announcement)
        ))

    def get_room_member_list(self, room_id: str):
        return self.send(RoomMemberListMsg(
            wechatId=self.wechat_id,
            body=RoomMemberListBody(roomId=room_id)
        ))

    def add_room_member(self, room_id: str, wxid: str):
        return self.send(RoomAddMemberMsg(
            wechatId=self.wechat_id,
            body=RoomAddMemberBody(roomId=room_id, wxid=wxid)
        ))

    def delete_room_member(self, room_id: str, wxid: str):
        return self.send(RoomDeleteMemberMsg(
            wechatId=self.wechat_id,
            body=RoomDeleteMemberBody(roomId=room_id, wxid=wxid)
        ))

    def at_room_member(self, room_id: str, wxid: str, nickname: str, message: str):
        return self.send(RoomAtMemberMsg(
            wechatId=self.wechat_id,
            body=RoomAtMemberBody(
                roomId=room_id,
                wxid=wxid,
                nickname=nickname,
                message=message
            )
        ))

    def quit_room(self, room_id: str):
        return self.send(RoomQuitMsg(
            wechatId=self.wechat_id,
            body=RoomQuitBody(roomId=room_id)
        ))

    def recv_transfer(self, wxid: str, transfer_id: str):
        return self.send(TransferRecvMsg(
            body=TransferRecvBody(wxid=wxid, transferId=transfer_id)
        ))

    def get_room_list(self, room_id: str):
        return self.send(RoomMemberListMsg(
            wechatId=self.wechat_id,
            body=RoomMemberListBody(roomId=room_id)
        ))
