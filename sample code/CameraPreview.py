import cv2
import sys

s = 0  # hard coded
if len(sys.argv) > 1:  # if system has any arguments to not open camera (i.e. no permission)
    s = sys.argv[1]

source = cv2.VideoCapture(s)


# Create window
win_name = 'Camera Preview'
cv2.namedWindow(win_name)


def draw_box(feed, pos, colour):
    end_x = pos[0] + 800
    end_y = pos[1] + 500

    cv2.rectangle(feed, pos, (end_x, end_y), colour, 2)


while cv2.waitKey(1) != 27:  # Escape
    has_frame, frame = source.read()
    if not has_frame:
        break

    # getting window size
    windowWidth = frame.shape[1]
    windowHeight = frame.shape[0]

    start_x = (windowWidth // 2) - 400
    start_y = (windowHeight // 2) - 250

    # draw box onto image
    draw_box(frame, (start_x, start_y), (255, 212, 108))

    # flip webcam frame
    horizontally_flipped_frame = cv2.flip(frame, 1)

    # display camera feed
    cv2.imshow(win_name, horizontally_flipped_frame)

source.release()
cv2.destroyWindow(win_name)
