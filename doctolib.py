"""
Created on Wed May 12 14:28:07 2021

@author: dsolis

"""

import numpy as np
import random 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import winsound
import os, sys

# Vaccination centers
places = ["https://www.doctolib.fr/centre-de-sante/antony/centre-de-vaccination-antony-bourg-la-reine-sceaux?highlight%5Bspeciality_ids%5D%5B%5D=5494",
"https://www.doctolib.fr/centre-de-vaccinations-internationales/velizy-villacoublay/apta-78-vaccination-covid-19-velizy-villacoublay?highlight%5Bspeciality_ids%5D%5B%5D=5494",
"https://www.doctolib.fr/centre-de-sante/gif-sur-yvette/centre-de-vaccination-covid-19-gif-sur-yvette-gif-sur-yvette?highlight%5Bspeciality_ids%5D%5B%5D=5494",
"https://www.doctolib.fr/centre-de-vaccinations-internationales/igny/centre-de-vaccination-covid-commune-d-igny?highlight%5Bspeciality_ids%5D%5B%5D=5494",
"https://www.doctolib.fr/centre-de-sante/chatenay-malabry/centre-de-vaccination-de-chatenay-malabry?highlight%5Bspeciality_ids%5D%5B%5D=5494"
            ]
# Vaccine options
vaccine = [ "1re injection vaccin COVID-19 (Pfizer-BioNTech)",
             "1re injection vaccin COVID-19 (Moderna)"
            ]

user = "email@mail.com"
passw = "yourpassword" 
freq = 120 + 10*(random.random()-0.5) # Appointment search frequency  

# Login
driver = webdriver.Firefox(executable_path='geckodriver.exe')
driver.get("https://www.doctolib.fr/sessions/new") 
time.sleep(3+random.random())
username = driver.find_element_by_id("username")
username.send_keys(user)
elem = driver.find_elements_by_id("password")  
elem[1].send_keys(passw)
conex = driver.find_element_by_xpath('//button[@class="Tappable-inactive dl-button-DEPRECATED_yellow dl-toggleable-form-button dl-button dl-button-block dl-button-size-normal"]')
ActionChains(driver).move_to_element(conex).click().perform()  

# Accesing the scheduling site
time.sleep(2.35+random.random())
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get("https://www.doctolib.fr/vaccination-covid-19")
time.sleep(1+random.random())

# Removing the pop-up
pop = driver.find_element_by_xpath('//button[@id="didomi-notice-agree-button"]')
ActionChains(driver).move_to_element(pop).click().perform()
time.sleep(3+random.random())
driver.maximize_window()        # Maximazing the browser window
category = driver.find_element_by_xpath('//input[@id="eligibility-3"]') # 18-49 years old option
ActionChains(driver).move_to_element(category).click().perform() 
rechercher = driver.find_element_by_xpath('//button[@class="Tappable-inactive dl-button-primary dl-button dl-button-size-normal"]')
ActionChains(driver).move_to_element(rechercher).click().perform() 

nn = len(places)    # Number of vaccination centers
# For each vaccination site a different tab
for i in range(nn):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[i])
    driver.get(places[i])
# Main code
breaker = False
while True:
    for i in range(nn):
        driver.switch_to.window(driver.window_handles[i])
        driver.refresh()
        time.sleep(3)
        for j in range(len(vaccine)):
            try:
                # Searching a place for the desired vaccine
                motif0 = driver.find_element_by_xpath('//div[@class="dl-step-children dl-layout-item dl-layout-size-xs-12 dl-layout-size-sm-12"]')
                ActionChains(driver).move_to_element(motif0).click().perform()
                
                select = Select(driver.find_element_by_id("booking_motive"))
                select.select_by_visible_text(vaccine[j])    
                time.sleep(3)
                
                # Date and time first dose (first time available)
                hora = driver.find_element_by_xpath('//div[@class="Tappable-inactive availabilities-slot"]')
                ActionChains(driver).move_to_element(hora).click().perform()
                time.sleep(1)
                # Date and time second dose (first time and day available)
                hora = driver.find_element_by_xpath('//div[@class="Tappable-inactive availabilities-slot"]')
                ActionChains(driver).move_to_element(hora).click().perform() 
                time.sleep(1)
                # Accepting terms and conditions
                confi1 = driver.find_element_by_xpath('//button[@class="dl-button-check-inner"]')
                ActionChains(driver).move_to_element(confi1).click().perform()
                time.sleep(1.5+random.random())
                confi2 = driver.find_element_by_xpath('//div[@class="dl-button-check-outer"]')
                ActionChains(driver).move_to_element(confi2).click().perform()
                time.sleep(1.5+random.random())
                confi3 = driver.find_element_by_xpath('//div[@class="dl-button-check-outer"]')
                ActionChains(driver).move_to_element(confi3).click().perform()
                time.sleep(1.5+random.random())
                conff = driver.find_element_by_xpath('//button[@class="Tappable-inactive dl-button-primary booking-motive-rule-button dl-button dl-button-block dl-button-size-normal"]')
                ActionChains(driver).move_to_element(conff).click().perform()
                print('Completed succesfully')
                breaker = True
                break
            except: pass
        if breaker == True: 
            breaker = True 
            break    
        else: continue        
    time.sleep(freq) # Appointment search frequency    
    if breaker:
        break 
# Alarm
for i in range(5):
    time.sleep(1)
    winsound.Beep(500, 1500)
        
# Final steps (pacient identification)
pac = driver.find_element_by_xpath('//label[@class="dl-radio-button-label dl-master-patient-item-label dl-master-patient-completed"]')
ActionChains(driver).move_to_element(pac).click().perform()
time.sleep(2)
rendezv = driver.find_element_by_xpath('//button[@class="Tappable-inactive dl-button-primary dl-margin-b dl-button dl-button-block dl-button-size-normal"]')
ActionChains(driver).move_to_element(rendezv).click().perform()
