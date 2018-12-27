import binascii
from PIL import Image

BITS_PER_PX = 3
BITS_PER_CHAR = 8
BITS_PER_BYTE = 8

def can_embed(img, msg):
    # ========== size of image must be bigger than message ==========
    width, height = img.size
    img_bits = width * height * BITS_PER_PX
    msg_bits = len(msg) * BITS_PER_CHAR
    return msg_bits <= img_bits

def img2bin_list(img):
    # ========== convert rgba pixels into 2D list of binaries ==========
    bin_list = []
    pixels = list(img.getdata().convert("RGBA"))            # pixels -> [(255,255,255,255),...]
    for pixel in pixels:
        rgba = []
        for p in pixel:
            binary = bin(p)[2:]                             # bin(p) -> 0b11111111 / bin(p)[2:] -> 11111111
            rgba.append(binary)
        bin_list.append(rgba)                               # bin_list -> [[11111111,11111111,11111111,11111111],...]
    return bin_list

def str2bin_list(msg):
    # ========== convert string into a concatenated binary ==========
    bin_list = []
    for char in msg:
        ascii = ord(char)                                   # ord(char) -> 65
        binary = bin(ascii)[2:]                             # bin(ascii)[2:] -> 1000001
        bin_list.append(binary)                             # bin_list  -> ['1000001','1000010','1000011'...]
        flat_list = sum([ list(b) for b in bin_list ], [])  # flat_list -> ['1','0','0','0','0','0','1','1',...]
    return flat_list

def lsb(val, digit):
    binary = val[:-1] + digit                               # val -> 11111111 / val[:-1] -> 1111111
    return int(binary, 2)                                   # 255

if __name__ == "__main__":
    print("hoge")
