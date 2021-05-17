import sys
import os
import schedule
import asyncio

from decouple import config
from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=config('DBPASS'),
    database="DiscordBotDB"
)

mycursor = mydb.cursor()

async def UrlLoop(browser, urls, bot):
    for url in urls:
        browser.get(url)
        await CheckStatus(browser, url, bot)
    await asyncio.sleep(60)

async def CheckStatus(browser, url, bot):
    try: 
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sc-AxjAm dZHTyF live-indicator-container')]")))
        try: 
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sc-AxjAm idVdfv channel-status-info channel-status-info--offline')]")))
            print(url + " is offline (False Positive)")
        except TimeoutException as ex:
            time = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'live-time')]")))
            print (url + " is live " + time.text)
            await AvoidDuplicateNoti(time, url, bot)
    except TimeoutException as ex:
        print(url + " is offline (Positive False)")

async def AvoidDuplicateNoti(time, url, bot):
    stringTime = (time.text).split(':')
    if (int(stringTime[0]) == 0 and int(stringTime[1]) <= 10 and int(stringTime[2]) <= 59):
        print("Send notification")
        channel = bot.get_channel(840394456585863228)
        await channel.send(url + " IS LIVE!")
    else:
        print("Duplicate notification")

async def TwitchMain(bot):
    await bot.wait_until_ready()

    options = FirefoxOptions()
    options.add_argument("--headless")

    # Instantiate the webdriver with the executable location of MS Edge
    browser = webdriver.Firefox(executable_path=r'C:\Users\Marco PC\Desktop\Projects\geckodriver.exe', options=options)

    while True:
        await FetchUrls(browser, bot)

async def FetchUrls(browser, bot):
    urls = []
    mycursor.execute("SELECT * FROM twitchurls")
    result = mycursor.fetchall()
    for x in result:
        urls.append(x[0])
    mydb.commit()
    await UrlLoop(browser, urls, bot)