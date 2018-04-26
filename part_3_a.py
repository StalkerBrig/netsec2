import time
import re

OFFER = 0
ACK = 1
#1 second time threshold
TIME_THRESH = 1



def ChangeDictionary(msg_id, time_stamp, user_id, dictionary):
    if msg_id not in dictionary:
        #the one indicates that there is one entry in this dictionary now.
        #We want to use this to find out which ones are privates nodes
        dictionary[msg_id] = [time_stamp, user_id, 1]
    else:  # it is in the dictionary
        check_time = dictionary[msg_id][0]
        num_times_in_dict = dictionary[msg_id][2]
        if abs(check_time-time_stamp) < TIME_THRESH:
            if check_time > time_stamp:
                dictionary[msg_id] = [time_stamp, user_id, num_times_in_dict+1]
            else: #the previous entry was a smaller time.. which would only be by miliseconds..
                dictionary[msg_id] = [check_time, user_id, num_times_in_dict+1]
        else: #it isn't in the same time threshold; i.e. it isn't the same message and isn't
              # a private node

            if check_time > time_stamp:
                dictionary[msg_id] = [time_stamp, user_id, 1]

def WriteToCSVFile(send_or_recieve, dictionary, file_name):
    file = open(file_name, "a+")

    dict_length = len(dictionary)

    iteration = 0

    file_string = send_or_recieve + ":["
    for row in dictionary.values():
        iteration += 1
        user_id = row[1]
        check_for_public_nodes = row[2]
        #this means it is a public node
        if check_for_public_nodes == 1:
            file_string += "'" + user_id

            file_string += "', "
        else:
            continue
    file_string = file_string[:-2]
    file_string += "]\n"
    file.write(file_string)
    file.close()


file_number = str(50)
file_name = "transcript_" + file_number + ".txt"

csv_file_name = "transcript_" + file_number + ".csv"
#this deletes the stuff in the csv file
open(csv_file_name, 'w').close()

round_offer_dict = {}
round_ack_dict = {}

#just to initialize
user_id = ""
time_stamp = ""
msg_id = ""
msg_id_type = -1

#TODO: This will assume that the first round will start with 1
new_round = 1

data_file_in = open(file_name, "r")

# goes through each line in the file
for row in data_file_in:
    row_split = row.split()

    #the rows that have an ID do not have the [
    if row[0] != "[":
        user_id = row_split[0]
        round_number = int(row_split[2])
        if round_number != new_round:
            WriteToCSVFile("S", round_offer_dict, csv_file_name)
            WriteToCSVFile("R", round_ack_dict, csv_file_name)
            round_offer_dict = {}
            round_ack_dict = {}
            new_round = round_number

    else:
        #the [:-1] gets rid of the ']'
        time_stamp = row_split[1][:-8]

        full_time_stamp  = row_split[0][1:] + " " + time_stamp

        epoch_time = time.mktime(time.strptime(full_time_stamp,"%Y-%m-%d %H:%M:%S"))
        miliseconds = float(row_split[1][-8:-1])
        '''
        split_time_stamp = re.split('[- : . ]', full_time_stamp)

        print(full_time_stamp)
        print(split_time_stamp)

        time_tuple = (split_time_stamp[0], split_time_stamp[1], split_time_stamp[2], split_time_stamp[3],
                      split_time_stamp[4], split_time_stamp[5] )
        '''


        full_epoch_time = epoch_time+miliseconds

        msg_id = row_split[2]

        if msg_id == "OFFER":
            msg_id_type = 0

        elif msg_id == "ACK":
            msg_id_type = 1

        else: #is the message id number
            if msg_id_type == OFFER:
                if msg_id[0] != "f":
                    msg_id_type = -1
                    continue
                ChangeDictionary(msg_id, full_epoch_time, user_id, round_offer_dict)
            elif msg_id_type == ACK:
                ChangeDictionary(msg_id, full_epoch_time, user_id, round_ack_dict)
            msg_id_type = -1

data_file_in.close()