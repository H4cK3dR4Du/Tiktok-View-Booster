# <- Bypassed the zefoy.com captcha and shits 👍 -> # 
# <- By H4cK3dR4Du (tls_spoof) -> #

import os, re, sys, time, json, random, string, base64, ctypes, threading
from urllib.parse import urlparse, unquote

try:
    from pystyle import Write, System, Colors, Colorate
    from colorama import Fore, Style, init
    from requests import Session
    from datetime import datetime
except ModuleNotFoundError:
    os.system('pip install pystyle')
    os.system('pip install colorama')
    os.system('pip install requests')
    os.system('pip install datetime')

class Output:
    reset = Fore.RESET
    black = Fore.BLACK
    red = Fore.RED
    green = Fore.GREEN
    yellow = Fore.YELLOW
    blue = Fore.BLUE
    magenta = Fore.MAGENTA
    cyan = Fore.CYAN
    white = Fore.WHITE
    gray = Fore.LIGHTBLACK_EX
    light_gray = Fore.LIGHTWHITE_EX
    light_red = Fore.LIGHTRED_EX
    light_green = Fore.LIGHTGREEN_EX
    light_yellow = Fore.LIGHTYELLOW_EX
    light_blue = Fore.LIGHTBLUE_EX
    light_magenta = Fore.LIGHTMAGENTA_EX
    light_cyan = Fore.LIGHTCYAN_EX

proxies = Session().get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&simplified=true').text
with open('proxies.txt', 'w') as file:
    file.write(proxies.replace('\n', ''))

class Config:
    config = json.loads(open('config.json', 'r').read())

    threads = config['threads']
    video_url = config['video_url']
    proxy_scraper = config['proxy_scraper']

class Tiktok:
    def __init__(self) -> None:
        self.chrome_version = random.randint(112, 122)
        self.headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome_version}.0.0.0 Safari/537.36"
        }

        self.selected_proxies = set()
        self.session = self._getSession()
        self.phpsessid = random.choice(['jtc6tdfgs4tike6rs5in97gb77', 'lsaigisdllrkrdmqafn11qtk56', 'asr29bksl92cuim29u9ga0o1f4', 'gfoesubki0or0vqn1qpscs0ds6'])
        self.vid_key = None
        self.captcha = None
        self.captchas = {}

    def _banner(self) -> None:
        views, likes, comments, shares = i._videoInfo()
        Write.Print(f"""
\t\t                          d8, d8b                        d8b                                      
\t\t                   d8P   `8P  ?88          d8P           ?88                                      
\t\t                d888888P       88b      d888888P          88b                                     
\t\t                  ?88'    88b  888  d88'  ?88'   d8888b   888  d88'                               
\t\t                  88P     88P  888bd8P'   88P   d8P' ?88  888bd8P'                                
\t\t                  88b    d88  d88888b     88b   88b  d88 d88888b                                  
\t\t                  `?8b  d88' d88' `?88b,  `?8b  `?8888P'd88' `?88b,                               
                                                                            
\t           d8,                           d8b                                                      
\t          `8P                            ?88                                 d8P                  
\t                                          88b                             d888888P                
\t?88   d8P  88b d8888b ?88   d8P  d8P      888888b  d8888b  d8888b  .d888b,  ?88'   d8888b  88bd88b
\td88  d8P'  88Pd8b_,dP d88  d8P' d8P'      88P `?8bd8P' ?88d8P' ?88 ?8b,     88P   d8b_,dP  88P'  `
\t?8b ,88'  d88 88b     ?8b ,88b ,88'      d88,  d8888b  d8888b  d88   `?8b   88b   88b     d88     
\t`?888P'  d88' `?888P' `?888P'888P'      d88'`?88P'`?8888P'`?8888P'`?888P'   `?8b  `?888P'd88'     
                                                                                        
\t╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
\t\t\t\t\t\tVideo ID: {Config.video_url.rsplit("/", 1)[-1]}
\t\t\t\t\t\tVideo Owner: @{Config.video_url.split('/')[3][1:]}
\t\t\t\t\t\tVideo Total Views: {views}
\t\t\t\t\t\tVideo Total Likes: {likes}
\t\t\t\t\t\tVideo Total Comments: {comments}
\t\t\t\t\t\tVideo Total Shares: {shares}
\t╚════════════════════════════════════════════════════════════════════════════════════════════════════╝                                                                         
""", Colors.blue_to_purple, interval=0.0000)

    def _getSession(self) -> Session:
        session = Session()

        with open('proxies.txt', 'r') as f:
            proxies_list = f.readlines()

        while True:
            self.proxy = random.choice(proxies_list).strip()
            if self.proxy not in self.selected_proxies:
                break

        self.selected_proxies.add(self.proxy)

        session.proxies = {
            'https': f'http://{self.proxy}',
            'http': f'http://{self.proxy}'
        }

        return session
    
    def _time() -> str:
        return "{:%H:%M:%S}".format(datetime.now())
    
    def _videoInfo(self) -> tuple[int, int, int, int]:
        headers = {
            "authority": "tiktok.livecounts.io",
            "Origin": "https://livecounts.io",
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome_version}.0.0.0 Safari/537.36"
        }

        r = Session().get(f'https://tiktok.livecounts.io/video/stats/{Config.video_url.rsplit("/", 1)[-1]}', headers=headers)
        if r.json()['success'] == True:
            return r.json()['viewCount'], r.json()['likeCount'], r.json()['commentCount'], r.json()['shareCount']
        else:
            self._videoInfo()

    def _getCaptchaText(self) -> tuple[bool, str]:
        r = self.session.get("https://zefoy.com/", headers=self.headers)
        if 'Enter Video URL' in r.text:
            self.vid_key = r.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            return True, "Solved"

        try:
            for x in re.findall(r'<input type="hidden" name="(.*)" value="(.*)">', r.text):
                self.captchas[x[0]] = x[1]
            
            self.captcha = r.text.split('type="text" name="')[1].split('" oninput="this.value=this.value.toLowerCase()"')[0]
            url = r.text.split('<img src="')[1].split('" onerror="imgOnError()" class="')[0]
            r = self.session.get(f"https://zefoy.com/{url}", headers=self.headers)
            captcha_path = os.path.join("data", f"captcha{random.randint(99999, 999999)}.png")
            open(captcha_path, 'wb').write(r.content)
            return False, captcha_path
        except:
            self._getCaptchaText()

    def _sendCaptcha(self) -> tuple[bool, str]:
        success, path = self._getCaptchaText()
        if success:
            return

        captcha_text, file = self._solveCaptcha(path)
        self.captchas[self.captcha] = captcha_text
        self.phpsessionID = self.session.cookies.get('PHPSESSID')
        self.session.cookies.set("PHPSESSID", self.phpsessionID, domain='zefoy.com')

        r = self.session.post("https://zefoy.com/", headers=self.headers, data=self.captchas)
        if "Enter Video URL" in r.text:
            self.vid_key = r.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            os.remove(file)
            self._parseVideo()
        else:
            os.remove(file)

    def _solveCaptcha(self, path) -> str:
        # <- I got this captcha solver from a random guy I found in github -> # 
        with open(path, 'rb') as file:
            files = {
                "task": file
            }

            headers = {
                "apikey": "K87899142388957"
            }

            url = 'https://api.ocr.space/parse/image?K87899142388957'
            r = self.session.post(url, headers=headers, files=files)
            
            if r.status_code == 200:
                captcha_text = r.json()['ParsedResults'][0]['ParsedText']
                return captcha_text, path
            else:
                self._sendCaptcha()

    def _parseVideo(self) -> str:
        while True:
            headers = {
                "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary0nU8PjANC8BhQgjZ",
                "Origin": "https://zefoy.com",
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome_version}.0.0.0 Safari/537.36"
            }

            data = f'------WebKitFormBoundary0nU8PjANC8BhQgjZ\r\nContent-Disposition: form-data; name="{self.vid_key}"\r\n\r\n{Config.video_url}\r\n------WebKitFormBoundary0nU8PjANC8BhQgjZ--\r\n'

            r = self.session.post(f'https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V', headers=headers, data=data)
            
            vid_info = base64.b64decode(unquote(r.text.encode()[::-1])).decode()
            if 'Session expired. Please re-login' in vid_info:
                self._sendCaptcha()
                return
            elif """onsubmit="showHideElements""" in vid_info:
                vid_info = [vid_info.split('" name="')[1].split('"')[0]]
                return vid_info[0]
            elif "Checking Timer..." in vid_info:
                timer = int(re.findall(r'ltm=(\d*);', vid_info)[0])
                time.sleep(timer)
                r = self.session.post(f'https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V', headers=headers, data=data)
                vid_info = base64.b64decode(unquote(r.text.encode()[::-1])).decode()
                vid_info = [vid_info.split('" name="')[1].split('"')[0]]
                return vid_info[0]
            else:
                return vid_info
        
    def _sendViews(self):
        video_info = self._parseVideo()
        if video_info == None:
            self._parseVideo()

        token = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        headers = {
            "Content-Type": f"multipart/form-data; boundary=----WebKitFormBoundary{token}",
            "Origin": "https://zefoy.com",
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome_version}.0.0.0 Safari/537.36"
        }

        data = f'------WebKitFormBoundary{token}\r\nContent-Disposition: form-data; name="{video_info}"\r\n\r\n{Config.video_url.rsplit("/", 1)[-1]}\r\n------WebKitFormBoundary{token}--\r\n'

        r = self.session.post(f"https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V", headers=headers, data=data)
        decoded = base64.b64decode(unquote(r.text.encode()[::-1])).decode()
        if "Too many requests. Please slow down." in decoded:
            time.sleep(10)
            self._sendViews()
        else:
            try:
                print(decoded.split("sans-serif;text-align:center;color:green;'>")[1].split("</")[0])
                print(self.session.proxies)
            except:
                timer = int(re.findall(r'ltm=(\d*);', decoded)[0])
                time.sleep(timer)
                data = f'------WebKitFormBoundary{token}\r\nContent-Disposition: form-data; name="{video_info}"\r\n\r\n{Config.video_url.rsplit("/", 1)[-1]}\r\n------WebKitFormBoundary{token}--\r\n'
                r2 = self.session.post(f"https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V", headers=headers, data=data)
                decoded2 = base64.b64decode(unquote(r2.text.encode()[::-1])).decode()
                print(decoded2.split("sans-serif;text-align:center;color:green;'>")[1].split("</")[0])
                print(self.session.proxies)
                self._sendCaptcha()

def view_booster():
    try:
        tiktok = Tiktok()
        tiktok._sendCaptcha()
        tiktok._sendViews()
    except:
        pass

if __name__ == "__main__":
    i = Tiktok()
    i._banner()
    
    try:
        while True:
            while threading.active_count()-1 < Config.threads:
                threading.Thread(target=view_booster).start()
            time.sleep(1)
    except Exception as e:
        print(e)
        pass