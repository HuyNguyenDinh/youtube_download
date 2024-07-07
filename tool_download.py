# import requests
from urllib.parse import unquote
import re
import os
import requests
from ftfy import fix_encoding

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def sanitize_filename(filename):
    """
    Remove or replace invalid characters from the filename.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition and handle encoding issues.
    """
    if not cd:
        return None
    # Find the filename in the content-disposition header
    fname = re.findall(r'filename\*=([^;]+)', cd)
    if len(fname) == 0:
        fname = re.findall(r'filename="?([^"]+)"?', cd)
        if len(fname) == 0:
            return None
        return fname[0]
    
    # Handle the case where the filename is encoded
    fname = fname[0]
    if 'UTF-8' in fname:
        fname = fname.split("''")[-1]
        fname = unquote(fname)
    fname = fix_encoding(fname)
    return fname

def get_youtube_url(name, save_folder):

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
    video_title = sanitize_filename(video_element.get_attribute('title') + ".mp3")
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
    print("URL to download", download_url)
    response = requests.get(download_url, stream=True)

    response.raise_for_status()
    # cd = response.headers.get('content-disposition')
    # file_name = get_filename_from_cd(cd)
    # file_name = "test.mp3"
    save_path = os.path.join(save_folder, video_title)

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    print(f"File downloaded and saved to: {save_path}")

get_youtube_url("hong nhan", "C:\\Users\\Dinh Huy\\Music")

