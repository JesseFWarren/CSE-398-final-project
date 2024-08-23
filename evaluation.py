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

def run_yolo_on_images(folder_path, model_name):

    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    exp = load_value()
    for image_path in images:
        label = os.path.splitext(os.path.basename(image_path))[0]
        image = Image.open(image_path)
        image_id = f"{label}"
        image_save_path = os.path.join("eval/tests", f"{image_id}.png")

        image.save(image_save_path)
        # Construct the command
        command = [
            "python", "detection.py", 
            '../../../../'+image_save_path,
            model_name
        ]

        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Run the shell script for each image

        print(result.stdout)
        print(result.stderr)
        print(image_path)
        print(image_id)
        label_file_path = f"yolov5/runs/detect/exp{exp}/labels/{image_id}.txt"
        if os.path.exists(label_file_path):  # Was something detected in the image?
            copy_label_file(image_id, exp)

        exp += 1
        save_value(exp)

def copy_label_file(image_id, exp):
    source_file = f"yolov5/runs/detect/exp{exp}/labels/{image_id}.txt"
    destination_file = f"eval/test_labels/label-{image_id}.txt"
 

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
    
def object_detected_in_bbx(bbx_file_path, target_class):
    detected = False
    num = 0
    if target_class == "stairs":
        num = 2
    elif target_class == "chimneys":
        num = 1
    elif target_class == "crosswalks":
        num = 0
    elif target_class == "cars":
        num = 3
    elif target_class == "bus":
        num = 4
    elif target_class == "bicycles":
        num = 5
    elif target_class == "a fire hydrant":
        num = 6
    elif target_class == "bridges":
        num = 7
    elif target_class == "motorcycles":
        num = 8
    elif target_class == "trafficlights":
        num = 9
    with open(bbx_file_path, 'r') as file:
        for line in file:
            elements = line.split()
            if len(elements) > 0 and elements[0] == str(num):
                detected = True
                break

    return detected

run_yolo_on_images('eval/test_captchas', 'modelA1')