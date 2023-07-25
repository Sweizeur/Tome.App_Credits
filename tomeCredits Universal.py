from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from mailtm import Email
import time

counter = 0
def increment_counter():
    global counter
    counter += 1
    return counter

class Boot:
  def selectBrowser(self):
    header = ' Select your browser [chrome | edge | firefox | safari] '
    print(f'\n{header:-^70}')
    global browserPath
    browserPath = input(">>> ")
    print(f'{"":-^70}')

  def headlessMode(self):
    header = ' Start in headless mode (no window) ?  [yes | no]'
    print(f'\n{header:-^70}')
    global headlessMode
    headlessMode = input(">>> ")
    print(f'{"":-^70}')

  def referralLink(self):
    header = ' Enter your referral link '
    print(f'\n{header:-^70}')
    global referralLink
    referralLink = input(">>> ")
    print(f'{"":-^70}')

class Browsers:
  def chrome():
    browserOptions = ChromeOptions()
    browserOptions.add_argument('--headless')
    global driver
    driver = webdriver.Chrome(options=browserOptions)
    print("[LOG] Launching website...")
    driver.get(referralLink)
  def chromeGUI():
    global driver
    driver = webdriver.Chrome()
    driver.set_window_size(375, 812)
    print("[LOG] Launching website...")
    driver.get(referralLink)
  
  def edge():
    browserOptions = EdgeOptions()
    browserOptions.add_argument('--headless')
    global driver
    driver = webdriver.Edge(options=browserOptions)
    print("[LOG] Launching website...")
    driver.get(referralLink)
  def edgeGUI():
    global driver
    driver = webdriver.Edge()
    driver.set_window_size(375, 812)
    print("[LOG] Launching website...")
    driver.get(referralLink)

  def firefox():
    browserOptions = FirefoxOptions()
    browserOptions.headless = True
    global driver
    driver = webdriver.Firefox(options=browserOptions)
    print("[LOG] Launching website...")
    driver.get(referralLink)
  def firefoxGUI():
    global driver
    driver = webdriver.Firefox()
    driver.set_window_size(375, 812)
    print("[LOG] Launching website...")
    driver.get(referralLink)

  def safari():
    global driver
    driver = webdriver.Safari()
    driver.set_window_size(375, 812)
    print("[LOG] Launching website...")
    driver.get(referralLink)

class Bot:
  def setup(self):
    if headlessMode.lower() == "no":
      if browserPath.lower() == "chrome":
        Browsers.chromeGUI()
      elif browserPath.lower() == "edge":
        Browsers.edgeGUI()
      elif browserPath.lower() == "firefox":
        Browsers.firefoxGUI()
      elif browserPath.lower() == "safari":
        Browsers.safari()
      else:
        print("[ERROR] Invalid browser")
        pass
    else: 
      quit()

  def quit(self):
    print("[LOG] Quitting...")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Onboardingstyles__Title-sc-17kwpbw-1.bhgVsD")))
    time.sleep(1)
    print(f'{" 100 credits added to your account. ":.>70}')
    print(f'Time elapsed: {time.time() - startTime} seconds')
    print(f'{"":=^70}')
    driver.quit()

  def tempMail(self):
    tempMail = Email()
    print("[LOG] Generating temporary email...")
    tempMail.register(username=None, password="P@ssword123")
    print("\nMail   >>> " + tempMail.address)
    print("Passwd >>> P@ssword123")
    return tempMail

  def checkVerificationLink(self, mailText):
    global link
    link = ""
    text = mailText['text'] if mailText['text'] else mailText['html']
    text = text.split(" ")
    text = [x.strip() for x in text]
    text = [x for x in text if x]
    text = [x for x in text if "https://auth.tome.app/u/email-verification?ticket=" in x]
    link = text[0]
    driver.get(link)

  def credits(self):
    driver.find_element(By.CSS_SELECTOR, ".ButtonReset__StyledResetButton-sc-1eju8s6-0.hpPtek.TomeButton__ButtonWrapper-sc-1vamjj4-0.hKCJSQ.Invitestyles__StyledButton-w0uhp2-4.bHQWMr").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
    global tempMail
    tempMail = self.tempMail()
    print("\n[LOG] Signing up...")
    driver.find_element(By.ID, "email").send_keys(tempMail.address)
    driver.find_element(By.ID, "password").send_keys("P@ssword123")
    driver.find_element(By.NAME, "action").click()
    print("[LOG] Signed in")
    time.sleep(2)
    print("[LOG] Verifying email...")
    tempMail.start(self.checkVerificationLink)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Onboardingstyles__Title-sc-17kwpbw-1.bhgVsD")))
    print("[LOG] Email verified")
    time.sleep(2)
    tempMail.stop()

start = Boot()
start.selectBrowser()
start.headlessMode()
start.referralLink()

while True:
  startTime = time.time()
  increment_counter()
  print(f'{"":=^70}')
  print(f'{"Run " + str(counter) + ":":^70}')
  browser = Bot()
  if headlessMode.lower() == "yes":
    if browserPath.lower() == "chrome":
      Browsers.chrome()
    elif browserPath.lower() == "edge":
      Browsers.edge()
    elif browserPath.lower() == "firefox":
      Browsers.firefox()
    elif browserPath.lower() == "safari":
      print("[ERROR] Safari does not support headless mode, continuing with GUI...")
      Browsers.safari()
    else:
      print("[ERROR] Invalid browser")
      quit()
  elif headlessMode.lower() == "no":
    browser.setup()
  else:
    print('[ERROR] Please choose "yes" or "no"')
    quit()
  browser.credits()
  browser.quit()