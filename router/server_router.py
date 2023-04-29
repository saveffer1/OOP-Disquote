from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError
import jwt
from model import TokenData, UserStatus, EmailStr
from schema import UserSchema, LoginSchema, UpdateUserModel
from fastapi.templating import Jinja2Templates
import base64
import shutil
import aiofiles
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
    
@router.post("/@me", status_code=200, tags=['server'])
async def get_dm(request: Request):
    token = request.cookies.get("authen")
    if token:
        try:
            user_email = token_manager.decode_access_token(token)
            user_id = discord_account.get_user_id(user_email)
            
            dm_channel = templates.TemplateResponse("chatboard.html", {"request": request, "svdm": "dm"})
            return dm_channel
        except:
            return RedirectResponse(url="/account/logout", status_code=303)
    else:
        return RedirectResponse(url="/account/login", status_code=303)

@router.get("/getlist", status_code=200, tags=['server'])
async def get_list_server(request: Request):
    token = request.cookies.get("authen")
    if token:
        try:
            user_email = token_manager.decode_access_token(token)
            user_id = discord_account.get_user_id(user_email)
            return discord_server.list_server(user_id)
        except:
            return RedirectResponse(url="/account/logout", status_code=303)
    else:
        return RedirectResponse(url="/account/login", status_code=303)

@router.get("/{server_id}", status_code=200, tags=['server'])
async def get_server(request: Request, server_id: int):
    server = discord_server.get_server_by_id(server_id)
    channels = server.get_channel_list()
    return {"ch": channels}
    # return templates.TemplateResponse("chatboard.html", {"request": request, "ch": channels})

@router.post("/create_server", status_code=200, tags=['server'])
async def create_server(request: Request, image: UploadFile = File(...), name: str = Form(...)):
    token = request.cookies.get("authen")
    if token:
        try:
            user_email = token_manager.decode_access_token(token)
            user_id = discord_account.get_user_id(user_email)
            if image and image.content_type != 'application/octet-stream':
                if len(await image.read()) <= 8388608:
                    print("image uploaded", image.content_type)
                    if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
                        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'Unsupported Media Type', 'detail': ''}, status_code=415)
                    else:
                        try:
                            file_name = image.filename
                            file_location = f"resource/server_avatar/{discord_server.get_server_id()}_{file_name}"
                            async with aiofiles.open(f"static/{file_location}", "wb+") as file_object:
                                content = await image.read()
                                await file_object.write(content)
                        except Exception as e:
                            return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'file error', 'detail': f'{e}'}, status_code=500)
                        finally:
                            discord_server.add_server(name, user_id, f"/static/{file_location}")
                            image.file.close()
                            return RedirectResponse(url="/channels/@me")
                else:
                    return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'max size 8MB', 'detail': ''}, status_code=413)
            else:
                discord_server.add_server(name, user_id)
                return RedirectResponse(url="/channels/@me")
        except:
            return RedirectResponse(url="/account/logout", status_code=303)
    else:
        return RedirectResponse(url="/account/login", status_code=303)
