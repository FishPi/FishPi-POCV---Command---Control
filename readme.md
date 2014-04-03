FishPi Proof-Of-Concept-Vehicle
===============================

This github repo contains the software for the FishPi POCV.

FishPi
------

FishPi is an autonomous marine vessel being developed with the aim of crossing the Atlantic unaided. Currently a Proof-Of-Concept-Vehicle is being built and the software for it lies here. The FishPi will use the [Raspberry Pi](http://www.raspberrypi.org/) at its heart. For more info on the FishPi see http://fishpi.org/. The Proof-Of-Concept-Vehicle (POCV) is a small model sized craft demonstrating the principles needed for autonomous control of a marine surface vessel.

Roadmap
-------

* v0.1 will support a manual UI mode, fly-by-wire control of motor and rudder, sensor readings (GPS, Compass, Gyro, Temperature) and camera control.
* v0.2 will support route planning, basic behaviours (course setting (heading and speed), waypoint following, path tracking), basic control algorithms (PID / adaptive linear model).
* v0.3 will support remote (web) UI mode, improved testing and calibration of control parameters, increased logging / diagnostics / playback.
* v0.4 will support further behaviours (path planning, loiter, manouver, obstacle avoidance), offline testing setup.

Software
--------

The FishPi software is being developed in Python (2.7) inline with the educational aims of the Raspberry Pi.

### Installation ###

Clone this repository to your local machine.

To install FishPi on your local machine:
-Make sure you have pip installed.
-Open a terminal, navigate to your FishPi directory and run "pip install -r requirements.txt".

To install FishPi on the embedded device (RaspberryPi or BeagleBone Black):
-Install Fabric on your local machine (see the "How to install Fabric" file).
-Make sure you have a network connection to the embedded device and the device has internet access.
-Open a terminal session on your local machine, navigate to the FishPi directory and run "fab full_install".
-When prompted for a host, specify the remote device like this: "username@host_address", you will then asked for the user password.
-Wait and let Fabric do its magic. :-) Done!


### Usage ###

Start the software by running `./fishpi/fishpi.py`.

Additional arguments supported include:
* `--help:            show this help message and exit`
* `--mode {inactive,local,manual,remote,auto}:   operational mode to run`
* `--debug:           increase debugging information output`
* `--version:         show program's version number and exit`

### Structure ###

Top level package:
* 'fishpi' 
    
Subpackages:
* 'sensor'
* 'perception'
* 'control'
* 'vehicle'
* 'ui'

### Tests ###

Test sub components and hardware with eg `./fishpi/sensor/test_GPS_I2C.py`.

License
-------

BSD 2-Clause License.

