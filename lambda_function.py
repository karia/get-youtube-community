import os
import subprocess
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from requests_oauthlib import OAuth1Session

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

#Get URL List from Google Spreadsheet
def getgs():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    docid = os.environ.get('GSHEET_ID')
    cred_json = 'credentials.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(docid).sheet1

    values_list = worksheet.col_values(1)
    return values_list

#add URL for Google Spreadsheet
def addgs(newurl):
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    docid = os.environ.get('GSHEET_ID')
    cred_json = 'credentials.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(docid).sheet1

    row = [newurl]
    worksheet.append_row(row)
    
    return

#tweet URL
def tweeturl(name,url):
    CK = os.environ.get('CONSUMER_KEY')
    CS = os.environ.get('CONSUMER_SECRET')
    AT = os.environ.get('ACCESS_TOKEN')
    ATS = os.environ.get('ACCESS_TOKEN_SECRET')
    twitter = OAuth1Session(CK, CS, AT, ATS)
    endpoint = "https://api.twitter.com/1.1/statuses/update.json"

    tweet = name + 'のYouTubeコミュニティに新規投稿があるみたいです: ' + url
    params = {"status" : tweet}
    print(params)

    res = twitter.post(endpoint, params = params)
    if res.status_code == 200:
        print("Success.")
    else:
        print("Failed. : %d"% res.status_code)

    return

def lambda_handler(event, context):
    community_url = event['community_url']
    channel_name = event['channel_name']

    chrome = Chrome()
    driver = chrome.headless_lambda()
    driver.get(community_url)

    currentlist = []
    for element in driver.find_elements_by_xpath('//*[@id="published-time-text"]/a'):
        posturl = element.get_attribute('href')
        currentlist.append(posturl)

    driver.quit()

    donelist = getgs()
    diffurls = set(currentlist) - set(donelist)

    if len(diffurls) == 0:
        print('no update')
    else:
        for i in diffurls:
            print('[NEW POST] ' + i)
            tweeturl(channel_name,i)
            addgs(i)
    return
