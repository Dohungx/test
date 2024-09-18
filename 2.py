import requests

# Danh sách proxy cần kiểm tra
proxy_list = [
    "104.207.61.82:3128", "104.167.30.235:3128", "104.207.44.142:3128",
    "104.207.47.86:3128", "104.167.24.57:3128", "104.207.49.36:3128",
    "104.207.57.18:3128", "104.207.53.84:3128", "104.207.33.70:3128",
    "104.207.48.66:3128", "104.167.30.16:3128", "104.207.55.219:3128",
    "104.167.31.141:3128", "104.207.37.238:3128", "104.207.40.254:3128",
    "104.167.28.177:3128", "104.207.49.17:3128", "104.207.62.40:3128",
    "104.207.40.65:3128", "104.207.41.204:3128", "104.207.57.121:3128",
    "104.167.26.6:3128", "104.167.24.203:3128", "104.207.59.81:3128",
    "104.207.56.176:3128", "104.207.60.30:3128", "104.207.41.249:3128",
    "104.207.61.144:3128", "104.207.58.235:3128", "104.207.53.240:3128",
    "104.207.45.10:3128", "104.167.29.236:3128", "104.167.24.253:3128",
    "104.207.45.193:3128", "104.207.37.240:3128", "104.207.55.250:3128",
    "104.207.58.76:3128", "104.207.40.47:3128", "104.207.43.237:3128",
    "104.207.46.90:3128", "104.207.56.42:3128", "104.207.37.7:3128",
    "104.207.50.174:3128", "104.207.33.209:3128", "104.207.51.211:3128",
    "104.207.34.28:3128", "104.207.49.15:3128", "104.207.40.234:3128",
    "104.207.44.58:3128", "104.167.27.156:3128", "104.207.61.95:3128",
    "104.207.45.89:3128", "104.207.62.93:3128", "104.207.39.51:3128",
    "104.167.27.186:3128", "104.167.28.222:3128", "104.207.41.203:3128",
    "104.207.52.162:3128", "104.207.49.137:3128", "104.207.48.61:3128",
    "104.207.57.77:3128", "104.207.41.33:3128", "104.167.24.37:3128",
    "104.167.30.65:3128", "104.207.53.149:3128", "104.207.33.142:3128",
    "104.207.46.7:3128", "104.207.36.15:3128", "104.167.28.152:3128",
    "104.207.39.175:3128", "104.207.44.197:3128", "104.207.36.184:3128",
    "104.207.39.69:3128", "104.167.27.144:3128", "104.207.60.249:3128",
    "104.207.35.71:3128", "104.167.25.125:3128", "104.207.42.227:3128",
    "104.207.42.103:3128", "104.207.63.59:3128", "104.207.33.90:3128",
    "104.207.39.159:3128", "104.167.25.76:3128", "104.207.34.247:3128",
    "104.207.34.222:3128", "104.207.42.158:3128", "104.207.43.129:3128",
    "104.207.35.46:3128", "104.207.51.236:3128", "104.207.60.159:3128",
    "104.207.62.3:3128", "104.207.57.106:3128", "104.167.31.116:3128",
    "104.167.25.68:3128", "104.207.38.17:3128", "104.207.40.231:3128",
    "104.207.40.195:3128", "104.207.39.101:3128", "104.207.52.167:3128",
    "104.207.45.64:3128"
]

# URL để kiểm tra
login_url = "https://www.facebook.com/login.php"

# Header để mô phỏng trình duyệt thật
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

def check_proxy(proxy):
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    data = {
        'email': 'test@example.com',
        'pass': 'testpassword',
        'login': 'Log In'
    }
    
    try:
        response = requests.post(login_url, headers=headers, data=data, proxies=proxy_dict, allow_redirects=False, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(f"Proxy {proxy} lỗi: {e}")
    return False

def main():
    working_proxies = []
    for proxy in proxy_list:
        if check_proxy(proxy):
            working_proxies.append(proxy)
            print(f"Proxy khả dụng: {proxy}")
        else:
            print(f"Proxy không khả dụng: {proxy}")

    with open('working_proxies.txt', 'w') as file:
        for proxy in working_proxies:
            file.write(f"{proxy}\n")

if __name__ == "__main__":
    main()
