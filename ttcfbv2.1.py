import json
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from pystyle import Write, Colors, Colorate
from datetime import datetime
import cloudscraper
import socket
import subprocess
from time import strftime
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from colorama import Fore, init
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
import psutil

def rgb_to_ansi(r, g, b):
    """Chuyển đổi RGB sang mã ANSI 24-bit (sáng hơn)"""
    return f"\033[38;2;{r};{g};{b}m"

# Màu cố định SÁNG HƠN
MAU_DO_SANG       = rgb_to_ansi(255, 100, 100)  # Đỏ nhạt/Hồng coral
MAU_LUC_SANG      = rgb_to_ansi(120, 255, 120)  # Xanh lá neon/Mint
MAU_VANG_SANG     = rgb_to_ansi(255, 255, 120)  # Vàng chanh sáng
MAU_TRANG_SANG    = rgb_to_ansi(240, 240, 240)  # Trắng kem
MAU_TIM_SANG_DAM      = rgb_to_ansi(200, 160, 255)

MAU_TIM_SANG      = "\033[38;2;220;200;255m"  # Tím lavender sáng
MAU_XANH_DUONG_SANG = rgb_to_ansi(100, 200, 255)  # Xanh da trời sáng
MAU_DEP_SANG      = rgb_to_ansi(180, 255, 255)  # Cyan pastel

# Biến cố định cho giao diện
do = MAU_DO_SANG
luc = MAU_LUC_SANG
vang = MAU_VANG_SANG
trang = MAU_TRANG_SANG
tim = MAU_TIM_SANG
timv2 = MAU_TIM_SANG_DAM
xanh = MAU_XANH_DUONG_SANG
dep = MAU_DEP_SANG
v = MAU_TIM_SANG # Giữ lại biến 'v' cho Tím sữa sáng/Lavender
thanh = f'{timv2} {trang}=> '
unicode_invisible = ("ㅤ")

def gradient_3(text):
    """Xanh lá (sáng) -> Xanh biển (sáng)"""
    start = (100, 255, 100)   # Xanh lá sáng
    end   = (100, 180, 255) # Xanh biển sáng
    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"
    
def gradient_tutu(text):
    """Hồng phấn (sáng) -> Mint nhạt (sáng) -> Vàng chanh pastel (sáng)"""
    start_color = (255, 220, 230)  # 🌸 Hồng phấn SÁNG
    mid_color   = (200, 255, 200)  # 🌿 Mint nhạt SÁNG
    end_color   = (255, 255, 180)  # 💛 Vàng chanh pastel SÁNG

    steps = len(text)
    result = ""

    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)

        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)

        result += rgb_to_ansi(r, g, b) + char

    return result + "\033[0m"
    
def inp(text):
    """Sử dụng gradient sáng hơn cho input"""
    # Gradient Tím Lavender sáng -> Cyan sáng
    start_color = (200, 180, 255)
    end_color = (180, 255, 255)
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        t = i / (length - 1 if length > 1 else 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

def gradient_2(text):
    """Cam Đào Sáng -> Hồng Neon Sáng -> Vàng Sáng"""
    start_color = (255, 160, 120)     # 🧡 Cam Đào Sáng
    mid_color   = (255, 120, 200)    # 💖 Hồng Neon Sáng
    end_color   = (255, 255, 100)     # 💛 Vàng sáng chói

    steps = len(text)
    result = ""

    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)

        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)

        result += rgb_to_ansi(r, g, b) + char

    return result + "\033[0m"
    
def gradient_1(text):
    """Xanh dương (Sáng) -> Cyan (Sáng) -> Trắng (Sáng)"""
    start_color = (100, 180, 255)     # 💧 Xanh dương sáng
    mid_color   = (180, 255, 255)     # 🧊 Cyan sáng
    end_color   = (255, 255, 255)   # ⚪ Trắng sáng

    steps = len(text)
    result = ""

    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)

        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)

        result += rgb_to_ansi(r, g, b) + char

    return result + "\033[0m"
    
def gradient(text, start_color=(255, 100, 255), end_color=(100, 255, 255)):
    """Tím Neon Sáng -> Cyan Neon Sáng"""
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (length - 1 if length > 1 else 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (length - 1 if length > 1 else 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (length - 1 if length > 1 else 1))
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"  # Reset màu về mặc định
    return result

# --- CÁC HÀM TIỆN ÍCH ---
import requests, re, os, json, base64, uuid, random, sys
from time import sleep
from datetime import datetime
from pystyle import Colors, Colorate
from bs4 import BeautifulSoup
listCookie = []
list_nv = []

def thanhngang(so):
    """Hiển thị thanh ngang với màu SÁNG"""
    for i in range(so):
        print(MAU_DEP_SANG + '═',end ='') # Dùng màu cyan pastel sáng
    print('')

def Delay(value):
    """Hiển thị thanh delay với màu SÁNG"""
    v_bright = MAU_TIM_SANG  # Tím sữa sáng
    xanh_cyan = MAU_XANH_DUONG_SANG # Cyan sáng
    vang_bright = MAU_VANG_SANG         # Vàng sáng
    filled_block = "█"
    empty_block = "░"
    BAR_LENGTH = 15 
    start_time = time.time()
    total_delay = value 
    MAX_LINE_LENGTH = 60 

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = total_delay - elapsed_time
        if remaining_time <= 0:
            print(' ' * MAX_LINE_LENGTH, end = '\r')
            print(f'    {luc}ĐANG LÀM', end='\r')
            break
        ratio = elapsed_time / total_delay
        fill_count = int(ratio * BAR_LENGTH)
        progress_bar = (
            f'{vang_bright}' + 
            filled_block * fill_count +         
            empty_block * (BAR_LENGTH - fill_count) + 
            f'{vang_bright}'
        )
        print(
            f'''{v_bright}[{luc}TTC-TOOL{v_bright}] [{dep}DELAY{v_bright}] [{trang}{str(remaining_time)[0:6]}{v_bright}] [{progress_bar}{v_bright}]''',
            '           ', 
            end = '\r')
        sleep(0.05)
        
def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

class Facebook:
    def __init__(self, cookie: str):
        try:
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.session = requests.Session()
            self.id = self.cookie.split('c_user=')[1].split(';')[0]
            self.headers = {'authority': 'www.facebook.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'vi', 'sec-ch-prefers-color-scheme': 'light', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'viewport-width': '1366', 'Cookie': self.cookie}
            url = self.session.get(f'https://www.facebook.com/{self.id}', headers=self.headers).url
            response = self.session.get(url, headers=self.headers).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
        except:
            pass

    def info(self):
        try:
            get = self.session.get('https://www.facebook.com/me', headers=self.headers).url
            url = 'https://www.facebook.com/' + get.split('%2F')[-2] + '/' if 'next=' in get else get
            response = self.session.get(url, headers=self.headers, params={"locale": "vi_VN"})
            data_split = response.text.split('"CurrentUserInitialData",[],{')
            json_data = '{' + data_split[1].split('},')[0] + '}'
            parsed_data = json.loads(json_data)
            id = parsed_data.get('USER_ID', '0')
            name = parsed_data.get('NAME', '')
            if id == '0' and name == '': return 'cookieout'
            elif '828281030927956' in response.text: return '956'
            elif '1501092823525282' in response.text: return '282'
            elif '601051028565049' in response.text: return 'spam'
            else: id, name = parsed_data.get('USER_ID'), parsed_data.get('NAME')
            return {'success': 200, 'id': id, 'name': name}
        except:
            pass
        
    def likepage(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometProfilePlusLikeMutation','variables': '{"input":{"is_tracking_encrypted":false,"page_id":"'+str(id)+'","source":null,"tracking":null,"actor_id":"'+str(self.id)+'","client_mutation_id":"1"},"scale":1}','server_timestamps': 'true','doc_id': '6716077648448761',}
            response = self.session.post('https://www.facebook.com/api/graphql/',data=data,headers=self.headers)
            if '"subscribe_status":"IS_SUBSCRIBED"' in response.text:
                return True
            else:
                return False
        except:
            pass

    def follow(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUserFollowMutation','variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1719765181042,489343,250100865708545,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,unexpected,1719765155735,648442,391724414624676,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1719765153341,865155,391724414624676,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'+str(id)+'","tracking":null,"actor_id":"'+str(self.id)+'","client_mutation_id":"5"},"scale":1}','server_timestamps': 'true','doc_id': '25581663504782089',}
            response = self.session.post('https://www.facebook.com/api/graphql/',data=data,headers=self.headers)
            if '"subscribe_status":"IS_SUBSCRIBED"' in response.text:
                return True
            else:
                return False
        except:
            pass

    def reaction(self, id: str, type: str):
        try:
            reac = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
            idreac = reac.get(type)
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation','variables': fr'{{"input":{{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1719027162723,322693,4748854339,,","feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{idreac}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"tracking":["AZWUDdylhKB7Q-Esd2HQq9i7j4CmKRfjJP03XBxVNfpztKO0WSnXmh5gtIcplhFxZdk33kQBTHSXLNH-zJaEXFlMxQOu_JG98LVXCvCqk1XLyQqGKuL_dCYK7qSwJmt89TDw1KPpL-BPxB9qLIil1D_4Thuoa4XMgovMVLAXncnXCsoQvAnchMg6ksQOIEX3CqRCqIIKd47O7F7PYR1TkMNbeeSccW83SEUmtuyO5Jc_wiY0ZrrPejfiJeLgtk3snxyTd-JXW1nvjBRjfbLySxmh69u-N_cuDwvqp7A1QwK5pgV49vJlHP63g4do1q6D6kQmTWtBY7iA-beU44knFS7aCLNiq1aGN9Hhg0QTIYJ9rXXEeHbUuAPSK419ieoaj4rb_4lA-Wdaz3oWiWwH0EIzGs0Zj3srHRqfR94oe4PbJ6gz5f64k0kQ2QRWReCO5kpQeiAd1f25oP9yiH_MbpTcfxMr-z83luvUWMF6K0-A-NXEuF5AiCLkWDapNyRwpuGMs8FIdUJmPXF9TGe3wslF5sZRVTKAWRdFMVAsUn-lFT8tVAZVvd4UtScTnmxc1YOArpHD-_Lzt7NDdbuPQWQohqkGVlQVLMoJNZnF_oRLL8je6-ra17lJ8inQPICnw7GP-ne_3A03eT4zA6YsxCC3eIhQK-xyodjfm1j0cMvydXhB89fjTcuz0Uoy0oPyfstl7Sm-AUoGugNch3Mz2jQAXo0E_FX4mbkMYX2WUBW2XSNxssYZYaRXC4FUIrQoVhAJbxU6lomRQIPY8aCS0Ge9iUk8nHq4YZzJgmB7VnFRUd8Oe1sSSiIUWpMNVBONuCIT9Wjipt1lxWEs4KjlHk-SRaEZc_eX4mLwS0RcycI8eXg6kzw2WOlPvGDWalTaMryy6QdJLjoqwidHO21JSbAWPqrBzQAEcoSau_UHC6soSO9UgcBQqdAKBfJbdMhBkmxSwVoxJR_puqsTfuCT6Aa_gFixolGrbgxx5h2-XAARx4SbGplK5kWMw27FpMvgpctU248HpEQ7zGJRTJylE84EWcVHMlVm0pGZb8tlrZSQQme6zxPWbzoQv3xY8CsH4UDu1gBhmWe_wL6KwZJxj3wRrlle54cqhzStoGL5JQwMGaxdwITRusdKgmwwEQJxxH63GvPwqL9oRMvIaHyGfKegOVyG2HMyxmiQmtb5EtaFd6n3JjMCBF74Kcn33TJhQ1yjHoltdO_tKqnj0nPVgRGfN-kdJA7G6HZFvz6j82WfKmzi1lgpUcoZ5T8Fwpx-yyBHV0J4sGF0qR4uBYNcTGkFtbD0tZnUxfy_POfmf8E3phVJrS__XIvnlB5c6yvyGGdYvafQkszlRrTAzDu9pH6TZo1K3Jc1a-wfPWZJ3uBJ_cku-YeTj8piEmR-cMeyWTJR7InVB2IFZx2AoyElAFbMuPVZVp64RgC3ugiyC1nY7HycH2T3POGARB6wP4RFXybScGN4OGwM8e3W2p-Za1BTR09lHRlzeukops0DSBUkhr9GrgMZaw7eAsztGlIXZ_4"],"session_id":"{uuid.uuid4()}","actor_id":"{self.id}","client_mutation_id":"3"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}','server_timestamps': 'true','doc_id': '7047198228715224',}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except:
            pass

    def reactioncmt(self, id: str, type: str):
        try:
            reac = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
            g_now = datetime.now()
            d = g_now.strftime("%Y-%m-%d %H:%M:%S.%f")
            datetime_object = datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f")
            timestamp = str(datetime_object.timestamp())
            starttime = timestamp.replace('.', '')
            id_reac = reac.get(type)
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation','variables': '{"input":{"attribution_id_v2":"CometVideoHomeNewPermalinkRoot.react,comet.watch.injection,via_cold_start,1719930662698,975645,2392950137,,","feedback_id":"'+encode_to_base64("feedback:"+str(id))+'","feedback_reaction_id":"'+id_reac+'","feedback_source":"TAHOE","is_tracking_encrypted":true,"tracking":[],"session_id":"'+str(uuid.uuid4())+'","downstream_share_session_id":"'+str(uuid.uuid4())+'","downstream_share_session_origin_uri":"https://fb.watch/t3OatrTuqv/?mibextid=Nif5oz","downstream_share_session_start_time":"'+starttime+'","actor_id":"'+self.id+'","client_mutation_id":"1"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}', 'server_timestamps': 'true','doc_id': '7616998081714004',}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except:
            pass
    
    def share(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'ComposerStoryCreateMutation','variables': '{"input":{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","attachments":[{"link":{"share_scrape_data":"{\\"share_type\\":22,\\"share_params\\":['+id+']}"}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"is_tracking_encrypted":true,"tracking":["AZWWGipYJ1gf83pZebtJYQQ-iWKc5VZxS4JuOcGWLeB-goMh2k74R1JxqgvUTbDVNs-xTyTpCI4vQw_Y9mFCaX-tIEMg2TfN_GKk-PnqI4xMhaignTkV5113HU-3PLFG27m-EEseUfuGXrNitybNZF1fKNtPcboF6IvxizZa5CUGXNVqLISUtAWXNS9Lq-G2ECnfWPtmKGebm2-YKyfMUH1p8xKNDxOcnMmMJcBBZkUEpjVzqvUTSt52Xyp0NETTPTVW4zHpkByOboAqZj12UuYSsG3GEhafpt91ThFhs7UTtqN7F29UsSW2ikIjTgFPy8cOddclinOtUwaoMaFk2OspLF3J9cwr7wPsZ9CpQxU21mcFHxqpz7vZuGrjWqepKQhWX_ZzmHv0LR8K07ZJLu8yl51iv-Ram7er9lKfWDtQsuNeLqbzEOQo0UlRNexaV0V2m8fYke8ubw3kNeR5XsRYiyr958OFwNgZ3RNfy-mNnO9P-4TFEF12NmNNEm4N6h0_DRZ-g74n-X2nGwx9emPv4wuy9kvQGeoCqc636BfKRE-51w2GFSrHAsOUJJ1dDryxZsxQOEGep3HGrVp_rTsVv7Vk3JxKxlzqt3hnBGDgi6suTZnJw69poVOIz6TPCTthRhj7XUu4heyKBSIeHsjBRC2_s3NwuZ4kKNCQ2JkVuBXz_hsRhDmbAnBi6WUFIJhLHO_bGgKbEASuU4vtj4FNKo_G8p-J1kYmCo0Pi72Csi3EikuocfjHFwfSD3cCbetr3V8Yp6OmSGkqX63FkSqzBoAcHFeD-iyCAkn0UJGqU-0o670ZoR-twkUDcSJPXDN2NYQfqiyb9ZknZ7j04w1ZfAyaE7NCiCc-lDt1ic79XyHunjOyLStgXIW30J4OEw_hAn86LlRHbYVhi-zBBTZWWnEl9piuUz0qtnN-qEd002DjNYaMy0aDAbL9oOYDdN8mHvnXq1aKove9I4Jy0WtlxeN8279ayz7NdDZZ9LrajY_YxIJJqdZtJIuRYTunEeDsFrORpu3RYRbFwpGnQbHeSLH1YvwOyOJRXhYYmVLJEGD2N9r5wkPbgbx2HoWsGjWj_DpkEAyg59eBJy4RYPJHvOsetBQABEWmGI7nhUDYTPdhrzVxqB_g4fQ9JkPzIbEhcoEZjmspGZcR4z4JxUDJCNdAz2aK4lR4P5WTkLtj2uXMDD_nzbl8r_DMcj23bjPiSe0Fubu-VIzjwr7JgPNyQ1FYhp5u4lpqkkBkGtfyAaUjCgFhg4FW-H3d3vPVMO--GxbhK9kN0QAcOE3ZqQR2dRz6NbhcvTyNfDxy0dFTRw-f-vxn04gjJB5ZEG3WfSzQv0VbqDYm6-NFYAzIxbDLoiCu34WAa2lckx5qxncXBhQj6Fro2gXGPXo4d32DvqQg7_RHQ-SF_WLqdxRCXF91NIqxYmFZsOJAuQ5m6TafzuNnQoJB3OQFoknv8Uy5O4FKuwazh1rvLrsj-1QEMi3sTrr9KxJkZy9EKXs92ndlb3edgfycLOffTil-gW2BvxeNiMQzqF1xJqFBKHDyatgwpXDX81HDwxkuMEaGPREIeQLuOlBJrL_20RD1e4Gu4tjQD8vRsb29UNG60DqpDvc-H4Z2oxeppm0KIwQNaCTtGUxxmvT807fXMnuVEf5QI5qTx9YRJh56GiWLoHC_zPMhoikMbAybIVWh9HtVgZGgImDmz0l9P4LgtpKNnKbQj_2ZKn2ZhOYKZLdt1P2Jq2Z2z76MtbRQTrpZpFb14zWVnh1LFCSFPAB7sqC1-u-KQOf2_SjEecztPccso8xZB2nkhLetyPn9aFuO-J_LCZydQeiroXx4Z8NxhDpbLoOpw2MbRCVB_TxfnLGNn1QD0To9TTChxK5AHNRRLDaj3xK1e0jd37uSmHTkT6QJVHFHEYMVLBcuV1MQcoy0wsvc1sRb",null],"logging":{"composer_session_id":"'+str(uuid.uuid4())+'"},"navigation_data":{"attribution_id_v2":"FeedsCometRoot.react,comet.most_recent_feed,tap_bookmark,1719641912186,189404,608920319153834,,"},"event_share_metadata":{"surface":"newsfeed"},"actor_id":"'+self.id+'","client_mutation_id":"3"},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometIsAdaptiveUFIEnabledrelayprovider":true,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__IncludeCommentWithAttachmentrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesRingrelayprovider":false,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":false}','server_timestamps': 'true','doc_id': '8167261726632010'}
            self.session.post("https://www.facebook.com/api/graphql/",headers=self.headers, data=data)
        except:
            pass

    def group(self, id: str):
        try:
            data = {'av':self.id,'fb_dtsg':self.fb_dtsg,'jazoest':self.jazoest,'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'GroupCometJoinForumMutation','variables':'{"feedType":"DISCUSSION","groupID":"'+id+'","imageMediaType":"image/x-auto","input":{"action_source":"GROUP_MALL","attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,via_cold_start,1673041528761,114928,2361831622,","group_id":"'+id+'","group_share_tracking_params":{"app_id":"2220391788200892","exp_id":"null","is_from_share":false},"actor_id":"'+self.id+'","client_mutation_id":"1"},"inviteShortLinkKey":null,"isChainingRecommendationUnit":false,"isEntityMenu":true,"scale":2,"source":"GROUP_MALL","renderLocation":"group_mall","__relay_internal__pv__GroupsCometEntityMenuEmbeddedrelayprovider":true,"__relay_internal__pv__GlobalPanelEnabledrelayprovider":false}','server_timestamps':'true','doc_id':'5853134681430324','fb_api_analytics_tags':'["qpl_active_flow_ids=431626709"]',}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except:
            pass

    def comment(self, id, msg:str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'useCometUFICreateCommentMutation','variables': fr'{{"feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"groupID":null,"input":{{"client_mutation_id":"4","actor_id":"{self.id}","attachments":null,"feedback_id":"{encode_to_base64(f"feedback:{id}")}","formatting_style":null,"message":{{"ranges":[],"text":"{msg}"}},"attribution_id_v2":"CometHomeRoot.react,comet.home,via_cold_start,1718688700413,194880,4748854339,,","vod_video_timestamp":null,"feedback_referrer":"/","is_tracking_encrypted":true,"tracking":["AZX1ZR3ETYfGknoE2E83CrSh9sg_1G8pbUK70jA-zjEIcfgLxA-C9xuQsGJ1l2Annds9fRCrLlpGUn0MG7aEbkcJS2ci6DaBTSLMtA78T9zR5Ys8RFc5kMcx42G_ikh8Fn-HLo3Qd-HI9oqVmVaqVzSasZBTgBDojRh-0Xs_FulJRLcrI_TQcp1nSSKzSdTqJjMN8GXcT8h0gTnYnUcDs7bsMAGbyuDJdelgAlQw33iNoeyqlsnBq7hDb7Xev6cASboFzU63nUxSs2gPkibXc5a9kXmjqZQuyqDYLfjG9eMcjwPo6U9i9LhNKoZwlyuQA7-8ej9sRmbiXBfLYXtoHp6IqQktunSF92SdR53K-3wQJ7PoBGLThsd_qqTlCYnRWEoVJeYZ9fyznzz4mT6uD2Mbyc8Vp_v_jbbPWk0liI0EIm3dZSk4g3ik_SVzKuOE3dS64yJegVOQXlX7dKMDDJc7P5Be6abulUVqLoSZ-cUCcb7UKGRa5MAvF65gz-XTkwXW5XuhaqwK5ILPhzwKwcj3h-Ndyc0URU_FJMzzxaJ9SDaOa9vL9dKUviP7S0nnig0sPLa5KQgx81BnxbiQsAbmAQMr2cxYoNOXFMmjB_v-amsNBV6KkES74gA7LI0bo56DPEA9smlngWdtnvOgaqlsaSLPcRsS0FKO3qHAYNRBwWvMJpJX8SppIR1KiqmVKgeQavEMM6XMElJc9PDxHNZDfJkKZaYTJT8_qFIuFJVqX6J9DFnqXXVaFH4Wclq8IKZ01mayFbAFbfJarH28k_qLIxS8hOgq9VKNW5LW7XuIaMZ1Z17XlqZ96HT9TtCAcze9kBS9kMJewNCl-WYFvPCTCnwzQZ-HRVOM04vrQOgSPud7vlA3OqD4YY2PSz_ioWSbk98vbJ4c7WVHiFYwQsgQFvMzwES20hKPDrREYks5fAPVrHLuDK1doffY1hPTWF2KkSt0uERAcZIibeD5058uKSonW1fPurOnsTpAg8TfALFu1QlkcNt1X4dOoGpYmBR7HGIONwQwv5-peC8F758ujTTWWowBqXzJlA2boriCvdZkvS15rEnUN57lyO8gINQ5heiMCQN8NbHMmrY_ihJD3bdM4s2TGnWH4HBC2hi0jaIOJ8AoCXHQMaMdrGE1st7Y3R_T6Obg6VnabLn8Q-zZfToKdkiyaR9zqsVB8VsMrAtEz0yiGpaOF3KdI2sxvii3Q5XWIYN6gyDXsXVykFS25PsjPmXCF8V1mS7x6e9N9PtNTWwT8IGBZp9frOTQN2O52dOhPdsuCHAf0srrBVHbyYfCMYbOqYEEXQG0pNAmG_wqbTxNew9kTsXDRzYKW-NmEJcvy_xh1dDwg8xJc58Cl71e-rau3iP7o8mWhVSaxi4Bi6LAuj4UKVCt3IYCfm9AR1d5LqBFWU9LrJbRZSMlmUYwZf7PlrKmpnCnZvuismiL7DH3cnUjP0lWAvhy3gxZm1MK8KyRzWmHnTNqaVlL37c2xoE4YSyponeOu5D-lRl_Dp_C2PyR1kG6G0TCWS66UbU89Fu1qmwWjeQwYhzj2Jly9LRyClAbe86VJhIZE18YLPB-n1ng78qz7hHtQ8qT4ejY4csEjSRjjnHdz8U-06qErY-CXNNsVtzpYGuzZ1ZaXqzAQkUcREm98KR8c1vaXaQXumtDklMVgs76gLqZyiG1eCRbOQ6_EcQv7GeFnq5UIqoMH_Xzc78otBTvC5j3aCs5Pvf6k3gQ5ZU7E4uFVhZA7xoyD8sPX6rhdGL8JmLKJSGZQM5ccWpfpDJ5RWJp0bIJdnAJQ8gsYMRAI2OBxx2m2c76lNiUnB750dMe2H3pFzFQVkWQLkmGVY37cgmRNHyXboDMQ1U2nlbNH017dmklJCk4jVU8aA9Gpo8oHw","{{\"assistant_caller\":\"comet_above_composer\",\"conversation_guide_session_id\":\"{uuid.uuid4()}\",\"conversation_guide_shown\":null}}"],"feedback_source":"DEDICATED_COMMENTING_SURFACE","idempotence_token":"client:{uuid.uuid4()}","session_id":"{uuid.uuid4()}"}},"inviteShortLinkKey":null,"renderLocation":null,"scale":1,"useDefaultActor":false,"focusCommentID":null}}','server_timestamps': 'true','doc_id': '7994085080671282',}
            self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data)
        except:
            pass
    
    def page_review(self, id, msg:str):
        try:
            data = {'av':self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'variables': '{"input":{"composer_entry_point":"inline_composer","composer_source_surface":"page_recommendation_tab","source":"WWW","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":"' +msg+ '"},"with_tags_ids":[],"text_format_preset_id":"0","page_recommendation":{"page_id":"'+id+'","rec_type":"POSITIVE"},"actor_id":"'+self.id+'","client_mutation_id":"1"},"feedLocation":"PAGE_SURFACE_RECOMMENDATIONS","feedbackSource":0,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"timeline","UFI2CommentsProvider_commentsKey":"ProfileCometReviewsTabRoute","hashtag":null,"canUserManageOffers":false}','doc_id': '5737011653023776'}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except:
            pass
    
    def sharend(self, id, msg:str):
        try:
            data = {
                'av':self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'variables': '{"input":{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","attachments":[{"link":{"share_scrape_data":"{\"share_type\":22,\"share_params\":['+id+']}"}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"is_tracking_encrypted":true,"tracking":["AZXEWGOa5BgU9Y4vr1ZzQbWSdaLzfI3EMNtpYwO1FzzHdeHKOCyc4dd677vkeHFmNfgBKbJ7vHSB96dnQh4fQ0-dZB3zHFN1qxxhg5F_1K8RShMHcVDNADUhhRzdkG2C6nujeGpnPkw0d1krhlgwq2xFc1lM0OLqo_qr2lW9Oci9BzC3ZkT3Jqt1m8-2vpAKwqUvoSfSrma8Y5zA1x9ZF0HLeHojOeodv_w5-S9hcdgy3gvF5o4lTdzfp3leby36PkwOyJqCOI51h6jp-cH0WUubXMbH2bVM-v9Mv7kHw9_yC8dP5b_tjerx7ggHtnhr1KtOEiolPmCkQiapP5dX9phUaW908T9Kh1aDk4sK7cd7QfVaGj6LSOiHS599VsgvvbHopOVxH80a96LkuhH4t0DLc8QjljGwAmublnMVuvUbVaiChuyjzAIQe-xj2C7yMGzxmOacqR7yaepDUI-fpRZAzkcfVUdumVzbjWtCYGZLJgw4lAKVv6Y37tBedtAGHF7P7EEdQSXOX6ADg0cEYUeusp9Oho1SAbz_rVGiJc-oSkWY6S2XwD5vBXwV9lfdg6vuH3DKDcIDDoua3xXN7sYbVOw3ClcTbxMAmQqE8ClYrlbIXNp-QCW2Rr_3ro3VgYqNo1UkRyDXgCHs8rWUNY6N-bhMWCHI9CPOEebbqXnSRayKmgxYrDOIuHIzyHujUBYLnEikCYIfVwaeEB4X-Et3ZZvgoHdaZAhSO3YNFLYjyimb1tR8A-Pm2KoKwIF6equnjWWLHKoovFhbhQLRmjYYBJUhP4n0yLunWLnPwn8e7ev9h4fsGMREmonEbizxwrsr1bqpDBrHWliiPTPHDdlJNVko7anmeT1txjmTaOrA8oejbs1hDeNEZoEuL2vkN7HdjiJFhLu2yTNw2Rc3WHHOb8FcFlwTOzCDUHGDbv_bV8iAlybhEZFE-3kmoMrw7kXPjwC8D_x4VRW1BQ1wVEsYFjBrLOjk05nsuuU0X5aD5DJi3zrL3bET2eGIIlbXdXvn57Q2JtCnnS0uRyaB2pHghXTkrT2l_1fPqTJIhJOi6YQDymf2paNIUd1Fe3fDZBp1D4VMsNphQr4mSIANKGHZP29cmWJox94ztH7mrLIhSRiSzs_DrTb5o5YH6AwBkg9XzNdlM7uMxAPB9lbqVAPWXEBANhoAHvYjQI1-61myVarQBrk36dbz15PASG1c5Fina9vATWju6Bfj7PjoqJ4rARcZBJOO011e2eLy4yekMuG8bD5TvEwuiRn_M23iuC-k_w77abKvcW4MJX1f4Gfv9S4C_8N4pSiWOPNRgHPJWEQ6vhhu3euzWVSKYJ5jmfeqA9jFd_U6qVkEXenI0ofFBXw-fzjoWoRHy5y8xBG9qg",null],"message":{"ranges":[],"text":"'+msg+'"},"logging":{"composer_session_id":"'+str(uuid.uuid4())+'"},"navigation_data":{"attribution_id_v2":"CometSinglePostDialogRoot.react,comet.post.single_dialog,via_cold_start,1743945123087,176702,,,"},"event_share_metadata":{"surface":"newsfeed"},"actor_id":"'+self.id+'","client_mutation_id":"1"},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":false,"__relay_internal__pv__CometIsReplyPagerDisabledrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__CometFeedStoryDynamicResolutionPhotoAttachmentRenderer_experimentWidthrelayprovider":500,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__CometFeedPYMKHScrollInitialPaginationCountrelayprovider":10,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":true}',
                'doc_id': '29449903277934341'
            }
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except: 
            pass

    def checkDissmiss(self):
        try:
            response = self.session.get('https://www.facebook.com/', headers=self.headers)
            if '601051028565049' in response.text: return 'Dissmiss'
            if '1501092823525282' in response.text: return 'Checkpoint282'
            if '828281030927956' in response.text: return 'Checkpoint956'
            if 'title="Log in to Facebook">' in response.text: return 'CookieOut'
            else: return 'Biblock'
        except: 
            pass
    
    def clickDissMiss(self):
        try:
            data = {"av": self.id,"fb_dtsg": self.fb_dtsg,"jazoest": self.jazoest,"fb_api_caller_class": "RelayModern","fb_api_req_friendly_name": "FBScrapingWarningMutation","variables": "{}","server_timestamps": "true","doc_id": "6339492849481770"}
            self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data)
        except: 
            pass

class TuongTacCheo(object):
    def __init__ (self, token):
        try:
            self.ss = requests.Session()
            session = self.ss.post('https://tuongtaccheo.com/logintoken.php',data={'access_token': token})
            self.cookie = session.headers['Set-cookie']
            self.session = session.json()
            self.headers = {
                'Host': 'tuongtaccheo.com',
                'accept': '*/*',
                'origin': 'https://tuongtaccheo.com',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                "cookie": self.cookie
            }
        except:
            pass

    def info(self):
        if self.session['status'] == 'success':
            return {'status': "success", 'user': self.session['data']['user'], 'xu': self.session['data']['sodu']}
        else:
            return {'error': 200}
        
    def cauhinh(self, id):
        response = self.ss.post('https://tuongtaccheo.com/cauhinh/datnick.php',headers=self.headers, data={'iddat[]': id, 'loai': 'fb', }).text
        if response == '1':
            return {'status': "success", 'id': id}
        else:
            return {'error': 200}
        
    def getjob(self, nv):
        response = self.ss.get(f'https://tuongtaccheo.com/kiemtien/{nv}/getpost.php',headers=self.headers)
        return response
    
    def nhanxu(self, id, nv):
        xu_truoc = self.ss.get('https://tuongtaccheo.com/home.php', headers=self.headers).text.split('"soduchinh">')[1].split('<')[0]
        response = self.ss.post(f'https://tuongtaccheo.com/kiemtien/{nv}/nhantien.php', headers=self.headers, data={'id': id}).json()
        xu_sau = self.ss.get('https://tuongtaccheo.com/home.php', headers=self.headers).text.split('"soduchinh">')[1].split('<')[0]
        if 'mess' in response and int(xu_sau) > int(xu_truoc):
            parts = response['mess'].split()
            msg = parts[-2]
            return {'status': "success", 'msg': '+'+msg+' Xu', 'xu': xu_sau} 
        else:
            return {'error': response}

def addcookie():
    i = 0
    while True:
        i += 1
        cookie = input(f'{thanh}{luc}Nhập Cookie Facebook Số{vang} {i}{trang}: {vang}')
        if cookie == '' and i != 1:
            break 
        fb = Facebook(cookie)
        info = fb.info()
        
        # LOGIC SỬA LỖI: 
        # 1. Kiểm tra 'info is not None' để tránh 'TypeError'.
        # 2. Nếu thành công, thêm cookie và tiếp tục.
        # 3. Nếu thất bại (info là None hoặc không có 'success'), báo lỗi và lùi i (-=1) để yêu cầu nhập lại.
        if info is not None and 'success' in info:
            name = info['name']
            print(f'{thanh}{luc}Tên: {vang}{name}')
            print(gradient_tutu("-"*50))
            listCookie.append(cookie)
        else:
            print(f'{do}Cookie Acc Facebook Die ! Vui Lòng Nhập Lại !!!')
            i -= 1 # Lùi bước đếm để lần lặp tiếp theo vẫn là số thứ tự cookie này.

os.system("cls" if os.name == "nt" else "clear")

if os.path.exists(f'tokenttcfb.json') == False:
    while True:
    #\033[38;2;160;231;229m dùng cho mấy cái chọn nhiệm vụ đẹp
# \033[38;2;120;240;255m    # 💙 Xanh sáng thiên thanh
# \033[38;2;255;170;200m    # 💗 Hồng pastel sáng
# \033[38;2;180;255;210m    # 💚 Xanh mint sáng
# \033[38;2;255;220;180m    # 🧡 Cam đào sáng
# \033[38;2;255;255;160m    # 🌟 Vàng sáng dịu
# \033[38;2;220;200;255m    # 💜 Tím sữa sáng
# \033[38;2;255;240;240m    # 🤍 Trắng hồng sữa
# \033[38;2;200;255;250m    # 🧊 Cyan kem sáng
# \033[38;2;240;240;255m    # 🌫 Xám khói sáng
# \033[38;2;230;210;255m    # 🌸 Hồng tím sáng
# \033[38;2;255;255;255m    # 🔆 Trắng sáng nhất (dùng cẩn thận!)

        token = input(f'{thanh}\033[38;2;0;255;0m Nhập Access_Token TTC{trang}:{vang} ')
        print('\033[1;36mĐang Xử Lý....','     ',end='\r')
        ttc = TuongTacCheo(token)
        checktoken = ttc.info()
        if checktoken.get('status') == 'success':
            users, xu = checktoken['user'], checktoken['xu']
            print(f"{luc}Đăng Nhập Thành Công")
            with open('tokenttcfb.json','w') as f:
                json.dump([token+'|'+users],f)
                break
        else:
            print(f'{do}Đăng Nhập Thất Bại')
else:
    token_json = json.loads(open('tokenttcfb.json','r').read())
    stt_token = 0
    for tokens in token_json:
        if len(tokens) > 5:
            stt_token += 1
            print(f'{thanh}{luc}Nhập {do}[{vang}{stt_token}{do}] {luc}Để Chạy Tài Khoản: {vang}{tokens.split('|')[1]}')
    print(gradient_tutu("-"*50))
    print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Chọn Acc Tương Tác Chéo Để Chạy Tool')
    print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Access_Token Tương Tác Chéo Mới')
    print(gradient_tutu("-"*50))
    while True:
        chon = input(f'{thanh}{luc}Nhập: {vang}')
        print(gradient_tutu("-"*50))
        if chon == '1':
            while True:
                try:
                    tokenttcfb = int(input(f'{thanh}{luc}Nhập Số Acc: {vang}'))
                    print(gradient_tutu("-"*50))
                    ttc = TuongTacCheo(token_json[tokenttcfb - 1].split("|")[0])
                    checktoken = ttc.info()
                    if checktoken.get('status') == 'success':
                        users, xu = checktoken['user'], checktoken['xu']
                        print(f"{luc}Đăng Nhập Thành Công")
                        break
                    else:
                        print(f'{do}Đăng Nhập Thất Bại')
                except:
                    print(f'{do}Số Acc Không Tồn Tại')
            break
        elif chon == '2':
            while True:
                token = input(f'{thanh}{luc}Nhập Access_Token TTC{trang}: {vang}')
                print('\033[1;32mĐang Xử Lý....','     ',end='\r')
                ttc = TuongTacCheo(token)
                checktoken = ttc.info()
                if checktoken.get('status') == 'success':
                    users, xu = checktoken['user'], checktoken['xu']
                    print(f"{luc}Đăng Nhập Thành Công")
                    token_json.append(token+'|'+users)
                    with open('tokenttcfb.json','w') as f:
                        json.dump(token_json,f)
                    break
                else:
                    print(f'{do}Đăng Nhập Thất Bại')
            break
        else:
            print(f'{do}Vui Long Nhập Chính Xác ')
os.system("cls" if os.name == "nt" else "clear")            

if os.path.exists(f'cookiefb-ttc.json') == False:
    addcookie()
    with open('cookiefb-ttc.json','w') as f:
        json.dump(listCookie, f)
else:
    print(f'{thanh}{luc}Acc TTC Đã Chọn{trang}: {vang}{users}')
    print(f'{thanh}{luc}Đang Có{trang}: {vang}{str(format(int(checktoken['xu']),","))}{luc} Xu')
    print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Sử Dụng Cookie Facebook Đã Lưu')
    print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Cookie Facebook Mới')
    print(gradient_tutu("-"*50))
    chon = input(f'{thanh}{luc}Nhập{trang}: {vang}')
    print(gradient_tutu("-"*50))
    while True:
        if chon == '1':
            print(f'{luc}Đang Lấy Dữ Liệu Đã Lưu ','          ',end='\r')
            sleep(1)
            listCookie = json.loads(open('cookiefb-ttc.json', 'r').read())
            break
        elif chon == '2':
            addcookie()
            with open('cookiefb-ttc.json','w') as f:
                json.dump(listCookie, f)
            break
        else:
            print(f'{do}Vui Lòng Nhập Đúng !!!')
os.system("cls" if os.name == "nt" else "clear")            

print(f'{thanh}{luc}Tên TTC{trang}: {vang}{users}')
print(f'{thanh}{luc}Đang Có{trang}: {vang}{str(format(int(checktoken['xu']),","))}{luc} Xu')
print(f'{thanh}{luc}Tổng Cookie Facebook{trang}: {vang}{len(listCookie)}')
print(gradient_tutu("-"*50))
print(f'{thanh}{dep}Nhập {do}[{vang}1{do}]{dep} Để Chạy Nhiệm Vụ Like Vip')
print(f'{thanh}{dep}Nhập {do}[{vang}2{do}]{dep} Để Chạy Nhiệm Vụ Like Thường')
print(f'{thanh}{dep}Nhập {do}[{vang}3{do}]{dep} Để Chạy Nhiệm Vụ Cảm Xúc Vip')
print(f'{thanh}{dep}Nhập {do}[{vang}4{do}]{dep} Để Chạy Nhiệm Vụ Cảm Xúc Thường')
print(f'{thanh}{dep}Nhập {do}[{vang}5{do}]{dep} Để Chạy Nhiệm Vụ Cảm Xúc Comment')
print(f'{thanh}{dep}Nhập {do}[{vang}6{do}]{dep} Để Chạy Nhiệm Vụ Comment')
print(f'{thanh}{dep}Nhập {do}[{vang}7{do}]{dep} Để Chạy Nhiệm Vụ Share')
print(f'{thanh}{dep}Nhập {do}[{vang}8{do}]{dep} Để Chạy Nhiệm Vụ Like Page')
print(f'{thanh}{dep}Nhập {do}[{vang}9{do}]{dep} Để Chạy Nhiệm Vụ Follow')
print(f'{thanh}{dep}Nhập {do}[{vang}0{do}]{dep} Để Chạy Nhiệm Vụ Group')
print(f'{thanh}{dep}Nhập {do}[{vang}q{do}]{dep} Để Chạy Nhiệm Vụ Review')
print(f'{thanh}{dep}Nhập {do}[{vang}s{do}]{dep} Để Chạy Nhiệm Vụ Share Nội Dung')
print(f'{thanh}{dep}Có Thể Chọn Nhiều Nhiệm Vụ {do}({vang}VD: 123...{do})')
print(gradient_tutu("-"*50))
nhiemvu = str(input(f'{thanh}{tim}Nhập Số Để Chọn Nhiệm Vụ{trang}: {vang}'))
for x in nhiemvu:
    list_nv.append(x)
list_nv = [x for x in list_nv if x in ['1','2','3','4','5','6','7','8','9','0', 'q', 's']]
while(True):
    try:
        delay = int(input(f'{thanh}{v}Nhập Delay Job{trang}: {vang}'))
        break
    except:
        print(f'{do}Vui Lòng Nhập Số')
while(True):
    try:
        JobbBlock = int(input(f'{thanh}{v}Sau Bao Nhiêu Nhiệm Vụ Chống Block{trang}: {vang}'))
        if JobbBlock <= 1:
            print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
        break
    except:
        print(f'{do}Vui Lòng Nhập Số')
while(True):
    try:
        DelayBlock = int(input(f'{thanh}{v}Sau {vang}{JobbBlock} {v}Nhiệm Vụ Nghỉ Bao Nhiêu Giây{trang}: {vang}'))
        break
    except:
        print(f'{do}Vui Lòng Nhập Số')
while(True):
    try:
        JobBreak = int(input(f'{thanh}{v}Sau Bao Nhiêu Nhiệm Vụ Chuyển Acc{trang}: {vang}'))
        if JobBreak <= 1:
            print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
        break
    except:
        print(f'{do}Vui Lòng Nhập Số')
runidfb = input(f'{thanh}{v}Bạn Có Muốn Ẩn Id Facebook Không? {do}({vang}y/n{do}){v}: {vang}')
print(gradient_tutu("-"*50))
stt = 0
totalxu = 0
xuthem = 0
while True:
    if len(listCookie) == 0:
        print(f'{do}Đã Xóa Tất Cả Cookie, Vui Lòng Nhập Lại !!!')
        addcookie()
        with open('cookiefb-ttc.json','w') as f:
            json.dump(listCookie, f)
    for cookie in listCookie:
        JobError, JobSuccess, JobFail = 0, 0, 0
        fb = Facebook(cookie)
        info = fb.info()
        if 'success' in info:
            namefb = info['name']
            idfb = str(info['id'])
            idrun = idfb[0]+idfb[1]+idfb[2]+"#"*(int(len(idfb)-3)) if runidfb.upper() =='Y' else idfb
        else:
            print(f'{do}Cookie Facebook Die ! Đã Xóa Ra Khỏi List !!!')
            listCookie.remove(cookie)
            break
        cauhinh = ttc.cauhinh(idfb)
        if cauhinh.get('status') == 'success':
            print(f'{luc}Id Facebook{trang}: {vang}{idrun}{do} | {luc}Tên{trang}: {vang}{namefb}')
        else:
            print(f'{luc}Chưa Cấu Hình Id Facebook{trang}: {vang}{idfb}{do} | {luc}Tên Tài Khoản{trang}: {vang}{namefb}')
            listCookie.remove(cookie)
            break
        list_nv_default = list_nv.copy()
        while True:
            random_nv = random.choice(list_nv)
            if random_nv == '1': fields = 'likepostvipcheo'
            if random_nv == '2': fields = 'likepostvipre'
            if random_nv == '3': fields = 'camxucvipcheo'
            if random_nv == '4': fields = 'camxuccheo'
            if random_nv == '5': fields = 'camxuccheobinhluan' 
            if random_nv == '6': fields = 'cmtcheo'
            if random_nv == '7': fields = 'sharecheo' 
            if random_nv == '8': fields = 'likepagecheo'
            if random_nv == '9': fields = 'subcheo'
            if random_nv == '0': fields = 'thamgianhomcheo'
            if random_nv == 'q': fields = 'danhgiapage'
            if random_nv == 's': fields = 'sharecheokemnoidung'
            chuyen = False
            try:
                getjob = ttc.getjob(fields)
                if "idpost" in getjob.text or "idfb" in getjob.text:
                    print(luc+f" Đã Tìm Thấy {len(getjob.json())} Nhiệm Vụ {fields.title()}       ",end = "\r")
                    for x in getjob.json():
                        nextDelay = False
                        if random_nv == "1": fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], "LIKE"); id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']; type = 'LIKE'; id = x['idpost']
                        if random_nv == "2": fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], "LIKE"); id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']; type = 'LIKE'; id = x['idpost']
                        if random_nv == "3": fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], x['loaicx']); id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']; type = x['loaicx']; id = x['idpost']
                        if random_nv == "4": fb.reaction(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], x['loaicx']); type = x['loaicx']; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        if random_nv == "5": fb.reactioncmt(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], x['loaicx']); type = x['loaicx']; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        if random_nv == "6": fb.comment(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], json.loads(x["nd"])[0]); type = 'COMMENT'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        if random_nv == "7": fb.share(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']); type = 'SHARE'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        if random_nv == "8": fb.likepage(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']); type = 'LIKEPAGE'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        if random_nv == "9": fb.follow(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']); type = 'FOLLOW'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        if random_nv == "0": fb.group(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']); type = 'GROUP'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        if random_nv == 'q': fb.page_review(x['UID'].split('_')[1] if '_' in x['UID'] else x['UID'], json.loads(x["nd"])[0]); type = 'REVIEW'; id = x['UID']; id_ = x['UID'].split('_')[1] if '_' in x['UID'] else x['UID']
                        if random_nv == "s": fb.sharend(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], json.loads(x["nd"])[0]); type = 'SHAREND'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                        nhanxu = ttc.nhanxu(id, fields)
                        if nhanxu.get('status') == 'success':
                            nextDelay, msg, xu, JobFail, timejob = True, nhanxu['msg'], nhanxu['xu'], 0, datetime.now().strftime('%H:%M:%S')
                            xutotal = msg.replace(' Xu','')
                            totalxu += int(xutotal)
                            stt+=1
                            JobSuccess += 1
                            
                            print(f'{do}[{xanh}{stt}{do}] | {dep}{timejob}{do} | {vang}{type.upper()}{do} | {trang}{id_}{do} | {vang}{msg}{do} | {luc}{str(format(int(xu),","))}{do}')
                            if stt % 10 == 0:
                                print(gradient_2(f' Tổng Cookie Facebook: {len(listCookie)} | Tổng Nhận: {str(format(int(totalxu),","))} Xu | Tổng Xu Hiện Có : {str(format(int(xu),","))}'))
                        else:
                            JobFail += 1
                            print(f'{do}[{JobFail}] {do}| ERROR {trang}JOB {type.upper()} {do}| {trang}{id_}','            ',end="\r")
                        
                        if JobFail >= 15:
                            check = fb.info()
                            if 'spam' in check:
                                print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Spam')
                                fb.clickDissMiss()
                            elif '282' in check:
                                print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Checkpoint282')
                                listCookie.remove(cookie)
                                chuyen = True
                                break
                            elif '956' in check:
                                print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Checkpoint956')
                                listCookie.remove(cookie)
                                chuyen = True
                                break
                            elif 'cookieout' in check:
                                print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Out Cookie, Đã Xoá Khỏi List')
                                listCookie.remove(cookie)
                                chuyen = True
                                break
                            else:
                                print(do+f'Tài Khoản {vang}{namefb} {do}Đã Bị Block {fields.upper()}                 ')
                                JobFail = 0
                                if nhiemvu in list_nv:
                                    list_nv.remove(nhiemvu)
                                if list_nv:
                                    nhiemvu = random.choice(list_nv)
                                else:
                                    print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Block Tất Cả Tương Tác                  ')
                                    listCookie.remove(cookie)
                                    chuyen = True
                                    list_nv = list_nv_default.copy()
                                break

                        if JobSuccess != 0 and JobSuccess % int(JobBreak) == 0:
                            chuyen = True
                            break

                        if nextDelay == True:
                            if stt % int(JobbBlock)==0:
                                Delay(DelayBlock)
                            else:
                                Delay(delay)

                    if chuyen == True:
                        break
                else:
                    if 'error' in getjob.text:
                        if getjob.json()['countdown']:
                            print(f'{do}Tiến Hành Get Job {fields.upper()}, COUNTDOWN: {vang}{str(round(getjob.json()["countdown"], 3))}{do}'   ,end="\r")
                            sleep(1)
                            Delay(getjob.json()['countdown'])
                        else:
                            print(do+getjob.json()['error']+'          ',end="\r")
                            sleep(1)
                            Delay(getjob.json()['countdown'])
            except:
                pass
