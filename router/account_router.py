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

@router.post('/register', status_code=201, tags=['user'])
async def register(request: Request, email: EmailStr = Form(...), username: str = Form(...), password: str = Form(...), image: UploadFile = File(None)):
    user = UserSchema(email=email, username=username, password=password)
    if discord_account.add_user(user):
        user = discord_account.user_account[user.email]
        if image and image.content_type != 'application/octet-stream':
            if len(await image.read()) <= 8388608:
                print("image uploaded", image.content_type)
                if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
                    return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'Unsupported Media Type', 'detail': ''}, status_code=415)
                else:
                    try:
                        file_name = image.filename
                        file_location = f"static/resource/user_avatar/{user.id}_{file_name}"
                        with open(file_location, "wb+") as file_object:
                            file_object.write(image.file.read())
                    except Exception as e:
                        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'file error', 'detail': f'{e}'}, status_code=500)
                    finally:
                        user.avatar = file_location
                        image.file.close()
            else:
                return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'max size 8MB', 'detail': ''}, status_code=413)
        else:
            user.avatar = 'static/assets/DiscordDefaultAvatar.jpg'
        return templates.TemplateResponse("registry.html", {"request": request, 'reg_message': 'success', 'detail': ''}, status_code=201)
    else:
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

        resp = templates.TemplateResponse("chatboard.html", {"request": request, "login_message": "You have been logged in!"}, status_code=200)
        resp.set_cookie(
            "authen",
            value=f"{token}",
            samesite="lax",
            secure=False,
            httponly=True,
            max_age=43200,
        )
        # system.logged_in_users.add(user.email)
        return resp
    else:
        return templates.TemplateResponse("registry.html", {"request": request, "login_message": "Wrong email or password!"}, status_code=401)


@router.get('/logout', status_code=200, tags=['user'])
async def logout(resp: Response, request: Request):
    #resp.delete_cookie(key="authen")
    resp = templates.TemplateResponse("registry.html", {"request": request, "login_message": "You have been logged out!"}, status_code=200)
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
        if discord_account.user_account[email]:  # check if email exist
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
        return discord_account.user_account[email].get_info()
