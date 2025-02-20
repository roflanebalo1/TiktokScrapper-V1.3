from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from src.applications.dto import CookieDTO, CookieFileORMDTO
from src.infrastructure.models import TikTokSessionORM, TiktokHashtagsORM, TiktokSongsORM, TiktokBreakoutSongsORM
from src.applications.interfaces.interfaces import ITiktokSessionRepository


class LoadCookies():

    def convert_to_cookie_dto(self, cookie_dto: list[dict]) -> list[CookieDTO]:
        return [CookieDTO(name=c["name"], value=c["value"]) for c in cookie_dto]

    def load_cookies(self, driver: WebDriver, cookie_dto):
            
            cookies = self.convert_to_cookie_dto(cookie_dto)
            
            for cookie in cookies:
                driver.add_cookie(cookie)