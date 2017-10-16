# this script just prints some of the socket data in a readable way
import os
import json

BASE_DATA_PATH = "/Volumes/DATA/data/data/"


def diversity_percentage(champ_dict):


def check_champs(json_file, champ_dict):
    first check if we have enough of champ.
    stats = json_file[0]['playerStats']
    for i in range(1, 11):
        champ = stats[str(i)]['championName']
        if champ in champ_dict:
            # we have enough of this champ!
            if champ_dict[champ] > 20:
                return

    for i in range(1, 11):
        champ = stats[str(i)]['championName']
        if champ not in champ_dict:
            champ_dict[champ] = 1

        if champ in champ_dict:
            champ_dict[champ] += 1


def read_json():

    champ_dict = {}
    ocr = 0
    for folder_name in os.listdir(BASE_DATA_PATH):
        print("Opening ", folder_name)
        if os.path.isdir(BASE_DATA_PATH + folder_name):
            if os.path.exists(BASE_DATA_PATH + folder_name + '/frames'):
                if not os.path.exists(BASE_DATA_PATH + folder_name + '/time_stamp_data_clean.json'):
                    ocr += len(os.listdir(BASE_DATA_PATH + folder_name + '/frames'))
                    print("Still need ocr data for %s and OCR is count is @ %d" % (folder_name, ocr))
            else:
                print("FRAMES doesn't exist for ", folder_name)

            # try:
            #     json_file = json.load(open(BASE_DATA_PATH + folder_name + '/socket.json', 'r'))
            # except Exception as e:
            #     print("JSON failed on ", folder_name)
            #     print(e)
            #     continue

            # check_champs(json_file, champ_dict)

    sorted_keys = sorted(champ_dict, key=champ_dict.get, reverse=True)
    for key in sorted_keys:
        print("%s played in %d games" % (key, champ_dict[key]))


if __name__ == '__main__':
    read_json()
