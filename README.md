## TL;DR
Client for using Twitter as a C&C server that embeds commands in steganography images.

## Usage
Manually create twitter account.
Create `config.py` (see `config_sample.py` for details) and enter your twitter id.
Manually upload the generated `output.jpg` in your twitter account (jpg highly recommended).
Once you fix `cron.conf` for your environment, run the following commands.

```
pip install -r requirements.txt
steganography -e ./steg_images/carrier.jpeg ./steg_images/output.jpg $(cat payload.txt)
crontab cron.conf
```

The script, running via cron, should find and download your uploaded image.

## 説明
https://blog.leojojo.me/2018/12/26/Steganography-Memes-for-Christmas/
