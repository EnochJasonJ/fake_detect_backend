import requests

scrapped = []

def fetchdata(title):
    url = f"https://api.upcitemdb.com/prod/trial/search?s={title}"
    res = requests.get(url)
    data = res.json()
    item = data['items'][0]

    db = {
        "title": item.get('title', ''),
        "brand": item.get('brand', ''),
        "manufacturer": item.get('manufacturer', ''),
        "description": item.get('description', ''),
        "image": item.get('image', '')
    }

    # Simulate a scraped item (replace with actual scraped values)
    scraped = {
        "title": "Aadi Black Casual Shoes",  # Suppose this was scraped from Walmart
        "brand": "Aadi",
        "manufacturer": "Aadi Shoes Pvt Ltd"
    }

    mismatches = is_fake(scraped, db)

    print("Mismatches found:" if mismatches else "No mismatches.")
    for key, value in mismatches.items():
        print(f"{key.capitalize()} mismatch: Scraped = {value['scraped']} | Verified = {value['verified']}")

def is_fake(scraped, db):
    mismatches = {}
    for key in ["title", "brand", "manufacturer"]:
        if scraped.get(key, '').lower() != db.get(key, '').lower():
            mismatches[key] = {
                "scraped": scraped.get(key, 'N/A'),
                "verified": db.get(key, 'N/A')
            }
    return mismatches

fetchdata("Aadi Black Casual Shoes")
