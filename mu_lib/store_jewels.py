from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
import re
import time

ID = 'Maraz'
PW = '***REMOVED***'

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://eternmu.cz/")

login = driver.find_element(By.ID, value='loginBox1')
login.clear()
login.send_keys(ID)

pw = driver.find_element(By.ID, value='loginBox2')
pw.clear()
pw.send_keys(PW)

btn = driver.find_element(By.CLASS_NAME, value='button-login')
btn.click()

driver.execute_script("window.scrollTo(0,500)")

web_truhla = driver.find_element(
    By.PARTIAL_LINK_TEXT, value='Webová truhla')
web_truhla.click()

driver.execute_script("window.scrollTo(0,900)")

ddrop_if = driver.find_element(By.ID, value='select - style - 2')

vals = list([str(i.text)
             for i in ddrop_if.find_elements(By.TAG_NAME, 'option')])

for i, option in enumerate(vals):
    ddrop = driver.find_element(By.ID, value='select - style - 2')
    drop = Select(ddrop)
    drop.select_by_index(f'{i}')

    value = re.search("\d+x", option)[0]
    amount = driver.find_element(By.NAME, value='amount')
    amount.clear()
    time.sleep(1)
    amount.send_keys(value[:-1])

    submit = driver.find_element(By.NAME, value='submit_jewel')
    submit.click()
    time.sleep(10)
    driver.execute_script("window.scrollTo(0,900)")

    # print(value)
