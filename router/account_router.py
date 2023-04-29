from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError
from model import TokenData, UserStatus, EmailStr
from schema import UserSchema, LoginSchema, UpdateUserModel
from fastapi.templating import Jinja2Templates
import base64
import shutil
import aiofiles
import asyncio
import pathlib
import imghdr
import io
import os
from .discord import discord_account, discord_server
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']

token_manager = TokenData(secret=SECRET, algorithm='HS256')

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post('/register', status_code=201, tags=['user'])
async def register(request: Request, email: EmailStr = Form(...), username: str = Form(...), password: str = Form(...), image: UploadFile = File(...)):
    guest = UserSchema(email=email, username=username, password=password)
    if discord_account.add_user(guest):
        if image and image.content_type != 'application/octet-stream':
            content = await image.read()
            if len(content) <= 8388608:
                if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
                    return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'Unsupported Media Type', 'detail': ''}, status_code=415)
                else:
                    file_name = ""
                    try:
                        file_name = image.filename
                        file_rename = f"{discord_account.get_user_id(email)}{pathlib.Path(file_name).suffix}"
                        file_location = f"static/resource/user_avatar/{file_rename}"
                        print("------------------")
                        print("Uploaded: ", file_name)
                        print("Read size: ", len(content), "bytes")
                        print(f"File size: {image.file.tell()} bytes")
                        print("------------------")
                        with open(file_location, "wb") as f:
                            f.write(content)
                    except Exception as e:
                        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'file error', 'detail': f'{e}'}, status_code=500)
                    finally:
                        discord_account.set_avatar(email, f"{file_rename}")
                        # image.file.close()
            else:
                return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'max size 8MB', 'detail': ''}, status_code=413)
        else:
            discord_account.set_avatar(email, 'default')
        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'success', 'detail': ''}, status_code=201)
    else:
        user = discord_account.get_user_account(email)
        del user
        return templates.TemplateResponse('registry.html', {'request': request, 'reg_message': "Account already exists", 'detail': ''}, status_code=409)

@router.post('/login', status_code=200, tags=['user'])
async def login(request: Request, email: EmailStr = Form(...), password: str = Form(...)):
    user = LoginSchema(email=email, password=password)
    print(user.email, user.password)
    if discord_account.user_login(user):
        # if user.email in system.logged_in_users:
        #     system.logged_in_users.remove(user.email)
        #     raise HTTPException(status_code=409, detail='Already logged in on another device or closed the browser without logging out')

        access_token = token_manager.create_access_token(
            data={"sub": user.email})

        token = jsonable_encoder(access_token)

        #resp = templates.TemplateResponse("chatboard.html", {"request": request, "login_message": "success"}, status_code=200)
        resp = RedirectResponse(url='/channels/@me')
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
async def logout(resp: Response, request: Request):
    #resp.delete_cookie(key="authen")
    resp = RedirectResponse(url="/account/login")
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
        return user.get_info()

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
@router.get('/friends_request', status_code=200, tags=['user'])
async def get_friends_request(request: Request):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        friends = []
        for friend_id in user.request_list():
            friend = discord_account.get_user_name_by_id(friend_id)
            friends.append(friend)
        return friends
            
# ขอเป็นเพื่อน การใช้งาน /account/friends_request/{ไอดีของเพื่อนที่จะขอเป็นเพื่อน}
@router.post('/friends_request/{friend_id}', status_code=200, tags=['user'])
async def accept_friend_request(request: Request, friend_id: str):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        request_user = discord_account.get_user_account_by_id(friend_id)
        request_user.add_request(user.get_info().get('id'))
        return {"status_code": 200, "detail": "success"}
    
# รับเพื่อน การใช้งาน ให้ post id ของคนที่จะรับเป็นเพื่อน กับ boolean ว่าจะรับหรือไม่ true = รับ false = ปฏิเสธ
@router.post('/friend_prompt', status_code=200, tags=['user'])
async def friend_prompt(request: Request, friend_id: str, prompt: bool):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        user.request_list(int(friend_id), prompt)
        return {"status_code": 200, "detail": "success"}

# ลบเพื่อน การใช้งาน ให้ post id ของคนที่จะลบเป็นเพื่อน
@router.post('/unfriend', status_code=200, tags=['user'])
async def del_friend(request: Request, friend_id: str):
    token = request.cookies.get("authen")
    if token:
        email = token_manager.decode_access_token(token)
        user = discord_account.get_user_account(email)
        user.unfriend(int(friend_id))
        return {"status_code": 200, "detail": "success"}