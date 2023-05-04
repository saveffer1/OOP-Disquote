from fastapi import (
    APIRouter, HTTPException, UploadFile, status, Response, Request, 
    Form, Body, File, Depends, Query
    )
from fastapi.responses import (HTMLResponse, JSONResponse, FileResponse, StreamingResponse)
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError
import jwt
from model import TokenData, UserStatus, EmailStr
from fastapi.templating import Jinja2Templates
import pathlib
import json
from .discord import discord_account, discord_server
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']

token_manager = TokenData(secret=SECRET, algorithm='HS256')

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{server_id}/{channel_id}/getlist", status_code=200, tags=["message"])
async def get_all_msg(request: Request, server_id: int, channel_id: int, lastMsgId: int = Query(None)):
    lst_msg = discord_server.get_msg_list(server_id, channel_id)
    if lst_msg is None:
        return []
    if lastMsgId is not None:
        lst_msg = [msg for msg in lst_msg if msg['id'] > lastMsgId]
    return lst_msg



@router.get("/{server_id}/{channel_id}/getlast", status_code=200, tags=["message"])
async def get_all_msg(request: Request, server_id: int, channel_id: int):
    lst_msg = discord_server.get_msg_list(server_id, channel_id)
    return lst_msg[-1]


@router.post("/{channel_id}/sendmsg", status_code=201, tags=["message"])
async def send_msg(request: Request, channel_id: int, server_id: int = Body(...), msg: str = Body(...)):
    token = request.cookies.get("authen")
    if token:
        try:
            user_email = token_manager.decode_access_token(token)
        except:
            return RedirectResponse(url="/account/logout", status_code=status.HTTP_303_SEE_OTHER)
        sender_id = discord_account.get_user_id(user_email)
        sent = discord_server.add_message(server_id, channel_id, sender_id, msg)
        if sent:
            return {"message": "success"}
        else:
            return {"message": "failed"}
    else:
        return RedirectResponse(url="/account/login", status_code=status.HTTP_303_SEE_OTHER)

# @router.delete("{channel_id}/sendfile", status_code=201)
# async def del_msg(request: Request, server_id: int, channel_id: int, msg_id: int):
#     deleted = discord_server.del_message(server_id, channel_id, msg_id)
#     if deleted:
#         return {"message": "success"}
#     else:
#         return {"message": "failed"}