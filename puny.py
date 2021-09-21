from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
from selenium.webdriver.firefox.options import Options
import datetime
from datetime import date
import calendar

options = Options()
options.headless = True

today_str = calendar.day_name[date.today().weekday()].lower()
f = open("classes.json")
data = json.load(f)
user = data["credentials"]["username"]
password = data["credentials"]["password"]
today = data["calendar"][today_str]

for c in today:
    building = c["building"]
    classroom = c["classroom"]
    shift = c["shift"]
    with webdriver.Firefox() as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.unimore.it/covid19/trovaaula.html")
        # accept cookies
        driver.find_element_by_xpath("/html/body/div[3]/p/a[1]").click()
        time.sleep(0.5)
        # choosing the building
        driver.find_element_by_xpath(
            f"/html/body/div[2]/div[3]/main//li[contains(text(), '{building}')]/a[1]").click()
        # choosing the classroom and shift
        driver.find_element_by_xpath(
            f"//td[contains(text(), '{classroom}')]/parent::tr/td[4]//a[contains(text(), '{shift}')]").click()
        time.sleep(0.5)
        # login
        driver.find_element_by_xpath("//*[@id='username']").send_keys(user)
        driver.find_element_by_xpath("//*[@id='password']").send_keys(password)
        driver.find_element_by_xpath(
            "/html/body/div/div/div/div[1]/form/div[4]/button").click()
        # confirm reservation
        time.sleep(0.5)
        driver.find_element_by_xpath(
            "/html/body/div[3]/div[4]/form/div/div/p[8]/button").click()
        input()
