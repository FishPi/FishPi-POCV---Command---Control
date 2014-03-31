#
# FishPi - An autonomous drop in the ocean
#
# This is the Fabric deployment file

# What this file should do:
#
# Install tools needed for deploy and installation:
#	- check if pip is installed, install it otherwise
# 	- check if git is installed, install it otherwise
#
# Install FishPi dependencies:
# 	- Install Python modules with pip: use requirements.txt
#	- Install other requirements with apt-get
#
# Deploy FishPi code:
# Option 1: Use git
# 	- check if there are uncommitted changes on the local machine
#	- commit changes if necessary
#	- pull changes from git on remote device
#
# Option 2: Use secure copy
#	- delete remote code
#	- copy local code to remote device
#
# Generally option 1 should be used. However, it might at some point be
# impossible or undesirable to let the remote device have internet access.
# In this case option 2 can be used.
