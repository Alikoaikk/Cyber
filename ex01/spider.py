# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/03 16:25:00 by akoaik            #+#    #+#              #
#    Updated: 2025/11/04 13:14:19 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import os
from pathlib import Path

def download_image(img_url, output_dir="./data"):
    try:
        # Make sure the folder exists
        os.makedirs(output_dir, exist_ok=True)

        # Download the image
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(img_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Error: {img_url} returned {response.status_code}")
            return False

        # Get the file name from the URL
        filename = os.path.basename(urlparse(img_url).path)
        if filename == "":
            filename = "image_" + str(abs(hash(img_url))) + ".jpg"

        # Full path to save the image
        filepath = os.path.join(output_dir, filename)

        # Save the image
        file = open(filepath, "wb")
        file.write(response.content)
        file.close()

        print(f"Saved: {filepath}")
        return True

    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
        return False


def extract_img (container) :

    images = container.find_all("img")
    img_urls = []
    allowed_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

    for images in images :
        src = images.get("src")
        if src and src.lower().endswith(allowed_ext) :
            img_urls.append(src)
    print(f"Found {len(img_urls)} images")
    return img_urls
    
def spider (url, depth=5, visited=None, args=None) :

    if visited is None :
        visited = set()
    if url in visited or depth == 0 :
        return
    visited.add(url)

    print(f"\nCrawling: {url}")

    try :
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        page = requests.get(url, headers=headers, timeout=5)
        container = bs(page.text, "lxml")
    except requests.RequestException :
        return

    imgs = extract_img(container)
    for src in imgs :
        full_url = urljoin(url, src)
        download_image(full_url, args.p if args else "./data")

    for a in container.find_all("a", href=True):
        link = urljoin(url, a["href"])
        if urlparse(link).netloc == urlparse(url).netloc :
            spider(url=link, depth=depth - 1 , visited=visited, args=args)