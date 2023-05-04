from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request, Form, Body, status
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

@router.get('/ping', status_code=200, tags=['server'])
@router.post('/ping', status_code=200, tags=['server'])
async def healthchk():
    return {'status_code': 200, 'detail': 'pong'}

@router.get("/all", status_code=200, tags=['server'])
async def get_all():
    return discord_server.get_all_server()

@router.get('/allinvite', status_code=200, tags=['server'])
async def get_all_invite():
    return discord_server.get_all_invite()

@router.post("/@me", status_code=200, tags=['server'])
@router.get("/@me", status_code=200, tags=['server'])
async def get_dm(request: Request):
    token = request.cookies.get("authen")
    if token:
        try:
            dm_channel = templates.TemplateResponse("chatboard.html", {"request": request, "svdm": "dm"})
            return dm_channel
        except:
            return RedirectResponse(url="/account/logout", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/account/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/getlist", status_code=200, tags=['server'])
async def get_list_server(request: Request):
    token = request.cookies.get("authen")
    if token:
        try:
            user_email = token_manager.decode_access_token(token)
            user_id = discord_account.get_user_id(user_email)
            return discord_server.get_user_server_list(user_id)
        except:
            return RedirectResponse(url="/account/logout", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/account/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{server_id}", status_code=200, tags=['channel'])
async def get_server(request: Request, server_id: int):
    token = request.cookies.get("authen")
    if token:
        try:
            email = token_manager.decode_access_token(token)
            server = discord_server.get_server_by_id(server_id)
            if server:
                return templates.TemplateResponse("chatboard.html", {"request": request, "ch": "yes"})
            return templates.TemplateResponse("chatboard.html", {"request": request})
        except:
            return RedirectResponse(url="/account/logout", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/account/login", status_code=status.HTTP_303_SEE_OTHER)
    
@router.get("/{server_id}/get_ch_list", status_code=200, tags=['channel'])
async def get_ch_list(request: Request, server_id: int):
    server = discord_server.get_server_by_id(server_id)
    channels = server.get_channel_list()
    return channels

@router.post("/{server_id}/create_channel", status_code=200, tags=['channel'])
async def create_channel(request: Request, server_id: int, ch_name: str = Body(...), ch_type: str = Body(...), ch_category: str = Body(...)):
    token = request.cookies.get("authen")
    if token:
        try:
            discord_server.add_channel(server_id, ch_name, ch_type, ch_category)
            return {"status_code": 200, "detail": "success"}
        except:
            return RedirectResponse(url="/account/logout", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/account/login", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/create_server", status_code=200, tags=['server'])
async def create_server(request: Request, image: UploadFile = File(...), name: str = Form(...)):
    token = request.cookies.get("authen")
    if token:
        try:
            user_email = token_manager.decode_access_token(token)
            user_id = discord_account.get_user_id(user_email)
            if image and image.content_type != 'application/octet-stream':
                content = await image.read()
                if len(content) <= 8388608:
                    print("image uploaded", image.content_type)
                    if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
                        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'Unsupported Media Type', 'detail': ''}, status_code=415)
                    else:
                        try:
                            file_name = image.filename
                            file_rename = f"{discord_server.get_server_id()}{pathlib.Path(file_name).suffix}"
                            file_location = f"static/resource/server_avatar/{file_rename}"
                            print("------------------")
                            print("Uploaded: ", file_name)
                            print("Read size: ", len(content), "bytes")
                            print(f"File size: {image.file.tell()} bytes")
                            print("------------------")
                            with open(file_location, "wb") as f:
                                f.write(content)
                        except Exception as e:
                            return templates.TemplateResponse("chatboard.html", {"request": request, 'crsv_message': 'file error', 'detail': f'{e}'}, status_code=500)
                        finally:
                            discord_server.add_server(name, user_id, f"{file_rename}")
                            image.file.close()
                            return RedirectResponse(url="/channels/@me", status_code=status.HTTP_303_SEE_OTHER)
                else:
                    return templates.TemplateResponse("chatboard.html", {"request": request, 'crsv_message': 'max size 8MB', 'detail': ''}, status_code=413)
            else:
                discord_server.add_server(name, user_id)
                return RedirectResponse(url="/channels/@me", status_code=status.HTTP_303_SEE_OTHER)
        except:
            return RedirectResponse(url="/account/logout", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/account/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/member_list/{server_id}", status_code=200, tags=['server'])
def get_member_list(server_id: int):
    member_list = discord_server.get_member_server_list(server_id)
    return member_list

@router.get("/{server_id}/{invite_code}", status_code=200, tags=['server'])
def goto_invite(request: Request, invite_code: str):
    token = request.cookies.get("authen")
    if token:
        server_id = discord_server.get_server_id_by_invite(invite_code)
        return templates.TemplateResponse("inviteconfirm.html", {"request": request, "invite_code": invite_code, "invite_to_server_id": server_id})
    else:
        return RedirectResponse(url="/account/login", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/join_server", status_code=200, tags=['server'])
async def join_the_server(request: Request, invite_code: str = Body(...), confirm: bool = Body(...)):
    if confirm:
        token = request.cookies.get("authen")
        if token:
                try:
                    user_email = token_manager.decode_access_token(token)
                    user_id = discord_account.get_user_id(user_email)
                    print("User ID: ", user_id)
                    server_id = discord_server.get_server_id_by_invite(invite_code)
                    if not discord_server.member_in_server(server_id, user_id):
                        discord_server.join_server(server_id, user_id)
                        return {"status_code": 200, "detail": "success", "prompt": "accepted"}
                    else:
                        return {"status_code": 200, "detail": "success", "prompt": "already in server"}
                except:
                    return {"datail": "error none type after decode cookie"}
    else:
        return {"status_code": 200, "detail": "success", "prompt": "rejected"}

@router.post("/leave_server/{server_id}", status_code=200, tags=['server'])
async def exit_server(request: Request, server_id: int):
    token = request.cookies.get("authen")
    if token:  # check if token exist
        email = token_manager.decode_access_token(token)
        server = discord_server.get_server_by_id(server_id)
        user = discord_account.get_user_account(email)
        user_id = user.id()
        print(server.get_member_list())
        server.remove_member(user_id)
        print(server.get_member_list())
        return  {"detail": "success"}