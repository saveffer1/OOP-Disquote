from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

router = APIRouter()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "admin")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# swagger ui host/admin/doc
@router.get("/doc")
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/admin/openapi.json", title="docs")

# redoc ui host/admin/redoc
@router.get("/redoc")
async def get_redocumentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/admin/openapi.json", title="redoc")

