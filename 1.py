import webbrowser

url = 'http://testtools.atwebpages.com/'
key = 'VBS'

ma = input("Enter the key: ")

if ma == key:
    print("Đúng Key, đang chuyển hướng")
    webbrowser.open(url)
else:
    print("Sai key, vui lòng thử lại")
