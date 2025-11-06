# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    key_manager.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/06 02:37:14 by akoaik            #+#    #+#              #
#    Updated: 2025/11/06 05:16:41 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
from encryption import encrypt, decrypt

KEY_FILE = "ft_otp.key"

def save_key(key_hex):

    data = f"{key_hex}:0"
    encrypted_data = encrypt(data)
    with open(KEY_FILE, "wb") as f:
        f.write(encrypted_data)
    os.chmod(KEY_FILE, 0o600)
    print("Key was successfully saved in ft_otp.key")

def load_key():

    if not os.path.exists(KEY_FILE):
        print("Error: ft_otp.key not found")
        exit(1)
    with open(KEY_FILE, "rb") as f:
        encrypted_data = f.read()
    data = decrypt(encrypted_data)
    key_hex, counter_str = data.split(":")
    return key_hex, int(counter_str)

def update_counter(key_hex, new_counter):
    data = f"{key_hex}:{new_counter}"
    encrypted_data = encrypt(data)
    with open(KEY_FILE, "wb") as f:
        f.write(encrypted_data)

