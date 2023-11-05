import torch
import numpy as np
import cv2
import time
import cvzone
import os

class ObjectDetection:
    """ 
    Implements YOLOv5 model for inference off webcam using OpenCV
    """

    def __init__(self, capture_index, model, testing_module):
        self.capture_index = capture_index
        self.model = model
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.testing_module = testing_module
        print("\n\nDevice Used:", self.device)

    def get_video_capture(self):

        return cv2.VideoCapture(self.capture_index)

    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, coords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, coords

    def class_to_label(self, x):
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Draws bounding box and label on frame
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.1: # param can be tuned to more accuratelly display 
                x1,y1,x2,y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) 

        return frame
    
    def draw_symbol(self, frame, symbol):
        image_path = os.path.join("res/", symbol.lower() + "-outline.png")
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        image = cv2.resize(image, (0,0), None, 0.2, 0.2)

        image_height, image_width, image_channels = image.shape
        frame_height, frame_width, frame_channels = frame.shape

        return cvzone.overlayPNG(frame, image, [10 + (image_width // 2), (image_height // 4)])

    def __call__(self):
        cap = self.get_video_capture()
        assert cap.isOpened()
        symbol_to_test = self.testing_module.get_new_test_symbol()

        while True:
            success, frame = cap.read()
            assert success
            frame = cv2.flip(cv2.resize(frame, (1248,832)), 1)
            cv2.putText(frame, "Please display \"" + symbol_to_test + "\"", (int((frame.shape[1]/2) - 110), 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
            

            if self.testing_module.check_symbol(results, symbol_to_test):
                symbol_to_test = self.testing_module.get_new_test_symbol()
            
            if(self.testing_module.get_show_symbol()):
                frame = self.draw_symbol(frame=frame, symbol=symbol_to_test)
            
            cv2.imshow('ASL Detection', frame)

            pressed_key = cv2.waitKey(1) & 0xFF

            if pressed_key == 32:
                symbol_to_test = self.testing_module.get_new_test_symbol()
            elif pressed_key == ord('s'):
                self.testing_module.set_show_symbol(True)
            elif pressed_key == 27:
                break
                
        
        cap.release()


