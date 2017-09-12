# inspiration for this class comes from Autopilot-TensorFlow on GitHub!
from retrain_yolo import process_data, get_detector_mask
import numpy as np


YOLO_ANCHORS = np.array(
    ((0.57273, 0.677385), (1.87446, 2.06253), (3.33843, 5.47434),
     (7.88282, 3.52778), (9.77052, 9.16828)))

class TrainingData:
    def __init__(self, npz_file):
        images = npz_file['images']
        boxes = npz_file['boxes']

        # pointers to handle all our batches
        self.train_batch_pointer = 0
        self.val_batch_pointer = 0

        # set up all the images
        self.train_images = images[:int(len(images) * 0.9)]
        self.train_boxes = boxes[:int(len(images) * 0.9)]
        self.val_images = images[-int(len(images) * 0.1):]
        self.val_boxes = boxes[-int(len(images) * 0.1):]

    def load_train_batch(self, batch_size):
        # fix pointers if they extend to far!
        if self.train_batch_pointer + batch_size > len(self.train_images):
            self.train_batch_pointer = 0

        initial_index = self.train_batch_pointer
        end_index = self.train_batch_pointer + batch_size
        print("Loading images/boxes from idnex %d to %d " % (initial_index, end_index))
        images_to_process = self.train_images[initial_index:end_index]
        boxes_to_process = self.train_boxes[initial_index:end_index]
        # processed
        p_images, p_boxes = process_data(images_to_process, boxes_to_process)
        detectors_mask, matching_true_boxes = get_detector_mask(p_boxes, YOLO_ANCHORS)

        yield([p_images, p_images, detectors_mask, matching_true_boxes],  np.zeros(len(p_images)))

if __name__ == '__main__':
    a = TrainingData(np.load('/Users/flynn/Documents/DeepLeague/data_training_set.npz'))
    a.load_train_batch(32)
    next(a.load_train_batch(32))
    a.load_train_batch(32)
