# shouts out to this guy for helping me out!
# https://github.com/shadySource/DATA/blob/master/package_dataset.py

from read_ocr_and_lolesport_data import get_game_data_dict
import numpy as np
from PIL import Image
from random import shuffle

FRAME_DIR = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/frames/"

label_dict = {"Elise": 0, "Sejuani": 1}
debug = True
shuffle = True



# returns array with label, x_min, y_min, x_max, y_max for a single champ
def get_box_for_champ(champ_index, frame_obj):
    champ_name = frame_obj.game_snap['playerStats'][champ_index]['championName']
    label = label_dict[champ_name]
    x_val = int(frame_obj.game_snap['playerStats'][champ_index]['x'])
    y_val = int(frame_obj.game_snap['playerStats'][champ_index]['y'])

    x_min = x_val - 19
    y_min = y_val - 20
    x_max = x_val + 11
    y_max = y_val + 10

    return np.array([label, x_min, y_min, x_max, y_max])

# TODO Make this look nicer
def dead(frame_obj, champ_num):
    if  frame_obj.game_snap['playerStats'][champ_num]['x'] == 0 and frame_obj.game_snap['playerStats'][champ_num]['y'] == 0:
        return True
    return False


def get_bounding_boxes_and_images(game_data):
    all_boxes = []
    all_images = []
    i = 0
    for time_stamp in game_data:
        boxes_in_timestamp = []
        frame_obj = game_data[time_stamp]
        if frame_obj.frame_path is not None:

            # be sure champ isn't dead
            if not dead(frame_obj, '2'):
                box = get_box_for_champ('2', frame_obj)
            if not dead(frame_obj, '7'):
                box_2 = get_box_for_champ('7', frame_obj)

            # be sure both aren't dead at the same
            if dead(frame_obj, '2') and dead(frame_obj, '7'):
                continue

            # negative coordinates
            if(box[1] < 0 or box[2] < 0 or box[3] < 0 or box[4] < 0):
                continue

            # bounding boxes
            boxes_in_timestamp.append(box)
            boxes_in_timestamp.append(box_2)
            all_boxes.append(np.array(boxes_in_timestamp))

            # image
            im = Image.open(FRAME_DIR + frame_obj.frame_path).crop((1625, 785, 1920, 1080))
            im = np.array(im, dtype = np.uint8)
            all_images.append(im)

            if debug:
                if i == 20:
                    break

            i += 1

    return all_boxes, all_images



if __name__ == '__main__':
    game_data = get_game_data_dict()
    # arrange all data in to these two nice lists
    all_boxes, all_images = get_bounding_boxes_and_images(game_data)

    if shuffle:
        np.random.seed(13)
        indices = np.arange(len(all_images))
        all_images = np.asarray(all_images)
        all_boxes = np.asarray(all_boxes)
        np.random.shuffle(indices)
        all_images, all_boxes = all_images[indices], all_boxes[indices]

    print(np.asarray(all_images).shape)
    print(np.asarray(all_boxes).shape)

    if debug:
        # test set
        test_set_cut = int(0.1 * len(all_images))
        np.savez("data_training_set", images=all_images, boxes=all_boxes)
        np.savez("data_test_set", images=all_images[-test_set_cut:], boxes=all_boxes[-test_set_cut:])

        print(np.asarray(all_images).shape)
        print(np.asarray(all_boxes).shape)

        print(np.asarray(all_images[-test_set_cut:]).shape)
        print(np.asarray(all_boxes[-test_set_cut:]).shape)
