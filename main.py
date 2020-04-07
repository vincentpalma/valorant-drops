# https://github.com/jg-fisher/protonMailGenerator/blob/master/emails.py
# https://github.com/ohyou/twitch-viewer

import pickle
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select

valid_accounts = {'DfsGUhyLwu':'Cotonchien55'}
proxies = ['51.158.180.179:8811','94.23.253.212:8080','82.119.170.106:8080','51.79.52.62:3128',
'176.31.141.22:51327','151.80.201.162:1080','178.33.14.216:9999','163.172.189.32:8811','51.158.180.179:8811',
'51.158.123.250:8811','51.158.165.18:8811','163.172.190.160:8811','51.158.172.165:8811','94.23.253.212:8080',
'51.38.105.215:1080','54.37.103.99:3128','51.158.111.242:8811','51.15.118.97:8080','91.121.67.146:9050',
'51.254.182.63:44241','92.222.155.168:41020','51.158.180.150:8811','51.158.186.242:8811','51.38.127.211:8080',
'51.79.159.45:8080','51.77.91.194:3128','163.172.146.119:8811','51.158.68.133:8811','137.74.157.159:1080',
'176.31.141.20:51327','163.172.180.18:8811','51.158.68.68:8811','62.210.91.240:80','51.158.119.88:8811',
'163.172.109.132:65420','51.68.61.17:8080','51.178.166.182:3128','51.158.98.121:8811']

ip = proxies[0].split(':')[0]
port = proxies[0].split(':')[1]

stream_url = 'https://www.twitch.tv/summit1g'

import random
import string

def randomString(stringLength=13):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

###########################################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={proxies[0]}')
#chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)

def recup(filename):
  pickle.dump(driver.get_cookies() , open(filename,"wb"))

def create_twitch_account(username,password,email,number):
  print('Creation of account number',number)
  print('Mail creation...')
  driver.get('https://mail.tutanota.com/signup')
  input('Email :',email.split('@')[0],'\nPassword :',password,'\nPress ENTER when finished')

  print('Riot account creation...')
  driver.get('https://signup.euw.leagueoflegends.com/en/signup/index#/')
  driver.find_element_by_css_selector("input[name='email']").send_keys(email+'@tutanota.com')
  driver.find_element_by_xpath("//div[contains(@class,'next-button')]/button").click()
  time.sleep(1)
  select = Select(driver.find_element_by_css_selector("select[name='dob-day']"))
  select.select_by_value(str(random.randint(1,27)))
  select = Select(driver.find_element_by_css_selector("select[name='dob-month']"))
  select.select_by_value(str(random.randint(1,12)))
  select = Select(driver.find_element_by_css_selector("select[name='dob-year']"))
  select.select_by_value(str(random.randint(1995,2000)))
  driver.find_element_by_xpath("//div[contains(@class,'next-button')]/button").click()
  time.sleep(1)

  driver.find_element_by_css_selector("input[name='username']").send_keys(username)
  driver.find_element_by_css_selector("input[name='password']").send_keys(password)
  driver.find_element_by_css_selector("input[name='confirm_password']").send_keys(password)
  input('Check box and do captcha, then press ENTER')

  print('Twitch account creation...')
  driver.get('https://www.twitch.tv/')
  driver.find_element_by_css_selector("button[data-a-target='signup-button']").click()
  
  ok = False
  while not ok:
    try:
      driver.find_element_by_css_selector("input[id='signup-username']")
      ok = True
    except:
      time.sleep(0.1)

  driver.find_element_by_css_selector("input[id='signup-username']").send_keys(username)
  driver.find_element_by_css_selector("input[id='password-input']").send_keys(password)
  driver.find_element_by_css_selector("input[id='password-input-confirmation']").send_keys(password)

  select = Select(driver.find_element_by_css_selector("select[data-a-target='birthday-month-select']"))
  select.select_by_value(str(random.randint(1,12)))
  driver.find_element_by_xpath("//div[contains(@data-a-target,'birthday-date-input')]/input").send_keys(str(random.randint(1,27)))
  driver.find_element_by_xpath("//div[contains(@data-a-target,'birthday-year-input')]/input").send_keys(str(random.randint(1995,2000)))

  driver.find_element_by_css_selector("input[id='email-input']").send_keys(email)
  time.sleep(0.5)
  driver.find_element_by_css_selector("button[data-a-target='passport-signup-button']").click()

  input('Press ENTER when finished mail confirmation and Riot linking')

  fn = 'cookie'+str(number)+'.pkl'
  recup(fn)
  return [username,password,email,fn]

def check_proxy(proxy):
  driver.get("https://ipv4.wtfismyip.com/text")
  soup = BeautifulSoup(driver.page_source,'html.parser')
  if proxy.split(':')[0] + '\n' == soup.text:
    print(f'PROXY CONNECTED, IP = {ip}')
    return True
  else:
    print(f'PROXY FAILED TO CONNECT TO {ip}')
    print('IPv4 is :',soup.text)
    return False

def check_ping():
  t = time.time()
  driver.get('https://www.twitch.tv/')
  while time.time() - t < 7:
    driver.find_element_by_css_selector("button[data-a-target='signup-button']").click()
  z = time.time()
  if z-t < 7:
    return True
  driver.Quit()
  return False
    
 

# Check valid proxies

# valid_proxies = []
# for proxy in proxies:
#   chrome_options = webdriver.ChromeOptions()
#   chrome_options.add_argument(f'--proxy-server={proxy}')

#   driver = webdriver.Chrome(chrome_options=chrome_options)
#   a = check_proxy(proxy)
#   if a:
#     valid_proxies.append(proxy)
#   driver.quit()
#   print(valid_proxies)

pickle.dump(valid_proxies,open("valid_proxies.txt","wb"))
# create_twitch_account("fovbizqimiqki","Martinchien55","valorvolvikacc")