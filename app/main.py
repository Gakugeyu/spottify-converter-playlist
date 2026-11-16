from fastapi import FastAPI, Request, HTTPException


from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


import os
import secrets 
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
redirect_uri = "http://127.0.0.1:8888/callback"

templates = Jinja2Templates(directory="static/templates")
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/status")
def status_check():
    return {"message": "Status OK!"}


@app.get("/", response_class=HTMLResponse)
async def front_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
    

@app.get("/login", response_class=RedirectResponse)
async def login_spotify():
    state = secrets.token_urlsafe(16)

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
def callback(code: str, state:str):

    return {
        "message": "Autorização recebida!"
    }