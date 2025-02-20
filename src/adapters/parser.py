from time import sleep
from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import urllib3
from contextlib import contextmanager
from src.applications.dto import CookieDTO, CookieFileORMDTO
from src.infrastructure.models import TikTokSessionORM, TiktokHashtagsORM, TiktokSongsORM, TiktokBreakoutSongsORM
from src.adapters.scrolls_click import Scrolls_Click

class Parser(Scrolls_Click):

    #def get_hashtags(self, cookies: list[CookieDTO]) -> list[TiktokHashtag]:...
    def get_hashtags(self, driver: WebDriver):
        driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en")
        while True:
            hashtags_elements = driver.find_elements(By.CLASS_NAME, "CommonDataList_cardWrapper__kHTJP")
            last_hashtag = hashtags_elements[-1]
            self.smooth_scroll(last_hashtag)
            sleep(3)
            if len(hashtags_elements) == 100:
                break
        hashtags_elements = driver.find_elements(By.CLASS_NAME, "CardPc_titleText__RYOWo")
        for element in hashtags_elements:
            hashtag_text = element.text
            TiktokHashtagsORM.objects.get_or_create(name=hashtag_text, value="hashtag")
        print("Хештеги успешно сохранены в базу данных.")
        sleep(5)
        
    def get_songs(self, driver: WebDriver):
        driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
        driver.execute_script("window.scrollBy(0,1500)","")
        for i in range(1, 10):
            driver.execute_script("window.scrollBy(0,1200)","")
            sleep(4)
        songs_elements = driver.find_elements(By.CLASS_NAME, "ItemCard_musicName__2znhM")
        songs = []
        for element in songs_elements:
            song_text = element.text
            songs.append(song_text)
        print(songs)
        author_elements = driver.find_elements(By.CLASS_NAME, "ItemCard_autherName__gdrue")
        authors = []
        for element in author_elements:
            author_text = element.text
            authors.append(author_text)
        print(authors)
        if len(songs_elements) != len(author_elements):
            raise ValueError("Списки должны быть одинаковой длины")
        for song, author in zip(songs_elements, author_elements):
            song_text = song.text
            author_text = author.text
            TiktokSongsORM.objects.get_or_create(name=song_text, author=author_text)
        print("Песни успешно сохранены в базу данных.")
        sleep(5)
        
    def get_songs_links(self, driver: WebDriver):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "index-mobile_goToDetailBtnWrapper__puubr")))

        song_elements = driver.find_elements(By.CLASS_NAME, "index-mobile_goToDetailBtnWrapper__puubr")

        song_links = [song.get_attribute("href") for song in song_elements if song.get_attribute("href")]

        print("Найденные ссылки на песни:")
        for link in song_links:
            print(link)

    def update_url_period(url, new_period=120):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params['period'] = [str(new_period)]
        new_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed_url._replace(query=new_query))
    
    def update_links(update_url_period, song_links):
        updated_song_links = [update_url_period(link) for link in song_links]
        return(updated_song_links)
    
    
    def get_breakout_songs(self, driver: WebDriver):
        driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
        driver.execute_script("window.scrollBy(13500,0)","")
        breakout_button = driver.find_elements(By.CLASS_NAME, "ContentTab_itemLabelText__hiCCd")
        breakout_click = breakout_button[1]
        self.smooth_click(breakout_click)
        sleep(5)
        for i in range(1, 10):
            driver.execute_script("window.scrollBy(0,1200)","")
            sleep(4)

        breakout_songs_elements = driver.find_elements(By.CLASS_NAME, "ItemCard_musicName__2znhM")
        breakout_author_elements = driver.find_elements(By.CLASS_NAME, "ItemCard_autherName__gdrue")

        if len(breakout_songs_elements) != len(breakout_author_elements):
            raise ValueError("Списки должны быть одинаковой длины")

        for breakout_song, breakout_author in zip(breakout_songs_elements, breakout_author_elements):
            breakout_song_text = breakout_song.text
            breakout_author_text = breakout_author.text
            TiktokBreakoutSongsORM.objects.get_or_create(name=breakout_song_text, author=breakout_author_text)
        print("Второй список песен успешно сохранен в базу данных.")
        sleep(5)