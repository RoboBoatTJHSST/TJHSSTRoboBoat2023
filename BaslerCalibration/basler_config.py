from pypylon import genicam, pylon

AOI_WIDTH = 800
AOI_HEIGHT = 800


class BaslerConfig(pylon.ConfigurationEventHandler):
    def __init__(self, trigger: bool, *args):
        super().__init__(*args)
        self.trigger = trigger

    def apply_config(self, node_map: genicam.INodeMap):
        # Disable all trigger types except the trigger type used for triggering the acquisition of
        # frames.
        if self.trigger:
            # Get required enumerations.
            trigger_selector = node_map.GetNode("TriggerSelector")
            trigger_mode = node_map.GetNode("TriggerMode")

            # Check the available camera trigger mode(s) to select the appropriate one: acquisition start trigger mode
            # (used by older cameras, i.e. for cameras supporting only the legacy image acquisition control mode;
            # do not confuse with acquisition start command) or frame start trigger mode
            # (used by newer cameras, i.e. for cameras using the standard image acquisition control mode;
            # equivalent to the acquisition start trigger mode in the legacy image acquisition control mode).
            trigger_name = "FrameStart"
            if trigger_name not in trigger_selector.GetSymbolics():
                trigger_name = "AcquisitionStart"
                if trigger_name not in trigger_selector.GetSymbolics():
                    raise pylon.RuntimeException(
                            "Could not select trigger. Neither FrameStart nor AcquisitionStart is available.")

            # Get all enumeration entries of trigger selector.
            trigger_selector_entries = trigger_selector.GetSymbolics()

            # Turn trigger mode off for all trigger selector entries except for the frame trigger given by triggerName.
            for trigger_selector_entry in trigger_selector_entries:
                # Set trigger mode to off.
                trigger_selector.SetValue(trigger_selector_entry);
                if trigger_name == trigger_selector_entry:
                    # Activate trigger.
                    trigger_mode.SetValue("On")

                    # The trigger source must be set to 'Software'.
                    node_map.GetNode("TriggerSource").SetValue("Software")
                else:
                    trigger_mode.SetValue("Off")
            # Finally select the frame trigger type
            trigger_selector.SetValue(trigger_name)

        # Set acquisition mode.
        node_map.GetNode("AcquisitionMode").SetValue("Continuous")

        # Set AOI
        node_map.GetNode("Width").SetValue(AOI_WIDTH)
        node_map.GetNode("Height").SetValue(AOI_HEIGHT)
        node_map.GetNode("BslCenterX").Execute()
        node_map.GetNode("BslCenterY").Execute()

        # Set Exposure
        EXPOSURE_TIME_US = 30000
        node_map.GetNode("ExposureTime").SetValue(EXPOSURE_TIME_US)

        # Set Pixel Format
        node_map.GetNode("PixelFormat").SetValue("BGR8")

        # Set FPS
        node_map.GetNode("AcquisitionFrameRateEnable").SetValue(True)
        node_map.GetNode("AcquisitionFrameRate").SetValue(30.0)

    def OnOpened(self, camera: pylon.InstantCamera):
        try:
            self.apply_config(camera.GetNodeMap())
        except pylon.GenericException as e:
            print(f"ERROR: {e}")
