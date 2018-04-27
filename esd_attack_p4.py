import read_file_part_1


# This will run an extended statistical dislosure attack and write a list of most likely friends to a csv file
def esd_attack(target, messages, batch_size, csv):
    obs_dist = {}
    back_dist = {}
    friends = {}

    print("Searching for target: " + target);
    with open("privatepeers.txt", "r") as f:
        for line in f:
            obs_dist[line[:-20]] = float(0)
            back_dist[line[:-20]] = float(0)
            print(line[:-20])
    # These are the t/t' variables from the formula
    rounds_sent_message = 0
    rounds_no_message = 0

    # This will be mi
    total_messages_sent = 0

    for record in messages:
        if (record[0] == 'S'):

            # For each message that was sent, add up the total number sent, the
            # number sent in that round
            messages_this_round = 0
            sent_this_round = False
            for message in record:
                if (message == target):
                    messages_this_round += 1
                    sent_this_round = True

            # Increment t or t' depending on if a message was sent in the last round
            if (sent_this_round == True):
                rounds_sent_message += 1
                total_messages_sent += messages_this_round
            else:
                rounds_no_message += 1

        # If this a record of received messages, then if the target sent messages this round
        # add 1/batch_size to the observed distribution dictionary. otherwise, do it for the
        # background distribution dictionary
        if (record[0] == 'R'):

            if (sent_this_round == True):
                for message in record[1:]:
                    obs_dist[message] += float(1.0 / float(batch_size))
            else:
                for message in record[1:]:
                    back_dist[message] += float(1.0 / float(batch_size))

    # This will make the Big U vector as described in the write up
    for key, value in back_dist.items():
        back_dist[key] = value * float(1.0 / float(rounds_no_message))
    # This is the Big O vector as described in the write up
    for key, value in obs_dist.items():
        obs_dist[key] = value * float(1.0 / float(rounds_sent_message))

    # m-bar definition is in the write up
    m_bar = total_messages_sent * float(1.0 / float(rounds_sent_message))

    # This is the final equation to calculate the v-vector. v-vector = friends.
    for key, value in obs_dist.items():
        friends[key] = float(1.0 / m_bar) * ((batch_size * obs_dist[key]) - ((batch_size - m_bar) * back_dist[key]))

    # Write the target,3best friends to the csv file
    csv.write(target)
    best_friends = sorted(friends.items(), key=lambda x: -x[1])[:3]
    for x in best_friends:
        csv.write("," + x[0])
    csv.write('\n')


# Get the message exchanges from the csv file
messages = read_file_part_1.GetFileInfo("p4-friends_send_receive.csv", "'", (", ", " ", "\n", "]"))

csv = open("p4-friends.csv", "w")

with open("part4targets.txt", "r") as targets:
    for target in targets:
        esd_attack(target[:-1], messages, 16, csv)