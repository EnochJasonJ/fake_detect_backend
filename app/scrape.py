from bs4 import BeautifulSoup
import requests


def scrapeAmazon(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')
    title = soup.find(id="productTitle")
    description = soup.find(id="feature-bullets")
    image = soup.find('img',{'id':'landingImage'})
    return {
        'title': title.get_text(strip=True) if title else ' ',
        'description': description.get_text(strip=True) if description else ' ',
        'image': image['src'] if image else ' '
    }
    # print(title)


# print(scrapeAmazon('https://www.amazon.com/Razer-BlackShark-V2-Gaming-Headset/dp/B09PZG4R17/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.12129333-2117-4490-9c17-6d31baf0582a&dib=eyJ2IjoiMSJ9.Ll8Fyu7PSXOZ2kfk7CkBcQdCDJNRizl7Yth1RGVu56RzfXo-LmQPYUzqQV7ZLS7ZjbcZy73QMvpqWVTwr5ONjyudPqfW-SiLA2FSeb8rIiJCwMEV3YMM605qytspBqKaYtN_samw1Zfzg6EFfaq2UBRZj1uq5j6Iy81YgnyUKKXIQtTIumNHMXlK-YyJRBSdlgnl8rSpRDSjPnpCU-ZEsvwGgw4fhHbL9U9Oy91fSXU.7C9c7Bc8jebeYsHkNRweHHGsZspAHuOOgFV6GVDvC1A&dib_tag=se&keywords=gaming%2Bheadsets&pd_rd_r=8f3dde0a-183e-4e0d-9149-75515d2e7e65&pd_rd_w=I9Od1&pd_rd_wg=OHWlF&qid=1744009247&sr=8-1&th=1'))