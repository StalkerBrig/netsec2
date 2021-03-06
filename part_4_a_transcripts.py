import socket
import sys
import re


def read_target_file(filename):
    target_ids = []
    with open(filename) as f:
        targets = f.readlines()
        for target in targets:
            split_targ = re.split('[@ : \n]', target)
            split_targ = split_targ[:-1]
            target_ids.append(split_targ)
    return target_ids


targets = read_target_file("publicpeers.txt")

priv_file_name = "priv_transcript.txt"

open(priv_file_name, 'w').close()

public_dict = {}

for target in targets:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
    except socket.error as err:
        print("Error %s" % (err))

    try:
        s.connect((target[1], int(target[2])))
    except socket.error as err:
        print("Error %s" % (err))
        continue

    these_peers = []
    threshold = 0
    no_at_sign = False
    while True:
        s.send("PEERS\n".encode())
        received = s.recv(1024).decode()
        received2 = s.recv(1024).decode()
        split_rec = re.split('[\n]', received2)
        split_rec = split_rec[:-1]
        split_rec.append(received[:-1])
        print(split_rec)
        for ele in split_rec:
            if '@' not in ele:
                no_at_sign = True
                break
        if no_at_sign:
            no_at_sign = False
            continue

        no_new = True
        for element in split_rec:
            found_peer = False
            for peer in these_peers:
                if element == peer:
                    found_peer = True
                    break
            if not found_peer:
                these_peers.append(element)
                no_new = False
                threshold = 0
        print(no_new, threshold)
        threshold += 1
        if no_new == True and threshold > 15:
            break

    for peer in these_peers:
        split_peer = re.split('[@ :]', peer)
        found_peer = False
        for target2 in targets:
            if split_peer[0] == target2[0]:
                found_peer = True
                break
        if not found_peer:
            #targets.append(split_peer)
            print("sure")


    #TODO
    user_id = target[0] + "@" + target[1] + ":" + target[2]
    print(user_id)
    if user_id not in public_dict:
        public_dict[user_id] = []

    for ele in these_peers:
        if ele not in public_dict[user_id]:
            public_dict[user_id].append(ele)
    print(public_dict)

    print(split_rec)
    for ele in these_peers:
        print(ele)
    s.close()


with open(priv_file_name, "w") as trash:
    for node, connections in public_dict.items():
        trash.write("! " + str(node) + "\n")
        for eles in connections:
            trash.write(eles + "\n")



