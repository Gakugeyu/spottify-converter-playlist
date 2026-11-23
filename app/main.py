from fastapi import FastAPI, Request, HTTPException


import requests
import base64
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
import secrets 
from urllib.parse import urlencode
from dotenv import load_dotenv
from config.session import configure_session


load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:8888/callback"



enconde_credentials = client_id + ":" + client_secret

string_bytes = enconde_credentials.encode('utf-8')
base64_bytes = base64.b64encode(string_bytes)
base64_enconde_credentials = base64_bytes.decode('utf-8')


templates = Jinja2Templates(directory="static/templates")
app = FastAPI()
configure_session(app)


app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/status")
def status_check():
    return {"message": "Status OK!"}


@app.get("/", response_class=HTMLResponse)
async def front_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
    

@app.get("/login", response_class=RedirectResponse)
async def login_spotify(request:Request):
    state = secrets.token_urlsafe(16)
    request.session["spotify_state"] = state

    parameters = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "playlist-read-private",
        "state": state
    }

    url_base = "https://accounts.spotify.com/authorize"
    url_autorizacao = f"{url_base}?{urlencode(parameters)}"

    return RedirectResponse(url=url_autorizacao,status_code=302)


@app.get("/callback")
def callback(request:Request, code: str, state:str):
    state_original = request.session.get("spotify_state")

    if state_original == state: 
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': f'Basic {base64_enconde_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'grant_type': 'authorization_code',
                'code':code,
                'redirect_uri':'http://127.0.0.1:8888/callback'}

        response = requests.post(url=url, headers=headers, data=payload)

        return {'status_code': response.status_code,
                'sucess': response.ok}

    else:
        return {"message":"ERROR!"}