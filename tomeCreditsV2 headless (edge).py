from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options
from mailtm import Email
import time

header = ' Enter your referral link '
print(f'\n{header:-^70}')
referralLink = input(">>> ")
print(f'{"":-^70}')

class Bot:
  def setup(self):
    global startTime
    startTime = time.time()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    self.driver = webdriver.Edge(options=options)
    print("\n[LOG] Launching website...")
    self.driver.get(referralLink)

  def quit(self):
    print("[LOG] Quitting...")
    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Onboardingstyles__Title-sc-17kwpbw-2")))
    time.sleep(1)
    text = ' 100 credits added to your account. '
    print(f'{text:.>70}')
    print(f'Time elapsed: {time.time() - startTime} seconds')
    print(f'{"":-^70}')
    self.driver.quit()

  def tempMail(self):
    self.tempMail = Email()
    print("[LOG] Generating temporary email...")
    self.tempMail.register(username=None, password="P@ssword123")
    print("[LOG] Temporary email generated")
    text = ' Your temporary credentials are '
    print(f'\n{text:-^70}')
    print("Mail   >>> " + self.tempMail.address)
    print("Passwd >>> P@ssword123")
    return self.tempMail

  def checkVerificationLink(self, mailText):
    global link
    link = ""
    text = mailText['text'] if mailText['text'] else mailText['html']
    text = text.split(" ")
    text = [x.strip() for x in text]
    text = [x for x in text if x]
    text = [x for x in text if "https://auth.tome.app/u/email-verification?ticket=" in x]
    link = text[0]
    self.driver.get(link)

  def credits(self):
    self.driver.find_element(By.CLASS_NAME, "ButtonReset__StyledResetButton-sc-1eju8s6-0.kDdkdo.TomeButton__ButtonWrapper-sc-1vamjj4-0.hKCJSQ.Invitestyles__StyledButton-w0uhp2-4.bHQWMr").click()
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
    global tempMail
    tempMail = self.tempMail()
    print("\n[LOG] Signing up...")
    self.driver.find_element(By.ID, "email").send_keys(tempMail.address)
    self.driver.find_element(By.ID, "password").send_keys("P@ssword123")
    self.driver.find_element(By.NAME, "action").click()
    print("[LOG] Waiting for verification link...")
    time.sleep(2)
    tempMail.start(self.checkVerificationLink)
    print("[LOG] Verifying email...")
    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Onboardingstyles__Title-sc-17kwpbw-2")))
    time.sleep(2)
    print("[LOG] Signed in")
    tempMail.stop()

while True:
  try:
    browser = Bot()
    browser.setup()
    browser.credits()
    browser.quit()
  except KeyboardInterrupt:
      break
  except:
      pass