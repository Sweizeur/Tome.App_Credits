from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from mailtm import Email

lien = input("Enter the referral link >> ")

while True:
    try:
        link = ""
        def listener(message):
            mess = message['text'] if message['text'] else message['html']
            mess = mess.split(" ")
            mess = [x.strip() for x in mess]
            mess = [x for x in mess if x]
            mess = [x for x in mess if "https://auth.tome.app/u/email-verification?ticket=" in x]
            global link
            link = mess[0]
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(lien)
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "ButtonReset__StyledResetButton-sc-1eju8s6-0.kDdkdo.TomeButton__ButtonWrapper-sc-1vamjj4-0.hKCJSQ.Invitestyles__StyledButton-w0uhp2-4.bHQWMr").click()
        time.sleep(3)
        mail = Email()
        mail.register()
        driver.find_element(By.NAME, "email").send_keys(str(mail.address))
        driver.find_element(By.NAME, "password").send_keys("password1234@")
        driver.find_element(By.NAME, "action").click()
        mail.start(listener)
        time.sleep(5)
        driver.get(link)
        time.sleep(2)
        mail.stop()
        print("+100 additional credits")
        driver.quit()
    except KeyboardInterrupt:
        break
    except:
        pass