# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/03 16:25:00 by akoaik            #+#    #+#              #
#    Updated: 2025/11/03 23:54:36 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import os

def check(args):
    if args.r:
        print("R is ON")
    else:
        print("R is OFF")

    if args.l == 5:
        print("L is Default=5")
    else :
        print(f"L is {args.l}")

    print(f"P is {args.p}")
    print(f"URL is {args.url}")

def falg_parse () :

    parser = argparse.ArgumentParser(description="Salemele")
    parser.add_argument("-r", action="store_true", help="Enable recursive mode")
    parser.add_argument("-l", type=int, default=5, help="Max recursion depth")
    parser.add_argument("-p", default="./data", help="Location of the saved files")
    parser.add_argument("url", help="Target website URL")
    args = parser.parse_args()
    check(args=args)
    return (args)

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
    
def spider (url, depth=2, visited=None) :
    
    if visited is None :
        visited = set()
    if url in visited or depth == 0 : 
        return 
    visited.add(url)

    try : 
        page = requests.get(url, timeout=5)
        container = bs(page.text, "lxml")
    except requests.RequestException : 
        return
    
    imgs = extract_img(container)
    for src in imgs :
        print(urljoin(url, src))
        
    for a in container.find_all("a", href=True):
        link = urljoin(url, a["href"])
        if urlparse(link).netloc == urlparse(url).netloc : 
            spider(url=link, depth=depth - 1 , visited=visited)
    

def main () :
    args = falg_parse()
    
    try:
        page = requests.get(args.url)
        print(f"page status code is {page.status_code}")
        if page.status_code == 200 :
            container = bs(page.text, "lxml")
            extract_img(container)

        if args.r : 
            print("Starting recursive ...")
            spider(args.url, depth=args.l)
    except requests.exceptions.RequestException:
        print(f"Error: Unable to connect to {args.url}")

    
    
main()