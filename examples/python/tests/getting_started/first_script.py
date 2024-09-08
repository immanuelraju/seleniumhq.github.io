from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import time

# Set up the WebDriver (make sure to set the correct path to your chromedriver)
service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service)

# Open the Dailymotion T-Series page
driver.get('https://www.dailymotion.com/tseries2')

# List to hold video URLs
video_urls = []

# Wait for the video elements to load
wait = WebDriverWait(driver, 10)

# Scrolling and scraping video URLs
while len(video_urls) < 500:
    try:
        # Wait for the video elements to load (adjust the XPath if necessary)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/video/")]')))
        
        # Find all video elements (adjust XPath if the structure changes)
        videos = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')
        
        # Extract URLs of the videos
        for video in videos:
            url = video.get_attribute('href')
            if url and url.startswith('https://www.dailymotion.com/video/') and url not in video_urls:
                video_urls.append(url)
        
        # Break if 500 video URLs are collected
        if len(video_urls) >= 500:
            video_urls = video_urls[:500]  # Ensure only the first 500 are taken
            break
        
        # Scroll down the page to load more videos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Small delay to allow the new content to load

    except Exception as e:
        print(f"Error occurred: {e}")
        break

# Close the driver
driver.quit()

# Ensure we have collected 500 video URLs
if len(video_urls) < 500:
    print(f"Only collected {len(video_urls)} video URLs.")
else:
    print(f"Collected 500 video URLs.")

# Extract video IDs
video_ids = [url.split('/video/')[1] for url in video_urls]

# Count characters in all video IDs
character_count = Counter(''.join(video_ids).lower())

# Find the most frequent character, prioritize by count and alphabetic order
most_frequent_char = min(character_count.items(), key=lambda x: (-x[1], x[0]))

# Print the result
print(f"{most_frequent_char[0]}:{most_frequent_char[1]}")
