import requests
from loguru import logger
from requests import ConnectTimeout, ReadTimeout
from requests.exceptions import ProxyError
from selenium.common import TimeoutException
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.utils import keys_to_typing


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
