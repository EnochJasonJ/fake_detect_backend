import requests
from bs4 import BeautifulSoup
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
import time
import logging
#
# def fetchdata(title):
#     url = f"https://api.upcitemdb.com/prod/trial/search?s={title}"
#     res = requests.get(url)
#     data = res.json()
#     item = data['items'][0]
#
#     db_data = {
#         "title": item.get('title', ''),
#         "brand": item.get('brand', ''),
#         "manufacturer": item.get('manufacturer', ''),
#         "description": item.get('description', ''),
#         "image": item.get('image', '')
#     }
#
#     return db_data
#
# def is_fake(scraped, db):
#     mismatches = {}
#     for key in ["title", "brand", "manufacturer"]:
#         if scraped.get(key, '').lower() != db.get(key, '').lower():
#             mismatches[key] = {
#                 "scraped": scraped.get(key, 'N/A'),
#                 "verified": db.get(key, 'N/A')
#             }
#     return mismatches

def scrape(url):
    try:
        params = {
            'api_key': 'd416a94ddb75f90c10569bda4f254260',
            'url': url,
            'country_code': 'in'
        }
        response = requests.get('https://api.scraperapi.com', params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find(id="productTitle")
        description = soup.find(id="feature-bullets")
        image = soup.find('img', {'id': 'landingImage'})
        review_block = soup.find_all("div",{"data-hook":"review-collapsed"})
        ratings_tag = soup.find("span", id="acrCustomerReviewText")
        reviews=[]
        for block in review_block:
            span  = block.find("span")
            if span:
                reviews.append(span.get_text(strip=True))
        ratings_count=0
        if ratings_tag:
            text = ratings_tag.get_text(strip=True)
            match = re.search(r'([\d,]+)',text)
            if match:
                ratings_digit = match.group(1).replace(',','')
                ratings_count = int(ratings_digit)
        product_data = {
                'title': title.get_text(strip=True) if title else 'Title not found',
                'description': description.get_text(strip=True) if description else 'Description not found',
                'image': image['src'] if image else 'Image not found',
                'review_count': 0,
                'ratings_count': ratings_count,
                'reviews': reviews
            }
        # db_data = fetchdata(product_data['title'])
        # mismatches = is_fake(product_data, db_data)
        # if mismatches:
        #     print("\nMismatches found:")
        #     for key, value in mismatches.items():
        #         print(f"{key.capitalize()} mismatch: Scraped = {value['scraped']} | Verified = {value['verified']}")
        # else:
        #     print("\nNo mismatches.")
        return product_data
    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}
    
# def scrape_flipkart(url):
#     try:
#         params = {
#             'api_key': 'd416a94ddb75f90c10569bda4f254260',
#             'url': url,
#             'country_code': 'in'
#         }
#         response = requests.get('https://api.scraperapi.com', params=params)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         title_tag = soup.find("span", {"class": "VU-ZEz"})
#         description_tag = soup.find("div", {"class": "U+9u4y"})
#         image_tag = soup.find("img", {"class": "DByuf4 IZexXJ jLEJ7H"})
#         review_blocks = soup.find_all("div", {"class": "_8-rIO3"})
#         reviews = []
#         for block in review_blocks:
#             span = block.find("div")
#             if span:
#                 reviews.append(span.get_text(strip=True).replace('READ MORE', ''))
#         product_data = {
#             'title': title_tag.get_text(strip=False) if title_tag else 'Title not found',
#             'description': description_tag.get_text(strip=True) if description_tag else 'Description not found',
#             'image': image_tag['src'] if image_tag else 'Image not found',
#             'reviews': reviews
#         }
#         print(f"{product_data}")
#         return product_data
#     except Exception as e:
#         return {'error': f"An error occurred: {str(e)}"}
#

def scrape_flipkart(url):
    try:
        params = {
            'api_key': 'd416a94ddb75f90c10569bda4f254260',
            'url': url,
            'country_code': 'in'
        }
        reviews = []
        page_number = 1  # Start with the first page of reviews
        while True:
            # Fetch the page of reviews
            params['page'] = page_number
            response = requests.get('https://api.scraperapi.com', params=params)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find review blocks
            review_blocks = soup.find_all("div", {"class": "_8-rIO3"})
            for block in review_blocks:
                span = block.find("div")
                if span:
                    reviews.append(span.get_text(strip=True).replace('READ MORE', ''))

            # Check if there’s a "next page" link or some other way to paginate
            next_page = soup.find("a", {"class": "_1LKTO3"})
            if not next_page:
                break  # No next page, so exit the loop
            page_number += 1  # Move to the next page

        # Extract product info (title, description, image)
        title_tag = soup.find("span", {"class": "VU-ZEz"})
        description_tag = soup.find("div", {"class": "U+9u4y"})
        image_tag = soup.find("img", {"class": "DByuf4 IZexXJ jLEJ7H"})
        review_count_tag = soup.find("span", {"class": "Wphh3N"})

        if review_count_tag:
            spans = review_count_tag.find_all("span")
            texts = [span.get_text(strip=True) for span in spans]
            print(texts)
            review_count = 0
            # Take the last item (the one with 'Reviews')
            last_text = texts[-1] if texts else ""
            if "Reviews" in last_text:
                match = re.search(r'(\d{1,3}(?:,\d{3})*)', last_text)  # Regex to find digits with commas
                if match:
                    review_digits = match.group(1).replace(',', '')
                    review_count = int(review_digits)
        else:
            review_count = 0

        print(f"Review Count Final: {review_count}")


        # if review_count_tag:
        #     spans = review_count_tag.find_all("span")
        #     print([span.get_text(strip=True) for span in spans])
        #     review_count = 0
        #     for span in spans:
        #         text = span.get_text(strip=True)
        #         if "Review" in text:
        #             match = re.search(r'(\d[\d,]*)', text)
        #             if match:
        #                 review_digits = match.group(1).replace(',', '')
        #                 review_count = int(review_digits)
        #             break
        # else:
        #     review_count = 0

        # if review_count_tag:
        #     spans = review_count_tag.find_all("span")
        #     texts = [span.get_text(strip=True) for span in spans]
        #     print(texts)
        #     review_count = 0
        #     for text in texts:
        #         if "Review" in text:
        #             match = re.search(r'(\d[\d,]*)', text)
        #             if match:
        #                 review_digits = match.group(1).replace(',', '')
        #                 review_count = int(review_digits)
        #             break
        # else:
        #     review_count = 0

        # print(f"Review Count Final: {review_count}")



        print("Review Count Final:", review_count)
        print(type(review_count))


        product_data = {
            'title': title_tag.get_text(strip=False) if title_tag else 'Title not found',
            'description': description_tag.get_text(strip=True) if description_tag else 'Description not found',
            'image': image_tag['src'] if image_tag else 'Image not found',
            'reviews': reviews,
            'review_count': review_count
        }
        # print(f"{product_data}")
        # db_data = fetchdata(product_data['title'])
        # mismatches = is_fake(product_data, db_data)
        # if mismatches:
        #     print("\nMismatches found:")
        #     for key, value in mismatches.items():
        #         print(f"{key.capitalize()} mismatch: Scraped = {value['scraped']} | Verified = {value['verified']}")
        # else:
        #     print("\nNo mismatches.")
        return product_data
    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}

def scrape_myntra(url):
    options = uc.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 25).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".pdp-product-description-content"))
)
        # print(driver.page_source)
        # pdp-title
        title_tag = driver.find_element(By.CSS_SELECTOR, ".pdp-title")
        # title_tag = driver.find_element(By.CSS_SELECTOR, ".pdp-description-container")
        description_tag = driver.find_element(By.CSS_SELECTOR, ".pdp-product-description-content")
        ratings_count=0
        # try:
        #     ratings_tag = driver.find_element(By.CSS_SELECTOR, ".index-ratingsCount")
        #     text = ratings_tag.text.strip()
        #     match = re.search(r'([\d\.]+)([Kk]?)', text)
        #     if match:
        #         number = float(match.group(1))
        #         if match.group(2).lower() == 'k':
        #             number *= 1000
        #         ratings_count = int(number)
        # except:
        #     pass
        #index-ratingsCount
        # image_tag = driver.find_element(By.CSS_SELECTOR, "img.image-grid-image")
        try:
            image_div = driver.find_element(By.CSS_SELECTOR, ".image-grid-image")
            style = image_div.get_attribute("style")
            match = re.search(r'url\("([^"]+)"\)', style)
            image = match.group(1) if match else "Not found"
        except:
            image = "Not found"
        review_blocks = driver.find_elements(By.CSS_SELECTOR, ".user-review-userReviewWrapper")

        reviews = []
        for block in review_blocks:
            span = block.find_element(By.TAG_NAME, "div")
            if span:
                reviews.append(span.text.strip().replace('READ MORE', ''))

        product_data = {
            'title': title_tag.text if title_tag else 'Title not found',
            'description': description_tag.text if description_tag else 'Description not found',
            'image': image,
            'reviews': reviews,
            # 'ratings_count': ratings_count
        }

        print(f"{product_data["title"][:50]}")
        # db_data = fetchdata(product_data['title'])
        # mismatches = is_fake(product_data, db_data)
        # if mismatches:
        #     print("\nMismatches found:")
        #     for key, value in mismatches.items():
        #         print(f"{key.capitalize()} mismatch: Scraped = {value['scraped']} | Verified = {value['verified']}")
        # else:
        #     print("\nNo mismatches.")
        return product_data

    except Exception as e:
        print("Error while scraping Myntra:")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}

    finally:
        driver.quit()

def scrape_reliance(url):
    options = uc.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
           
        # print(driver.page_source)
        title_tag = driver.find_element(By.CSS_SELECTOR, ".product-name")
        description_tag = driver.find_element(By.CSS_SELECTOR, ".lb_accordeon__item")
        # image_tag = driver.find_element(By.CSS_SELECTOR, "img.image-grid-image")
        try:
            image_tag = driver.find_element(By.CSS_SELECTOR, "img.fy__img")
            image = image_tag.get_attribute("src")  # Get the src attribute
        except:
            image = "Image not found"
        review_blocks = driver.find_elements(By.CSS_SELECTOR, ".rd-feedback-service-review-row-description")

        reviews = []
        for block in review_blocks:
            try:
                reviews.append(block.text.strip().replace('READ MORE', ''))
            except:
                pass

        product_data = {
            'title': title_tag.text if title_tag else 'Title not found',
            'description': description_tag.text if description_tag else 'Description not found',
            'image': image,
            'reviews': reviews
        }

        print(f"\nTitle:\t{product_data["title"]}\n")
        print(f"\nDescription:\t{product_data["description"]}\n")
        print(f"\nImage:\t{product_data["image"]}\n")
        print(f"\nReviews:\t{product_data["reviews"]}\n")

        # db_data = fetchdata(product_data['title'])
        # mismatches = is_fake(product_data, db_data)
        # if mismatches:
        #     print("\nMismatches found:")
        #     for key, value in mismatches.items():
        #         print(f"{key.capitalize()} mismatch: Scraped = {value['scraped']} | Verified = {value['verified']}")
        # else:
        #     print("\nNo mismatches.")
        return product_data

    except Exception as e:
        print("Error while scraping Myntra:")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}

    finally:
        driver.quit()


def scrape_snapdeal(url):
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = Chrome(options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pdp-e-i-head")))
        title_tag = driver.find_element(By.CSS_SELECTOR, ".pdp-e-i-head")
        description_tag = driver.find_element(By.CSS_SELECTOR, ".detailssubbox")
        try:
            image_tag = driver.find_element(By.CSS_SELECTOR, "img.cloudzoom")
            image = image_tag.get_attribute("src")
        except:
            image = "Image not found"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, ".load-more-btn")
            if load_more_button:
                load_more_button.click()
                time.sleep(2)
        except:
            pass
        review_blocks = driver.find_elements(By.CSS_SELECTOR, ".commentlist")
        reviews = []
        for block in review_blocks:
            try:
                review_head = block.find_element(By.CSS_SELECTOR, ".head").text
                review_text = block.find_element(By.CSS_SELECTOR, ".user-review p").text
                reviews.append({
                    'review_head': review_head,
                    'review_text': review_text
                })
            except Exception as e:
                print(f"Error extracting review: {e}")
                continue
        product_data = {
            'title': title_tag.text if title_tag else 'Title not found',
            'description': description_tag.text if description_tag else 'Description not found',
            'image': image,
            'reviews': reviews
        }
        print(f"\nTitle:\t{product_data['title']}\n")
        print(f"\nDescription:\t{product_data['description']}\n")
        print(f"\nImage:\t{product_data['image']}\n")
        print(f"\nReviews:\t{product_data['reviews']}\n")

        # db_data = fetchdata(product_data['title'])
        # mismatches = is_fake(product_data, db_data)
        # if mismatches:
        #     print("\nMismatches found:")
        #     for key, value in mismatches.items():
        #         print(f"{key.capitalize()} mismatch: Scraped = {value['scraped']} | Verified = {value['verified']}")
        # else:
        #     print("\nNo mismatches.")
        return product_data
    except Exception as e:
        print("Error while scraping Snapdeal:")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}
    finally:
        driver.quit()


def scrape_instagram(link):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    driver.get(link)
    try:
        caption = driver.find_element("xpath", "//div[contains(@class, '_a9zs')]").text
        image_url = driver.find_element("xpath", "//img[contains(@class, '_aagv')]").get_attribute("src")
    except Exception as e:
        caption = "Unable to extract"
        image_url = ""
    driver.quit()
    return f"Caption: {caption}\nImage: {image_url}"


# scrape_snapdeal("https://www.snapdeal.com/product/aadi-black-casual-shoes/638773718836")

    
# scrape_reliance("https://www.reliancedigital.in/product/apple-mgn63hna-macbook-air-apple-m1-chip8gb256gb-ssdmacos-big-surretina-3378-cm-133-inch")
# scrape_reliance("https://www.reliancedigital.in/product/asus-mb540ws-vivobook-16-laptop-intel-core-i5-12500h16-gb512-gb-ssdwindows-11-homewuxga-4064-cm-16-inch-luwm9v-7538233")
# scrape_myntra("https://www.myntra.com/tshirts/powerlook/powerlook-men-self-design-polo-collar-casual-t-shirt/31116616/buy")
# scrape_myntra("https://www.myntra.com/watches/boss/boss-men-patterned-dial--bracelet-style-straps-analogue-watch-1513905/24552842/buy")




