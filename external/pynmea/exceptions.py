""" Collection of pynmea specific errors
"""

class NoDataGivenError(Exception):
    def __init__(self, message):
        self.message = message