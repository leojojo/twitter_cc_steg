from PIL import Image 
import argparse, binascii
import util

def steg(path, msg): 
    # ========== convert image and message to binary ==========
    img = Image.open(path)
    if not util.can_embed(img, msg):
        print("message too big")
        quit()
    img_bin = util.img2bin_list(img)
    msg_bin = util.str2bin_list(msg)
    print("msg", msg_bin[0]+msg_bin[1]+msg_bin[2]+msg_bin[3]+msg_bin[4]+msg_bin[5]+msg_bin[6]+msg_bin[7]+msg_bin[8]+msg_bin[9]+msg_bin[10]+msg_bin[11]+msg_bin[12])

    # ========== embed 1 bit of str_bin in each of rgba ==========
    new_pixels = []
    for pixel in img_bin:
        if len(msg_bin) != 0:
            digit = msg_bin.pop(0)                                      # msg_bin -> ['1','0','0',...] / msg_bin.pop(0) -> '1'
            rgba = tuple( util.lsb(p,digit) for p in pixel )            # rgba -> (65,67,67,255)
            new_pixels.append(rgba)

    # ========== create new image ==========
    x = list(img.getdata())
    print("orig", x[0], x[1], x[2])
    print("new", new_pixels[0], new_pixels[1], new_pixels[2])
    new_img = Image.new("RGBA", img.size)
    new_img.putdata(new_pixels)
    new_img.save("output.png")



def unsteg(path):
    img = Image.open(path)
    data = img.getdata()



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--carrier", required=True,
        help="image to embed data in")
    ap.add_argument("-p", "--payload", required=False,
        help="data to be embedded in image")
    args = vars(ap.parse_args())

    if (args["payload"] is not None):
        steg(args["carrier"], args["payload"])
    else:
        unsteg(args["carrier"])



if __name__ == "__main__":
    main()
