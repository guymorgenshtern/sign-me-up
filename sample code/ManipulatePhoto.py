import cv2
import os


# load all available images from given folder
def __load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
            images.append(cv2.flip(img, 1))  # flip images as well
    return images


def __rotate_image(image, angle, scale=1.0):
    (height, width) = image.shape[:2]

    # get centre of image
    (centre_x, centre_y) = (height // 2, width // 2)

    # https://www.geeksforgeeks.org/python-opencv-getrotationmatrix2d-function/
    rotation_matrix = cv2.getRotationMatrix2D((centre_x, centre_y), angle, scale)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (height, width))

    return rotated_image


win_name = 'Image Manipulation'
cv2.namedWindow(win_name)

images = __load_images_from_folder("../res")

for im in images:
    # random number here, ideally should cap at how much a symbol can be rotated and still be considered the same symbol
    for i in range(10):
        cv2.waitKey(1000)
        rotated_image = __rotate_image(im, i * 5)
        cv2.imshow(win_name, rotated_image)
        # when we're ready we can use imwrite to save manipulated images to train the model with

cv2.waitKey(10000)

cv2.destroyAllWindows()