# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/04 17:07:37 by akoaik            #+#    #+#              #
#    Updated: 2025/11/04 23:06:15 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import os
from PIL import Image
from datetime import datetime

allowed_ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def check_image(file_path):

    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        return False

    if not file_path.lower().endswith(allowed_ext):
        print(f"Error: Unsupported file type")
        return False

    return True


def get_metadata_string(file_path):
    output = []
    output.append(f"{'=' * 60}")
    output.append(f"File: {file_path}")
    output.append(f"{'=' * 60}\n")

    try:
        file_stats = os.stat(file_path)
        output.append("File Information:")
        output.append(f"  Size: {file_stats.st_size:,} bytes")
        output.append(f"  Created: {datetime.fromtimestamp(file_stats.st_ctime)}")
        output.append(f"  Modified: {datetime.fromtimestamp(file_stats.st_mtime)}\n")
    except Exception as e:
        output.append(f"Error reading file stats: {e}")

    try:
        img = Image.open(file_path)
        output.append("Image Information:")
        output.append(f"  Format: {img.format}")
        output.append(f"  Mode: {img.mode}")
        output.append(f"  Size: {img.size[0]} x {img.size[1]} pixels\n")

        exif = img.getexif()
        if exif:
            output.append("EXIF Metadata:")
            for tag_id, value in exif.items():
                output.append(f"  {tag_id}: {value}")
        else:
            output.append("No EXIF data found")

    except Exception as e:
        output.append(f"Error reading image: {e}")

    return "\n".join(output)


def show_metadata(file_path):
    
    print(f"\n=== {file_path} ===")

    # Get file stats
    file_stats = os.stat(file_path)
    print(f"Size: {file_stats.st_size} bytes")
    print(f"Created: {datetime.fromtimestamp(file_stats.st_ctime)}")
    print(f"Modified: {datetime.fromtimestamp(file_stats.st_mtime)}")

    # Open image and get metadata
    try:
        img = Image.open(file_path)
        print(f"Format: {img.format}")
        print(f"Size: {img.size[0]} x {img.size[1]} pixels")

        # Get EXIF data
        exif = img.getexif()
        if exif:
            print("\nEXIF Data:")
            for tag_id, value in exif.items():
                print(f"  {tag_id}: {value}")
        else:
            print("No EXIF data found")

    except Exception as e:
        print(f"Error reading image: {e}")


def parse():
    parser = argparse.ArgumentParser(description="Display image metadata and EXIF data")
    parser.add_argument("-gui", action="store_true", help="Launch GUI mode")
    parser.add_argument("images", nargs="*", help="Image file paths")
    args = parser.parse_args()
    return args

def main():
    args = parse()

    # Check if GUI mode
    if args.gui:
        from gui import main as gui_main
        gui_main()
        return

    if not args.images:
        print("Usage: ./scorpion FILE1 [FILE2 ...] or ./scorpion -gui")
        return

    for img_path in args.images:
        if check_image(img_path):
            show_metadata(img_path)


if __name__ == "__main__":
    main()