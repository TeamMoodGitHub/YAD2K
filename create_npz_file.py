# shouts out to this guy for helping me out!
# https://github.com/shadySource/DATA/blob/master/package_dataset.py

from read_ocr_and_lolesport_data import get_game_data_dict
import numpy as np
from PIL import Image
from random import shuffle
import os

label_dict = {"Elise": 0, "Sejuani": 1, "Jhin": 2, "Rengar": 3, "Jayce": 4,
"Ashe": 5, "Graves": 6, "Nautilus": 7, "Shen": 8, "Orianna": 9, "Ezreal": 10,
"Poppy": 11, "Khazix": 12, "Rumble": 13, "Karma": 14, "Syndra": 15, "Nami": 15,
"Malzahar": 16, "Ryze": 17, "TahmKench": 18, "LeeSin": 19, "Sivir": 20}

debug = False
shuffle = True

BASE_DATA_PATH = 'data/'

# returns array with label, x_min, y_min, x_max, y_max for a single champ
def get_box_for_champ(champ_index, frame_obj):
    champ_name = frame_obj.game_snap['playerStats'][champ_index]['championName']
    label = label_dict[champ_name]
    x_val = int(frame_obj.game_snap['playerStats'][champ_index]['x'])
    y_val = int(frame_obj.game_snap['playerStats'][champ_index]['y'])

    # label xmin ymin xmax ymax
    return np.array([label, x_val - 19, y_val - 20, x_val + 11, y_val + 10])

# TODO Make this look nicer
def dead(frame_obj, champ_index):
    if  frame_obj.game_snap['playerStats'][champ_index]['x'] == 0 and frame_obj.game_snap['playerStats'][champ_index]['y'] == 0:
        return True
    return False

def check_boxes_for_champs_in_dict(frame_obj):
    boxes_in_frame = []
    for i in range(1, 11):
        champ_index = str(i)
        champ_name = frame_obj.game_snap['playerStats'][champ_index]['championName']

        # for now only care about specific champs in our labels. not eveything.
        if champ_name not in label_dict:
            continue

        # if champ is dead, we dont care for their position
        if dead(frame_obj, champ_index):
            continue

        # this will always return a box, no matter what.
        # every champ always has a position
        box = get_box_for_champ(champ_index, frame_obj)

        if(box[1] < 0 or box[2] < 0 or box[3] < 0 or box[4] < 0):
            continue

        boxes_in_frame.append(box)
    if len(boxes_in_frame) == 0:
        return boxes_in_frame, True
    return boxes_in_frame, False

def get_bounding_boxes_and_images(game_data, folder):
    all_boxes = []
    all_images = []

    counter = 0
    for time_stamp in game_data:
        boxes_in_timestamp = []
        frame_obj = game_data[time_stamp]
        if frame_obj.frame_path is not None:
            # go through every champion
            boxes, empty = check_boxes_for_champs_in_dict(frame_obj)
            # if the frame came back with no boxes, we don't care for it. it has no data we care about.
            if empty:
                continue

            all_boxes.append(np.array(boxes))

            # image work
            # im = Image.open(BASE_DATA_PATH + folder + '/frames/' + frame_obj.frame_path).crop((1625, 785, 1920, 1080))
            # im = np.array(im, dtype = np.uint8)
            # all_images.append(im)

            if debug:
                if counter == 10:
                    break
            counter += 1

            if len(all_images) % 50 == 0:
                print("Image array length... ", len(all_images))

    return all_boxes, all_images

if __name__ == '__main__':

    all_boxes = []
    all_images = []
    for folder_name in os.listdir(BASE_DATA_PATH):
        if os.path.isdir(BASE_DATA_PATH + folder_name):
            print("Aggregating data for ", folder_name)
            game_data = get_game_data_dict(folder_name)
            # arrange all data in to these two nice lists
            boxes, images = get_bounding_boxes_and_images(game_data, folder_name)
            print("Appending %d images " % len(images))
            all_boxes.extend(boxes)
            all_images.extend(images)

    print("Length of boxes arr ", len(all_boxes))

    if shuffle:
        np.random.seed(13)
        indices = np.arange(len(all_images))
        all_images = np.asarray(all_images)
        all_boxes = np.asarray(all_boxes)
        np.random.shuffle(indices)
        all_images, all_boxes = all_images[indices], all_boxes[indices]

    print(np.asarray(all_images).shape)
    print(np.asarray(all_boxes).shape)


    # test set
    test_set_cut = int(0.1 * len(all_images))
    np.savez("data_training_set", images=all_images[:-test_set_cut], boxes=all_boxes[:-test_set_cut])
    np.savez("data_test_set", images=all_images[-test_set_cut:], boxes=all_boxes[-test_set_cut:])

    print(np.asarray(all_images[:-test_set_cut]).shape)
    print(np.asarray(all_boxes[:-test_set_cut]).shape)

    print(np.asarray(all_images[-test_set_cut:]).shape)
    print(np.asarray(all_boxes[-test_set_cut:]).shape)
