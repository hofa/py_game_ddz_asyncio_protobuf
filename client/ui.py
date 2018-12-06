import tkinter
from PIL import Image, ImageTk
import os
class PH:
    def __init__(self):
        self.file_path = os.path.dirname(os.path.realpath(__file__)) + "/images/ph.png"
        self.x_side = 7
        self.y_side = 13
        self.card_width = 65
        self.card_height = 92
        self.im = Image.open(self.file_path)
        self.max_colums = 14
        self.max_rows = 4
        self.x_j = 3.3
        self.y_j = 3.5
        self.define = {
            0: (0, 1),
            1: (1, 1),
            2: (2, 1),
            3: (3, 1),

            4: (0, 2),
            5: (1, 2),
            6: (2, 2),
            7: (3, 2),

            8: (0, 3),
            9: (1, 3),
            10: (2, 3),
            11: (3, 3),

            12: (0, 4),
            13: (1, 4),
            14: (2, 4),
            15: (3, 4),

            16: (0, 5),
            17: (1, 5),
            18: (2, 5),
            19: (3, 5),

            20: (0, 6),
            21: (1, 6),
            22: (2, 6),
            23: (3, 6),

            24: (0, 7),
            25: (1, 7),
            26: (2, 7),
            27: (3, 7),

            28: (0, 8),
            29: (1, 8),
            30: (2, 8),
            31: (3, 8),

            32: (0, 9),
            33: (1, 9),
            34: (2, 9),
            35: (3, 9),

            36: (0, 10),
            37: (1, 10),
            38: (2, 10),
            39: (3, 10),

            40: (0, 11),
            41: (1, 11),
            42: (2, 11),
            43: (3, 11),

            44: (0, 12),
            45: (1, 12),
            46: (2, 12),
            47: (3, 12),

            48: (0, 0),
            49: (1, 0),
            50: (2, 0),
            51: (3, 0),

            52: (0, 13),
            53: (1, 13),

            99: (2, 13)
        }

        self.cache = {}
        self.left_b_cache =  ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "/images/left.png"))
        self.right_b_cache =  ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "/images/right.png"))

    def get(self, row=0, column=0):
        return self.im.crop((
            self.x_side + row * (self.card_width + self.x_j),
            self.y_side + column * (self.card_height + self.y_j),
            self.x_side + self.card_width + row * (self.card_width + self.x_j),
            self.y_side + self.card_height + column * (self.card_height + self.y_j)
        ))

    def addTransparency(self, img, factor = 0.7):
        img = img.convert('RGBA')
        img_blender = Image.new('RGBA', img.size, (0,0,0,0))
        img = Image.blend(img_blender, img, factor)
        return img

    def get_cache(self):
        return self.cache

    def fetch_all(self):
        for card in self.define:
            c, r = self.define[card]
            sb = self.get(r, c)
            # if card == 52:
            #     self.cache[card] = ImageTk.PhotoImage(self.addTransparency(sb))
            # else:
            #     self.cache[card] = ImageTk.PhotoImage(sb)
            self.cache[card] = ImageTk.PhotoImage(sb)
        
        # left = self.get(13, 2)
        # left = left.rotate(90)
        # self.left_b_cache = ImageTk.PhotoImage(left)
        # self.right_b_cache = ImageTk.PhotoImage(self.get(3, 13))
        return self.cache
    