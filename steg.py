from PIL import Image 
import argparse, binascii
import util

OUTPUT_PATH = 'output.png'

def steg(path, msg): 
    # ========== convert image and message to binary ==========
    img = Image.open(path)
    if not util.can_embed(img, msg):
        print('message too big')
        quit()
    img_bin = util.img2bin_list(img)
    msg_bin = util.str2bin_list(msg)
    #print('msg', msg_bin[0]+msg_bin[1]+msg_bin[2]+msg_bin[3]+msg_bin[4]+msg_bin[5]+msg_bin[6]+msg_bin[7]+msg_bin[8]+msg_bin[9]+msg_bin[10]+msg_bin[11]+msg_bin[12])

    # ========== add header to message ==========
    msg_length = util.str2bin_list(str(len(msg)))                               # len(msg) -> 3/msg_length -> 0011011
    delimiter_bin = util.str2bin_list(util.DELIMITER)                           # '\\0' -(in binary)-> 0101110000110000
    msg_bin = msg_length + delimiter_bin + msg_bin                              # <length>\0<message>

    # ========== embed 1 bit of str_bin in each of rgba ==========
    new_pixels = []
    for pixel in img_bin:
        if len(msg_bin) != 0:
            rgba = tuple( util.embed_lsb(p,msg_bin.pop(0)) for p in pixel )     # rgba -> (0101011,,,11111110) ... sort of like (66,66,66,254)
            new_pixels.append(rgba)
        else:
            rgba = tuple( int(p,2) for p in pixel )                             # rgba -> (0101010,,,11111111) ... sort of like (65,65,65,255)
            new_pixels.append(rgba)

    # ========== create new image ==========
    #x = list(img.getdata())
    #print('orig', x[0], x[1], x[2])
    #print('new', new_pixels[0], new_pixels[1], new_pixels[2])
    #print(new_pixels)
    new_img = Image.new('RGBA', img.size)
    new_img.putdata(new_pixels)
    new_img.save(OUTPUT_PATH)
    return 'saved ' + OUTPUT_PATH



def unsteg(path):
    # ========== convert image to binary ==========
    img = Image.open(path)
    img_bin = util.img2bin_list(img)

    # ========== extract least-significant-bits from rgba ==========
    lsb_list = []
    for pixel in img_bin:
        for p in pixel:
            lsb = p[-1]                                                         # 1111110 -> 0
            lsb_list.append(lsb)

    # ========== convert bit list into character ==========
    char_list = []
    lsb_list = util.split_list(lsb_list, util.BITS_PER_CHAR)                    # ['0','1','0','1','0','1','0','1',...] -> [['0','1','0','1','0','1','0'],['1',...]]
    for lsb in lsb_list:
        byte = int(''.join(lsb),2)                                              # ['0','1','0','1','0','1','0'] -> 42
        char = str(chr(byte))                                                   # 42 -> '*'
        char_list.append(char)

    # ========== slice message from extracted list of characters ==========
    index = util.get_delimiter_index(char_list)                                 # ['1','0','\\','0','A','B','C',...] -> 3
    if not index is None:
        try:
            length = int(''.join(char_list[:index]))                            # ['1','0','\\','0','A','B','C',...] -> 10
        except ValueError:
            print('Could not extract message from {}'.format(path))
            quit()
        msg_body = char_list[index+2:]                                          # ['1','0','\\','0','A','B','C',...] -> ['A','B','C',...'not','part','of','msg']
        msg = ''.join(msg_body[:length])                                        # ['1','0','\\','0','A','B','C',...] -> ['A','B','C','D','E','F','G','H','I','J']
        return msg
    print('Could not extract message from {}'.format(path))
    quit()



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--carrier', required=True,
        help='image to embed data in')
    ap.add_argument('-p', '--payload', required=False,
        help='data to be embedded in image')
    args = vars(ap.parse_args())

    if args['payload'] is not None:
        msg = steg(args['carrier'], args['payload'])
    else:
        msg = unsteg(args['carrier'])
    print(msg)



if __name__ == '__main__':
    main()
