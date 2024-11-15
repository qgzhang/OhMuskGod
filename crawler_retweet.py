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
###########################################################################################

def parse_tweet(tweet_element):
    """Extracts the text and image from a tweet element, identifying if it's a retweet."""
    try:
        # Identify if it’s a retweet
        is_retweet = len(tweet_element.find_elements(By.XPATH, ".//div[contains(text(), 'Retweeted')]")) > 0
        
        # Extract the main tweet text and image
        text = tweet_element.find_element(By.CSS_SELECTOR, "div[lang]").text
        images = tweet_element.find_elements(By.XPATH, ".//img[@alt='Image']")
        image_urls = [img.get_attribute("src") for img in images]
        
        # Initialize the tweet structure
        tweet_data = {"text": text, "image": image_urls}

        # If it's a retweet, extract the retweet's text and image
        if is_retweet:
            retweet_text = tweet_element.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
            retweet_images = tweet_element.find_elements(By.XPATH, ".//img[@alt='Image']")
            retweet_image_urls = [img.get_attribute("src") for img in retweet_images]
            tweet_data["retweet"] = {"text": retweet_text, "image": retweet_image_urls}
        else:
            tweet_data["retweet"] = None  # Not a retweet

        return tweet_data

    except Exception as e:
        print(f"Error parsing tweet: {e}")
        return None

# Function to get Elon Musk's latest tweets with structured data
def get_latest_tweets():
    driver.refresh()  # Refresh page to get the latest posts
    time.sleep(3)  # Wait for the page to load

    # Find tweet elements
    tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article")

    tweets_data = []
    for tweet_element in tweet_elements[:5]:  # Limit to the latest 5 tweets
        tweet_data = parse_tweet(tweet_element)
        if tweet_data:
            tweets_data.append(tweet_data)

    # Display each tweet with its structured data
    for tweet in tweets_data:
        print(tweet)
        print("-------")

        
###########################################################################################


# Run every minute
try:
    while True:
        get_latest_tweets()
        time.sleep(60)  # Wait 1 minute before checking again
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    driver.quit()  # Close the browser when done
