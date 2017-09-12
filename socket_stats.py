# this script just prints some of the socket data in a readable way
import os
import json

BASE_DATA_PATH = "data/"

def read_json():

    champ_dict = {}
    for folder_name in os.listdir(BASE_DATA_PATH):
        if os.path.isdir(BASE_DATA_PATH + folder_name):
            print("Opening ", folder_name)
            json_file = json.load(open(BASE_DATA_PATH + folder_name + '/socket.json', 'r'))
            stats = json_file[0]['playerStats']
            for i in range(1, 11):
                champ = stats[str(i)]['championName']
                if champ not in champ_dict:
                    champ_dict[champ] = 1
                else:
                    champ_dict[champ] += 1
    sorted_keys = sorted(champ_dict, key=champ_dict.get, reverse=True)
    for key in sorted_keys:
        print("%s played in %d games" % (key, champ_dict[key]))


if __name__ == '__main__':
    read_json()
