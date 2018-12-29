import binascii
from PIL import Image

DELIMITER = '\\0'
BITS_PER_PX = 3
BITS_PER_CHAR = 8

def can_embed(img, msg):
    # ========== size of image must be bigger than message ==========
    width, height = img.size
    img_bits = width * height * BITS_PER_PX
    msg_bits = len(msg) * BITS_PER_CHAR
    return msg_bits <= img_bits

def img2bin_list(img):
    # ========== convert rgba pixels into 2D list of binaries ==========
    bin_list = []
    pixels = list(img.getdata().convert('RGBA'))                                # pixels -> [(255,255,255,255),...]

    for pixel in pixels:
        rgba = []
        for p in pixel:
            binary = bin(p)[2:].zfill(BITS_PER_CHAR)                            # bin(p) -> 0b11111111 / bin(p)[2:] -> 11111111
            rgba.append(binary)
        bin_list.append(rgba)                                                   # bin_list -> [[11111111,11111111,11111111,11111111],...]
    return bin_list

def str2bin_list(msg):
    # ========== convert string into a concatenated binary ==========
    if not len(msg) == 0:
        bin_list = []
        for char in msg:
            ascii = ord(char)                                                   # ord(char) -> 65
            binary = bin(ascii)[2:].zfill(BITS_PER_CHAR)                        # bin(ascii)[2:] -> 01000001
            bin_list.append(binary)                                             # bin_list  -> ['01000001','01000010','01000011'...]
            flat_list = sum([ list(b) for b in bin_list ], [])                  # flat_list -> ['0','1','0','0','0','0','0','1','0',...]
        return flat_list
    else:
        print('string is length 0')
        quit()

def split_list(lst, n):
    # ========== split list into sublists of length n ==========
    return [ lst[i:i+n] for i in range(0, len(lst), n) ]                        # [1,2,3,4,5], 2 -> [[1,2],[3,4],[5]]

def embed_lsb(val, digit):
    # ========== put digit into least significant bit of val ==========
    binary = val[:-1] + digit                                                   # val -> 11111111 / val[:-1] -> 1111111
    return int(binary, 2)                                                       # 255

def get_delimiter_index(char_list):
    # ========== checks if message has delimiter, returns index of \ ==========
    try:
        index =  char_list.index(DELIMITER[0])                                  # ['1','0','\\','0','A','B','C',...] -> 3
        if char_list[index+1] == DELIMITER[1]:
            return index
        else:
            return None
    except ValueError:
        return None

if __name__ == '__main__':
    valid = ['1','0','\\','0','A','B','C','D','E','F','G','H','I','J','みないでー','やめてー']
    i = ['a','\\','0','A','B','C','みないでー','やめてー']
    n = ['3','3','0','A','B','C','みないでー','やめてー']
    v = ['3','\\','z','A','B','C','みないでー','やめてー']
    a = ['3','\\','\\','0','A','B','C','みないでー','やめてー']
    print(get_delimiter_index(valid))
    print(get_delimiter_index(i))
    print(get_delimiter_index(n))
    print(get_delimiter_index(v))
    print(get_delimiter_index(a))

    #lst = [1,2,3,4,5]
    #print(split_list(lst,2))

    #val = '010101010'
    #digit = '1'
    #print(val, digit)
    #print(embed_lsb(val,digit))

    #img = Image.get('sample.png')
    #print(img2bin_list(img))

    #msg = 'ABC'
    #print(str2bin_list(msg))
