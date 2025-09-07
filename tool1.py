import os
from time import sleep
from datetime import datetime

try:
    import requests
except:
    os.system("pip3 install requests")
    import requests

headers = {
    'authority': 'traodoisub.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'user-agent': 'traodoisub tiktok tool',
}

def login_tds(token):
    try:
        r = requests.get('https://traodoisub.com/api/?fields=profile&access_token='+token, headers=headers, timeout=5).json()
        if 'success' in r:
            print(f"Đăng nhập thành công! User: {r['data']['user']} | Xu hiện tại: {r['data']['xu']}")
            return 'success'
        else:
            print(f"Token TDS không hợp lệ, hãy kiểm tra lại!")
            return 'error_token'
    except:
        return 'error'

def load_job(type_job, token):
    try:
        r = requests.get(f'https://traodoisub.com/api/?fields={type_job}&access_token={token}', headers=headers, timeout=5).json()
        if 'data' in r:
            return r
        elif "countdown" in r:
            sleep(round(r['countdown']))
            print(f"{r['error']}")
            return 'error_countdown'
        else:
            print(f"{r['error']}")
            return 'error_error'
    except:
        return 'error'

def duyet_job(type_job, token, uid):
    try:
        r = requests.get(f'https://traodoisub.com/api/coin/?type={type_job}&id={uid}&access_token={token}', headers=headers, timeout=5).json()
        if "cache" in r:
            return r['cache']
        elif "success" in r:
            print(f"Nhận thành công {r['data']['job_success']} nhiệm vụ | {r['data']['msg']} | {r['data']['xu']}")
            return 'error'
        else:
            print(f"{r['error']}")
            return 'error'
    except:
        return 'error'

def check_tiktok(id_tiktok, token):
    try:
        r = requests.get(f'https://traodoisub.com/api/?fields=tiktok_run&id={id_tiktok}&access_token={token}', headers=headers, timeout=5).json()
        if 'success' in r:
            print(f"{r['data']['msg']} | ID: {r['data']['id']}")
            return 'success'
        else:
            print(f"{r['error']}")
            return 'error_token'
    except:
        return 'error'

# Tương tự, các phần nhập token, chọn nhiệm vụ, delay, max_job vẫn giữ nhưng bỏ write/color
# Ví dụ:
token_tds = input("Nhập token TDS: ")
check_log = login_tds(token_tds)

id_tiktok = input("Nhập ID tiktok: ")
check_tiktok(id_tiktok, token_tds)

choice = int(input("Lựa chọn nhiệm vụ muốn làm (1-Follow, 2-Like): "))
delay = int(input("Thời gian delay (giây): "))
max_job = int(input("Bao nhiêu nhiệm vụ dừng tool: "))
