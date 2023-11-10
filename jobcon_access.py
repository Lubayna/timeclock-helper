from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import json 

f = open('credentials.json')
data = json.load(f)

url= data["JOBCON_URL"] 
user=data["JOBCON_ID"] 
password=data["JOBCON_PASSWORD"] 

chrome_options = Options()

def stamp(ts_and_text):
  ts = ts_and_text['ts']
  text = ts_and_text['text']
  if text == '業務開始します' or text == '打刻表を確認する' or text == '業務終了します':
      driver = webdriver.Chrome()
      driver.get(url)
      driver.find_element(By.ID, 'user_email').send_keys(user)
      driver.find_element(By.ID, 'user_password').send_keys(password)
      driver.find_element(By.ID, "login_button").click()
      time.sleep(3)
      
      if text == '業務開始します':
        driver.find_element(By.ID, 'adit-button-work-start').click()

      elif text == '打刻表を確認する':
        driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/div[2]/div/a[1]').click()

      elif text == '業務終了します':
        driver.find_element(By.ID, 'adit-button-work-end').click()
      time.sleep(3)
      driver.quit()


