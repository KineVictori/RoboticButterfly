
import cv2
import sys
import numpy

PREVIEW  = 0  # Preview Mode
CANNY    = 1  # Canny Edge Detector

feature_params = dict(maxCorners=500, qualityLevel=0.2, minDistance=15, blockSize=9)


# default camera device index = 0
camera_index = 0

# check if cmd override default value
if len(sys.argv) > 1:
    camera_index = sys.argv[1]


image_filter = CANNY
alive = True

win_name = 'Camera Test'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None
# creating video capture object
camera_input = cv2.VideoCapture(camera_index)

# naming the window to send camera output to


# stream video from camera, unless escape key is pressed
#while cv2.waitKey(1) != 27: # 27 = Escape key
 #   has_video, video = camera_input.read()
  #  if not has_video:
   #     break
    #cv2.imshow(win_name, video)


while alive:
    has_video, video = camera_input.read()
    if not has_video:
        break

    video = cv2.flip(video, 1)

    if image_filter == PREVIEW:
        result = video
    elif image_filter == CANNY:
        # combining blur and canny for filtering out noise
        new = cv2.bilateralFilter(video, 9, 75, 75)
        result = cv2.GaussianBlur(new, (11, 11), 2.5)

    cv2.imshow(win_name, result)

    key = cv2.waitKey(1)
    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False
    elif key == ord("C") or key == ord("c"):
        image_filter = CANNY
    elif key == ord("P") or key == ord("p"):
        image_filter = PREVIEW



# stop camera and destroy window
camera_input.release()
cv2.destroyWindow(win_name)
