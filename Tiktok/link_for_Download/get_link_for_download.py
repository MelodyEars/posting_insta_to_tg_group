import time
import json

from pathlib import Path
from uuid import uuid4

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

from Tiktok.Settings_Selenium import BaseClass


class ssstik_io(BaseClass):
    def __init__(self, proxy=None):
        super().__init__()
        self.download_path = Path('tiktok_videos')
        self.proxy = proxy

    def __enter__(self):
        self.DRIVER = self.run_driver(proxy=self.proxy, headless=True, download_path=self.download_path)

        self.DRIVER.get('https://ssstik.io/en')
        self.elem_exists('body', by=By.TAG_NAME, wait=120)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            folder = Path('mistakes')
            folder.mkdir(exist_ok=True)
            self.DRIVER.save_screenshot(folder / "TikTokApiMistake.png")

        self.DRIVER.quit()

    @staticmethod
    def download_video(url: str) -> Path:
        folder = Path('tiktok_videos')

        name_video = str(uuid4()) + ".mp4"

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

    def get_info_video(self, url_tiktok_video) -> tuple[str, Path]:
        self.send_text_by_elem(value='main_page_text', text_or_key=url_tiktok_video + "\n", by=By.ID, wait=120)
        time.sleep(2)
        link_video = self.elem_exists('//div[@id="target"]//a', wait=120, return_xpath=True).get_attribute("href")
        name = self.elem_exists('p.maintext', by=By.CSS_SELECTOR, wait=120).text()
        video_path = self.download_video(link_video)

        return name, video_path

    def back_page(self):
        self.DRIVER.back()

    def get_all_video_by_tiktokname(self, tiktok_name: str, scroll=False):
        self.DRIVER.get(f'https://www.tiktok.com/@{tiktok_name}?lang=en')
        self.elem_exists('body', by=By.TAG_NAME, wait=120)

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
        return video_list


if __name__ == '__main__':
    with ssstik_io() as api:
        print(len(api.get_all_video_by_tiktokname("therock", scroll=True)))
        api.DRIVER.quit()


