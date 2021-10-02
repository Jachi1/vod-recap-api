import re
import json
from fastapi import FastAPI
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from urllib.parse import parse_qs
from urllib.parse import urlparse
from chatdownloader import get_chat


app = FastAPI()

TWITCH_ID=re.compile(r'https://www.twitch.tv/videos/(\d+)')

YOUTUBE_BASE_URL="https://www.youtube.com/watch?v"
TWITCH_BASE_URL="https://www.twitch.tv/videos/{id}"


@app.get("/youtube")
def get_youtube_vod(url: str):
    parsed_query = parse_qs(url)
    chat = get_chat(f"{YOUTUBE_BASE_URL}={parsed_query[YOUTUBE_BASE_URL]}")
    return chat

@app.get("/twitch")
def get_twitch_vod(url: str):
    if id := TWITCH_ID.match(url):
        chat = get_chat(TWITCH_BASE_URL.format(id=id.group(1)))
        print("Recieved chat.")
        return JSONResponse(content=chat)
    return {"err": "Failed to get id from url"}
   