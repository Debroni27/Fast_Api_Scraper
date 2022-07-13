from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response, JSONResponse
from urllib3 import response

from models import UrlRequest
from urllib.parse import unquote
from RequestUrlProcessor import RequestUrlProcessor
from SeleniumUrlProcessor import SeleniumUrlProcessor

app = FastAPI()

seleniumbrowser = SeleniumUrlProcessor()
requestbrowser = RequestUrlProcessor()


@app.on_event("shutdown")
def shutdown_event():
  seleniumbrowser.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/urlprocess", response_class=Response)
async def process_url_request(data: UrlRequest):

  engine = requestbrowser
  if data.processing_params and data.processing_params.engine == "selenium":
   engine = seleniumbrowser
   r = engine.process_url(data)
   return r
  else:
    decoded = unquote(data.url)
    r = engine.process_url(data)
    headers = r.headers
    content = r.content
    status_code = r.status_code
    result = ''

    for h in headers:
        result += h+':'+headers[h]+'\n'
    result += '\n'+str(content)
    if r.headers.get("ContentType") == "text/html":
        return HTMLResponse(result, 200)
    elif r.headers.get("ContentType") == "text/json":
        return JSONResponse(result, 200)
    elif r.headers.get("ContentType")=="text/css":
        return Response(result, 200)
    else:
        return Response(content=result, status_code=200)