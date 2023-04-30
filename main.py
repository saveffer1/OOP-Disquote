import uvicorn
import os
import glob
import pathlib
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response, UploadFile, File
from fastapi.responses import (RedirectResponse, HTMLResponse, 
                               JSONResponse, FileResponse,
                               StreamingResponse)
from fastapi.templating import Jinja2Templates
import base64

from router import router_document, router_account, router_admin, router_server

ALLOWED_ORIGINS = ['http://localhost', '0.0.0.0']

def create_app():
    fast_app = FastAPI(title='Discord Clone', docs_url=None,
        redoc_url=None, openapi_url='/admin/openapi.json',)
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fast_app

app = create_app()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def initial_startup():
    resource = 'static/resource'
    path = ['server', 'user_avatar', 'server_avatar']
    if os.path.exists(resource):
        """ del all resource before start server"""
        for folder in path:
            if os.listdir(f'static/resource/{folder}') != []:
                files = glob.glob(f'static/resource/{folder}/*')
                for f in files:
                    os.remove(f)
            else:
                continue
    else:
        """ check if not resource folder create it """
        os.mkdir(resource)
        for folder in path:
            os.mkdir(resource + '/' + folder)
    
    
@app.exception_handler(404)
def handle_404(e: Exception, request: Request):
    return templates.TemplateResponse("404.html", {"request": e}, status_code=404)

@app.exception_handler(500)
def handle_500(e: Exception, request: Request):
    return templates.TemplateResponse("500.html", {"request": e}, status_code=500)
    
@app.get('/ping', status_code=200, tags=['healthcheck'])
@app.post('/ping', status_code=200, tags=['healthcheck'])
async def healthchk():
    return {'status_code': 200, 'detail': 'pong'}

@app.get("/", response_class=HTMLResponse)
def mainindex(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/account/login", response_class=HTMLResponse)
def registry(request: Request):
    return templates.TemplateResponse("registry.html", {"request": request})

@app.get("/account/register", response_class=HTMLResponse)
def registry(request: Request):
    return templates.TemplateResponse("registry.html", {"request": request})

@app.post("/server", response_class=HTMLResponse)
@app.get("/server", response_class=HTMLResponse)
def server(request: Request):
    if request.cookies.get('authen'):
        return templates.TemplateResponse("chatboard.html", {"request": request})
    else:
        print("test")
        resp = RedirectResponse(url='/account/login')
        return resp
@app.get("/annoucement", response_class=HTMLResponse)
def annoucement(request: Request):
    return templates.TemplateResponse("annouce.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def loginpageadm(request: Request):
    return RedirectResponse(url='/admin/login')

suffixes_to_media_types = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
}

@app.get("/image/user_avartar/{file_name}")
async def get_image_user(request: Request, file_name: str):
    file_path = f"static/assets/DiscordDefaultAvatar.jpg"
    if file_name != 'default':
        file_path = f"static/resource/user_avatar/{file_name}"
    suffix = pathlib.Path(file_path).suffix
    media_type = suffixes_to_media_types.get(suffix, "application/octet-stream")
    return StreamingResponse(open(file_path, "rb"), media_type=media_type)

@app.get("/image/server_avartar/{file_name}")
async def get_image_server(request: Request, file_name: str):
    file_path = f"static/assets/DiscordDefaultAvatar.jpg"
    if file_name != 'default':
        file_path = f"static/resource/server_avatar/{file_name}"
    suffix = pathlib.Path(file_path).suffix
    media_type = suffixes_to_media_types.get(suffix, "application/octet-stream")
    return StreamingResponse(open(file_path, "rb"), media_type=media_type)





@app.get("/chat-guild", response_class=HTMLResponse)
def chat_guild(request: Request):
    return templates.TemplateResponse("chat-guild.html", {"request": request})



@app.get("/container-server", response_class=HTMLResponse)
def container_server(request: Request):
    return templates.TemplateResponse("container-server.html", {"request": request})


@app.get("/container-dm", response_class=HTMLResponse)
def container_dm(request: Request):
    return templates.TemplateResponse("container-dm.html", {"request": request})


@app.get("/chat-dm", response_class=HTMLResponse)
def chat_dm(request: Request):
    return templates.TemplateResponse("chat-dm.html", {"request": request})




@app.get("/friendslist", response_class=HTMLResponse)
def friendslist(request: Request):
    return templates.TemplateResponse("friendslist.html", {"request": request})



@app.get("/addfriend", response_class=HTMLResponse)
def addfriend(request: Request):
    return templates.TemplateResponse("addfriend.html", {"request": request})

@app.get("/pending", response_class=HTMLResponse)
def addfriend(request: Request):
    return templates.TemplateResponse("pending.html", {"request": request})

app.include_router(router_server, prefix='/channels')
app.include_router(router_account, prefix='/account')
app.include_router(router_admin, prefix='/admin')
app.include_router(router_document, prefix='/admin')

if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, ssl_keyfile=None, ssl_certfile=None)
    uvicorn.run("main:app", host="localhost", port=8080,reload=True, ssl_keyfile=None, ssl_certfile=None)
