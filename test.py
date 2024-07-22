from datetime import timedelta, datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt
from jose.exceptions import JWTError
from pathlib import Path

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google"

# r"./certs/jwt-private.pem"
private_key_path = Path(__file__).parent / "certs" / "jwt-private.pem"

def encode_jwt(
        payload: dict,
        private_key: str = private_key_path.read_text(),
        algorithm: str = "RS256",
        expire_weeks: int = 30,
        expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    if expire_timedelta:
        expire = datetime.utcnow() + expire_timedelta
    else:
        expire = datetime.utcnow() + timedelta(weeks=expire_weeks)
    to_encode.update(
        exp=expire,
        iat=datetime.utcnow(),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded

@app.get("/login/google")
async def login_google():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=openid%20profile%20email"
        f"&access_type=offline"
    )
    return {"url": google_auth_url}


@app.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(token_url, data=data, headers=headers)
    token_response = response.json()
    if "access_token" not in token_response:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    access_token = token_response["access_token"]
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print(f"{access_token=}")
    user_info = user_info_response.json()
    print(f"{encode_jwt(user_info)=}")
    return user_info


@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["RS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
