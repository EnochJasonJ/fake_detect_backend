import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import numpy as np

def scrapeAmazonSelenium(url):
    # Set up undetected chromedriver
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode (without opening browser window)
    options.add_argument("--no-sandbox")  # Avoid sandboxing issues
    options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the driver
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        
        # Wait for the product title and image to load (max wait time 10 seconds)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title = soup.find(id="productTitle")
        description = soup.find(id="feature-bullets")
        image = soup.find('img', {'id': 'landingImage'})
        review_block = soup.find_all("div",{"data-hook":"review-collapsed"})
        reviews=[]

        for block in review_block:
            span  = block.find("span")
            if span:
                reviews.append(span.get_text(strip=True))

        # Extract text or URL from the tags found
        product_data = {
            'title': title.get_text(strip=True) if title else 'Title not found',
            'description': description.get_text(strip=True) if description else 'Description not found',
            'image': image['src'] if image else 'Image not found',
            'reviews': reviews
        }
        return product_data  # Convert numpy array back to list to avoid ambiguity in evaluation

    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}

    finally:
        driver.quit()

# Example usage
# url = "https://www.amazon.com/Redragon-S101-Keyboard-Ergonomic-Programmable/dp/B00NLZUM36"
# product_data = scrapeAmazonSelenium(url)
# print(f"Title:\n{product_data['title']}")
# # print(f"Description:\n{product_data['description']}")
# print(f"Reviews:\n{product_data['reviews']}")
