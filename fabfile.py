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


def deploy_fishpi():
    if not package_installed('git'):
        install('git')

    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            puts("Cloning FishPi repository...")
            sudo("git clone https://github.com/FishPi/FishPi-POCV---Command---Control.git %s" % code_dir)
    with cd(code_dir):
        puts("Pulling newest changes from FishPi repository...")
        sudo("git pull")


def deploy_adafruit_libs():
    with settings(warn_only=True):
        if run("test -d %s" % adafruit_dir).failed:
            puts("Cloning FishPi's Adafruit libraries repository...")
            sudo("git clone https://github.com/FishPi/FishPi-POCV---Command---Control.git %s" % adafruit_dir)
    with cd(adafruit_dir):
        puts("Pulling newest changes from FishPi's Adafruit libraries repository...")
        sudo("git pull")

def prepare_deploy():
    commit()
    push()


def full_install():
    deploy_fishpi()
    deploy_adafruit_libs()
    install_requirements()
