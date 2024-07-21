from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
from chromedriver_py import binary_path # this will get you the path variable

# Input username
username = input("Enter username: ")

# URL for the IG page
ig_url = f"https://www.instagram.com/{username}/?hl=en"

# Setting up the Scraper
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
svc = webdriver.ChromeService(executable_path=binary_path)
browser = webdriver.Chrome(options=chrome_options, service=svc)

# Opening the instagram page to the desired username
browser.get(ig_url)

#Login in to instagram and continue when finished
is_logged_in = False
is_logged_in = input("Please enter the browser and enter your login credentials. Once ready type in 'ready': ")
while True:
    if is_logged_in == "ready":
        break
    else:
        is_logged_in = input("Please make sure to type in 'ready' correctly: ")

#Cookie Way
cookies = {cookie['name']: cookie['value'] for cookie in browser.get_cookies()}
user_id = str(cookies["ds_user_id"])
print(user_id)
user_id = '42542857552' #https://www.instagram.com/web/search/topsearch/?query=so.mbras TODO

#user_id you can also hard code the user id here. 
##################################################################FOLLOWING######################################################################################
haters_list = []

#Load the API Call in Browser to gain access to cookies
get_following = f"https://www.instagram.com/graphql/query/?query_hash=58712303d941c6855d4e888c5f0cd22f&variables=%7B%22id%22:%22" + user_id + "%22,%22first%22:48,%22after%22:%22%22%7D"
browser.get(get_following)
following_json_element = WebDriverWait(browser, 6).until(
    EC.presence_of_element_located((By.XPATH,"/html/body/pre"))
)
following_json = json.loads(following_json_element.text)
following_cursor = following_json["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
following_has_next_page = bool(following_json["data"]["user"]["edge_follow"]["page_info"]["has_next_page"])
following_following = following_json["data"]["user"]["edge_follow"]["edges"]

#Loopin all of the followings
for i in range(0,len(following_following)):
    haters_list.append(following_following[i]["node"]["username"])

while True:
    if following_has_next_page == True:
        get_following = f"https://www.instagram.com/graphql/query/?query_hash=58712303d941c6855d4e888c5f0cd22f&variables=%7B%22id%22:%22{user_id}%22,%22first%22:48,%22after%22:%22{following_cursor}%22%7D"
        browser.get(get_following)
        following_json_element = WebDriverWait(browser, 6).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/pre"))
        )
        #Getting Specific Data
        following_json = json.loads(following_json_element.text)
        following_cursor = following_json["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
        following_has_next_page = bool(following_json["data"]["user"]["edge_follow"]["page_info"]["has_next_page"])
        following_following = following_json["data"]["user"]["edge_follow"]["edges"]

        #Loopin all of the followers
        for i in range(0,len(following_following)):
            haters_list.append(following_following[i]["node"]["username"])
    else:
        break

##################################################################FOLLOWERS######################################################################################
get_followers = "https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables={%22id%22:%22" + user_id + "%22,%22first%22:48,%22after%22:%22%22}"
browser.get(get_followers)
followers_json_element = WebDriverWait(browser, 6).until(
    EC.presence_of_element_located((By.XPATH,"/html/body/pre"))
)
followers_json = json.loads(followers_json_element.text)
followers_cursor = followers_json["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
followers_has_next_page = bool(followers_json["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"])
followers_followers = followers_json["data"]["user"]["edge_followed_by"]["edges"]

#Loopin all of the followings
for i in range(0,len(followers_followers)):
    try:
        haters_list.remove(followers_followers[i]["node"]["username"])
    except:
        print("Maybe you are the OP, cause you don't follow back " + followers_followers[i]["node"]["username"] + " smh my head")
while True:
    if followers_has_next_page == True:
        get_followers = "https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables={%22id%22:%22" + user_id + "%22,%22first%22:48,%22after%22:%22" + followers_cursor + "%22}"
        browser.get(get_followers)
        followers_json_element = WebDriverWait(browser, 6).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/pre"))
        )
        #Getting Specific Data
        followers_json = json.loads(followers_json_element.text)
        followers_cursor = followers_json["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
        followers_has_next_page = bool(followers_json["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"])
        followers_followers = followers_json["data"]["user"]["edge_followed_by"]["edges"]

        #Loopin all of the followers
        for i in range(0,len(followers_followers)):
            try:
                haters_list.remove(followers_followers[i]["node"]["username"])
            except:
                print("Maybe you are the OP, cause you don't follow back " + followers_followers[i]["node"]["username"] + " smh my head")
    else:
        break

print("Here are the people who do not follow you back:")
print(haters_list)