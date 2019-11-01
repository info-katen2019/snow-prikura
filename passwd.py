import secrets
import string

with open("pass_list.dat", "w") as w_file:
    for i in range(0, 5000):
        passwd = ''.join([secrets.choice(string.ascii_letters + string.digits) for i in range(8)])
        w_file.write("ID: " + str(i) + " Pass: " + passwd + "\n")
    