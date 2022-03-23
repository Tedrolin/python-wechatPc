from enum import Enum
from typing import Union, Type, Literal

from pydantic import BaseModel, Field


class OpcodeEnum(Enum):
    OPCODE_READY = 0x00  # ws客户端准备完毕
    OPCODE_SUCCESS = 0x01  # 操作成功
    OPCODE_FAILURE = 0x02  # 操作失败
    OPCODE_WECHAT_OPEN = 0x10  # 新开一个微信客户端
    OPCODE_WECHAT_QUIT = 0x11  # 退出一个微信
    OPCODE_WECHAT_GET_LOGIN_STATUS = 0x12  # 获取登录状态
    OPCODE_MESSAGE_SEND_TEXT = 0x20  # 发送文本消息
    OPCODE_MESSAGE_SEND_IMAGE = 0x21  # 发送图片消息
    OPCODE_MESSAGE_SEND_FILE = 0x22  # 发送附件消息
    OPCODE_MESSAGE_SEND_CARD = 0x23  # 发送名片消息
    OPCODE_MESSAGE_SEND_XML = 0x24  # 发送xml消息
    OPCODE_FRIEND_ADD = 0x30  # wxid加好友
    OPCODE_FRIEND_ADD_FROM_V1 = 0x31  # v1加好友
    OPCODE_FRIEND_DELETE = 0x32  # 删除好友
    OPCODE_FRIEND_VERIFY = 0x33  # v1+v2同意好友请求
    OPCODE_FRIEND_LIST = 0x34  # 好友列表
    OPCODE_FRIEND_REMARK = 0x35  # 修改备注
    OPCODE_ROOM_CREATE = 0x40  # 创建群聊
    OPCODE_ROOM_EDIT_NAME = 0x41  # 修改群名称
    OPCODE_ROOM_ANNOUNCEMENT = 0x42  # 发送群公告
    OPCODE_ROOM_MEMBER_LIST = 0x43  # 获取群成员列表
    OPCODE_ROOM_ADD_MEMBER = 0x44  # 拉好友入群
    OPCODE_ROOM_DELETE_MEMBER = 0x45  # 删除群成员
    OPCODE_ROOM_AT_MEMBER = 0x46  # 艾特群成员
    OPCODE_ROOM_QUIT = 0x47  # 退出群聊
    OPCODE_TRANSFER_RECV = 0x50  # 收款
    OPCODE_WECHAT_QRCODE = 0x90  # 返回登录二维码地址
    OPCODE_LOGIN_INFO = 0x91  # 返回当前登录的微信号信息
    OPCODE_MESSAGE_RECEIVE = 0x92  # 返回接收的微信消息

OPCODE_READY                    = 0x00  # ws客户端准备完毕
OPCODE_SUCCESS                  = 0x01  # 操作成功
OPCODE_FAILURE                  = 0x02  # 操作失败
OPCODE_WECHAT_OPEN              = 0x10  # 新开一个微信客户端
OPCODE_WECHAT_QUIT              = 0x11  # 退出一个微信
OPCODE_WECHAT_GET_LOGIN_STATUS  = 0x12  # 获取登录状态
OPCODE_MESSAGE_SEND_TEXT        = 0x20  # 发送文本消息
OPCODE_MESSAGE_SEND_IMAGE       = 0x21  # 发送图片消息
OPCODE_MESSAGE_SEND_FILE        = 0x22  # 发送附件消息
OPCODE_MESSAGE_SEND_CARD        = 0x23  # 发送名片消息
OPCODE_MESSAGE_SEND_XML         = 0x24  # 发送xml消息
OPCODE_FRIEND_ADD               = 0x30  # wxid加好友
OPCODE_FRIEND_ADD_FROM_V1       = 0x31  # v1加好友
OPCODE_FRIEND_DELETE            = 0x32  # 删除好友
OPCODE_FRIEND_VERIFY            = 0x33  # v1+v2同意好友请求
OPCODE_FRIEND_LIST              = 0x34  # 好友列表
OPCODE_FRIEND_REMARK            = 0x35  # 修改备注
OPCODE_ROOM_CREATE              = 0x40  # 创建群聊
OPCODE_ROOM_EDIT_NAME           = 0x41  # 修改群名称
OPCODE_ROOM_ANNOUNCEMENT        = 0x42  # 发送群公告
OPCODE_ROOM_MEMBER_LIST         = 0x43  # 获取群成员列表
OPCODE_ROOM_ADD_MEMBER          = 0x44  # 拉好友入群
OPCODE_ROOM_DELETE_MEMBER       = 0x45  # 删除群成员
OPCODE_ROOM_AT_MEMBER           = 0x46  # 艾特群成员
OPCODE_ROOM_QUIT                = 0x47  # 退出群聊
OPCODE_TRANSFER_RECV            = 0x50  # 收款
OPCODE_WECHAT_QRCODE            = 0x90  # 返回登录二维码地址
OPCODE_LOGIN_INFO               = 0x91  # 返回当前登录的微信号信息
OPCODE_MESSAGE_RECEIVE          = 0x92  # 返回接收的微信消息


class Body(BaseModel):
    pass


class WebsocketMsg(BaseModel):
    wechatId: str
    opCode: int
    body = {}


class EditRoomNameBody(Body):
    roomId: str
    roomName: str


class EditRoomNameMsg(WebsocketMsg):
    opCode: int = Literal[0x41]
    body: EditRoomNameBody


class SetRoomAnnouncementBody(Body):
    roomId: str
    announcement: str


class SetRoomAnnouncementMsg(WebsocketMsg):
    opCode = OPCODE_ROOM_ANNOUNCEMENT
    body: SetRoomAnnouncementBody


class RoomMemberListBody(Body):
    roomId: str


class RoomMemberListMsg(WebsocketMsg):
    opCode = OPCODE_ROOM_MEMBER_LIST
    body: RoomMemberListBody


class RoomAddMemberBody(Body):
    roomId: str
    wxid: str


class RoomAddMemberMsg(WebsocketMsg):
    opCode = OPCODE_ROOM_ADD_MEMBER
    body: RoomAddMemberBody


class RoomDeleteMemberBody(Body):
    roomId: str
    wxid: str


class RoomDeleteMemberMsg(WebsocketMsg):
    opCode = OPCODE_ROOM_DELETE_MEMBER
    body: RoomDeleteMemberBody


class RoomAtMemberBody(Body):
    roomId: str
    wxid: str
    nickname: str
    message: str


class RoomAtMemberMsg(WebsocketMsg):
    opCode = OPCODE_ROOM_AT_MEMBER
    body: RoomAtMemberBody


class RoomQuitBody(Body):
    roomId: str


class RoomQuitMsg(WebsocketMsg):
    opCode = OPCODE_ROOM_QUIT
    body: RoomQuitBody


class TransferRecvBody(Body):
    roomId: str
    transferId: str


class TransferRecvMsg(WebsocketMsg):
    opCode = OPCODE_TRANSFER_RECV
    body: TransferRecvBody


class CloseWechatMsg(WebsocketMsg):
    opCode = OPCODE_WECHAT_QUIT
    body = {}


class OpenWechatMsg(WebsocketMsg):
    wechatId = '1234567890ABCDEFGHIJKLMNOPQRSTUV'
    opCode = OPCODE_WECHAT_OPEN
    body = {}


class GetLoginInfoMsg(WebsocketMsg):
    opCode = OPCODE_LOGIN_INFO
    body = {}


class GetLoginStatusMsg(WebsocketMsg):
    opCode = OPCODE_WECHAT_GET_LOGIN_STATUS
    body = {}


class LogoutMsg(WebsocketMsg):
    opCode = OPCODE_WECHAT_QUIT
    body = {}


class SendTextBody(Body):
    wxid: str
    content: str


class SendTextMsg(WebsocketMsg):
    opCode = OPCODE_MESSAGE_SEND_TEXT
    body: SendTextBody


class SendImageBody(Body):
    wxid: str
    imageUrl: str


class SendImageMsg(WebsocketMsg):
    opCode = OPCODE_MESSAGE_SEND_IMAGE
    body: SendImageBody


class SendFileBody(Body):
    wxid: str
    fileUrl: str


class SendFileMsg(WebsocketMsg):
    opCode = OPCODE_MESSAGE_SEND_FILE
    body: SendFileBody


class SendCardBody(Body):
    wxid: str
    xml: str


class SendCardMsg(WebsocketMsg):
    opCode = OPCODE_MESSAGE_SEND_CARD
    body: SendCardBody


class SendXmlBody(Body):
    type: str
    wxid: str
    fromWxid: str
    imageUrl: str
    xml: str


class SendXmlMsg(WebsocketMsg):
    opCode = OPCODE_MESSAGE_SEND_XML
    body: SendXmlBody


class FriendAddBody(Body):
    wxid: str
    message: str


class FriendAddMsg(WebsocketMsg):
    opCode = OPCODE_FRIEND_ADD
    body: FriendAddBody


class FriendAddFromV1Body(Body):
    v1: str
    message: str


class FriendAddFromV1Msg(WebsocketMsg):
    opCode = OPCODE_FRIEND_ADD_FROM_V1
    body: FriendAddFromV1Body


class FriendDeleteBody(Body):
    wxid: str


class FriendDeleteMsg(WebsocketMsg):
    opCode = OPCODE_FRIEND_DELETE
    body: FriendDeleteBody


class FriendVerifyBody(Body):
    v1: str
    v2: str


class FriendVerifyMsg(WebsocketMsg):
    opCode = OPCODE_FRIEND_VERIFY
    body: FriendVerifyBody


class FriendListMsg(WebsocketMsg):
    opCode = OPCODE_FRIEND_LIST
    body = {}


class RoomCreateBody(Body):
    wxid1: str
    wxid2: str


class RoomCreateMsg(WebsocketMsg):
    opCode = OPCODE_ROOM_CREATE
    body: RoomCreateBody


class SetFriendRemarkBody(Body):
    wxid: str
    remark: str


class SetFriendRemarkMsg(WebsocketMsg):
    opCode = OPCODE_FRIEND_REMARK
    body: SetFriendRemarkBody


def msgs() -> Type:
    return Union[tuple([
        EditRoomNameMsg,
        SetRoomAnnouncementMsg,
        RoomMemberListMsg,
        RoomAddMemberMsg,
        RoomDeleteMemberMsg,
        RoomAtMemberMsg,
        RoomQuitMsg,
        CloseWechatMsg,
        OpenWechatMsg,
        GetLoginInfoMsg,
        GetLoginStatusMsg,
        LogoutMsg,
        SendTextMsg,
        SendImageMsg,
        SendFileMsg,
        SendCardMsg,
        SendXmlMsg,
        FriendAddMsg,
        FriendAddFromV1Msg,
        FriendDeleteMsg,
        FriendVerifyMsg,
        FriendListMsg,
        RoomCreateMsg,
        SetFriendRemarkMsg
    ])]
