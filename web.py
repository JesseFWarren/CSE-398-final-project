from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
import shutil

def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def scrape_image(driver, wait):

    driver.switch_to.default_content()
    challenge_iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="recaptcha challenge expires in two minutes"]')))   
    image = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="api2/payload"]')))

    image_src = image.get_attribute('src')
    class_name = image.get_attribute('class')


    label = driver.find_element(By.TAG_NAME, 'strong').text

    response = requests.get(image_src)

    image_content = response.content

        # Open the image from bytes
    image = Image.open(BytesIO(image_content))

    # Calculate dimensions for the smaller images
    width, height = image.size
    single_width = width // 3
    single_height = height // 3

    clear_directory('yolov5/data/test_images/tests')
    images = []
    for i in range(3):  # for each row
        for j in range(3):  # for each column
            left = j * single_width
            top = i * single_height
            right = left + single_width
            bottom = top + single_height
            cropped_image = image.crop((left, top, right, bottom))
            file_name = f"{label}_part_{i * 3 + j}.png"
            file_path = os.path.join("yolov5/data/test_images/tests", file_name)
            cropped_image.save(file_path)
            images.append(cropped_image)

    return images, label


def copy_label_file(image_id, exp):
    source_file = f"yolov5/runs/detect/exp{exp}/labels/{image_id}.txt"
    destination_file = "label.txt"
 

    shutil.copyfile(source_file, destination_file)


def save_value(value, filename="value.txt"):
    """ Save the given value to a file """
    with open(filename, "w") as file:
        file.write(str(value))

def load_value(filename="value.txt"):
    """ Load the value from a file """
    try:
        with open(filename, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Default value if the file does not exist

def run_yolo_on_images(label, images, model_name):
    i = 0
    for i, image in enumerate(images):
        image_id = f"{label}_part_{i}"
        image_path = os.path.join("yolov5/data/test_images/tests/", f"{image_id}.png")
        image.save(image_path)
        image_id = f"{label}_part_{i}.png"

         # Construct the command
        command = [
            "python", "detection.py", 
            image_id,
            model_name
        ]

        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Run the shell script for each image

        print(result.stdout)
        print(result.stderr)

        image_id = f"{label}_part_{i}"
        exp = load_value()
        file_path = f"yolov5/runs/detect/exp{exp}/labels/{image_id}.txt"
        if os.path.exists(file_path): # Was something detected in the image?
            copy_label_file(image_id, exp)
            # Determine if the specified object is detected in the image
            if object_detected_in_bbx('label.txt', label):
                select_image_in_selenium(i)
            
        exp = exp + 1
        save_value(exp)
        

def select_image_in_selenium(image_index):
    # Code to click the appropriate image in the captcha based on index
    elements = driver.find_elements(By.CLASS_NAME, 'rc-imageselect-tile')
    elements[image_index].click()

def object_detected_in_bbx(bbx_file_path, target_class):
    detected = False
    num = 0
    if target_class == "stairs":
        num = 2
    elif target_class == "chimneys":
        num = 1
    elif target_class == "crosswalks":
        num = 0
    else:
        num = -1
    with open(bbx_file_path, 'r') as file:
        for line in file:
            elements = line.split()
            if len(elements) > 0 and elements[0] == str(num):
                detected = True
                break

    return detected

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


images, label = scrape_image(driver, wait)

run_yolo_on_images(label, images, 'model5')

images, label = scrape_image(driver, wait)

run_yolo_on_images(label, images, 'model5')

verify_button = driver.find_element(By.ID, 'recaptcha-verify-button')
verify_button.click()