# References: https://www.youtube.com/watch?v=YVFWBJ1WVF8

import openai
import numpy as np
import pandas as pd
import re
import string
import tensorflow as tf
import os
import shutil
import tensorflow as tf
import selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

driver = webdriver.Chrome()

# Open a website
url = "https://www.instagram.com"
driver.get(url)

time.sleep(2)

def login(username, password):
        bot_username = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "username"))
        )
        bot_username.clear()
        bot_username.click()
        bot_username.send_keys(username)
        print("Username entered")
        
        time.sleep(1)
        
        # Find and fill password field
        print("Attempting to find password field...")
        bot_password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "password"))
        )
        bot_password.clear()
        bot_password.click()
        for char in password:
            bot_password.send_keys(char)
            time.sleep(0.1)
        print("Password entered")
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
        )
        submit_btn.click()
        time.sleep(7)
        print("Login button clicked")

def getPost():
    post_url1 = "https://www.instagram.com/p/DCZ1h03T9TR/"
    post_url2="https://www.instagram.com/p/DCDDfiDO-sc/"
    post_url3="https://www.instagram.com/p/DArFRm4gE_m/"
    post_url4="https://www.instagram.com/nytimes/reel/C5UY6B4LJC6/"
    post_url5="https://www.instagram.com/p/C4uT5PXp56T/"
    post_url="https://www.instagram.com/p/DA-n-7jAx0P/"
    driver.get(post_url)
    time.sleep(5)

    # Extract comments
    while True:
        try:
            loadComments =  WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//svg[@aria-label='Load more comments']"))
            )
            loadComments.click()
            time.sleep(2)
        except:
            break

    comments = driver.find_elements(By.XPATH, "//span")
    cleanedComments = []
    for comment in comments:
        text = comment.text
        # Filter out non-comment content using regex or string conditions if needed
        if text and len(text) > 0:  # Adjust condition to exclude usernames, metadata, etc.
        # Optionally, you can use regex to clean up the text further
            cleanedText = re.sub(r'[^\w\s]', '', text)  # Example: Remove special characters
            cleanedComments.append(cleanedText)
    return cleanedComments

def cleanComments(commentList):
    index = 0
    while index < len(commentList):
        comment = commentList[index]
        if comment == "" or not comment:
            commentList.pop(index)
        elif comment[0].isdigit() and "like" in comment:
            commentList.pop(index)
        elif comment[0].isdigit() and ("h" in comment or "hr" in comment):
            commentList.pop(index)
        elif "reply" in comment or "Reply" in comment:
            commentList.pop(index)
        else:
            index +=1
    return commentList
             
login(username, password)
comments = getPost()

cleanedComments = cleanComments(comments)

newList = [i for i in range(1, len(cleanedComments)+1)]
df = pd.DataFrame({"Indexes": newList, "Comments": cleanedComments})
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.close()

print(df.iloc[:, 1].tolist())

#gets API key
API_KEY=open("API_KEY.txt","r").read()
openai.api_key=API_KEY

#creates list that stores chat and user interactions
chat_log=[]

#loops through comments
for comment in df.iloc[:, 1].tolist():
    #checks sentiment of comment
    chat_log.append({"role": "user", "content": f"Does this message have negative or positive sentiment: {comment}. If the comment is Instagram metadata, just ignore it."})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    #puts gpt response into chat_log
    gpt_response=response['choices'][0]['message']['content']
    chat_log.append({"role":"assistant", "content":gpt_response.strip("\n").strip()})

#checks overall sentiment
chat_log.append({"role":"user", "content":"From all the past messages, is there generally a negative or positive sentiment? What kind of sentiment is it: political, emotional, etc.? Also, ignore any programming syntax, languages, names, usernames, and platform features. Only consider the comments that you would see under an instagram post"})
#puts gpt response into chat_log
response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
)
gpt_response=response['choices'][0]['message']['content']
print(gpt_response)