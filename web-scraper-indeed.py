import pandas as pd
import random
import time
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
PROXY = ""  # Host:PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={PROXY}')
driver = webdriver.Chrome(executable_path=r'chromedriver', options=chrome_options)

#job_title = ['data+scientist', 'data+engineer', 'data+analyst']
Job_data = []

for page in range (0,110,10):
#for page in range (0,510,10):
  driver.get(f'https://www.indeed.com/jobs?q=data+analyst&start={page}')
  #driver.get(f'https://www.indeed.com/jobs?q=data+scientist&start={page}')
  #driver.get(f'https://www.indeed.com/jobs?q=data+engineer&start={page}')

  time.sleep(random.uniform(8.5, 10.9))
  try:
    close = driver.find_element(By.XPATH, '//button[@class = "icl-CloseButton icl-Modal-close"]')
    close.click()
  except:
    pass

  jobs = driver.find_elements(By.XPATH, '//div[@class = "css-1m4cuuf e37uo190"]')

  for job in jobs:
    job.location_once_scrolled_into_view
    job.click()
    time.sleep(random.uniform(4.6, 6.9))
    try:
        Job_title = driver.find_element(By.XPATH, '//h2[@class= "icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title is-embedded"]').text.strip()
        title = Job_title.split('\n')
    except:
        title = 'NaN'
    try:
        Company = driver.find_element(By.XPATH,'//span[@class="css-1saizt3 e1wnkr790"]').text.strip()
        cmpny = Company.split('\n')
    except:
        cmpny = 'NaN'
    try:
        Location = driver.find_element(By.XPATH, '//div[@class="css-6z8o9s eu4oa1w0"]').text.strip()
        loc = Location.split('\n')
    except:
        loc = 'NaN'
    try:
        Salary = driver.find_element(By.XPATH, '//span[@class = "css-2iqe2o eu4oa1w0"]').text.strip()
        salary = Salary.split('\n')
    except:
        salary = 'NaN'
    try:
        Job_Description = driver.find_element(By.XPATH, '//*[@id = "jobDescriptionText"]').text.strip()
    except:
        Job_Description = 'NaN'

    data = {'Job_Title': title[0],'Company': cmpny[0],'Location': loc[0],'Salary': salary[0],'Job_Description': Job_Description}
    Job_data.append(data)
    print('[*] Saving Job Data')

df = pd.DataFrame(Job_data)
df.head(10)
#df.to_csv('IndeedDataEngineer_2023.csv')
df.to_csv('IndeedDataAnalyst_2023.csv')
#df.to_csv('IndeedDataScientist_2023.csv')
#df.to_csv('IndeedPython_2023.csv')
driver.quit()
