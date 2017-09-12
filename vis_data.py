import cv2
from PIL import Image, ImageDraw
import numpy as np
from read_ocr_and_lolesport_data import get_game_data_dict


def visualize_game_data(game_data, folder):
    for time_stamp in game_data:
        frame_obj = game_data[time_stamp]
        # not all frame objs have actual frames asscoiated with them!
        if frame_obj.frame_path is not None:
            print("%s .... %s" % (frame_obj.time_obj.time_as_string, frame_obj.frame_path))
            x_val = int(frame_obj.game_snap['playerStats']['7']['x'])
            y_val = int(frame_obj.game_snap['playerStats']['7']['y'])

            x_val_2 = int(frame_obj.game_snap['playerStats']['2']['x'])
            y_val_2 = int(frame_obj.game_snap['playerStats']['2']['y'])

            # load in image w/ PIL for easy drawing / cropping
            im = Image.open('data/' + folder  + '/frames/' + frame_obj.frame_path).crop((1625, 785, 1920, 1080))
            draw = ImageDraw.Draw(im)
            draw.rectangle([(x_val - 19, y_val - 20),(x_val + 11, y_val + 10)], outline='red')
            draw.rectangle([(x_val_2 - 19, y_val_2 - 20),(x_val_2 + 11, y_val_2 + 10)], outline='blue')

            print('\n')
            # now draw using PIL
            del draw

            im = np.array(im, dtype = np.uint8)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB )
            cv2.imshow("IMAGE", im)
            if cv2.waitKey(1) == ord('q'):
                break

# to visualize dataset after all processing
def visualize_npz_data(npz_file_path):
    np_obj = np.load(npz_file_path)
    for image, boxes in zip(np_obj['images'], np_obj['boxes']):
        print(boxes)
        img = Image.fromarray(image)
        class_name, x_min, y_min, x_max, y_max = boxes[0][0], boxes[0][1], boxes[0][2], boxes[0][3], boxes[0][4]
        draw = ImageDraw.Draw(img)
        draw.rectangle([(x_min, y_min), (x_max, y_max)], outline='red')

        img = np.array(img, dtype = np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        cv2.imshow("IMAGE", img)
        if cv2.waitKey(500)  ==  ord('q'):
            break
        del draw
if __name__ == "__main__":
    # at this point, game_data has a dict of frame objects with a frame_path IF one was found for it.
    # game data's keys are in order of game time.
    # game_data = get_game_data_dict('C9_FOX_G_2_MARCH_4_2017')
    # visualize_game_data(game_data, 'C9_FOX_G_2_MARCH_4_2017')
    visualize_npz_data('data_training_set.npz')
