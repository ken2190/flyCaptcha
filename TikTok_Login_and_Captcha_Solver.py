# Get your key from https://rapidapi.com/flyCaptcha/api/flycaptcha.
# In case you need support send us a message on Telegram https://t.me/flyCaptcha

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json
import time
import pprint
import requests
import os
import random
import string
import base64
import urllib.request
import hashlib
import logging
from time import sleep

logger = logging.Logger('catch_all')

options = webdriver.chrome.options.Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("start-maximized")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--accept-lang=en-US,en;q=0.5")
options.add_argument("--dom-automation=disabled")

driver = webdriver.Chrome(executable_path='chromedriver', options=options) # Path to webdriver -> This is MacOS example
actions = ActionChains(driver, duration=550)

driver.get("https://www.tiktok.com/login/phone-or-email/email")

time.sleep(10) 

write_username = driver.find_element(By.XPATH, '//input[contains(@name,"username")]');
write_username.send_keys("xxx"); # Your Username from TikTok Account
time.sleep(2);

write_password = driver.find_element(By.XPATH, '//input[contains(@type,"password")]');
write_password.send_keys("xxx"); # Your Password from TikTok Account
time.sleep(2)

login_btn = driver.find_element(By.XPATH, '//button[contains(@data-e2e,"login-button")]').click();
time.sleep(8)

# Captcha
captcha_rotation = driver.find_elements("xpath",
                                        '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")]')  # Check captcha is rotating
if len(captcha_rotation) > 0:
    for i in range(1, 30):
        captcha_rotation = driver.find_elements("xpath",
                                                '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")]')
        if len(captcha_rotation) > 0:
            logger.warning('Solving captcha rotation ...')
            slider_captcha_location = driver.find_element(By.XPATH,
                                                          '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"]')  # Get coordinates img x and y
            coordinate_slider_captcha = slider_captcha_location.location
            coordinate_slider_captcha_x = coordinate_slider_captcha['x']
            coordinate_slider_captcha_y = coordinate_slider_captcha['y']

            # Start request solving captcha
            full_img_url = driver.find_element(By.XPATH,
                                               '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")]').get_attribute(
                "src")  # Get link full img
            small_img_url = driver.find_element(By.XPATH,
                                                '//div[contains(@class,"captcha_verify_container")]/div/img[2][contains(@style,"transform: translate(-50%, -50%) rotate")]').get_attribute(
                "src")  # Get link small img

            url = "https://flycaptcha.p.rapidapi.com/captcha/tiktok/rotate"

            payload = {
                "url1": small_img_url,
                "url2": full_img_url,
                "proxy": ""
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "0", # Your rapidapi key
                "X-RapidAPI-Host": "flycaptcha.p.rapidapi.com"
            }

            response = requests.post(url, json=payload, headers=headers)

            print(response.json())

            solve_captcha_response = json.loads(response.json())

            logger.warning(f'Captcha response: {solve_captcha_response}')
            # End request solving captcha

            if len(solve_captcha_response) > 1:
                x = solve_captcha_response["x"]
                y = solve_captcha_response["y"]
                actions.click_and_hold(slider_captcha_location)
                for i in range(0, 1):
                    move = x * 0.65 * 2.1
                    actions.move_by_offset(move, 0)
                    sleep(0.0001)
                for i in range(0, 13):
                    actions.move_by_offset(1, 0)
                    sleep(0.1)
                actions.release().perform()
                sleep(10)
            else:
                refresh_captcha_circle = driver.find_element(By.XPATH,
                                                             '//div[contains(@class,"captcha_verify_action")]//span[contains(@class,"secsdk_captcha_refresh--icon")]').click()
                sleep(5)
        else:
            logger.warning("Captcha successful solved")
            break

captcha_3D = driver.find_elements("xpath",
                                  '//div[contains(@class,"captcha_verify_img")]/img')  # Check captcha the same shapes
slide_image = driver.find_elements("xpath", '//*[@id="tiktok-verify-ele"]/div/div[2]/img[2]')
if len(captcha_3D) > 0 and len(slide_image) == 0:
    for i in range(1, 30):
        captcha_3D = driver.find_elements("xpath",
                                          '//div[contains(@class,"captcha_verify_img")]/img')
        if len(captcha_3D) > 0:
            logger.warning('Solving captcha the same shapes...')
            full_img_url_location = driver.find_element(By.XPATH,
                                                        '//div[contains(@class,"captcha_verify_img")]/img')  # Get coordinates img x and y
            coordinate_full_img_url = full_img_url_location.location
            coordinate_full_img_url_x = coordinate_full_img_url['x']
            coordinate_full_img_url_y = coordinate_full_img_url['y']

            # Start request solving captcha
            full_img_url = driver.find_element(By.XPATH,
                                               '//div[contains(@class,"captcha_verify_img")]/img').get_attribute(
                "src")  # Get link full img

            url = "https://flycaptcha.p.rapidapi.com/captcha/tiktok/objects"

            payload = {
                "url1": full_img_url,
                "proxy": ""
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "0", # Your rapidapi key
                "X-RapidAPI-Host": "flycaptcha.p.rapidapi.com"
            }

            response = requests.post(url, json=payload, headers=headers)

            print(response.json())

            coordinates = json.loads(response.json())
            logger.warning(f'Captcha response: {coordinates}')
            # End request solving captcha

            if len(coordinates) > 1:
                cordinate_x_1 = int(coordinates["x0"]) * 0.62
                cordinate_y_1 = int(coordinates["y0"]) * 0.62
                cordinate_x_2 = int(coordinates["x1"]) * 0.62
                cordinate_y_2 = int(coordinates["y1"]) * 0.62
                target_cordinate_x_1 = int(cordinate_x_1) + int(coordinate_full_img_url_x)
                target_cordinate_y_1 = int(cordinate_y_1) + int(coordinate_full_img_url_y)
                target_cordinate_x_2 = int(cordinate_x_2) + int(coordinate_full_img_url_x)
                target_cordinate_y_2 = int(cordinate_y_2) + int(coordinate_full_img_url_y)
                try:
                    actions.move_by_offset(target_cordinate_x_1, target_cordinate_y_1).click().perform()
                    actions.move_by_offset(-target_cordinate_x_1, -target_cordinate_y_1).perform()
                    sleep(0.1 or 0.5)
                    actions.move_by_offset(target_cordinate_x_2, target_cordinate_y_2).click().perform()
                    sleep(1 or 2)
                    click_verify_3D_captcha = driver.find_element(By.XPATH,
                                                                  '//div[contains(@class,"verify-captcha-submit-button")]').click()
                    sleep(10)
                except Exception as e:
                    refresh_captcha_circle = driver.find_element(By.XPATH,
                                                                 '//div[contains(@class,"captcha_verify_action")]//span[contains(@class,"secsdk_captcha_refresh--icon")]').click()
                    sleep(5)
            else:
                refresh_captcha_circle = driver.find_element(By.XPATH,
                                                             '//div[contains(@class,"captcha_verify_action")]//span[contains(@class,"secsdk_captcha_refresh--icon")]').click()
                sleep(5)
        else:
            logger.warning("Captcha successful solved")
            break

captcha_puzzle = driver.find_elements('xpath',
                                      '//*[@id="tiktok-verify-ele"]/div/div[2]')  # Check captcha puzzle
if len(captcha_puzzle) > 0:
    for i in range(1, 30):
        captcha_puzzle = driver.find_elements('xpath', '//*[@id="tiktok-verify-ele"]/div/div[2]')
        if len(captcha_puzzle) > 0:
            logger.warning('Solving captcha puzzle ...')
            slider_captcha_location = driver.find_element(By.XPATH,
                                                          '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"]')  # Get coordinates img x and y
            coordinate_slider_captcha = slider_captcha_location.location
            coordinate_slider_captcha_x = coordinate_slider_captcha['x']
            coordinate_slider_captcha_y = coordinate_slider_captcha['y']

            img = driver.find_element(By.XPATH, '//*[@id="captcha-verify-image"]').get_attribute(
                "src")  # Get link puzzle img
            sleep(1)
            puzzle_image = img

            img = driver.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[2]/img[2]').get_attribute(
                "src")  # Get link piece img
            sleep(1)
            piece_image = img

            url = "https://flycaptcha.p.rapidapi.com/captcha/tiktok/slide"

            payload = {
                "url1": puzzle_image,
                "url2": piece_image,
                "proxy": ""
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "0", # Your rapidapi key
                "X-RapidAPI-Host": "flycaptcha.p.rapidapi.com"
            }

            response = requests.post(url, json=payload, headers=headers)

            print(response.json())

            solve_captcha_response = json.loads(response.json())

            logger.warning(f'Captcha response: {solve_captcha_response}')
            # End request solving captcha

            if len(solve_captcha_response) > 1:
                response_cordinate_x = solve_captcha_response["x"]
                response_cordinate_y = solve_captcha_response["y"]
                response_cordinate_x = int(response_cordinate_x)
                response_cordinate_y = int(response_cordinate_y)
                response_cordinate_x_range_move_number = int(response_cordinate_x) / 1.8
                actions.click_and_hold(slider_captcha_location)
                for i in range(0, 1):
                    actions.move_by_offset(response_cordinate_x_range_move_number, 0)
                    sleep(0.0001)
                for i in range(0, 13):
                    actions.move_by_offset(1, 0)
                    sleep(0.1)
                actions.release().perform()
                sleep(10)
            else:
                refresh_captcha_circle = driver.find_element(By.XPATH,
                                                             '//*[@id="tiktok-verify-ele"]/div/div[4]/div/a[1]/span[2]').click()
                sleep(5)
        else:
            logger.warning("Captcha successful solved")
            break
too_many_attemps = driver.find_elements("xpath", '//div[contains(@type,"error")]') # Check error
if len(too_many_attemps) > 0:
   print('Error! Too many attemps')
   time.sleep(5)
   
time.sleep(30)
# Close the driver
driver.quit()
