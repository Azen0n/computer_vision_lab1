import cv2
import numpy as np
from PIL import Image

from base.lab3 import difference_of_gaussian


def main():
    capture = cv2.VideoCapture('starry.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = capture.get(cv2.CAP_PROP_FPS)
    video = cv2.VideoWriter('starry_edges.mp4', fourcc, fps, size)
    while capture.isOpened():
        ret, image = capture.read()
        if image is None:
            break
        image = Image.fromarray(image)
        new_image = difference_of_gaussian(image, 2, 0.5)
        video.write(np.asarray(new_image))
        print('Frame completed')

    capture.release()
    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
