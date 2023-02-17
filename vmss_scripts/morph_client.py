
import socket
from datetime import datetime
import os
from random import randint

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))

def get_available_machines():
    # gets reachable machines
    # bash_out = os.popen("bash /home/varuna/t-nisar/Megatron-LM/get_available_machines.sh").read()
    bash_out = os.popen("bash /home/znyang/varuna/varuna/get_available_machines.sh").read()
    machines = bash_out.split("\n")
    if machines[-1] == "":
        machines = machines[:-1]
    available = randint(20,len(machines))
    machines = machines[:available]
    return machines

if __name__ == "__main__":

    server_ip = "172.17.0.2"
    server_port = 4200

    # with open("/home/varuna/t-nisar/Megatron-LM/nservers","r") as f:
    #     current_num_machines = int(f.read())
    current_num_machines = 2

    # new_machines = get_available_machines()
    new_machines = ["172.17.0.4"]
    print(new_machines)
    # if len(new_machines) % 2 != 0:
    #     new_machines = new_machines[:-1]
    #     print(new_machines)

    if len(new_machines) == current_num_machines:
        print(str(datetime.now()), "no morph")
    else:
        of = open("/home/znyang/varuna/examples/Megatron-LM/available_machines.out","w")
        for m in new_machines:
            of.write(m)
            if "\n" not in m:
                of.write("\n")
        of.close()
        client(server_ip, server_port, "morph")
        print(str(datetime.now()), len(new_machines))


