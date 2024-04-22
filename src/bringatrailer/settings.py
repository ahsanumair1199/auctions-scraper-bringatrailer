from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# END IMPORTS


# WEBDRIVER CONFIGURATION
options = Options()
options.headless = False
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--window-size=1920,1200")
chrome_prefs = {
    "profile.default_content_setting_values": {
        "images": 2,
    }
}
options.experimental_options["prefs"] = chrome_prefs
chrome_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service, options=options)
# Changing the property of the navigator value for webdriver to undefined
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
