from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from model import Report
from jose import JWTError
from model import TokenData, UserStatus, EmailStr
from schema import UserSchema, LoginSchema, UpdateUserModel
from fastapi.templating import Jinja2Templates
from .discord import discord_account, discord_server
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']

token_manager = TokenData(secret=SECRET, algorithm='HS256')

router = APIRouter()
templates = Jinja2Templates(directory="templates")
adm_dashboard = Report()

@router.get('/login', status_code=200, tags=['admin'])
def login(request: Request):
    return templates.TemplateResponse("adm-login.html", {"request": request, "login_message": ""}, status_code=200)

@router.post('/login', status_code=200, tags=['admin'])
async def login(request: Request, email: EmailStr = Form(...), password: str = Form(...)):
    admin = LoginSchema(email=email, password=password)
    print("admin login", admin.email, admin.password)
    if discord_account.admin_login(admin):
        # if user.email in system.logged_in_users:
        #     system.logged_in_users.remove(user.email)
        #     raise HTTPException(status_code=409, detail='Already logged in on another device or closed the browser without logging out')

        access_token = token_manager.create_access_token(
            data={"sub": admin.email})

        token = jsonable_encoder(access_token)

        # resp = templates.TemplateResponse("chatboard.html", {"request": request, "login_message": "success"}, status_code=200)
        resp = RedirectResponse(url='/admin/dashboard')
        resp.set_cookie(
            "admin_authen",
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
        return templates.TemplateResponse("adm-login.html", {"request": request, "login_message": "Wrong email or password!"}, status_code=401)

@router.get('/logout', status_code=200, tags=['admin'])
def logout(request: Request, response: Response):
    response.delete_cookie("admin_authen")
    return RedirectResponse(url='/admin/login')

@router.get('/dashboard', status_code=200, tags=['admin'])
@router.post('/dashboard', status_code=200, tags=['admin'])
def show_dashboard(request: Request):
    return templates.TemplateResponse("adm-dash.html", {"request": request})

@router.get("/info", name="fastdash:get-your-system-info",)
@router.post("/info", name="fastdash:get-your-system-info",)
async def dashboard_info():
    ipaddress = adm_dashboard.get_ipaddress()
    platform = adm_dashboard.get_platform()
    uptime = adm_dashboard.get_uptime()
    cpu = adm_dashboard.get_cpu_usage()
    cores = adm_dashboard.get_cpus()
    memory = adm_dashboard.get_mem()
    #disk = adm_dashboard.get_disk()
    #diskrw = adm_dashboard.get_disk_rw()
    #loadavg = adm_dashboard.get_load()
    # Get traffic
    #traffic = adm_dashboard.get_traffic("127.0.0.1")
    #users = adm_dashboard.get_users()
    #netstat = adm_dashboard.get_netstat()

    return {
        "ipaddress": ipaddress,
        "platform": platform,
        "uptime": uptime,
        "cpu": cpu,
        "cores": cores,
        "memory": memory
        #"disk": disk,
        #"diskrw": diskrw,
        #"loadavg": loadavg,
        #"traffic": traffic,
        #"users": users,
        #"netstat": netstat,
    }


@router.get("/info/cpu", name="fastdash:get-your-system-info",)
async def cpu_info():
    cpu = adm_dashboard.get_cpu_usage()
    return {"cpu": cpu}

@router.get("/info/ram", name="fastdash:get-your-system-info",)
async def ram_info():
    memory = adm_dashboard.get_mem()
    ram = memory['percent']
    return {"ram": ram}