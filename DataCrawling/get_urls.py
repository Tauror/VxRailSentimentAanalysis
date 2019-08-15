import re
import sys
import time
from selenium import webdriver


def get_urls():
    BASE = 'https://www.reddit.com'
    RE_URL = r'/r/[\w]+/comments/.*?/.*?/'
    ROOT_URL = 'http://www.reddit.com/search/?q=vxrail/'
    js = "var q=document.documentElement.scrollTop=100000"

    browser = webdriver.Chrome()
    browser.implicitly_wait(30)
    browser.maximize_window()
    try:
        browser.get(ROOT_URL)
        time.sleep(10)
        first_text = browser.page_source
        # alter = browser.switch_to.alert
        # alter.accept()

        while True:
            browser.execute_script(js)
            time.sleep(5)
            browser.execute_script(js)
            time.sleep(20)
            new_text = browser.page_source
            if new_text != first_text:
                first_text = new_text
            else:
                break
    except Exception as e:
        browser.quit()
        print('Get sub urls failed at:', str(e))
        sys.exit(1)

    browser.quit()

    SUB_URLS = set([BASE + url for url in re.findall(RE_URL, first_text)])
    
    return SUB_URLS


######################   For Test   #####################

# urls = get_urls()
