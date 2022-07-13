from seleniumrequests import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import os

from models import UrlRequest


class SeleniumUrlProcessor:

    def __init__(self):
        direct = os.path.dirname(os.path.abspath(__file__)).split('/')
        direct = '/'.join(direct[:-1])
        self.downloads_path = '/tmp/downloads/'

        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.downloads_path,
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True}
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--enable-javascript')
        chrome_options.add_experimental_option('prefs', prefs)

        self.browser = Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        params = {'behavior': 'allow', 'downloadPath': self.downloads_path}
        self.browser.execute_cdp_cmd('Page.setDownloadBehavior', params)


    def process_url(self, data:UrlRequest=None):
        direct = os.path.dirname(os.path.abspath(__file__)).split('/')
        direct = '/'.join(direct[:-1])
        self.downloads_path = '/tmp/downloads/'

        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.downloads_path,
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True}
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--enable-javascript')
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        params = {'behavior': 'allow', 'downloadPath': self.downloads_path}
        browser.get(data.url)
        cookies = data.cookies
        if len(cookies) == 0:
            content = browser.page_source
            return browser.page_source
        else:
            browser.add_cookie(cookies)
            content = browser.page_source
            return browser.page_source

    def close(self):
        self.browser.close()
