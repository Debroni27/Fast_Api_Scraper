from models import  UrlRequest
import requests
from urllib.parse import unquote

class RequestUrlProcessor:

    def __init__(self):
        pass

    def process_url(self, data: UrlRequest = None):
        decoded = unquote(data.url)
        response = requests.request(method=data.method, url=decoded, headers=data.headers, cookies=data.cookies, proxies = data.processing_params.proxy, allow_redirects=False
                                    )
        return response
