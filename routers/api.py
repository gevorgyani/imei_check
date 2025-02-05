import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from utils.validators import is_valid_imei
from services.imei_service import check_imei_with_api
from config import settings
from core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
auth_scheme = HTTPBearer() #Настраивает схему авторизации через Bearer-токен (обычно используется для передачи токенов в заголовке Authorization)

class IMEIRequest(BaseModel):
    imei: str
    token: str

class IMEIResponse(BaseModel):
    status: str
    details: dict

@app.post("/v1/checks", response_model=IMEIResponse)
async def check_imei(
    imei_request: IMEIRequest,
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    if credentials.credentials != settings.API_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    imei = imei_request.imei
    if not is_valid_imei(imei):
        raise HTTPException(status_code=400, detail="Invalid IMEI format")

    try:
        api_response = await check_imei_with_api(imei)
        return IMEIResponse(status="success", details=api_response)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"API error: {e.response.text}")