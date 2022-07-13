import json

import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response, JSONResponse
from models import UrlRequest
import os
from selenium import webdriver
from seleniumrequests import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import multiprocessing as mp
import urllib.parse
from urllib.parse import unquote
from bs4 import BeautifulSoup
from RequestUrlProcessor import RequestUrlProcessor


app = FastAPI()

seleniumbrowser = None #SeleniumUrlProcessor()
requestbrowser = RequestUrlProcessor()


@app.get("/")
async def root():
    return {"message": "Hello World"}


#@app.post("/urlprocessFromFile", response_class=HTMLResponse)
# async def process_url_request(data: UrlRequest,):
#     html_content = browser.process_url(data)
#     return HTMLResponse(html_content, status_code=200)

@app.post("/urlprocess", response_class=HTMLResponse)
async def process_url_request(data: UrlRequest):

    engine = requestbrowser
    if data.processing_params != None & data.processing_params.engine == "selenium":
        engine = seleniumbrowser
    html_content = engine.process_url(data)
    return HTMLResponse(html_content, status_code=200)



@app.post("/allurlFromFile")
async def process_url_request_from_file(number):

    # direct = os.path.dirname(os.path.abspath(__file__)).split('/')
    # direct = '/'.join(direct[:-1])
    # downloads_path = '/tmp/downloads/'
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"download.default_directory": downloads_path,
    #          "download.prompt_for_download": False,
    #          "download.directory_upgrade": True}
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--enable-javascript')
    # chrome_options.add_experimental_option('prefs', prefs)
    # browser = Chrome(executable_path = os.path.relpath("chromedriver"), chrome_options=chrome_options)
    # params = {'behavior': 'allow', 'downloadPath': downloads_path}
    # browser.execute_cdp_cmd('Page.setDownloadBehavior', params)
    file = open("jsonFileUrls.json")
    data = json.load(file)


    for line in data:
        header = [
            "user-agent:Mozilla/4.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 ",
            "referer:https://www.google.com/",
            "content-encoding:br"
        ]
        decoded = unquote(line)
        req = UrlRequest()
        req.url = decoded
        req.headers = header
        req.method = "POST"
#        RequestURL =  requestbrowser.process_url(req)
        r2 = requests.request(req.url,header),
        r = requestbrowser.process_url(req.url,req.headers,method=req.method)
        if r.headers.get("ContentType") == "text/html":
            return HTMLResponse(r.content, 200)
        elif r.headers.get("ContentType") == "text/json":
            return JSONResponse(r.content,200)
        else:
            return Response(r.content, 200)
        file.close()

