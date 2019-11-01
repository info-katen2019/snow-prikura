import secrets
import string

passwd_list = []

def gen_passwd(n):
    for i in range(1, n):
        passwd = ''.join([secrets.choice(string.ascii_letters + string.digits) for i in range(8)])
        passwd_list.append(passwd)
    return passwd_list