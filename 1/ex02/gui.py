# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    gui.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akoaik <akoaik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/04 20:35:15 by akoaik            #+#    #+#              #
#    Updated: 2025/11/04 20:35:51 by akoaik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import tkinter as tk
from tkinter import filedialog
import scorpion


class ScorpionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scorpion")
        self.root.geometry("900x700")
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Open Image", command=self.open_file).pack(pady=10)

        self.output_text = tk.Text(self.root, width=80, height=25)
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )

        if file_path and scorpion.check_image(file_path):
            self.display_metadata(file_path)

    def display_metadata(self, file_path):
        self.output_text.delete(1.0, tk.END)
        metadata = scorpion.get_metadata_string(file_path)
        self.output_text.insert(tk.END, metadata)


def main():
    root = tk.Tk()
    app = ScorpionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
