""" This file work with Selenium """
import time
import random

from http.client import RemoteDisconnected
from urllib3.exceptions import ProtocolError

import undetected_chromedriver as uc

from loguru import logger
from requests import ReadTimeout, JSONDecodeError

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from SETTINGS import executable_path, google_version, PROXY
from Tiktok.Settings_Selenium.Extensions import ProxyExtension
from Tiktok.Settings_Selenium.SuportDriver import removeCDC, EnhancedActionChains, proxy_data, geolocation


class BaseClass:

    def __init__(self):
        self.action = None
        self.DRIVER = uc.Chrome

    def _set_up_driver(self, headless=False):
        your_options = {
            "headless": headless,
            "browser_executable_path": executable_path,
            "user_multi_procs": True,
            "use_subprocess": False,
            "version_main": google_version,
        }

        options = uc.ChromeOptions()

        options.add_argument("--incognito")

        if PROXY:
            # proxy = ("64.32.16.8", 8080, "username", "password")  # your proxy with auth, this one is obviously fake
            # pass  host, port, user, password
            proxy_extension = ProxyExtension(**PROXY)
            options.add_argument(f"--load-extension={proxy_extension.directory}")
            resp = proxy_data(PROXY)

            # ____________________________ location _______________________________
            try:
                capabilities = geolocation(resp.json()['loc'])
                your_options['desired_capabilities'] = capabilities
            except JSONDecodeError:
                raise Exception("Щось не так з проксі. Було залучено останній з файлу 'proxies.txt'")

        # if not profile or user_data_dir == incognito
        self.DRIVER = uc.Chrome(options=options, **your_options,)
        removeCDC(self.DRIVER)

        self.action = EnhancedActionChains(self.DRIVER)

        self.DRIVER.maximize_window()
        self.DRIVER.delete_all_cookies()

        return self.DRIVER

    def run_driver(self, args, kwargs):
        try:
            return self._set_up_driver(*args, **kwargs)

        except (ConnectionResetError, ProtocolError, TimeoutError, ReadTimeout,
                ConnectionError, RemoteDisconnected) as e:
            logger.error(f'{type(e).__name__} in selenium_driver.py')
            return self.run_driver(*args, **kwargs)

    def elem_exists(self, value, by=By.XPATH, wait=120, return_xpath=False, scroll_to=False):
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
            take_xpath = WebDriverWait(self.DRIVER,
                                       wait,
                                       ignored_exceptions=ignored_exceptions
                                       ).until(EC.presence_of_element_located((by, value)))

            if scroll_to:
                self.DRIVER.execute_script("arguments[0].scrollIntoView();", take_xpath)
                time.sleep(random.uniform(.5, 1))

            if not return_xpath:
                exist = True
            else:
                # retrurn
                return take_xpath

        except TimeoutException:
            exist = False

        return exist

    def _intercepted_click(self, elem_for_click):
        try:
            elem_for_click.click()
        except ElementClickInterceptedException:
            time.sleep(.5)
            self._intercepted_click(elem_for_click)

    def click_element(
            self, value, by=By.XPATH, wait=60, move_to=True, scroll_to=False, intercepted_click=False
    ) -> bool:

        if scroll_to:
            self.elem_exists(value=value, by=by, wait=wait, scroll_to=True)

        try:
            elem_for_click = WebDriverWait(self.DRIVER, wait).until(EC.element_to_be_clickable((by, value)))
        except TimeoutException:
            return False

        if move_to:
            self.mouse_move_to(elem_for_click)
            time.sleep(random.uniform(0.3, 0.7))

        if intercepted_click:
            self._intercepted_click(elem_for_click)
        else:
            elem_for_click.click()

        return True

    def send_text_by_elem(self, value, text_or_key, by=By.XPATH, scroll_to=False, wait=60):

        if self.click_element(value, by=by, scroll_to=scroll_to, wait=wait, move_to=True):
            research_xpath = self.DRIVER.find_element(by, value=value)

            research_xpath.clear()
            research_xpath.send_keys(text_or_key)

        else:
            input(f"No found or no be clickable {value}")

    def refrash_page(self):
        """if you have "Not Found data" call this function"""
        self.DRIVER.refresh()
        self.DRIVER.reconnect(.5)

    def switch_iframe_xpath(self, value, by=By.XPATH, wait=60):
        try:
            WebDriverWait(self.DRIVER, wait).until(
                EC.frame_to_be_available_and_switch_to_it((by, value)))
            return True
        except TimeoutException:
            return False

    def come_back_iframe(self):
        self.DRIVER.switch_to.parent_frame()

    def mouse_move_to(self, element):
        # perform the operation
        self.action.move_to_element(element).pause(1).perform()

    def scroll_to_elem(self, value):
        web_elem = self.elem_exists(value, return_xpath=True)
        self.DRIVER.execute_script("arguments[0].scrollIntoView();", web_elem)

    def reset_actions(self):
        self.action.reset_actions()

    def close_alert(self, url, wait=0.3):
        self.DRIVER.execute_script(f"location='{url}'; alert();")
        self.DRIVER.switch_to.alert.accept()
        self.DRIVER.reconnect(wait)
