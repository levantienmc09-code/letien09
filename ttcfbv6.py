import json
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper
import socket
import subprocess
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import subprocess
import psutil
import re
import base64
import uuid
import random
import threading
from threading import Thread, Lock

# ==================== HỆ THỐNG MÀU SẮC ====================
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    @staticmethod
    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
    
    PRIMARY = rgb.__func__(147, 112, 219)
    PRIMARY_LIGHT = rgb.__func__(186, 85, 211)
    PRIMARY_DARK = rgb.__func__(106, 90, 205)
    
    SECONDARY = rgb.__func__(64, 224, 208)
    SECONDARY_LIGHT = rgb.__func__(127, 255, 212)
    
    SUCCESS = rgb.__func__(46, 204, 113)
    WARNING = rgb.__func__(241, 196, 15)
    ERROR = rgb.__func__(231, 76, 60)
    INFO = rgb.__func__(52, 152, 219)
    
    TEXT_WHITE = rgb.__func__(255, 255, 255)
    TEXT_LIGHT = rgb.__func__(236, 240, 241)
    TEXT_GRAY = rgb.__func__(189, 195, 199)
    TEXT_DARK = rgb.__func__(149, 165, 166)

# ==================== HỆ THỐNG HIỂN THỊ ====================
class PremiumDisplay:
    def __init__(self):
        self.width = 80
        self.lock = Lock()
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
        self.stats = {
            'total_jobs': 0,
            'success_jobs': 0,
            'failed_jobs': 0,
            'total_xu': 0,
            'start_time': None
        }
        
    def clear(self):
        os.system('clear')
    
    def get_spinner(self):
        frame = self.spinner_frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.spinner_frames)
        return f"{Colors.SECONDARY}{frame}{Colors.RESET}"
    
    def print_gradient_text(self, text, start_color, end_color):
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            t = i / (length - 1) if length > 1 else 0
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
            result += Colors.rgb(r, g, b) + char
        return result + Colors.RESET
    
    def print_header(self, title, subtitle=None):
        self.clear()
        print()
        
        border_top = self.print_gradient_text("╔═══════════════════════════════════════════════════════════════════════════════╗", (147, 112, 219), (186, 85, 211))
        print(border_top)
        
        title_text = f"║ {title} "
        title_padding = 78 - len(title_text) + 2
        title_display = Colors.PRIMARY + Colors.BOLD + title_text + " " * title_padding + "║"
        print(title_display + Colors.RESET)
        
        if subtitle:
            subtitle_text = f"║ {subtitle} "
            subtitle_padding = 78 - len(subtitle_text) + 2
            subtitle_display = Colors.PRIMARY_LIGHT + subtitle_text + " " * subtitle_padding + "║"
            print(subtitle_display + Colors.RESET)
        
        border_bottom = self.print_gradient_text("╚═══════════════════════════════════════════════════════════════════════════════╝", (186, 85, 211), (106, 90, 205))
        print(border_bottom)
        print()
    
    def print_card(self, title, content_lines, color=Colors.PRIMARY):
        print(f"  {Colors.TEXT_DARK}┌─────────────────────────────────────────────────────────────┐{Colors.RESET}")
        
        title_display = f"{color}{Colors.BOLD}{title}{Colors.RESET}"
        title_text = f"  {Colors.TEXT_DARK}│{title_display}{' ' * (54 - len(title))}{Colors.TEXT_DARK}        │{Colors.RESET}"
        print(title_text)
        
        print(f"  {Colors.TEXT_DARK}├─────────────────────────────────────────────────────────────┤{Colors.RESET}")
        
        for line in content_lines:
            line_text = f"  {Colors.TEXT_DARK}│{Colors.TEXT_LIGHT}{line:<98}{Colors.TEXT_DARK} │{Colors.RESET}"
            print(line_text)
        
        print(f"  {Colors.TEXT_DARK}└─────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print()

    def print_status(self, message, level="info"):
        icons = {
            "success": f"{Colors.SUCCESS}✓",
            "error": f"{Colors.ERROR}✗",
            "warning": f"{Colors.WARNING}⚠",
            "info": f"{Colors.INFO}ℹ",
            "loading": f"{Colors.SECONDARY}⟳"
        }
        
        icon = icons.get(level, icons["info"])
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        with self.lock:
            print(f"{Colors.TEXT_DARK}[{timestamp}]{Colors.RESET} {icon} {message}{Colors.RESET}")

    def print_job_error(self, stt, timejob, job_type, id_):
        error_text = (
            f"{Colors.TEXT_DARK}[{Colors.ERROR}{stt}{Colors.TEXT_DARK}] "
            f"{Colors.TEXT_GRAY}{timejob} "
            f"{Colors.ERROR}{job_type.upper():<12} "
            f"{Colors.TEXT_LIGHT}{id_:<15} "
            f"{Colors.ERROR}   ERROR{Colors.RESET}"
        )
        print(f"{error_text}                    ",end="\r")

    def print_job_result(self, stt, timejob, job_type, id_, msg, xu):
        job_display = f"{Colors.TEXT_DARK}[{Colors.PRIMARY}{stt}{Colors.TEXT_DARK}] {Colors.TEXT_GRAY}{timejob} {Colors.WARNING}{job_type.upper():<12} {Colors.TEXT_LIGHT}{id_:<15} {Colors.SUCCESS}{msg:<10} {Colors.INFO}{str(format(int(xu),','))} Xu{Colors.RESET}"
        print(f"\r{job_display}")
    
    def print_stats_summary(self, total_cookies, total_xu, current_xu):
        stats_text = self.print_gradient_text(
            f" 📊 Tổng Cookie: {total_cookies} | 💰 Tổng Nhận: {str(format(int(total_xu),','))} Xu | 🏦 Hiện Có: {str(format(int(current_xu),','))} Xu",
            (255, 160, 120), (255, 255, 100)
        )
        print(f"{stats_text}")
    
    def print_progress_bar(self, current, total, prefix="", length=30):
        percent = current / total
        filled = int(length * percent)
        bar = "█" * filled + "░" * (length - filled)
        
        if percent < 0.3:
            color = Colors.ERROR
        elif percent < 0.7:
            color = Colors.WARNING
        else:
            color = Colors.SUCCESS
            
        print(f"\r{prefix} {color}{bar}{Colors.RESET} {int(percent*100)}%", end="", flush=True)

# ==================== HỆ THỐNG DELAY ====================
def Delay(value, display=None):
    start_time = time.time()
    total_delay = value 
    BAR_LENGTH = 20

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = total_delay - elapsed_time
        if remaining_time <= 0:
            print('\r' + ' ' * 80 + '\r', end='', flush=True)
            print(f'   Đang tiếp tục làm job...',end='\r')
            break
        
        ratio = elapsed_time / total_delay
        fill_count = int(ratio * BAR_LENGTH)
        progress_bar = "█" * fill_count + "░" * (BAR_LENGTH - fill_count)
        
        progress_text = f" ⏳ Delay: {remaining_time:.1f}s [{progress_bar}]" 
        print(f'\r{Colors.INFO}{progress_text}{Colors.RESET}','                    ', end='\r', flush=True)
        
        sleep(0.1)

# ==================== CÁC CLASS CHỨC NĂNG ====================
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

# ==================== HỆ THỐNG QUẢN LÝ CONFIG ====================
class ConfigManager:
    def __init__(self):
        self.config_file = 'configjob.json'
        self.default_config = {
            'selected_jobs': [],
            'delay': 5,
            'jobb_block': 10,
            'delay_block': 30,
            'job_break': 20,
            'hide_id': True,
            'all_jobs_selected': False
        }
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for key, value in self.default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except:
                pass
        return self.default_config.copy()
    
    def save_config(self, config):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def save_jobs(self, jobs_list, all_selected=False):
        config = self.load_config()
        config['selected_jobs'] = jobs_list
        config['all_jobs_selected'] = all_selected
        return self.save_config(config)
    
    def load_jobs(self):
        config = self.load_config()
        return config.get('selected_jobs', []), config.get('all_jobs_selected', False)

# ==================== GIAO DIỆN CHÍNH ====================
class TTCFBPremium:
    def __init__(self):
        self.display = PremiumDisplay()
        self.config_manager = ConfigManager()
        self.listCookie = []
        self.list_nv, self.all_jobs_selected = self.config_manager.load_jobs()
        self.ttc = None
        self.is_running = False
        self.stats = {
            'total_jobs': 0,
            'success_jobs': 0,
            'failed_jobs': 0,
            'total_xu': 0,
            'start_time': None
        }
    
    def run(self):
        self.display.clear()
        self.display.print_header("TTCFB PREMIUM EDITION", "Hệ Thống Tương Tác Chéo Facebook Đẳng Cấp")
        self.load_data()
        self.main_menu()
    
    def load_data(self):
        if os.path.exists('tokenttcfb.json'):
            try:
                with open('tokenttcfb.json', 'r') as f:
                    token_data = json.load(f)
                    if token_data:
                        token = token_data[0].split('|')[0]
                        self.ttc = TuongTacCheo(token)
                        info = self.ttc.info()
                        if info.get('status') == 'success':
                            self.display.print_status(f"Đã tải tài khoản TTC: {info['user']}", "success")
            except:
                pass
        
        self.load_cookies_from_folder()
    
    def load_cookies_from_folder(self):
        cookie_folder = 'Cookie'
        if not os.path.exists(cookie_folder):
            os.makedirs(cookie_folder)
            return
        
        cookie_files = [f for f in os.listdir(cookie_folder) if f.endswith('_cookie.json')]
        
        for cookie_file in cookie_files:
            try:
                with open(os.path.join(cookie_folder, cookie_file), 'r') as f:
                    cookie_data = json.load(f)
                    if isinstance(cookie_data, list) and cookie_data:
                        self.listCookie.extend(cookie_data)
            except:
                continue
        
        if self.listCookie:
            self.display.print_status(f"Đã tải {len(self.listCookie)} cookie từ {len(cookie_files)} file", "success")
        
        if self.all_jobs_selected:
            self.display.print_status("Đã tải: ALL JOB từ config", "success")
        elif self.list_nv:
            self.display.print_status(f"Đã tải {len(self.list_nv)} job từ config", "success")
    
    def main_menu(self):
        while True:
            self.display.clear()
            self.display.print_header("TTCFB PREMIUM - MENU CHÍNH")
            
            account_info = []
            if self.ttc:
                info = self.ttc.info()
                if info.get('status') == 'success':
                    account_info.append(f"📌 Tài khoản TTC: {Colors.SUCCESS}{info['user']}{Colors.TEXT_LIGHT}")
                    account_info.append(f"📍 Số dư hiện tại: {Colors.WARNING}{info['xu']} Xu{Colors.TEXT_LIGHT}")
                else:
                    account_info.append(f"❌ {Colors.ERROR}Chưa đăng nhập TTC{Colors.TEXT_LIGHT}")
            else:
                account_info.append(f"❌ {Colors.ERROR}Chưa đăng nhập TTC{Colors.TEXT_LIGHT}")
            
            account_info.append(f"📎 Cookie Facebook: {Colors.INFO}{len(self.listCookie)} tài khoản{Colors.TEXT_LIGHT}")
            
            if self.all_jobs_selected:
                account_info.append(f"📎 Nhiệm vụ đã chọn: {Colors.PRIMARY}ALL JOB{Colors.TEXT_LIGHT}")
                account_info.append(f"📎 Job: {Colors.SUCCESS}Tất cả job{Colors.TEXT_LIGHT}")
            elif self.list_nv:
                account_info.append(f"📎 Nhiệm vụ đã chọn: {Colors.PRIMARY}{len(self.list_nv)} loại{Colors.TEXT_LIGHT}")
                job_names = []
                task_descriptions = self.get_task_descriptions()
                for job in self.list_nv[:3]:
                    if job in task_descriptions:
                        job_names.append(task_descriptions[job])
                if len(self.list_nv) > 3:
                    job_names.append(f"... và {len(self.list_nv) - 3} job khác")
                account_info.append(f"📎 Job: {', '.join(job_names)}")
            else:
                account_info.append(f"📎 Nhiệm vụ đã chọn: {Colors.ERROR}Chưa chọn job nào{Colors.TEXT_LIGHT}")
            
            self.display.print_card("📊 THÔNG TIN HỆ THỐNG", account_info)
            
            menu_options = [
                f"{Colors.PRIMARY}1.{Colors.TEXT_LIGHT} Quản lý tài khoản TTC",
                f"{Colors.PRIMARY}2.{Colors.TEXT_LIGHT} Quản lý cookie Facebook", 
                f"{Colors.PRIMARY}3.{Colors.TEXT_LIGHT} Quản lý nhiệm vụ",
                f"{Colors.PRIMARY}4.{Colors.TEXT_LIGHT} Bắt đầu tương tác",
                f"{Colors.PRIMARY}5.{Colors.TEXT_LIGHT} Thống kê chi tiết",
                f"{Colors.ERROR}0.{Colors.TEXT_LIGHT} Thoát chương trình"
            ]
            
            self.display.print_card("🎛️ LỰA CHỌN", menu_options)
            
            choice = input(f"\n{Colors.SECONDARY}↳ Nhập lựa chọn: {Colors.RESET}").strip()
            
            if choice == "1":
                self.manage_ttc()
            elif choice == "2":
                self.manage_cookies()
            elif choice == "3":
                self.manage_tasks()
            elif choice == "4":
                self.start_interaction()
            elif choice == "5":
                self.show_stats()
            elif choice == "0":
                self.display.print_status("Cảm ơn bạn đã sử dụng TTCFB Premium!", "success")
                break
            else:
                self.display.print_status("Lựa chọn không hợp lệ!", "error")
                sleep(1)
    
    def get_task_descriptions(self):
        return {
            "1": "Like VIP",
            "2": "Like Thường", 
            "3": "Cảm Xúc VIP",
            "4": "Cảm Xúc Thường",
            "5": "Cảm Xúc Comment",
            "6": "Comment",
            "7": "Share",
            "8": "Like Page", 
            "9": "Follow",
            "0": "Group",
            "q": "Review",
            "s": "Share Nội Dung"
        }
    
    def manage_ttc(self):
        while True:
            self.display.clear()
            self.display.print_header("QUẢN LÝ TÀI KHOẢN TTC")
            
            status_info = []
            if self.ttc:
                info = self.ttc.info()
                if info.get('status') == 'success':
                    status_info.append(f"✅ {Colors.SUCCESS}Đã đăng nhập{Colors.TEXT_LIGHT}")
                    status_info.append(f"👤 Tài khoản: {Colors.INFO}{info['user']}{Colors.TEXT_LIGHT}")
                    status_info.append(f"💰 Số dư: {Colors.WARNING}{info['xu']} Xu{Colors.TEXT_LIGHT}")
                else:
                    status_info.append(f"❌ {Colors.ERROR}Token không hợp lệ{Colors.TEXT_LIGHT}")
            else:
                status_info.append(f"❌ {Colors.ERROR}Chưa đăng nhập{Colors.TEXT_LIGHT}")
            
            self.display.print_card("📊 TRẠNG THÁI", status_info)
            
            saved_accounts = self.get_saved_ttc_accounts()
            if saved_accounts:
                accounts_info = ["📁 Tài khoản đã lưu:"]
                for i, acc in enumerate(saved_accounts, 1):
                    accounts_info.append(f"  {i}. {acc['user']} - {acc['xu']} Xu")
                self.display.print_card("💾 TÀI KHOẢN ĐÃ LƯU", accounts_info)
            
            options = [
                f"{Colors.PRIMARY}1.{Colors.TEXT_LIGHT} Thêm token TTC mới",
                f"{Colors.PRIMARY}2.{Colors.TEXT_LIGHT} Chọn tài khoản đã lưu",
                f"{Colors.WARNING}3.{Colors.TEXT_LIGHT} Xóa token hiện tại",
                f"{Colors.TEXT_GRAY}0.{Colors.TEXT_LIGHT} Quay lại"
            ]
            self.display.print_card("🎛️ TÙY CHỌN", options)
            
            choice = input(f"\n{Colors.SECONDARY}↳ Lựa chọn: {Colors.RESET}").strip()
            
            if choice == "1":
                self.add_ttc_token()
            elif choice == "2":
                self.select_saved_ttc_account()
            elif choice == "3":
                self.remove_ttc_token()
            elif choice == "0":
                break
            else:
                self.display.print_status("Lựa chọn không hợp lệ!", "error")
                sleep(1)
    
    def get_saved_ttc_accounts(self):
        saved_accounts = []
        if os.path.exists('tokenttcfb.json'):
            try:
                with open('tokenttcfb.json', 'r') as f:
                    token_data = json.load(f)
                    for token_info in token_data:
                        if '|' in token_info:
                            token, user = token_info.split('|', 1)
                            ttc = TuongTacCheo(token)
                            info = ttc.info()
                            if info.get('status') == 'success':
                                saved_accounts.append({
                                    'token': token,
                                    'user': user,
                                    'xu': info['xu']
                                })
            except:
                pass
        return saved_accounts
    
    def select_saved_ttc_account(self):
        saved_accounts = self.get_saved_ttc_accounts()
        if not saved_accounts:
            self.display.print_status("❌ Không có tài khoản nào đã lưu!", "warning")
            sleep(2)
            return
        
        self.display.clear()
        self.display.print_header("CHỌN TÀI KHOẢN TTC")
        
        accounts_list = []
        for i, acc in enumerate(saved_accounts, 1):
            accounts_list.append(f"{Colors.PRIMARY}{i}.{Colors.TEXT_LIGHT} {acc['user']} - {Colors.WARNING}{acc['xu']} Xu{Colors.TEXT_LIGHT}")
        
        self.display.print_card("💾 TÀI KHOẢN ĐÃ LƯU", accounts_list)
        
        try:
            choice = int(input(f"\n{Colors.SECONDARY}↳ Chọn tài khoản (1-{len(saved_accounts)}): {Colors.RESET}").strip())
            if 1 <= choice <= len(saved_accounts):
                selected_acc = saved_accounts[choice-1]
                self.ttc = TuongTacCheo(selected_acc['token'])
                self.display.print_status(f"✅ Đã chọn tài khoản: {selected_acc['user']}", "success")
            else:
                self.display.print_status("❌ Lựa chọn không hợp lệ!", "error")
        except ValueError:
            self.display.print_status("❌ Vui lòng nhập số!", "error")
        
        sleep(2)
    
    def add_ttc_token(self):
        print(f"\n{Colors.INFO}💡 Nhập token TTC của bạn:{Colors.RESET}")
        token = input(f"{Colors.SECONDARY}↳ Token: {Colors.RESET}").strip()
        
        if token:
            try:
                test_ttc = TuongTacCheo(token)
                info = test_ttc.info()
                
                if info.get('status') == 'success':
                    user = info['user']
                    xu = info['xu']
                    
                    token_info = f"{token}|{user}"
                    
                    saved_tokens = []
                    if os.path.exists('tokenttcfb.json'):
                        with open('tokenttcfb.json', 'r') as f:
                            saved_tokens = json.load(f)
                    
                    token_exists = False
                    for i, saved_token in enumerate(saved_tokens):
                        if saved_token.startswith(token + '|'):
                            saved_tokens[i] = token_info
                            token_exists = True
                            break
                    
                    if not token_exists:
                        saved_tokens.append(token_info)
                    
                    with open('tokenttcfb.json', 'w') as f:
                        json.dump(saved_tokens, f)
                    
                    self.ttc = test_ttc
                    self.display.print_status(f"✅ Đã đăng nhập thành công: {user} ({xu} Xu)", "success")
                else:
                    self.display.print_status("❌ Token không hợp lệ!", "error")
            except Exception as e:
                self.display.print_status(f"❌ Lỗi: {str(e)}", "error")
        else:
            self.display.print_status("❌ Token không được để trống!", "error")
        
        sleep(2)
    
    def remove_ttc_token(self):
        if self.ttc:
            confirm = input(f"\n{Colors.WARNING}⚠ Bạn có chắc muốn xóa token? (y/n): {Colors.RESET}").strip().lower()
            if confirm == 'y':
                try:
                    if os.path.exists('tokenttcfb.json'):
                        with open('tokenttcfb.json', 'r') as f:
                            saved_tokens = json.load(f)
                        
                        current_user = self.ttc.info().get('user', '')
                        saved_tokens = [token for token in saved_tokens if not token.endswith(f"|{current_user}")]
                        
                        with open('tokenttcfb.json', 'w') as f:
                            json.dump(saved_tokens, f)
                        
                        self.ttc = None
                        self.display.print_status("✅ Đã xóa token!", "success")
                    else:
                        self.ttc = None
                        self.display.print_status("✅ Đã xóa token!", "success")
                except Exception as e:
                    self.display.print_status(f"❌ Lỗi xóa token: {str(e)}", "error")
            else:
                self.display.print_status("❌ Hủy xóa token!", "info")
        else:
            self.display.print_status("❌ Không có token để xóa!", "warning")
        
        sleep(2)
    
    def manage_cookies(self):
        while True:
            self.display.clear()
            self.display.print_header("QUẢN LÝ COOKIE FACEBOOK")
            
            cookie_info = []
            if self.listCookie:
                cookie_info.append(f"✅ {Colors.SUCCESS}Đã có {len(self.listCookie)} cookie{Colors.TEXT_LIGHT}")
                for i, cookie in enumerate(self.listCookie[:3]):
                    try:
                        fb = Facebook(cookie)
                        info = fb.info()
                        if info and 'success' in info:
                            status = f"{Colors.SUCCESS}✓ Live{Colors.TEXT_LIGHT}"
                            name = info['name']
                        else:
                            status = f"{Colors.ERROR}✗ Die{Colors.TEXT_LIGHT}"
                            name = "Unknown"
                        cookie_info.append(f"👤 {Colors.INFO}{name}{Colors.TEXT_LIGHT} - {status}")
                    except:
                        cookie_info.append(f"❌ {Colors.ERROR}Cookie không hợp lệ{Colors.TEXT_LIGHT}")
                if len(self.listCookie) > 3:
                    cookie_info.append(f"📋 ... và {len(self.listCookie) - 3} cookie khác")
            else:
                cookie_info.append(f"❌ {Colors.ERROR}Chưa có cookie nào{Colors.TEXT_LIGHT}")
            
            self.display.print_card("🍪 COOKIE HIỆN TẠI", cookie_info)
            
            options = [
                f"{Colors.PRIMARY}1.{Colors.TEXT_LIGHT} Thêm cookie mới (nhiều cookie)",
                f"{Colors.WARNING}2.{Colors.TEXT_LIGHT} Xóa tất cả cookie", 
                f"{Colors.ERROR}3.{Colors.TEXT_LIGHT} Kiểm tra cookie",
                f"{Colors.TEXT_GRAY}0.{Colors.TEXT_LIGHT} Quay lại"
            ]
            self.display.print_card("⚙️ QUẢN LÝ", options)
            
            choice = input(f"\n{Colors.SECONDARY}↳ Lựa chọn: {Colors.RESET}").strip()
            
            if choice == "1":
                self.add_multiple_cookies()
            elif choice == "2":
                self.clear_cookies()
            elif choice == "3":
                self.check_cookies()
            elif choice == "0":
                break
            else:
                self.display.print_status("Lựa chọn không hợp lệ!", "error")
                sleep(1)
    
    def add_multiple_cookies(self):
        print(f"\n{Colors.INFO}💡 Nhập nhiều cookie Facebook (mỗi cookie 1 dòng, để trống dòng để kết thúc):{Colors.RESET}")
        cookies = []
        i = 1
        
        while True:
            cookie = input(f"{Colors.SECONDARY}↳ Cookie {i}: {Colors.RESET}").strip()
            if not cookie:
                break
            cookies.append(cookie)
            i += 1
        
        if not cookies:
            self.display.print_status("❌ Không có cookie nào được nhập!", "error")
            sleep(2)
            return
        
        self.display.print_status(f"🔍 Đang kiểm tra {len(cookies)} cookie...", "loading")
        
        valid_cookies = []
        ttc_user = self.ttc.info().get('user', 'Unknown') if self.ttc else 'Unknown'
        
        for cookie in cookies:
            try:
                fb = Facebook(cookie)
                info = fb.info()
                
                if 'success' in info:
                    fb_name = info['name']
                    valid_cookies.append(cookie)
                    
                    file_name = f"{ttc_user}_{fb_name}_cookie.json"
                    cookie_folder = 'Cookie'
                    
                    if not os.path.exists(cookie_folder):
                        os.makedirs(cookie_folder)
                    
                    file_path = os.path.join(cookie_folder, file_name)
                    
                    with open(file_path, 'w') as f:
                        json.dump([cookie], f)
                    
                    self.display.print_status(f"✅ Đã thêm: {fb_name} -> {file_name}", "success")
                else:
                    self.display.print_status(f"❌ Cookie không hợp lệ: {cookie[:50]}...", "error")
            except Exception as e:
                self.display.print_status(f"❌ Lỗi kiểm tra cookie: {str(e)}", "error")
            
            sleep(0.5)
        
        self.listCookie.extend(valid_cookies)
        
        if valid_cookies:
            self.display.print_status(f"✅ Đã thêm {len(valid_cookies)} cookie hợp lệ!", "success")
        else:
            self.display.print_status("❌ Không có cookie nào hợp lệ!", "error")
        
        sleep(2)
    
    def clear_cookies(self):
        if self.listCookie:
            confirm = input(f"\n{Colors.WARNING}⚠ Bạn có chắc muốn xóa TẤT CẢ cookie? (y/n): {Colors.RESET}").strip().lower()
            if confirm == 'y':
                try:
                    cookie_folder = 'Cookie'
                    if os.path.exists(cookie_folder):
                        import shutil
                        shutil.rmtree(cookie_folder)
                        os.makedirs(cookie_folder)
                    
                    self.listCookie = []
                    self.display.print_status("✅ Đã xóa tất cả cookie!", "success")
                except Exception as e:
                    self.display.print_status(f"❌ Lỗi xóa cookie: {str(e)}", "error")
            else:
                self.display.print_status("❌ Hủy xóa cookie!", "info")
        else:
            self.display.print_status("❌ Không có cookie để xóa!", "warning")
        
        sleep(2)
    
    def check_cookies(self):
        if not self.listCookie:
            self.display.print_status("❌ Không có cookie để kiểm tra!", "warning")
            sleep(2)
            return
        
        self.display.clear()
        self.display.print_header("KIỂM TRA COOKIE FACEBOOK")
        
        live_cookies = []
        dead_cookies = []
        
        self.display.print_status("🔍 Đang kiểm tra cookie...", "loading")
        
        for i, cookie in enumerate(self.listCookie):
            try:
                fb = Facebook(cookie)
                info = fb.info()
                
                if 'success' in info:
                    live_cookies.append({
                        'cookie': cookie,
                        'name': info['name'],
                        'id': info['id']
                    })
                    self.display.print_status(f"✅ Cookie {i+1}: {info['name']} - LIVE", "success")
                else:
                    dead_cookies.append(cookie)
                    self.display.print_status(f"❌ Cookie {i+1}: DIE", "error")
            except:
                dead_cookies.append(cookie)
                self.display.print_status(f"❌ Cookie {i+1}: DIE", "error")
            
            sleep(0.5)
        
        result_info = [
            f"✅ Sống: {Colors.SUCCESS}{len(live_cookies)}{Colors.TEXT_LIGHT}",
            f"❌ Chết: {Colors.ERROR}{len(dead_cookies)}{Colors.TEXT_LIGHT}",
            f"📊 Tổng: {Colors.INFO}{len(self.listCookie)}{Colors.TEXT_LIGHT}"
        ]
        
        self.display.print_card("📊 KẾT QUẢ KIỂM TRA", result_info)
        
        if dead_cookies:
            confirm = input(f"\n{Colors.WARNING}⚠ Có {len(dead_cookies)} cookie chết. Xóa chúng? (y/n): {Colors.RESET}").strip().lower()
            if confirm == 'y':
                self.listCookie = [cookie for cookie in self.listCookie if cookie not in dead_cookies]
                
                cookie_folder = 'Cookie'
                for cookie_file in os.listdir(cookie_folder):
                    if cookie_file.endswith('_cookie.json'):
                        try:
                            file_path = os.path.join(cookie_folder, cookie_file)
                            with open(file_path, 'r') as f:
                                cookie_data = json.load(f)
                            
                            updated_cookies = [c for c in cookie_data if c not in dead_cookies]
                            
                            if updated_cookies:
                                with open(file_path, 'w') as f:
                                    json.dump(updated_cookies, f)
                            else:
                                os.remove(file_path)
                        except:
                            continue
                
                self.display.print_status(f"✅ Đã xóa {len(dead_cookies)} cookie chết!", "success")
        
        input(f"\n{Colors.TEXT_GRAY}Nhấn Enter để tiếp tục...{Colors.RESET}")

    def manage_tasks(self):
        while True:
            self.display.clear()
            self.display.print_header("QUẢN LÝ NHIỆM VỤ")
            
            selected_info = []
            task_descriptions = self.get_task_descriptions()
            
            if self.all_jobs_selected:
                selected_info.append(f"{Colors.SUCCESS}🎯 ĐANG CHỌN: ALL JOB{Colors.TEXT_LIGHT}")
                selected_info.append(f"{Colors.INFO}Tất cả job đều được chọn{Colors.TEXT_LIGHT}")
            elif self.list_nv:
                for job in self.list_nv:
                    if job in task_descriptions:
                        selected_info.append(f"{Colors.SUCCESS}✓ {task_descriptions[job]}{Colors.TEXT_LIGHT}")
                selected_info.append(f"\n{Colors.INFO}Tổng: {len(self.list_nv)} job đã chọn{Colors.TEXT_LIGHT}")
            else:
                selected_info.append(f"{Colors.TEXT_GRAY}Chưa chọn job nào{Colors.TEXT_LIGHT}")
            
            self.display.print_card("🎯 NHIỆM VỤ ĐÃ CHỌN", selected_info)
            
            all_tasks = []
            task_descriptions = self.get_task_descriptions()
            for key, desc in task_descriptions.items():
                if self.all_jobs_selected:
                    status = f"{Colors.SUCCESS}✓ ALL{Colors.RESET}"
                else:
                    status = f"{Colors.SUCCESS}✓" if key in self.list_nv else f"{Colors.TEXT_GRAY}○"
                all_tasks.append(f"{Colors.PRIMARY}{key}.{Colors.TEXT_LIGHT} {desc:<18} {status}")
            
            self.display.print_card("📋 TẤT CẢ NHIỆM VỤ", all_tasks)
            
            management_options = [
                f"{Colors.PRIMARY}1.{Colors.TEXT_LIGHT} Chọn job (vd: 123)",
                f"{Colors.PRIMARY}2.{Colors.TEXT_LIGHT} Chọn tất cả (all)",
                f"{Colors.WARNING}3.{Colors.TEXT_LIGHT} Tắt tất cả (tatall)", 
                f"{Colors.ERROR}4.{Colors.TEXT_LIGHT} Xóa config job",
                f"{Colors.TEXT_GRAY}0.{Colors.TEXT_LIGHT} Quay lại"
            ]
            
            self.display.print_card("⚙️ QUẢN LÝ", management_options)
            
            choice = input(f"\n{Colors.SECONDARY}↳ Lựa chọn: {Colors.RESET}").strip().lower()
            
            if choice == "1":
                self.select_specific_tasks()
            elif choice == "2":
                self.select_all_tasks()
            elif choice == "3":
                self.clear_all_tasks()
            elif choice == "4":
                self.delete_job_config()
            elif choice == "0":
                break
            else:
                self.display.print_status("Lựa chọn không hợp lệ!", "error")
                sleep(1)

    def select_specific_tasks(self):
        print(f"\n{Colors.INFO}💡 Nhập số job (vd: 123 để chọn job 1,2,3){Colors.RESET}")
        choice = input(f"{Colors.SECONDARY}↳ Chọn job: {Colors.RESET}").strip().lower()
        
        if choice:
            new_tasks = []
            for char in choice:
                if char in self.get_task_descriptions() and char not in new_tasks:
                    new_tasks.append(char)
            
            if new_tasks:
                self.list_nv = new_tasks
                self.all_jobs_selected = False
                if self.config_manager.save_jobs(self.list_nv, False):
                    self.display.print_status(f"✅ Đã chọn {len(new_tasks)} job và lưu vào config!", "success")
                else:
                    self.display.print_status(f"⚠ Đã chọn {len(new_tasks)} job nhưng lỗi lưu config!", "warning")
            else:
                self.display.print_status("❌ Không có job nào được chọn!", "warning")
        else:
            self.display.print_status("ℹ Không thay đổi!", "info")
        
        sleep(1)
    
    def select_all_tasks(self):
        self.list_nv = list(self.get_task_descriptions().keys())
        self.all_jobs_selected = True
        if self.config_manager.save_jobs(self.list_nv, True):
            self.display.print_status("✅ Đã chọn TẤT CẢ job và lưu vào config!", "success")
        else:
            self.display.print_status("⚠ Đã chọn tất cả job nhưng lỗi lưu config!", "warning")
        sleep(1)
    
    def clear_all_tasks(self):
        confirm = input(f"\n{Colors.WARNING}⚠ Bạn có chắc muốn TẮT TẤT CẢ job? (y/n): {Colors.RESET}").strip().lower()
        if confirm == 'y':
            self.list_nv = []
            self.all_jobs_selected = False
            if self.config_manager.save_jobs(self.list_nv, False):
                self.display.print_status("✅ Đã TẮT TẤT CẢ job!", "success")
            else:
                self.display.print_status("⚠ Đã tắt job nhưng lỗi lưu config!", "warning")
        else:
            self.display.print_status("ℹ Không thay đổi!", "info")
        sleep(1)
    
    def delete_job_config(self):
        confirm = input(f"\n{Colors.ERROR}🗑️ Bạn có chắc muốn XÓA config job? (y/n): {Colors.RESET}").strip().lower()
        if confirm == 'y':
            try:
                if os.path.exists(self.config_manager.config_file):
                    os.remove(self.config_manager.config_file)
                    self.list_nv = []
                    self.all_jobs_selected = False
                    self.display.print_status("✅ Đã XÓA config job!", "success")
                else:
                    self.display.print_status("⚠ Không tìm thấy config job!", "warning")
            except Exception as e:
                self.display.print_status(f"❌ Lỗi xóa config: {e}", "error")
        else:
            self.display.print_status("ℹ Không thay đổi!", "info")
        sleep(1)

    def start_interaction(self):
        if not self.ttc:
            self.display.print_status("❌ Vui lòng đăng nhập TTC trước!", "error")
            sleep(2)
            return
        
        if not self.listCookie:
            self.display.print_status("❌ Vui lòng thêm ít nhất một cookie Facebook!", "error")
            sleep(2)
            return
        
        if not self.list_nv and not self.all_jobs_selected:
            self.display.print_status("❌ Vui lòng chọn ít nhất một nhiệm vụ!", "error")
            sleep(2)
            return
        
        self.display.clear()
        self.display.print_header("BẮT ĐẦU TƯƠNG TÁC")
        
        ttc_info = self.ttc.info()
        start_info = [
            f"👤 Tài khoản TTC: {Colors.SUCCESS}{ttc_info['user']}{Colors.TEXT_LIGHT}",
            f"💰 Số dư ban đầu: {Colors.WARNING}{ttc_info['xu']} Xu{Colors.TEXT_LIGHT}",
            f"🔑 Số cookie: {Colors.INFO}{len(self.listCookie)}{Colors.TEXT_LIGHT}",
        ]
        
        if self.all_jobs_selected:
            start_info.append(f"🎯 Nhiệm vụ: {Colors.PRIMARY}ALL JOB{Colors.TEXT_LIGHT}")
        else:
            start_info.append(f"🎯 Số nhiệm vụ: {Colors.PRIMARY}{len(self.list_nv)}{Colors.TEXT_LIGHT}")
            
        start_info.append(f"⏰ Thời gian: {Colors.TEXT_GRAY}{datetime.now().strftime('%H:%M:%S %d/%m/%Y')}{Colors.TEXT_LIGHT}")
        
        self.display.print_card("🚀 THÔNG TIN BẮT ĐẦU", start_info)
        
        print(f"\n{Colors.TEXT_LIGHT}Nhập cài đặt tương tác:")
        
        config = self.config_manager.load_config()
        settings = {
            'delay': self.get_number_input("⏱️ Delay giữa các job (giây)", config.get('delay', 5)),
            'jobb_block': self.get_number_input("🛡️ Sau bao nhiêu job chống block", config.get('jobb_block', 10)),
            'delay_block': self.get_number_input("💤 Thời gian nghỉ chống block (giây)", config.get('delay_block', 30)),
            'job_break': self.get_number_input("🔄 Sau bao nhiêu job chuyển acc", config.get('job_break', 20))
        }
        
        hide_id_input = input(f"\n{Colors.SECONDARY}↳ Ẩn ID Facebook? (y/n) [{'y' if config.get('hide_id', True) else 'n'}]: {Colors.RESET}").strip().lower()
        hide_id = hide_id_input if hide_id_input else ('y' if config.get('hide_id', True) else 'n')
        hide_id = hide_id == 'y'
        
        config.update(settings)
        config['hide_id'] = hide_id
        self.config_manager.save_config(config)
        
        confirm = input(f"\n{Colors.WARNING}⚠ Bắt đầu chạy tương tác? (y/n): {Colors.RESET}").strip().lower()
        if confirm != 'y':
            return
        
        self.stats = {
            'total_jobs': 0,
            'success_jobs': 0,
            'failed_jobs': 0,
            'total_xu': 0,
            'start_time': datetime.now()
        }
        
        self.is_running = True
        self.run_interaction_loop(settings, hide_id)

    def get_number_input(self, prompt, default):
        while True:
            try:
                value = input(f"{Colors.SECONDARY}↳ {prompt} [{default}]: {Colors.RESET}").strip()
                if not value:
                    return default
                return int(value)
            except ValueError:
                self.display.print_status("Vui lòng nhập số hợp lệ!", "error")

    def run_interaction_loop(self, settings, hide_id):
        stt = 0
        totalxu = 0
        ttc_info = self.ttc.info()
        current_xu = int(ttc_info['xu'])
        
        self.display.clear()
        if self.all_jobs_selected:
            self.display.print_header("ĐANG CHẠY TƯƠNG TÁC - ALL JOB", "Nhấn Ctrl+C để dừng")
        else:
            self.display.print_header("ĐANG CHẠY TƯƠNG TÁC", "Nhấn Ctrl+C để dừng")
            
        if self.ttc:
            try:
                info = self.ttc.info()
                if info.get("status") == "success":
                    user = info["user"]
                    xu = info["xu"]
                    self.display.print_status(
                        f"Tài khoản TTC: {user} | Số dư: {xu} Xu",
                        "info"
                    )
                else:
                    self.display.print_status("Không thể lấy thông tin tài khoản TTC!", "error")
            except:
                self.display.print_status("Lỗi khi đọc thông tin tài khoản TTC!", "error")
        else:
            self.display.print_status("Chưa đăng nhập tài khoản TTC!", "warning")

        try:
            while self.is_running:
                if len(self.listCookie) == 0:
                    self.display.print_status("Đã xóa tất cả cookie, vui lòng nhập lại!", "error")
                    break
                
                for cookie in self.listCookie:
                    if not self.is_running:
                        break
                        
                    JobError, JobSuccess, JobFail = 0, 0, 0
                    fb = Facebook(cookie)
                    info = fb.info()
                    
                    if 'success' in info:
                        namefb = info['name']
                        idfb = str(info['id'])
                        idrun = idfb[0]+idfb[1]+idfb[2]+"#"*(int(len(idfb)-3)) if hide_id else idfb
                    else:
                        self.display.print_status(f"Cookie die! Đã xóa: {namefb if 'namefb' in locals() else 'Unknown'}", "error")
                        self.listCookie.remove(cookie)
                        break

                    
                    cauhinh = self.ttc.cauhinh(idfb)
                    if cauhinh.get('status') == 'success':
                        self.display.print_status(f"Bắt đầu với: {namefb} ID:{idrun}", "info")
                    else:
                        self.display.print_status(f"Lỗi cấu hình ID: {namefb}", "error")
                        self.listCookie.remove(cookie)
                        break
                    
                    list_nv_default = self.list_nv.copy() if not self.all_jobs_selected else list(self.get_task_descriptions().keys())
                    
                    while self.is_running:
                        random_nv = random.choice(list_nv_default)
                        
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
                            getjob = self.ttc.getjob(fields)
                            if "idpost" in getjob.text or "idfb" in getjob.text:
                                job_data = getjob.json()
                                if isinstance(job_data, list) and len(job_data) > 0:
                                    print(f"✓ Đã tìm thấy {len(job_data)} job {fields}",'                  ',end="\r")
                                    
                                    for x in job_data:
                                        if not self.is_running:
                                            break
                                            
                                        nextDelay = False
                                        
                                        if random_nv == "1": 
                                            fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], "LIKE")
                                            id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']
                                            type = 'LIKE'
                                            id = x['idpost']
                                        
                                        if random_nv == "2": 
                                            fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], "LIKE")
                                            id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']
                                            type = 'LIKE'
                                            id = x['idpost']
                                        
                                        if random_nv == "3": 
                                            fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], x['loaicx'])
                                            id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']
                                            type = x['loaicx']
                                            id = x['idpost']
                                        
                                        if random_nv == "4": 
                                            fb.reaction(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], x['loaicx'])
                                            type = x['loaicx']
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        if random_nv == "5": 
                                            fb.reactioncmt(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], x['loaicx'])
                                            type = x['loaicx']
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        if random_nv == "6": 
                                            fb.comment(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], json.loads(x["nd"])[0])
                                            type = 'COMMENT'
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        if random_nv == "7": 
                                            fb.share(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'])
                                            type = 'SHARE'
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        if random_nv == "8": 
                                            fb.likepage(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'])
                                            type = 'LIKEPAGE'
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        if random_nv == "9": 
                                            fb.follow(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'])
                                            type = 'FOLLOW'
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        if random_nv == "0": 
                                            fb.group(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'])
                                            type = 'GROUP'
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        if random_nv == 'q': 
                                            fb.page_review(x['UID'].split('_')[1] if '_' in x['UID'] else x['UID'], json.loads(x["nd"])[0])
                                            type = 'REVIEW'
                                            id = x['UID']
                                            id_ = x['UID'].split('_')[1] if '_' in x['UID'] else x['UID']
                                        
                                        if random_nv == "s": 
                                            fb.sharend(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], json.loads(x["nd"])[0])
                                            type = 'SHAREND'
                                            id = x['idpost']
                                            id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                        
                                        nhanxu = self.ttc.nhanxu(id, fields)
                                        if nhanxu.get('status') == 'success':
                                            nextDelay, msg, xu, JobFail = True, nhanxu['msg'], nhanxu['xu'], 0
                                            xutotal = msg.replace(' Xu','')
                                            totalxu += int(xutotal)
                                            stt += 1
                                            JobSuccess += 1
                                            timejob = datetime.now().strftime('%H:%M:%S')
                                            
                                            self.display.print_job_result(stt, timejob, type, id_, msg, xu)
                                            
                                            if stt % 10 == 0:
                                                self.display.print_stats_summary(len(self.listCookie), totalxu, xu)
                                            
                                            self.stats['total_jobs'] += 1
                                            self.stats['success_jobs'] += 1
                                            self.stats['total_xu'] += int(xutotal)
                                            
                                        else:
                                            JobFail += 1
                                            timejob = datetime.now().strftime('%H:%M:%S')
                                        self.display.print_job_error(stt+1, timejob, type, id_)
                                        
                                        if JobFail >= 15:
                                            check = fb.info()
                                            if 'spam' in check:
                                                self.display.print_status(f"Tài khoản {namefb} bị spam!", "warning")
                                                fb.clickDissMiss()
                                            elif '282' in check:
                                                self.display.print_status(f"Tài khoản {namefb} bị checkpoint 282!", "error")
                                                self.listCookie.remove(cookie)
                                                chuyen = True
                                                break
                                            elif '956' in check:
                                                self.display.print_status(f"Tài khoản {namefb} bị checkpoint 956!", "error")
                                                self.listCookie.remove(cookie)
                                                chuyen = True
                                                break
                                            elif 'cookieout' in check:
                                                print(f"✗ Cookie {namefb} bị out!",'                  ',end="\r")
                                                self.listCookie.remove(cookie)
                                                chuyen = True
                                                break
                                            else:
                                                self.display.print_status(f"Tài khoản {namefb} bị block {fields}!", "warning")
                                                JobFail = 0
                                                if random_nv in list_nv_default:
                                                    list_nv_default.remove(random_nv)
                                                if list_nv_default:
                                                    random_nv = random.choice(list_nv_default)
                                                else:
                                                    self.display.print_status(f"Tài khoản {namefb} bị block tất cả!", "error")
                                                    self.listCookie.remove(cookie)
                                                    chuyen = True
                                                    list_nv_default = self.list_nv.copy() if not self.all_jobs_selected else list(self.get_task_descriptions().keys())
                                                break
                                        
                                        if JobSuccess != 0 and JobSuccess % settings['job_break'] == 0:
                                            chuyen = True
                                            break
                                        
                                        if nextDelay:
                                            if stt % settings['jobb_block'] == 0:
                                                Delay(settings['delay_block'], self.display)
                                            else:
                                                Delay(settings['delay'], self.display)
                                    
                                    if chuyen:
                                        break
                                        
                            else:
                                if 'error' in getjob.text:
                                    if 'countdown' in getjob.json():
                                        countdown = getjob.json()['countdown']
                                        print(f"ℹ Countdown {fields}: {countdown:.1f}s",end='\r')
                                        Delay(countdown, self.display)
                                    else:
                                        self.display.print_status(f"Lỗi: {getjob.json().get('error', 'Unknown')}", "error")
                                        if random_nv in list_nv_default:
                                            list_nv_default.remove(random_nv)
                                        if not list_nv_default:
                                            break
                                        Delay(5, self.display)
                        except Exception as e:
                            self.display.print_status(f"Lỗi xử lý job: {e}", "error")
                            if random_nv in list_nv_default:
                                list_nv_default.remove(random_nv)
                            if not list_nv_default:
                                break
                    
                    if not self.is_running:
                        break
                        
        except KeyboardInterrupt:
            self.is_running = False
            self.display.print_status("Đã dừng tương tác!", "warning")
        
        self.is_running = False
        input(f"\n{Colors.TEXT_GRAY}Nhấn Enter để tiếp tục...{Colors.RESET}")
    
    def show_stats(self):
        self.display.clear()
        self.display.print_header("THỐNG KÊ CHI TIẾT")
        
        if self.stats['start_time']:
            runtime = datetime.now() - self.stats['start_time']
            stats_info = [
                f"🕒 Thời gian chạy: {Colors.INFO}{str(runtime).split('.')[0]}{Colors.TEXT_LIGHT}",
                f"📊 Tổng job: {Colors.PRIMARY}{self.stats['total_jobs']}{Colors.TEXT_LIGHT}",
                f"✅ Thành công: {Colors.SUCCESS}{self.stats['success_jobs']}{Colors.TEXT_LIGHT}",
                f"❌ Thất bại: {Colors.ERROR}{self.stats['failed_jobs']}{Colors.TEXT_LIGHT}",
                f"💰 Tổng xu nhận: {Colors.WARNING}{self.stats['total_xu']}{Colors.TEXT_LIGHT}",
                f"📈 Tỉ lệ thành công: {Colors.SECONDARY}{(self.stats['success_jobs']/max(1, self.stats['total_jobs']))*100:.1f}%{Colors.TEXT_LIGHT}"
            ]
        else:
            stats_info = [f"{Colors.TEXT_GRAY}Chưa có dữ liệu thống kê{Colors.TEXT_LIGHT}"]
        
        self.display.print_card("📈 THỐNG KÊ TỔNG QUAN", stats_info)
        
        input(f"\n{Colors.TEXT_GRAY}Nhấn Enter để tiếp tục...{Colors.RESET}")

# ==================== CHẠY CHƯƠNG TRÌNH ====================
if __name__ == "__main__":
    try:
        app = TTCFBPremium()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.ERROR}👋 Đã thoát chương trình!{Colors.RESET}")
    except Exception as e:
        print(f"\n\n{Colors.ERROR}💥 Lỗi: {e}{Colors.RESET}")