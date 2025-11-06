# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    htop.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/06 01:59:57 by akoaik            #+#    #+#              #
#    Updated: 2025/11/06 16:23:55 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hmac, hashlib, struct

def hotp (key_hex, counter) :
    
    # convert the key to hex raw bytes 
    key = bytes.fromhex(key_hex)

    #  RFC say that must exactly 8 bytes using big endian
    msg = struct.pack(">Q", counter)
    
    # create hash based auth code 
    # the hashlib.sha1 is the hash algo
    #  .digest gives a 20 byte binery result 
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    
    # takes the last byte of hash
    # & 0x0F keep only the lower 4 bits (number from 0 to 15)
    # this variable tell us where inside the hash we will start to read the next 4 bytes
    # this is define in RFC  
    offset = hmac_hash[-1] & 0x0F

    part = hmac_hash[offset:offset+4]
    # extract 4 byte from the hash starting at the calculated offset
    # this 4 bytes will be turned int othe final number

    num = int.from_bytes(part, "big") & 0x7FFFFFFF
    # convert those 4 bytes into an integer (big is the big endian)
    # the hexa clears the highest bit keeping the value positive
    # the result is a 31 bit positive integer

    otp = num % 1000000
    # reduce the big number to last 6 digits
    # remainder after dividind it
    # that keep the value between 0 and 999 999

    return f"{otp:06d}"
    # the 6 digits string adding the zeros if needed
    # like 42 -> "000042"