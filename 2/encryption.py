# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    encryption.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/06 05:19:53 by akoaik            #+#    #+#              #
#    Updated: 2025/11/06 05:20:31 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

KEY = 0x42

def encrypt(data):
    return bytes([b ^ KEY for b in data.encode()])

def decrypt(encrypted_data):
    return bytes([b ^ KEY for b in encrypted_data]).decode()
