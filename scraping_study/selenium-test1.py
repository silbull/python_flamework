from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver =webdriver.Chrome()

#Googleのブラウザを開く
driver.get('https://www.google.com/')
time.sleep(1) #処理を一時的に停止

#スタビジを検索
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('スタビジ')
search_box.submit()
time.sleep(2)

#検索結果1位をクリック
g = driver.find_elements(By.CLASS_NAME, "g")[0] #添字(インデックス)にアクセスするためには、elementsにしないといけない
r = g.find_element(By.CLASS_NAME, "r") #エラー発生で挫折
r.click()
