
import random
import time
from pprint import pprint


import requests
from fake_useragent import UserAgent

from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc

from bs4 import BeautifulSoup


class Chrome(uc.Chrome):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get = None

    def get(self, url):
        # block js execution
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "alert();"})
        # but let get(url) immediately return
        super().get(url)
        # resume js execution
        self.switch_to.alert.accept()
        # immediately stop and restart the service to avoid timings detection
        self.reconnect()
        # this is only needed once per session, is it ?
        self.get = super().get


def get_list_user_posts():
    proxy = 'http://38533:SMehrS2S@185.174.103.162:2831'

    request = requests.get('https://www.tiktok.com/@therock?lang=en', headers={'User-Agent':  UserAgent().random})
    pprint(request.text)


# import requests
#
# def download_video(url, filename):
#     response = requests.get(url)
#     if response.status_code == 200:
#         video_content = response.content
#         with open(filename, 'wb') as file:
#             file.write(video_content)
#         print(f"Відео збережено у файлі: {filename}")
#     else:
#         print("Помилка при отриманні відео")


def get_info_video():

    driver = uc.Chrome(headless=True, browser_executable_path='/usr/bin/chromium', use_subprocess=False)

    def elem_exists(DRIVER, value, by=By.XPATH, wait=120, return_xpath=False, scroll_to=False):
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
            take_xpath = WebDriverWait(DRIVER,
                                       wait,
                                       ignored_exceptions=ignored_exceptions
                                       ).until(EC.presence_of_element_located((by, value)))

            if scroll_to:
                DRIVER.execute_script("arguments[0].scrollIntoView();", take_xpath)
                time.sleep(random.uniform(.5, 1))

            if not return_xpath:
                exist = True
            else:
                # retrurn
                return take_xpath

        except TimeoutException:
            exist = False

        return exist

    try:
        driver.get('https://www.tiktok.com/@mariscookies143/video/7248519845829004587?lang=en')
        elem_exists(driver, 'body', by=By.TAG_NAME, wait=30)
        html = driver.page_source
        # soup = BeautifulSoup(html, 'html.parser')
        with open("page.html", "w", encoding="utf-8") as file:
            file.write(html)
    finally:
        driver.quit()



if __name__ == '__main__':
    # get_info_video()
    get_list_user_posts()
