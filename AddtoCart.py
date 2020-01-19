import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}

with requests.Session() as s:
    s.headers = headers
    r = s.get('https://kindle.amazon.com/login')
    soup = BeautifulSoup(r.content, "html.parser")
    signin_data = {s["name"]: s["value"]
                   for s in soup.select("form[name=signIn]")[0].select("input[name]")
                   if s.has_attr("value")}

    signin_data[u'email'] = 'kgleong2001@gmail.com'
    signin_data[u'password'] = 'fusion1323'

    response = s.post('https://www.amazon.com/ap/signin', data=signin_data)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    warning = soup.find('div', {'id': 'message_warning'})
    if warning:
        print('Failed to login: {0}'.format(warning.text))
    print(response.content)


# from getpass import getpass
# import webbrowser
# import requests
# import os


# amazon_username = "kgleong2001@gmail.com"
# amazon_password = "fusion1323"

# headers = {
# 	"User-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
# 	"action": "sign-in",
# 	"email": amazon_username,
# 	"password": amazon_password
# 	}

# r = requests.get("https://www.amazon.com/gp/sign-in.html", headers=headers)
# print(r.status_code)

# r = requests.get("https://www.amazon.com/gp/flex/sign-in/select.html", headers=headers)
# print(r.status_code)

# r = requests.get("https://www.amazon.com/", headers=headers)
# print(r.status_code)
