from pydantic import BaseModel, validator
import typing

class ProcessingParams(BaseModel):
    engine: str = None # selenium, requests ...
    proxy: str = None


class UrlRequest(BaseModel):
    url: str = None
    method: str = None
#    headers: [header map]
#    cookies: [cookie map]
    body: str = None
    processing_params: ProcessingParams = None
    headers: typing.Dict[str, str] = None
    cookies: typing.Dict[str, str] = None





    @validator("headers", pre=True, always=True)
    def check_headers(cls, headers):
        if not headers:
            return {}
        elif len(headers) == 0:
           return {}
        return headers


    @validator("cookies", pre=True, always=True)
    def check_cookies(cls, cookies):
        if not cookies:
            return {}
        elif len(cookies) == 0:
           return {}
        return cookies