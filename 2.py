import requests
import time

# URL của API ProxyScrape
proxy_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

# Hàm kiểm tra tính khả dụng của proxy
def check_proxy(proxy):
    try:
        response = requests.get("http://testtools.atwebpages.com/", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

# Lấy danh sách proxy từ ProxyScrape
def get_proxies():
    try:
        response = requests.get(proxy_api_url)
        if response.status_code == 200:
            return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching proxies: {e}")
    return []

# Kiểm tra tất cả các proxy và lưu proxy khả dụng vào tệp proxy.txt
def filter_proxies():
    proxies = get_proxies()
    if not proxies:
        print("No proxies retrieved.")
        return

    available_proxies = []
    for proxy in proxies:
        print(f"Checking proxy: {proxy}")
        if check_proxy(proxy):
            available_proxies.append(proxy)
            print(f"Proxy {proxy} is working.")
        else:
            print(f"Proxy {proxy} is not working.")
        time.sleep(1)  # Đợi một chút để không gửi quá nhiều yêu cầu nhanh chóng

    with open('proxy.txt', 'w') as file:
        for proxy in available_proxies:
            file.write(proxy + '\n')
    print(f"Saved {len(available_proxies)} working proxies to proxy.txt")

if __name__ == "__main__":
    filter_proxies()