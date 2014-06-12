#
# FishPi - An autonomous drop in the ocean
#
# This is the Fabric deployment file

from __future__ import with_statement
from fabric.api import cd, local, run, sudo, settings
from fabric.utils import puts

code_dir = '/usr/local/src/fishpi/'
adafruit_dir = code_dir + 'external/adafruit/'


def package_installed(pkg_name):
    puts("Checking if %s is installed..." % pkg_name)
    cmd = ('dpkg-query -l "%s" | grep -q ^.i' % pkg_name)
    with settings(warn_only=True):
        result = run(cmd)
    return result.succeeded


def install(pkg_name):
    puts("Installing %s..." % pkg_name)
    sudo('apt-get --force-yes --yes install %s' % (pkg_name))


def commit():
    local("git add -p && git commit")


def push():
    local("git push")


### High level functions ###

def install_requirements():
    # check if pip is installed
    if not package_installed('python-pip'):
        install('python-pip')
    with cd(code_dir):
        puts("Installing required Python libraries...")
        sudo("pip install -r requirements.txt")


def deploy_fishpi(system=""):
    if not package_installed('git'):
        install('git')

    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            puts("Cloning FishPi repository...")
            sudo("git clone https://github.com/FishPi/FishPi-POCV---Command---Control.git %s" % code_dir)
    with cd(code_dir):
        puts("Pulling newest changes from FishPi repository...")
        sudo("git pull")

        # now let's create the right devices.conf for the system
        system = system.lower()
        if system == "rpi" or system == "raspberry" or system == "raspberrypi":
            puts("Creating devices.conf for RaspberryPi...")
            sudo("cp --remove-destination fishpi/devices_rpi.conf fishpi/devices.conf")
        elif system == "bbb" or system == "beaglebone" or system == "beagleboneblack":
            puts("Creating devices.conf for BeagleBone Black...")
            sudo("cp --remove-destination fishpi/devices_bbb.conf fishpi/devices.conf")


def deploy_adafruit_libs():
    with settings(warn_only=True):
        if run("test -d %s" % adafruit_dir).failed:
            puts("Cloning FishPi's Adafruit libraries repository...")
            sudo("git clone https://github.com/FishPi/FishPi-POCV---Command---Control.git %s" % adafruit_dir)
    with cd(adafruit_dir):
        puts("Pulling newest changes from FishPi's Adafruit libraries repository...")
        sudo("git pull")


def clean_fishpi():
    puts("Cleaning code directory...")
    with settings(warn_only=True):
        sudo("rm -r /usr/local/src/fishpi/")


def prepare_deploy():
    commit()
    push()


def full_install(system=""):
    clean_fishpi()
    deploy_fishpi(system)
    deploy_adafruit_libs()
    install_requirements()
