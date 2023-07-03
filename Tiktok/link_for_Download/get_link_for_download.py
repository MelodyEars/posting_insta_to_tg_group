import time
import json

from pathlib import Path
from uuid import uuid4

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

from Tiktok.Settings_Selenium import BaseClass
from SETTINGS import TIKTOK_BROWSER_HEADLESS


class TiktokDownloader(BaseClass):
    def __init__(self, tt_name: str, proxy=None):
        super().__init__()
        self.tt_name = tt_name
        self.proxy = proxy

    def __enter__(self):
        self.DRIVER = self.run_driver(headless=TIKTOK_BROWSER_HEADLESS)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            folder = Path('mistakes')
            folder.mkdir(exist_ok=True)
            self.DRIVER.save_screenshot(folder / "TikTokApiMistake.png")

        self.DRIVER.quit()

    # _________________________________________________________________  download video
    @staticmethod
    def download_video(url: str, video_num: str | int) -> Path:
        folder = Path('tiktok_videos')

        name_video = str(video_num) + ".mp4"

        folder.mkdir(exist_ok=True)

        filepath = folder / name_video
        response = requests.get(url, headers={'User-Agent': UserAgent().random})

        if response.status_code == 200:
            video_content = response.content
            with open(filepath, 'wb') as file:
                file.write(video_content)
            print(f"Відео збережено у файлі: {filepath}")

        else:
            print("Помилка при отриманні відео")

        return filepath

    def get_info_video(self, video_num: str | int) -> tuple[str, Path]:
        url_tiktok_video = f'https://www.tiktok.com/@{self.tt_name}/video/{video_num}?lang=en'

        # attend site for download video without watermark
        self.DRIVER.get('https://ssstik.io/en')
        self.elem_exists('body', by=By.TAG_NAME, wait=120)

        # input url
        self.send_text_by_elem(value='main_page_text', text_or_key=url_tiktok_video + "\n", by=By.ID, wait=120)
        time.sleep(2)

        # get link for download
        link_video = self.elem_exists('//div[@id="target"]//a', wait=120, return_xpath=True).get_attribute("href")

        # get info about video(name, hashtag)
        name = self.elem_exists('p.maintext', by=By.CSS_SELECTOR, wait=120, return_xpath=True).text

        video_path: Path = self.download_video(link_video, video_num)

        return name, video_path

    # _________________________________________________________________  get all video from user
    def get_all_video_by_tiktokname(self, scroll=False) -> list:
        # go to main page of user
        self.DRIVER.get(f'https://www.tiktok.com/@{self.tt_name}?lang=en')
        self.elem_exists('body', by=By.TAG_NAME, wait=120)

        # in order to get all videos need to scroll a page
        if scroll:
            offset = 30
            while self.elem_exists(f'(//div[@data-e2e="user-post-item-list"]/div)[{offset}]', scroll_to=True, wait=30):
                offset += 30
                print(f"offset: {offset}")
                # time.sleep(5)

        # Отримуємо вміст елемента
        content = self.elem_exists("SIGI_STATE", by=By.ID, return_xpath=True).get_attribute("innerHTML")

        # Створюємо об'єкт BeautifulSoup для парсингу HTML
        soup = BeautifulSoup(content, "html.parser")

        # Знаходимо необхідні дані в JSON-структурі
        json_data = json.loads(soup.text)

        video_list = list(json_data['ItemList']["user-post"]["list"])
        print(f"Count videos: {len(video_list)}")
        return video_list
