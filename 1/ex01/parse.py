# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parse.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/04 11:18:57 by akoaik            #+#    #+#              #
#    Updated: 2025/11/04 12:09:38 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse

def check(args):

    if args.l != 5 and not args.r:
        print("Error: -l flag requires -r flag to be enabled")
        exit(1)

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