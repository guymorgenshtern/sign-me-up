import torch
from Detection import ObjectDetection
from TestingModule import TestingModule


class SignMeUp:

    def __init__(self, model_name):

        self.model = self.load_model(model_name)

        self.testing_module = TestingModule(self.model.names, 0.1)
        self.detection = ObjectDetection(model=self.model, capture_index=0, testing_module=self.testing_module)


    def load_model(self, model_name):
        """
        Loads YOLOv5 model from pytorch hub
        returns trained model
        """

        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        return model

    
    def __call__(self):
        self.detection()


x = SignMeUp("../400e-transfered.pt")
x()