import streamlit as st

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

st.set_page_config(page_title = "Vibe Check", page_icon = ":smirk:", layout = 'wide')

st.write("HOMEPAGE")



#---- HEADER SECTION ----
with st.container():
    col1, col2 = st.columns([1,2])
    with col2:
        st.title("VIBE CHECK")
    st.subheader("Go to the search tab and enter the URL of any verified Instagram account. Within seconds, the true sentiments of the social media influencer shall be revealed!")

#---- LOG IN ----
with st.container():
    st.subheader("Log in to Instagram")
    st.session_state.user = st.text_input("Username:")
    st.session_state.password = st.text_input('Password:', type = 'password')
spacer = st.markdown("<div style = 'height: 25px'></div", unsafe_allow_html = True)
peopleValues = {
    1: {
        "KSI": 'https://www.instagram.com/p/DCRULaDy1AF/?img_index=1',
        "Travis Scott": 'https://www.instagram.com/p/DCT99fbJDHt/?img_index=1'
    },
    2: {
        "Kamala Harris": 'https://www.instagram.com/p/DCDDfiDO-sc/?img_index=1',
        "Donald Trump": 'https://www.instagram.com/p/DCbnV9iuTIL/'
    },
    3: {
        "New York Times": 'https://www.instagram.com/p/DCcAGGkBq55/?img_index=1',
        "Google": 'https://www.instagram.com/p/DCXjfPrROpr/?img_index=1'
    },
    4: {
        "Britney Spears": 'https://www.instagram.com/p/DCa5tizNnMP/?img_index=1',
        "Megan Rapinoe": 'https://www.instagram.com/p/DB2B20oTX7n/?img_index=1'
    }
}
username = st.session_state.user
password = st.session_state.password
spacer = st.empty()
postUrl = ""
with st.container():
    columns = st.columns(4)
    for key, value in peopleValues.items():
        column = columns[key-1]
        with column:
            newVal =  st.markdown("""<button style='text-align: center; display: block;
                                margin: 0 auto; width: 140px; height: 60px;
                                background-color: #8963BA; color: white;
                                border-radius: 5px;'>{}</button>
                                """.format(list(value.keys())[0]), unsafe_allow_html = True)
            if newVal:
                postUrl = value[list(value.keys())[0]]
            spacer = st.markdown("<div style = 'height: 25px'></div", unsafe_allow_html = True)
            newVal2 = st.markdown("""<button style='text-align: center; display: block;
                                margin: 0 auto; width: 140px; height: 60px;
                                background-color: #8963BA; color: white;
                                border-radius: 5px;'>{}</button>
                                """.format(list(value.keys())[1]), unsafe_allow_html = True)
            if newVal2:
                postUrl = value[list(value.keys())[1]]
            #js_popup("KSI Popup Content")
st.write("")
driver = webdriver.Chrome()

    # Open a website
url = "https://www.instagram.com"
driver.get(url)

time.sleep(3)

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
        time.sleep(10)
        print("Login button clicked")

def getPost():
    driver.get(postUrl)
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

st.markdown("<h3 style = 'text-align:center'>Sentiment: {}</h3> ".format(gpt_response), unsafe_allow_html = True)

#---- BROUGHT TO YOU BY ----
with st.container():
    st.write('----')
    st.write("Brought to you by Python in the Pitt")
    st.write("--Vidhya Vishwanath, Laya Satish, Isha Singh--")
    



