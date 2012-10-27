""" Functions that get used by multiple classes go in here
"""


def checksum_calc(nmea_str):
    """ Loop through all of the given characters and xor the current to the
        previous (cumulatively).
    """
    chksum_val = 0
    nmea_str = nmea_str.replace('$', '')
    nmea_str = nmea_str.split('*')[0]
    for next_char in nmea_str:
        chksum_val ^= ord(next_char)

    return "%02X" % chksum_val

