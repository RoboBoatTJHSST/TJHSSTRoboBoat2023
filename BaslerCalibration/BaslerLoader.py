import torch
import numpy as np
from pypylon import pylon
from BaslerCalibration.basler_config import BaslerConfig


class LoadBasler:
    # YOLOv5 streamloader, i.e. `python detect.py --source 'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP streams`
    def __init__(self):
        torch.backends.cudnn.benchmark = True  # faster for fixed-size inference
        # Create an instant camera object with the camera device found first.
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.RegisterConfiguration(BaslerConfig(False), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
        # Make converter to turn image into opencv format
        self.converter = pylon.ImageFormatConverter()
        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        # Print the model name of the camera.
        print("Using device ", self.camera.GetDeviceInfo().GetModelName())
        # Start the grabbing of c_countOfImagesToGrab images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        self.camera.StartGrabbingMax(10000, pylon.GrabStrategy_LatestImageOnly)

    def __iter__(self):
        return self

    def __next__(self):
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        im = None
        image = None
        grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        # Image grabbed successfully?
        if grab_result.GrabSucceeded():
            # Access the image data
            image = self.converter.Convert(grab_result)
            image = image.GetArray().copy()
            im = np.asarray(image)
            im = np.ascontiguousarray([im.transpose((2, 0, 1))])
        else:
            # grabResult.ErrorDescription does not work properly in python could throw UnicodeDecodeError
            print("Error: ", grab_result.ErrorCode)
        grab_result.Release()

        return 'basler', im, image, None, ''

    def __len__(self):
        return 10000000000000
