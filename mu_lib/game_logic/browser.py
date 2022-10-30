from multiprocessing import Process
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


def do_reset(id: str, password: str, position: int):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://eternmu.cz/")

    login = driver.find_element(By.ID, value='loginBox1')
    login.clear()
    login.send_keys(id)

    pw = driver.find_element(By.ID, value='loginBox2')
    pw.clear()
    pw.send_keys(password)

    btn = driver.find_element(By.CLASS_NAME, value='button-login')
    btn.click()

    reset_link = driver.find_element(
        By.PARTIAL_LINK_TEXT, value='Reset postavy')
    reset_link.click()

    tbody = driver.find_element_by_tag_name("tbody")
    tr_char = tbody.find_elements(By.TAG_NAME, "tr")[position]
    reset_btn = tr_char.find_element(
        By.CSS_SELECTOR, value='[title^="Posled"]')
    reset_btn.click()

    driver.execute_script("window.scrollTo(0,500)")

    logout_btn = driver.find_element(By.PARTIAL_LINK_TEXT, value='Log Out')
    logout_btn.click()

    driver.close()
