from multiprocessing import Process
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from datetime import datetime, timedelta


class ResetError(Exception):
    pass


def do_reset(id: str, password: str):
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

    # driver.execute_script("document.body.style.zoom='50%'")
    reset_btn = driver.find_element(By.CSS_SELECTOR, value='[title^="Posled"]')
    reset_btn.click()

    driver.execute_script("window.scrollTo(0,500)")

    logout_btn = driver.find_element(By.PARTIAL_LINK_TEXT, value='Log Out')
    logout_btn.click()

    driver.close()


def reset(id: str, password: str):
    reset.last_time = getattr(reset, "last_time", 0)
    if reset.last_time and datetime.now() - reset.last_time < timedelta(seconds=1200):
        return

    for _ in range(3):
        p = Process(target=do_reset, args=(id, password))
        p.start()
        p.join(30)
        if p.exitcode == 0:
            reset.last_time = datetime.now()
            return

    raise ResetError("Reset failed!")
