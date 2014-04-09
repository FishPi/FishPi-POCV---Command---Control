#
# FishPi - An autonomous drop in the ocean
#
# This is the Fabric deployment file

from __future__ import with_statement
from fabric.api import cd, env, local, run, sudo, settings
from fabric.utils import puts

import os
import platform
import sys


embedded_code_dir = '/usr/local/src/fishpi/'


def determine_system_info():
    env.os = platform.system()
    if env.os == 'Linux':
        env.os_distname, env.os_version, encv.os_id = platform.linux_distribution()


def install_embedded():
    """ Install FishPi on the embedded remote device """
    deploy_embedded()

    if not package_installed('python-pip'):
        install('python-pip')

    install_requirements(embedded_code_dir)


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


def package_installed(pkg_name):
    puts("Checking if %s is installed..." % pkg_name)
    cmd = ('dpkg-query -l "%s" | grep -q ^.i' % pkg_name)
    with settings(warn_only=True):
        result = run(cmd)
    return result.succeeded


def install(pkg_name):
    puts("Installing %s..." % pkg_name)
    sudo('apt-get --force-yes --yes install %s' % (pkg_name))


def install_requirements(code_dir):
    with cd(code_dir):
        puts("Installing required Python libraries...")
        sudo("pip install -r requirements.txt")


######################################
### Functions for local deployment ###
######################################


def install_desktop():
    """ Install FishPi on the developer machine """
    if not sys.platform.startswith('linux'):
        puts("This does not seem to be a Linux platform. Sorry, this installer only works under Linux so far. Bye!")
        return False

    if not package_installed_local('python-pip'):
        install_local('python-pip')

    # Let's install wx
    install_wx_local()

    install_local_requirements()

    # Ok, let's see if the installation of PIL succeeded. If not, install it via apt-get
    if not package_installed_local('python-imaging'):
        install_local('python-imaging')
    if not package_installed_local('Python-Imaging-Tk'):
        install_local('Python-Imaging-Tk')


def install_wx_local():
    determine_system_info()
    if env.os != 'Linux' or env.os_distname != ('debian' or 'ubuntu'):
        puts("This does not seem to be a debian-like Linux. Sorry, the Python wx installer does not work on this platform.")
        return
    if env.os_id == '':
        env.os_id = 'squeeze'  # This is a dirty fix. Would this work under Ubuntu?

    local("curl http://apt.wxwidgets.org/key.asc | sudo apt-key add -")
    local("""echo "# wxWidgets/wxPython repository at apt.wxwidgets.org
        deb http://apt.wxwidgets.org/ %s-wx main
        deb-src http://apt.wxwidgets.org/ %s-wx main" >> /etc/apt/sources.list""" % (env.os_id, env.os_id))
    local("sudo apt-get update")
    local("sudo apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n")


def package_installed_local(pkg_name):
    puts("Checking if %s is locally installed..." % pkg_name)
    cmd = ('dpkg-query -l "%s" | grep -q ^.i' % pkg_name)
    with settings(warn_only=True):
        result = local(cmd)
    return result.succeeded


def install_local(pkg_name):
    puts("Installing %s..." % pkg_name)
    local('sudo apt-get --force-yes --yes install %s' % (pkg_name))


def install_local_requirements():
    # get dir of fabfile
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with cd(current_dir):
        puts("Installing required Python libraries...")
        sudo("pip install -r requirements.txt")


#########################
### Functions for git ###
#########################


def git_upload():
    commit()
    push()


def commit():
    local("git add -p && git commit")


def push():
    local("git push")
