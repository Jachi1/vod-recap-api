# vod-recap-api
RESTful API for vod-recap

## Requirements
- Python 3.9.5

## Usage
```bash
uvicorn main:app --reload

# Get request to http://127.0.0.1:8000/twitch or http://127.0.0.1:8000/youtube with url argument
# Example: http://127.0.0.1:8000/twitch?url=https://www.twitch.tv/videos/1164962258
# The longer the vod, the longer the request will take. 
# For example, an 8000 viewer streamer with a 1.5 hour vod will take ~2 minutes to complete the query
```
