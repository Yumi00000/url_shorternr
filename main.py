import json
import os.path
import random
import string

import aiofiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_main_page(request: Request):
    return templates.TemplateResponse(request=request, name="url_getter.html")


async def save_jason_to_file(short_url, long_url):
    if os.path.exists("data.json"):
        async with aiofiles.open("data.json", "r") as json_file:
            current_data = json.loads(await json_file.read())
    else:
        current_data = {}
    current_data[short_url] = long_url
    async with aiofiles.open("data.json", "w") as json_file:
        await json_file.write(json.dumps(current_data))


async def get_long_url_from_json_file(short_url):
    if os.path.exists("data.json"):
        async with aiofiles.open("data.json", "r") as json_file:
            current_data = json.loads(await json_file.read())
        return current_data[short_url]
    return None


@app.post("/")
async def recorde_url(long_url: str = Form()):
    shor_url = ''.join(random.choice(string.ascii_letters + string.digits))
    await save_jason_to_file(shor_url, long_url)
    return shor_url


@app.get("/{short_url}")
async def say_hello(short_url: str):
    long_url = await get_long_url_from_json_file(short_url)
    if long_url:
        return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)
    else:
        "invalid short url"

