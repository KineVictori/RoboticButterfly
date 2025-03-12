
import cv2
import sys

# default camera device index = 0
camera_index = 0

# check if cmd override default value
if len(sys.argv) > 1:
    camera_index = sys.argv[1]

# creating video capture object
camera_input = cv2.VideoCapture(camera_index)

# naming the window to send camera output to
win_name = 'Camera Test'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# stream video from camera, unless escape key is pressed
while cv2.waitKey(1) != 27: # 27 = Escape key
    has_video, video = camera_input.read()
    if not has_video:
        break
    cv2.imshow(win_name, video)

# stop camera and destroy window
camera_input.release()
cv2.destroyWindow(win_name)