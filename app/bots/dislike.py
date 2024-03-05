import streamlit as st
from googleapiclient.discovery import build
from selenium import webdriver
import time
import streamlit as st
from database import create_connection
from datetime import datetime
from selenium.webdriver.common.by import By


def add_dislike(user_id, video_url, status, job_type, number_of_value, completed_value, price):
    conn = create_connection()
    cursor = conn.cursor()
    created_at = updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO Jobs (user_id, video_url, status, job_type, number_of_value, completed_value, price, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;  -- This line returns the id of the inserted row
    ''', (user_id, video_url, status, job_type, number_of_value, completed_value, price, created_at, updated_at))
    job_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return job_id

def dislike_video(youtube, video_id, credentials, file_path):
    try:
        response = youtube.videos().rate(id=video_id, rating='dislike').execute()
        print("Video disliked successfully!")
        return True
    except Exception as e:
        print(f"Error disliking video: {e}")
        return False

def search_and_interact(credentials, search_query, file_path, address, port, protocol):
    youtube = build('youtube', 'v3', credentials=credentials)
    # proxy_address = address
    # proxy_port = port
    # proxy_protocol = protocol
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument(f'--proxy-server={proxy_protocol}://{proxy_address}:{proxy_port}')
    # browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()  
    # browser.delete_all_cookies()
    try:
        # browser.get(search_query)
        # time.sleep(2)
        # try:
        #     browser.find_element(By.XPATH, '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click()
        # except:
        #     pass
        # current_url = browser.current_url
        video_id = search_query.split("v=")[1]
        dislike_result = dislike_video(youtube, video_id, credentials, file_path)
        if not dislike_result:
            print("Dislike action failed!")
        elif dislike_result:
            print("Successfully Disliked the video.")
    except Exception as e:
        print(f"Exception occurred during dislike: {e}")
    finally:
        # browser.quit()
        pass
