#!/usr/bin/python
#
# FishPi - An autonomous drop in the ocean
#
# Camera viewer test server
#


import io
import socket
import struct

if __name__ == "__main__":

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    connection = server_socket.accept()[0].makefile('rb')

    test_image = open('test.bmp', 'rb')
    stream = io.open('test.bmp', 'rb')
    stream.seek(0, 2)

    # mh, always writing 0...
    try:
        while True:
            print("Writing %s" % stream.tell())
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0, 2)
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        server_socket.close()
        stream.close()
