import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ser = Service("/Users/souravmohile/Development/chromedriver")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
SHEETY_URL = "https://api.sheety.co/20308d467201a276809c3b2f10ef2fc2/peopleWhoDontFollowBack >:(/sheet1"

# TODO: LOGIN
driver.get(f"https://www.instagram.com/{USERNAME}/")

# Click on Login
# driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button/div").click()

time.sleep(5)

# Enter user and pswd
driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(USERNAME)
driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(PASSWORD)

# Hit logginnn
driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button/div").click()

time.sleep(5)

# TODO: GET RID OF POPUPS
# Not nowww
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()

time.sleep(5)

# TODO: TOTAL NUMBER OF FOLLOWING AND FOLLOWERS
follower = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div")
following = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/div/span")
text1 = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div/span").text
text2 = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/div/span").text
followers_count = int(text1.replace("followers", ""))
following_count = int(text2.replace("following", ""))

time.sleep(5)

# TODO: GET LIST OF FOLLOWERS
# Click on followers
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div/span").click()

time.sleep(5)

while True:
    driver.execute_script('''
                var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                fDialog.scrollTop = fDialog.scrollHeight
            ''')
    list_of_followers = driver.find_elements_by_xpath("//div[@class='PZuss']/li/div/div/div[2]/div/span/a")

    list_of_followers_count = len(list_of_followers)
    if list_of_followers_count == followers_count:
        break

new_list_of_followers = []
for i in list_of_followers:
    new_list_of_followers.append(i.text)

time.sleep(5)

# Click the X
driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button").click()

time.sleep(2)

# TODO: GET LIST OF FOLLOWING
# Click on following
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/div").click()

time.sleep(5)

while True:
    driver.execute_script('''
                var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                fDialog.scrollTop = fDialog.scrollHeight
            ''')
    list_of_following = driver.find_elements_by_xpath("//div[@class='PZuss']/li/div/div/div[2]/div/span/a")

    list_of_following_count = len(list_of_following)
    if list_of_following_count == following_count:
        break

new_list_of_following = []
for j in list_of_following:
    new_list_of_following.append(j.text)

# TODO: COMPARE LISTS
# List of people that don't follow me back-
dont_follow_back = []

for i in new_list_of_following:
    if i not in new_list_of_followers:
        dont_follow_back.append(i)

# TODO: ADD THE ONES WHO DONT FOLLOW BACK TO SHEETS
sheety_header = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

length = len(dont_follow_back)
for i in range(0, length):
    sheety_parameters = {
        "sheet1": {
            "username": dont_follow_back[i]
        }
    }

    response = requests.post(url=SHEETY_URL,
                             json=sheety_parameters,
                             headers=sheety_header)

