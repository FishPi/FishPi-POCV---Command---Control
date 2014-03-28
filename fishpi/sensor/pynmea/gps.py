import bluetooth


class GPSReader(object):
    def __init__(self):
        target = "BT-GPS"
        nearby_devices = bluetooth.discover_devices()
        for dev in nearby_devices:
            if bluetooth.lookup_name(dev) == target:
                # Get GPS stuff
                pass



if __name__ == "__main__":
    gps = GPSReader()