from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request, Form, Body
from fastapi.responses import (HTMLResponse, JSONResponse, FileResponse, StreamingResponse)
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError
from model import TokenData, UserStatus, EmailStr
from fastapi.templating import Jinja2Templates
import base64
import shutil
import aiofiles
import asyncio
import pathlib
import imghdr
import io
import os
from datetime import timedelta
from .discord import discord_account, discord_server
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']

token_manager = TokenData(secret=SECRET, algorithm='HS256')

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post('/register', status_code=201, tags=['user'])
async def register(request: Request, email: EmailStr = Form(...), username: str = Form(...), password: str = Form(...), image: UploadFile = File(None)):
    if discord_account.email_is_exist(email):
        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'Email already exist', 'detail': ''}, status_code=409)
    if image and image.content_type != 'application/octet-stream':
        content = await image.read()
        if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
            return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'Unsupported Media Type', 'detail': ''}, status_code=415)
        elif len(content) <= 8388608:
            file_name = ""
            try:
                file_name = image.filename
                file_rename = f"{discord_account.systeminfo().get('last_user_id')}{pathlib.Path(file_name).suffix}"
                file_location = f"static/resource/user_avatar/{file_rename}"
                print("------------------")
                print("Uploaded: ", file_name)
                print("Read size: ", len(content), "bytes")
                print(f"File size: {image.file.tell()} bytes")
                print("------------------")
                with open(file_location, "wb") as f:
                    f.write(content)
                discord_account.add_user(email, username, password, file_rename)
                return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'success', 'detail': ''}, status_code=201)
            except Exception as e:
                return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'file error', 'detail': f'{e}'}, status_code=500)
        else:
            return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'max size 8MB', 'detail': ''}, status_code=413)
    else:
        discord_account.add_user(email, username, password)
        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'success', 'detail': ''}, status_code=201)
        
@router.post('/login', status_code=200, tags=['user'])
async def login(request: Request, email: EmailStr = Form(...), password: str = Form(...)):
    print(email, password)
    if discord_account.user_login(email=email, password=password):
        # if user.email in system.loguserged_in_users:
        #     system.logged_in_users.remove(user.email)
        #     raise HTTPException(status_code=409, detail='Already logged in on another device or closed the browser without logging out')

        access_token = token_manager.create_access_token(
            data={"sub": email},
            expires_delta=timedelta(hours=12)
            )

        token = jsonable_encoder(access_token)

        #resp = templates.TemplateResponse("chatboard.html", {"request": request, "login_message": "success"}, status_code=200)
        resp = RedirectResponse(url='/channels/@me', status_code=308)
        resp.set_cookie(
            "authen",
            value=f"{token}",
            samesite="lax",
            secure=False,
            httponly=True,
            max_age=43200,
        )

        # resp = RedirectResponse(url='/server', )
        # system.logged_in_users.add(user.email)
        return resp
    else:
        return templates.TemplateResponse("registry.html", {"request": request, "login_message": "Wrong email or password!"}, status_code=401)

@router.get('/logout', status_code=200, tags=['user'])
@router.post('/logout', status_code=200, tags=['user'])
async def logout(resp: RedirectResponse, request: Request):
    #resp.delete_cookie(key="authen")
    resp = RedirectResponse(url="/account/login", status_code=308)
    resp.delete_cookie(key="authen")
    return resp

@router.get('/auth', status_code=200, tags=['user'])
async def auth(request: Request):
    token = request.cookies.get("authen")
    if token:  # check if token exist
        try:
            email = token_manager.decode_access_token(token)
            if email is None:  # check if token is valid
                raise HTTPException(status_code=401, detail='Unauthorized 1')
        except JWTError:  # token is not valid
            raise HTTPException(status_code=401, detail='Unauthorized 2')
        if discord_account.get_user_account(email):  # check if email exist
            return {"status_code": 200, "detail": "Authorized"}
        else:  # email not exist
            raise HTTPException(status_code=401, detail='Unauthorized 3')
    else:  # token not exist
        raise HTTPException(status_code=401, detail='Unauthorized 4')

@router.get('/me', status_code=200, tags=['user'])
async def info(request: Request):
    token = request.cookies.get("authen")
    if token:  # check if token exist
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        return user.info()

# รายชื่อเพื่อนของเรา
@router.get('/friends', status_code=200, tags=['user'])
async def get_friends(request: Request):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        friends = []
        for friend_id in user.get_friend_list():
            friend = discord_account.get_user_account_by_id(friend_id)
            friends.append(friend)
        return friends
    
# รายชื่อคำขอเป็นเพื่อน
@router.get('/request_list', status_code=200, tags=['user'])
async def get_friends_request(request: Request):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        friends = []
        for friend_id in user.request_list:
            friend = discord_account.get_user_name_by_id(friend_id)
            friends.append(friend)
        return friends
            
# ขอเป็นเพื่อน การใช้งาน /account/friends_request/{ไอดีของเพื่อนที่จะขอเป็นเพื่อน}
@router.post('/friends_request/{friend_name}/{friend_tag}', status_code=200, tags=['user'])
async def friends_request(request: Request, friend_name: str, friend_tag: str):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        request_user = discord_account.get_user_account_by_name_and_tag(friend_name, friend_tag)
        if user and request_user:
            request_user.add_request(user.id())
            return {"status_code": 200, "req_f": "success"}
        else:
            return {"status_code": 400, "req_f": "fail user not found"}
    
# รับเพื่อน การใช้งาน ให้ post id ของคนที่จะรับเป็นเพื่อน กับ boolean ว่าจะรับหรือไม่ true = รับ false = ปฏิเสธ
@router.post('/friends_request_prompt', status_code=200, tags=['user'])
async def friend_prompt(request: Request, friend_id: int = Body(...), prompt: bool = Body(...)):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        user.request_list(int(friend_id), prompt)
        return {"status_code": 200, "prompt_f": "success"}

# ลบเพื่อน การใช้งาน ให้ post id ของคนที่จะลบเป็นเพื่อน
@router.post('/unfriend', status_code=200, tags=['user'])
async def del_friend(request: Request, friend_id: int):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        user.unfriend(int(friend_id))
        return {"status_code": 200, "del_f": "success"}

@router.get('/get_name/{user_id}', status_code=200, tags=['user'])
async def get_name(request: Request, user_id: int):
    user = discord_account.get_user_account_by_id(user_id)
    if user:
        return user.username()
    else:
        return {"status_code": 400, "get_name_f": "fail user not found"}