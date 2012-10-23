FishPi Proof-Of-Concept-Vehicle
===============================

This github repo contains the software for the FishPi POCV.

FishPi
------

FishPi is an autonomous marine vessel being developed with the aim of crossing the Atlantic unaided. Currently a Proof-Of-Concept-Vehicle is being built and the software for it lies here. The FishPi will use the [Raspberry Pi](http://www.raspberrypi.org/) at its heart. For more info on the FishPi see http://fishpi.org/.

Software
--------

The FishPi software is being developed in python 2.7 inline with the educational aims of the Raspberry Pi.

### Usage

Start the software by running `./fishpi/fishpi.py`

### Structure

Top level package 'fishpi' with subpackages 'sensor', 'perception', 'control', 'vehicle', 'ui'.

### Tests

Test sub components and hardware with eg `./fishpi/sensor/test_GPS_I2C.py`.

License
-------

BSD 2-Clause License.

