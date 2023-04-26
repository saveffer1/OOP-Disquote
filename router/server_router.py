from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError
from model import TokenData, UserStatus, EmailStr
from schema import UserSchema, LoginSchema, UpdateUserModel
from fastapi.templating import Jinja2Templates
import base64
import shutil
from .discord import discord_account, discord_server
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']

token_manager = TokenData(secret=SECRET, algorithm='HS256')

router = APIRouter()
templates = Jinja2Templates(directory="templates")

router.get("/get_list", status_code=200, tags=['server'])
async def get_list_server(request: Request):
    token = request.cookies.get("authen")
    if token:
        user_email = token_manager.decode_access_token(token)
        user_id = discord_account.get_user_id(user_email)
        return discord_server.list_server(user_id)

router.get("/{server_id}", status_code=200, tags=['server'])
async def get_server(request: Request, server_id: str):
    token = request.cookies.get("authen")
    if token:
        user_email = token_manager.decode_access_token(token)
        # user_id = discord_account.get_user_id(user_email)
        #return discord_server.get_server_info(server_id)
        return {"server_id": server_id, "user_email": user_email}
    

@router.get('/ping', status_code=200, tags=['server'])
@router.post('/ping', status_code=200, tags=['server'])
async def healthchk():
    return {'status_code': 200, 'detail': 'pong'}

@router.get("/@me", status_code=200, tags=['server'])
async def get_dm(request: Request):
    token = request.cookies.get("authen")
    if token:
        user_email = token_manager.decode_access_token(token)
        user_id = discord_account.get_user_id(user_email)
        
        dm_channel = templates.TemplateResponse("chatboard.html", {"request": request, "svdm": "dm"})
        return dm_channel
