from ast import Assert
import time
from tokenize import String
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class test1(LiveServerTestCase):

    # def testlogin(self):
    #     driver = webdriver.Chrome()
    #     driver.get("http://127.0.0.1:8000/")
    #     # time.sleep(5)
    #     username= driver.find_element(By.NAME, 'username')
    #     password= driver.find_element(By.NAME, 'password')

    #     submit = driver.find_element(By.CSS_SELECTOR, '.btn.login_btn')

    #     # username.send_keys('developer')
    #     # password.send_keys('tester@123')
    #     # username.send_keys('developer') #incorrect password
    #     # password.send_keys('tester@12')
    #     # username.send_keys('develop') #incorrect username
    #     # password.send_keys('tester@123')
    #     # username.send_keys('develo') #incorrect username n password
    #     # password.send_keys('tester@12')
    #     # username.send_keys('') #empty username n password
    #     # password.send_keys('')
    #     # username.send_keys('') #empty username n correct password
    #     # password.send_keys('tester@123')
    #     username.send_keys('developer') #empty username n correct password
    #     password.send_keys('')
    #     submit.click()
    #     time.sleep(7)
        
    #     actualUrl="http://127.0.0.1:8000/dashboard/"
    #     expectedUrl= driver.current_url 
      
    #     self.assertEqual(actualUrl, expectedUrl)
    #     driver.close()
        # return driver

    def testSignUp(self):
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/signup/")
        # time.sleep(5)
        username= driver.find_element(By.NAME, 'username')
        email= driver.find_element(By.NAME, 'email')
        password1= driver.find_element(By.NAME, 'password1')
        password2= driver.find_element(By.NAME, 'password2')
        phone_number= driver.find_element(By.ID, 'id_phone_number')
        address= driver.find_element(By.NAME, 'address')
        submit = driver.find_element(By.CSS_SELECTOR, 'body > div > div > div > div > div > div > form > div > button')

        username.send_keys('arpit')
        email.send_keys('arpit@citisoft.com')
        password1.send_keys('tester@123')
        password2.send_keys('tester@123')
        phone_number.send_keys('7894567895')
        address.send_keys("Texas")
        submit.click()
        time.sleep(5)
        
        actualUrl="http://127.0.0.1:8000/"
        expectedUrl= driver.current_url 
      
        self.assertEqual(actualUrl, expectedUrl)
        driver.close()