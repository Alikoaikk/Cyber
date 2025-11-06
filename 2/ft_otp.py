# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/05 13:19:57 by akoaik            #+#    #+#              #
#    Updated: 2025/11/06 05:16:41 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import sys
import os
from htop import hotp
from key_manager import save_key, load_key, update_counter

def read_key_from_file(filename):
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' not found")
        exit(1)

    try:
        with open(filename, 'r') as f:
            key = f.read().strip()
        return key
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

def check_key (key) :

    if len(key) < 64 :
        print("Error: key must be 64 hexadecimal characters.")
        exit(1)
    try :
        bytes.fromhex(key)
    except ValueError :
        print("Error: key must be 64 hexadecimal characters.")
        exit(1)

def generate_otp () :

    key_hex, counter = load_key()

    # Generate OTP using HOTP algorithm
    otp = hotp(key_hex, counter)
    update_counter(key_hex, counter + 1)
    print(otp)

def parse () :
    
    parser = argparse.ArgumentParser(description="ft_otp : HOTP one time password generator")
    
    # the user must choose only one flag
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-g", "--generate-key",
                       help="generate and store a key")
    group.add_argument("-k", "--get_otp", action="store_true",
                       help="generate a new one time password")
    args = parser.parse_args()

    return args 
    
def main () :

    args = parse()
    if args.generate_key :
        key = read_key_from_file(args.generate_key)
        check_key(key)
        save_key(key)
    elif args.get_otp :
        generate_otp()


main()