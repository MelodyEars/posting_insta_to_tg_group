""" This file work with Selenium """
import time
import random

from http.client import RemoteDisconnected
from urllib3.exceptions import ProtocolError

import undetected_chromedriver as uc

from loguru import logger
from requests import ReadTimeout

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.utils import keys_to_typing

from SETTINGS import executable_path, google_version


def removeCDC(driver):
    cdc_props: list[str] = driver.execute_script(
        """
        let objectToInspect = window,
            result = [];
        while(objectToInspect !== null)
        { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
          objectToInspect = Object.getPrototypeOf(objectToInspect); }
        return result.filter(i => i.match(/^[a-z]{3}_[a-z]{22}_.*/i))
        """
    )
    if len(cdc_props) < 1:
        return
    cdc_props_js_array = "[" + ", ".join('"' + p + '"' for p in cdc_props) + "]"
    driver.execute_cdp_cmd(
        cmd="Page.addScriptToEvaluateOnNewDocument",
        cmd_args={"source": f"{cdc_props_js_array}.forEach(p => delete window[p] && console.log('removed', p));"},
    )


class EnhancedActionChains(ActionChains):
    def send_keys_1by1(self, keys_to_send, time_s=0.2):
        typing = keys_to_typing(keys_to_send)

        for key in typing:
            self.key_down(key)
            self.key_up(key)
            self.w3c_actions.key_action.pause(time_s)

        return self


class BaseClass:

    def __init__(self):
        self.action = None
        self.DRIVER = uc.Chrome

    def _set_up_driver(self, headless=False):
        options = uc.ChromeOptions()

        options.add_argument("--incognito")

        your_options = {
            "options": options,
            "headless": headless,
            "browser_executable_path": executable_path,
            "user_multi_procs": True,
            "use_subprocess": False,
            "version_main": google_version,
        }

        # if not profile or user_data_dir == incognito
        self.DRIVER = uc.Chrome(**your_options,)
        removeCDC(self.DRIVER)

        self.action = EnhancedActionChains(self.DRIVER)

        self.DRIVER.maximize_window()
        self.DRIVER.delete_all_cookies()

        return self.DRIVER

    def run_driver(self, headless=False):
        try:
            return self._set_up_driver(headless)

        except (ConnectionResetError, ProtocolError, TimeoutError, ReadTimeout,
                ConnectionError, RemoteDisconnected) as e:
            logger.error(f'{type(e).__name__} in selenium_driver.py')
            return self.run_driver(headless)

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
