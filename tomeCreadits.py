from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from mailtm import Email
import time

header = ' Enter your referral link '
print(f'\n{header:-^70}')
referralLink = input(">>> ")
print(f'{"":-^70}')

BROWSERS = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox,
    "safari": webdriver.Safari,
    "edge": webdriver.Edge,
    "opera": webdriver.Opera,
    "ie": webdriver.Ie,
    # Ajouter d'autres navigateurs pris en charge si nécessaire
}

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

header1 = ' Browser name (chrome, firefox, safari, edge, opera, ie)'
print(f'\n{header1:-^70}')
browserpath = input(">>> ")
print(f'{"":-^70}')

class Bot:
  def setup(self):
    driver_class = BROWSERS.get(browserpath.lower())
    if driver_class is None:
      print("Browser not supported")
      quit()
    else:
      # Instancier l'objet webdriver
      self.driver = driver_class()
    self.driver.set_window_size(375, 812)
    self.driver.get(referralLink)

  def quit(self):
    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Onboardingstyles__Title-sc-17kwpbw-2")))
    time.sleep(1)
    text = ' 100 credits added to your account. '
    print(f'{text:.>70}')
    print(f'{"":-^70}')
    self.driver.quit()

  def tempMail(self):
    self.tempMail = Email()
    print("\n[LOG] Generating temporary email...")
    self.tempMail.register(username=None, password="P@ssword123")
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
    self.driver.find_element(By.ID, "email").send_keys(tempMail.address)
    self.driver.find_element(By.ID, "password").send_keys("P@ssword123")
    self.driver.find_element(By.NAME, "action").click()
    time.sleep(2)
    tempMail.start(self.checkVerificationLink)
    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Onboardingstyles__Title-sc-17kwpbw-2")))
    time.sleep(2)
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
