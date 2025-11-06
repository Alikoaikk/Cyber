# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider_cloud.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/04 16:25:41 by akoaik            #+#    #+#              #
#    Updated: 2025/11/05 23:04:32 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cloudscraper
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import os

def download_image(img_url, output_dir="./data"):
    try:
        os.makedirs(output_dir, exist_ok=True)

        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'linux',
                'mobile': False
            }
        )
        response = scraper.get(img_url, timeout=10)

        if response.status_code != 200:
            print(f"Error: {img_url} returned {response.status_code}")
            return False

        filename = os.path.basename(urlparse(img_url).path)
        if filename == "":
            filename = "image_" + str(abs(hash(img_url))) + ".jpg"

        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as file :
            file.write(response.content)

        print(f"Saved: {filepath}")
        return True

    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
        return False


def extract_img(container) :

    images = container.find_all("img")
    img_urls = []
    allowed_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

    for images in images :
        src = images.get("src")
        if src and src.lower().endswith(allowed_ext) :
            img_urls.append(src)
    print(f"Found {len(img_urls)} images")
    return img_urls

def spider(url, depth=5, visited=None, args=None) :

    if visited is None :
        visited = set()
    if url in visited or depth == 0 :
        return
    
    visited.add(url)

    print(f"\nCrawling: {url}")

    try :
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'linux',
                'mobile': False
            }
        )
        page = scraper.get(url, timeout=15)
        container = bs(page.text, "lxml")
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return

    imgs = extract_img(container)
    for src in imgs :
        # Convert relative URLs to absolute URLs (e.g., "/image.jpg" -> "https://example.com/image.jpg")
        full_url = urljoin(url, src)
        download_image(full_url, args.p if args else "./data")

    for a in container.find_all("a", href=True):
        # Convert relative links to absolute URLs for recursive crawling
        link = urljoin(url, a["href"])
        if urlparse(link).netloc == urlparse(url).netloc :
            spider(url=link, depth=depth - 1 , visited=visited, args=args)
