from multiprocessing import Process
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select


def save_zen(id: str, password: str, position: int):
    """Start browser, login and close browser."""
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://eternmu.cz/")

    login = driver.find_element(By.ID, value="loginBox1")
    login.clear()
    login.send_keys(id)

    pw = driver.find_element(By.ID, value="loginBox2")
    pw.clear()
    pw.send_keys(password)

    btn = driver.find_element(By.CLASS_NAME, value="button-login")
    btn.click()

    reset_link = driver.find_element(By.PARTIAL_LINK_TEXT, value="Webová truhla")
    reset_link.click()

    for _ in range(20):
        driver.execute_script("window.scrollTo(0,800)")

        # select character
        time.sleep(2)
        dropdown = Select(driver.find_elements(By.TAG_NAME, value="select")[2])
        # dropdown.selectByIndex(position)
        dropdown.select_by_index(0)

        # enter amount
        xpath = "//input[(@type='text') and (@name = 'amount')]"
        amount = driver.find_elements(
            By.XPATH,
            value=xpath,
        )[2]
        amount.clear()
        amount.send_keys("100000000")
        driver.execute_script("window.scrollTo(0,800)")

        # click submit
        # time.sleep(2)
        xpath = "//input[(@name='submit_zen')]"
        btn = driver.find_element(By.XPATH, value=xpath)
        btn.click()

    driver.close()


def do_reset_on_web(id: str, password: str, position: int):
    """Start browser, login, reset character and close browser."""
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://eternmu.cz/")

    login = driver.find_element(By.ID, value="loginBox1")
    login.clear()
    login.send_keys(id)

    pw = driver.find_element(By.ID, value="loginBox2")
    pw.clear()
    pw.send_keys(password)

    btn = driver.find_element(By.CLASS_NAME, value="button-login")
    btn.click()

    reset_link = driver.find_element(By.PARTIAL_LINK_TEXT, value="Reset postavy")
    reset_link.click()

    tbody = driver.find_element(By.TAG_NAME, "tbody")
    tr_char = tbody.find_elements(By.TAG_NAME, "tr")[position]
    reset_btn = tr_char.find_element(By.CSS_SELECTOR, value='[title^="Posled"]')
    reset_btn.click()

    driver.execute_script("window.scrollTo(0,500)")

    logout_btn = driver.find_element(By.PARTIAL_LINK_TEXT, value="Log Out")
    logout_btn.click()

    driver.close()
