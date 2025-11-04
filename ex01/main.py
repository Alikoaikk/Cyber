# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/04 11:29:56 by akoaik            #+#    #+#              #
#    Updated: 2025/11/04 13:16:12 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
from bs4 import BeautifulSoup as bs
from parse import falg_parse
from spider import extract_img, spider

def main () :
    args = falg_parse()
    
    try:
        if args.r :
            print("Starting recursive spider...")
            spider(args.url, depth=args.l, args=args)
        else:
            print("Downloading images from single page...")
            spider(args.url, depth=1, args=args)
    except requests.exceptions.RequestException:
        print(f"Error: Unable to connect to {args.url}")

main()