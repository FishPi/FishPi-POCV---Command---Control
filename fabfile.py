#
# FishPi - An autonomous drop in the ocean
#
# This is the Fabric deployment file

from __future__ import with_statement
from fabric.api import cd, local, run, sudo, settings
from fabric.utils import puts

import sys


embedded_code_dir = '/usr/local/src/fishpi/'


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

def install_requirements(code_dir):
    # check if pip is installed
    if not package_installed('python-pip'):
        install('python-pip')
    with cd(code_dir):
        puts("Installing required Python libraries...")
        sudo("pip install -r requirements.txt")


def deploy_embedded():
    if not package_installed('git'):
        install('git')

    with settings(warn_only=True):
        if run("test -d %s" % embedded_code_dir).failed:
            puts("Cloning FishPi repository...")
            sudo("git clone https://github.com/SvenChmie/FishPi-POCV---Command---Control.git %s" % embedded_code_dir)
    with cd(embedded_code_dir):
        puts("Pulling newest changes from FishPi repository...")
        sudo("git pull")


def prepare_deploy():
    commit()
    push()


def install_embedded():
    """ Install FishPi on the embedded remote device """
    deploy_embedded()
    install_requirements(embedded_code_dir)


def install_desktop():
    """ Install FishPi on the developer machine """
    install_requirements('')
    # Install PIL in case it failed with pip (which it sometimes does)
    # and Imaging-TK on Linux.
    if sys.platform.startswith('linux'):
        if not package_installed('python-imaging'):
            install('python-imaging')
        if not package_installed('Python-Imaging-Tk'):
            install('Python-Imaging-Tk')
