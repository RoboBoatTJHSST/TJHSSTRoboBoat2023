from pypylon import pylon
from pypylon import genicam
from BaslerCalibration.basler_config import BaslerConfig
import cv2
import time

try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.RegisterConfiguration(BaslerConfig(False), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)

    # Make converter to turn image into opencv format
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())
    cv2.namedWindow('title', cv2.WINDOW_NORMAL)

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(10000, pylon.GrabStrategy_LatestImageOnly)

    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
            cv2.imshow('title', img)
            if cv2.pollKey() == ord('q'):
                break
        else:
            # grabResult.ErrorDescription does not work properly in python could throw UnicodeDecodeError
            print("Error: ", grabResult.ErrorCode)
        grabResult.Release()
        time.sleep(0.05)

    # camera has to be closed manually
    camera.Close()

except genicam.GenericException as e:
    # Error handling.
    print(f"An exception occurred: {e}")
