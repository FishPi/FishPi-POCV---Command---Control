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

<<<<<<< HEAD
#### Required Software ####
To install Fishpi, you need Python 2.7, pip, and git. 

On a Debian-style Linux you just have to do this:
apt-get install python-dev python-pip git

For OXS and Windows, you can find instructions here:
Python: https://www.python.org/download/ (Make sure you get Python 2.7!)
git: http://git-scm.com/book/en/Getting-Started-Installing-Git
pip: http://pip.readthedocs.org/en/latest/installing.html

#### Installation on local machine:

Now, installation works the same way on all platforms:
Open the command line tool of your choice and type in the commands below. If the installation fails with a permission error, prepend each line with a "sudo" on Linux and OSX. On Windows open the terminal with administrator rights and try again.

pip install fabric
git clone https://github.com/FishPi/FishPi-POCV---Command---Control.git
cd FishPi-POCV---Command---Control
fab install_desktop

#### Installation on embedded device (RaspberryPi or BeagleBone Black):
Make sure you have a network connection to the embedded device and the device has internet access.
Open a command line on your local machine, navigate to the FishPi directory and run the command below. Replace "remote_host" with the IP of your embedded device. You will be prompted for the root password of your device. 

fab install_embedded -H remote_host

Wait and let Fabric do its magic. :-) Done!
=======
Clone this repository to your local machine.

#### To install FishPi on your local machine:
- Make sure you have pip installed.
- Open a terminal, navigate to your FishPi directory and run "pip install -r requirements.txt".

#### To install FishPi on the embedded device (RaspberryPi or BeagleBone Black):
- Install Fabric on your local machine (see the "How to install Fabric" file).
- Make sure you have a network connection to the embedded device and the device has internet access.
- Open a terminal session on your local machine, navigate to the FishPi directory and run "fab full_install".
- When prompted for a host, specify the remote device like this: "username@host_address", you will then be asked for the user password.
- Wait and let Fabric do its magic. :-) Done!
>>>>>>> 57ab7582273a8fbf5721a775342e28ae37671717


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

