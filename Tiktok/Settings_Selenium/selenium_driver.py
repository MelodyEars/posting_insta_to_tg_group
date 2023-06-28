""" This file work with Selenium """
import time
import random
from http.client import RemoteDisconnected

import requests

import undetected_chromedriver as uc

from loguru import logger
from requests import JSONDecodeError, ReadTimeout
from requests.exceptions import ProxyError, ConnectTimeout

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib3.exceptions import ProtocolError

# from base_exception import ProxyInvalidException
from SETTINGS import executable_path

from .SeleniumExtension import EnhancedActionChains, ProxyExtension


def removeCDC(driver):
    cdc_props: list[str] = driver.execute_script(  # type: ignore
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

    # file_bin = re.sub(rb"\$cdc_[a-zA-Z0-9]{22}_", lambda m: bytes(
    #     random.choices((string.ascii_letters + string.digits).encode("ascii"), k=len(m.group()))), file_bin)


def geolocation(loc_value_JSON: str):
    data = loc_value_JSON.split(",")
    latitude = float(data[0])
    longitude = float(data[1])
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['locationContextEnabled'] = True
    capabilities['locationContextDefaultZoomLevel'] = 13
    capabilities['locationContextEnabled'] = True
    capabilities['locationContextMaxDistance'] = 10000
    capabilities['locationContextGeoLocation'] = {'latitude': latitude, 'longitude': longitude}

    return capabilities


def proxy_data(proxy: dict):
    proxies = {"http": f"http://{proxy['user']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"}
    url = "http://ipinfo.io/json"

    try:
        resp = requests.get(url, proxies=proxies, timeout=10)

    except (ConnectionError, TimeoutException, ConnectionResetError, TimeoutError, ReadTimeout, ConnectTimeout):
        logger.error(f"Щось з проксі {proxy['user']}:{proxy['password']}:{proxy['host']}:{proxy['port']}!")
        return proxy_data(proxy)
    except ProxyError:
        logger.error(f"Щось з проксі {proxy['user']}:{proxy['password']}:{proxy['host']}:{proxy['port']}!")
        raise Exception("ProxyError: Invalid proxy ")
    logger.info(resp)
    return resp


# class Chrome(uc.Chrome):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.get = None
#
#     def get(self, url):
#         # block js execution
#         self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "alert();"})
#         # but let get(url) immediately return
#         super().get(url)
#         # resume js execution
#         self.switch_to.alert.accept()
#         # immediately stop and restart the service to avoid timings detection
#         self.reconnect()
#         # this is only needed once per session, is it ?
#         self.get = super().get

        # driver.execute_script("""setTimeout(() => window.location.href="https://www.bet365.com", 100)""");


class BaseClass:

    def __init__(self):
        self.action = None
        self.DRIVER = uc.Chrome

    def __set_new_download_path(self, download_path):
        # Defines auto download and download PATH
        params = {
            "behavior": "allow",
            "downloadPath": str(download_path)
        }

        self.DRIVER.execute_cdp_cmd("Page.setDownloadBehavior", params)

        return self.DRIVER

    def _set_up_driver(self, browser_executable_path=executable_path,
                   download_path="default", proxy=None, headless=False, detection_location=True):

        resp = None

        your_options = {}
        options = uc.ChromeOptions()

        if proxy is not None:
            # proxy = ("64.32.16.8", 8080, "username", "password")  # your proxy with auth, this one is obviously fake
            # pass  host, port, user, password
            proxy_extension = ProxyExtension(**proxy)
            options.add_argument(f"--load-extension={proxy_extension.directory}")
            resp = proxy_data(proxy)

            # ____________________________ location _______________________________
            if detection_location:
                try:
                    capabilities = geolocation(resp.json()['loc'])
                    your_options['desired_capabilities'] = capabilities
                except JSONDecodeError:
                    raise Exception("Щось не так з проксі. Було залучено останній з файлу 'proxies.txt'")

        your_options["headless"] = headless
        your_options["options"] = options
        your_options["browser_executable_path"] = browser_executable_path

        # if not profile or user_data_dir == incognito
        self.DRIVER = uc.Chrome(**your_options, user_multi_procs=True, use_subprocess=False)

        removeCDC(self.DRIVER)

        self.DRIVER.maximize_window()
        self.action = EnhancedActionChains(self.DRIVER)

        # __________________________________ timezone _________________________________
        if proxy is not None:
            tz_params = {'timezoneId': resp.json()['timezone']}
            self.DRIVER.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)

        # if you need download to your folder
        if download_path == "default":
            return self.DRIVER

        else:
            return self.__set_new_download_path(download_path)

    def run_driver(self, browser_executable_path=executable_path,
                   download_path="default", proxy=None, headless=False, detection_location=True):
        try:
            return self._set_up_driver(browser_executable_path, download_path, proxy, headless, detection_location)

        except (ConnectionResetError, ProtocolError, TimeoutError, ReadTimeout,
                ConnectionError, RemoteDisconnected) as e:
            logger.error(f'{type(e).__name__} in selenium_driver.py')
            return self.run_driver(browser_executable_path, download_path, proxy, headless, detection_location)

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

    def stealth_send_text(self, value, text_or_key, by=By.XPATH, scroll_to=False, wait=60):
        if self.click_element(value, by=by, scroll_to=scroll_to, wait=wait):
            self.action.send_keys_1by1(text_or_key).perform()

    def reset_actions(self):
        self.action.reset_actions()

    def close_alert(self, url, wait=0.3):
        self.DRIVER.execute_script(f"location='{url}'; alert();")
        self.DRIVER.switch_to.alert.accept()
        self.DRIVER.reconnect(wait)
