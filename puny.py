import sys
import getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import datetime
from datetime import date
import calendar
import re


def strToHour(str):
    return datetime.datetime.strptime(str, "%H:%M")


def click(driver, xpath):
    e = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, xpath)))
    e.click()


def type(driver, xpath, str):
    e = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    e.send_keys(str)


def main():
    user, password = "", ""
    today = []

    with open("classes.json", 'r') as f:
        data = json.load(f)
        user = data["credentials"]["username"]
        password = data["credentials"]["password"]
        today_str = calendar.day_name[date.today().weekday()].lower()
        today = data["calendar"][today_str]

    for c in today:
        building = c["building"]
        classroom = c["classroom"]
        shift_start = strToHour(c["shift_start"])
        shift_end = strToHour(c["shift_end"])

        options = Options()
        options.headless = True
        with webdriver.Firefox(options=options) as driver:
            w = WebDriverWait(driver, 5)
            driver.get("https://www.unimore.it/covid19/trovaaula.html")
            click(driver, "/html/body/div[3]/p/a[1]")
            # waiting for the cookie bar to finish the hiding animation
            time.sleep(0.5)
            click(driver,
                  f"/html/body/div[2]/div[3]/main//li[contains(text(), '{building}')]/a[1]")
            # choosing the classroom and shift
            shifts = driver.find_elements_by_xpath(
                f"//td[contains(text(), '{classroom}')]/parent::tr/td[4]//a")

            found = False
            for s in shifts:
                hours = re.findall("\\d{2}:\\d{2}", s.text)
                start = strToHour(hours[0])
                end = strToHour(hours[1])
                if (start <= shift_start) and (end >= shift_end):
                    found = True
                    s.click()
                    break
            if not found:
                print("can't find your shift")

            # login
            type(driver, "//*[@id='username']", user)
            type(driver, "//*[@id='password']", password)
            click(driver, "/html/body/div/div/div/div[1]/form/div[4]/button")
            # confirm reservation
            click(driver, "/html/body/div[3]/div[4]/form/div/div/p[8]/button")


if __name__ == __name__:
    main()
