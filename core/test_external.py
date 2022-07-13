
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response, JSONResponse
from models import UrlRequest
from urllib.parse import unquote
from RequestUrlProcessor import RequestUrlProcessor

app = FastAPI()

seleniumbrowser = None  # SeleniumUrlProcessor()
requestbrowser = RequestUrlProcessor()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.post("/urlprocessFromFile", response_class=HTMLResponse)
# async def process_url_request(data: UrlRequest,):
#     html_content = browser.process_url(data)
#     return HTMLResponse(html_content, status_code=200)

@app.post("/urlprocess", response_class=Response)
async def process_url_request(data: UrlRequest):
    engine = requestbrowser
    if data.processing_params and data.processing_params.engine == "selenium":
        engine = seleniumbrowser
    data.url = unquote(data.url)
    r = engine.process_url(data)
    if r.headers.get("ContentType") == "text/html":
        return HTMLResponse(r.content, 200)
    elif r.headers.get("ContentType") == "text/json":
        return JSONResponse(r.content, 200)
    else:
        return Response(r.content, 200)




@app.post("/allurlFromFile")
async def process_url_request_from_file(data: UrlRequest):
    decoded = unquote(data.url)
    req = UrlRequest
    req.proxies = data.processing_params.proxy
    session = requests.Session()
    session.proxies.update(req.proxies)
    req.url = decoded
    req.headers = data.headers
    req.method = data.method
    cookies_dict = data.cookies
    req.cookies = cookies_dict
    r = requestbrowser.process_url(req)
    if r.headers.get("ContentType") == "text/html":
        return HTMLResponse(r.content, 200)
    elif r.headers.get("ContentType") == "text/json":
        return JSONResponse(r.content, 200)
    elif r.headers.get("ContentType") == "application/json":
        return JSONResponse(r.content, 200)
    else:
        return Response(r.content, 200)