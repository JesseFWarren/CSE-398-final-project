from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from PIL import Image
import numpy as np
import cv2
import torch
import torchvision
import requests
from io import BytesIO
import os
import time
import random
import pandas as pd
import subprocess
import os
import re
import shutil

def take_screenshot_with_selenium(driver, save_path):
    random_number = ''.join(random.choices('0123456789', k=6))
    # Wait for the reCAPTCHA images to be visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="api2/payload"]'))
    )
    # Locate the reCAPTCHA element
    captcha_element = driver.find_element(By.CSS_SELECTOR, 'div.rc-imageselect-payload')
    # Take screenshot of just the reCAPTCHA element
    captcha_element.screenshot(f"{save_path}/captcha_screenshot_{random_number}.png")

def run():
    captcha_site = 'https://www.google.com/recaptcha/api2/demo'
    click_delay = .5
    solved = False

    # create a new instance of the Chrome browser
    driver = webdriver.Chrome()

    # navigate to the website
    driver.get(captcha_site)

    # wait for reCAPTCHA iframe to load and switch to it
    wait = WebDriverWait(driver, 10)
    # switch back to the main frame and wait for the "recaptcha challenge expires in two minutes" iframe to load
    recaptcha_iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))

    # wait for div#rc-anchor-container to load and click on div.recaptcha-checkbox-border
    recaptcha_wait = WebDriverWait(driver, 10)
    recaptcha = recaptcha_wait.until(EC.presence_of_element_located((By.ID, 'rc-anchor-container')))
    recaptcha.click()

    time.sleep(3)

    driver.switch_to.default_content()
    challenge_iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="recaptcha challenge expires in two minutes"]')))   

    take_screenshot_with_selenium(driver, 'yolov5/data/test_images/tests2')

    time.sleep(3)

    driver.quit()

for i in range(500):
    run()