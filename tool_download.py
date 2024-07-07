# import requests
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_youtube_url(name):

    driver = webdriver.Chrome()

    driver.get("https://www.youtube.com/")

    time.sleep(5)

    search_elem = driver.find_element(By.NAME, 'search_query')
    search_elem.send_keys(name)
    search_elem.send_keys(Keys.RETURN)
    time.sleep(3)

    video_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'video-title'))
    )

    video_url = video_element.get_attribute('href')
    print(f'URL of the first video: {video_url}')

    downloader_url = "https://yt1ss.pro/eu158/"
    driver.get(downloader_url)
    time.sleep(3)
    search_box = driver.find_element(By.ID, "txt-url")
    search_box.send_keys(video_url)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(2) td:last-child button").click()
    time.sleep(3)
    btn_download = driver.find_element(By.ID, "A_downloadUrl")
    download_url = btn_download.get_attribute("href")
    print(download_url)

get_youtube_url("Rap Viet mua 1")

