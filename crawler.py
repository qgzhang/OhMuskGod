from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import time

# Path to the ChromeDriver executable
driver_path = '/Users/zha406/Codes/Libraries/chromedriver-mac-arm64/chromedriver'

# Set up the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)


# Navigate to X's main page to set the correct domain
driver.get("https://x.com")
time.sleep(2)  # Allow page to load fully

# Load cookies from the exported JSON file
with open("twitter_cookies.json", "r") as file:
    cookies = json.load(file)
    for cookie in cookies:
        # Change the domain to ".x.com" to match the current domain
        cookie["domain"] = ".x.com"
        
        # Remove any problematic attributes
        if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
            del cookie["sameSite"]
        
        driver.add_cookie(cookie)

# Refresh to apply cookies and access the logged-in session
driver.refresh()
time.sleep(2)

# Open Elon Musk's profile on X
url = 'https://x.com/elonmusk'
driver.get(url)

# Function to get Elon Musk's latest tweets
def get_latest_tweets():
    driver.refresh()  # Refresh page to get the latest posts
    time.sleep(3)  # Wait for the page to load

    # Find tweet elements (may vary depending on Twitter's HTML structure)
    tweets = driver.find_elements(By.CSS_SELECTOR, 'div[lang]')

    # Print the text of the tweets
    for tweet in tweets[:5]:  # Fetch the latest 5 tweets
        print(tweet.text)
        print("-------")

# Run every minute
try:
    while True:
        get_latest_tweets()
        time.sleep(60)  # Wait 1 minute before checking again
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    driver.quit()  # Close the browser when done
