import re

from fastapi import FastAPI
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from urllib.parse import parse_qs
from chatdownloader import TwitchVodDownloader
from chatdownloader import YoutubeVodDownloader


app = FastAPI()

origins = ["*"]     # specify domains that can use this api
allowed_methods=["GET"]
allowed_headers=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers
)

TWITCH_ID=re.compile(r'https://www.twitch.tv/videos/(\d+)')

YOUTUBE_BASE_URL="https://www.youtube.com/watch?v"
TWITCH_BASE_URL="https://www.twitch.tv/videos/{id}"


@app.get("/youtube")
def get_youtube_vod(url: str):
    parsed_query = parse_qs(url)
    if YOUTUBE_BASE_URL in parsed_query.keys():
        youtube = YoutubeVodDownloader()
        chat = youtube.get_chat(f"{YOUTUBE_BASE_URL}={parsed_query[YOUTUBE_BASE_URL][0]}")
        return JSONResponse(content=chat)
    return {"err": "Failed to get id from url"}

@app.get("/twitch")
def get_twitch_vod(url: str):
    if id := TWITCH_ID.match(url):
        twitch = TwitchVodDownloader()
        chat = twitch.get_chat(TWITCH_BASE_URL.format(id=id.group(1)))
        return JSONResponse(content=chat)
    return {"err": "Failed to get id from url"}
   