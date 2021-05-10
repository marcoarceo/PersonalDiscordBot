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



if __name__ == '__main__':
    # Instantiate the webdriver with the executable location of MS Edge
    browser = webdriver.Edge(r"C:\Program Files\Python37\msedgedriver.exe")

    # Simply just open a new Edge browser and go to the url specified above
    browser.maximize_window()
    browser.get(url)

    schedule.every(10).minutes.do()

