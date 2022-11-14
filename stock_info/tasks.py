from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import CurrentPrice, Stock, Trade
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/annuresh/Development/my_ideas/tradex")
driver = webdriver.Chrome("/home/annuresh/Development/my_ideas/chromedriver", options=options)


@shared_task
def grow_login():
    """
    Function to login to a groww account
    """
    driver.get("https://groww.in/")
    driver.maximize_window()
    driver.find_element_by_class_name("btn51Btn").click()
    driver.find_element_by_id(
        "login_email1").send_keys("ananthus991@gmail.com")
    driver.find_element_by_class_name("lils382ContinueBtn").click()
    # wait 2 sec
    time.sleep(2)
    driver.find_element_by_id("login_password1").send_keys("1717reshmi")

    driver.find_element_by_class_name("leps592LoginButton").click()
    # wait 4 sec
    time.sleep(4)

    e = driver.find_element_by_id("otpinput88parent")

    for index, item in enumerate(
                    e.find_elements(By.CLASS_NAME, "otpinput88item"), 1):
        item.find_element_by_class_name("otpinput88").send_keys(input())

    for index, item in enumerate(
                    e.find_elements(By.CLASS_NAME, "otpinput88item"), 1):
        if index % 2 == 0:
            item.find_element_by_class_name("otpinput88").send_keys("7")
        else:
            item.find_element_by_class_name("otpinput88").send_keys("1")
    return "LOGIN SUCCESS"


def get_groww():
    driver.get("https://groww.in/")
    driver.maximize_window()
    try:
        for index, item in enumerate(
                        e.find_elements(By.CLASS_NAME, "otpinput88item"), 1):
            if index % 2 == 0:
                item.find_element_by_class_name("otpinput88").send_keys("7")
            else:
                item.find_element_by_class_name("otpinput88").send_keys("1")
        return "login success"
    except:
        return "login success"

print(get_groww())


@shared_task
def stock_price(link):
    driver.get(link)
    time.sleep(2)
    element = driver.find_elements_by_class_name("pbar29Horizontal")
    while True:
        print(float(element[0].get_attribute("aria-valuenow")))

print(stock_price("https://groww.in/stocks/mmtc-ltd"))


def buy(units):
    element = driver.find_element_by_class_name("bso21gsd")
    element.find_elements_by_tag_name("div")[2].click()
    element.find_elements_by_tag_name("div")[1].click()
    share_type = driver.find_elements_by_class_name("ml6")[0]
    if share_type.text != "Intraday":
        share_type.click()
        driver.find_elements_by_class_name("cur-po")[0].click()
    driver.find_element_by_id("inputShare").send_keys(units)
    driver.find_elements_by_class_name("btn51Btn")[1].click()
    # To close successfull popup
    time.sleep(1)
    driver.find_elements_by_class_name("btn51Btn")[1].click()
    return "Successfully brought" + str(units) + "Units"


def sell(units):
    element = driver.find_element_by_class_name("bso21gsd")
    element.find_elements_by_tag_name("div")[2].click()
    share_type = driver.find_elements_by_class_name("ml6")[0]
    if share_type.text != "Intraday":
        share_type.click()
        driver.find_elements_by_class_name("cur-po")[0].click()
    driver.find_element_by_id("inputShare").send_keys(units)
    driver.find_elements_by_class_name("btn51Btn")[1].click()
    time.sleep(1)
    # To close successfull popup
    driver.find_elements_by_class_name("btn51Btn")[1].click()
    return "Saled" + str(units) + "Units"


