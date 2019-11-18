import os
import subprocess

from selenium import webdriver

class Chrome:
    def headless_lambda(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/headless/python/bin/headless-chromium"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-infobars")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--homedir=/tmp")
    
        driver = webdriver.Chrome(
            executable_path="/opt/headless/python/bin/chromedriver",
            chrome_options=options
        )
        return driver

def lambda_handler(event, context):
    community_url=os.environ.get('COMMUNITY_URL')

    chrome=Chrome()
    driver=chrome.headless_lambda()
    driver.get(community_url)

    urllist = []
    for element in driver.find_elements_by_xpath('//*[@id="published-time-text"]/a'):
        posturl = element.get_attribute('href')
        urllist.append(posturl)

    return urllist
    driver.quit()
