import sys
import os
import schedule

from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.options import Options

def UrlLoop(browser, urls):
    for url in urls:
        browser.get(url)
        time = CheckStatus(browser)

def CheckStatus(browser):
    try: 
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'live-indicator-container tw-border-radius-large tw-inline')]")))
        try: 
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'channel-status-info channel-status-info--offline tw-border-radius-medium tw-inline-block')]")))
            print("The user is offline")
        except TimeoutException as ex:
            time = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'live-time')]")))
            print ("The user is live " + time.text)
            AvoidDuplicateNoti(time)
    except TimeoutException as ex:
        print("The user is offline")

def AvoidDuplicateNoti(time):
    stringTime = (time.text).split(':')
    if (int(stringTime[0]) == 0 and int(stringTime[1]) <= 10 and int(stringTime[2]) <= 59):
        print("Send notification")
    else:
        print("Duplicate notification")
    

if __name__ == '__main__':
    # Need to extract all of the urls from the database into a list
    urls = ['https://www.twitch.tv/xqcow', 'https://www.twitch.tv/asunaweeb', 'https://www.twitch.tv/grimm', 'https://www.twitch.tv/timthetatman', 'https://www.twitch.tv/shroud']

    # Instantiate the webdriver with the executable location of MS Edge
    browser = webdriver.Edge(r"C:\Program Files\Python37\msedgedriver.exe")

    # Simply just open a new Edge browser and go to the url specified above
    browser.maximize_window()

    schedule.every(10).seconds.do(UrlLoop, browser, urls)

    while 1:
        schedule.run_pending()

