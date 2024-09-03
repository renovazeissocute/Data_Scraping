from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Step 1: Set up WebDriver (Chrome)
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Open the browser
driver = webdriver.Chrome(service=service, options=options)

# Step 2: Navigate to the URL of the Facebook group
url = 'https://www.facebook.com/groups/realestatethailand'
driver.get(url)

# Give time for logging in (manually input your login credentials)
print("Please log in to Facebook in the opened browser and press Enter when done")
input("Press Enter to continue after logging in...")

# Step 3: Create a function to scrape data
def scrape_facebook_posts(driver):
    # Scroll down to load more posts (you can adjust the number of scrolls)
    for _ in range(45):  # Adjust the number of times as needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)   # Wait for the content to load

    # Extract the posts
    posts = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
    data = []

    # Loop through the posts and extract content
    for post in posts:
        try:
            content = post.text  # Extract the content of the post
            # Save the extracted data
            data.append({
                "Content": content,
            })
        except Exception as e:
            print(f"Error extracting post: {e}")
    # Convert the list of dictionaries to a DataFrame
    return pd.DataFrame(data)

# Step 4: Use the function and save the data to a CSV file
df = scrape_facebook_posts(driver)
print(df)

# Close the browser
driver.quit()

# Save the data to a CSV file
df.to_csv("facebook_data.csv", index=False, encoding='utf-8-sig')
print("Data saved successfully: facebook_posts.csv")