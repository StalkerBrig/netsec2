NO_SPLIT_VAL = False

#Just for printing arrays
def aprint(array):
    for element in array:
        print(element)
    print("********************************************")


def GetFileInfo(file_name, split_val, split_val2):

    data_file_in = open(file_name, "r")
    result_array = []
    all_data_array = []

    #goes through each line in the file
    for element in data_file_in:
        #determines what separates the elements in each line
        #No split value means it is just being separated by spaces

        if split_val != NO_SPLIT_VAL:
            tmp_array = element.split(split_val)
        else:
            tmp_array = element.split()

        tmp_array[-1] = tmp_array[-1].strip()

        split_array = [e for e in tmp_array if e not in split_val2]
        #gets rid of new line on the last value

        if split_array[0] == "R:[":
            split_array[0] = "R"
        elif split_array[0] == "S:[":
            split_array[0] = "S"

        all_data_array.append(split_array)

    return all_data_array