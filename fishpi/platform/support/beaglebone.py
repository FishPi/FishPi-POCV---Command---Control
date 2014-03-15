#
# FishPi - An autonomous drop in the ocean
#
# Support Code for BeagleBone Black

class BeagleBoneSupport(object):
	""" Support package for BeagleBone. Exports the overlays from the device tree for the used hardware """

	def __init__(self):
		pass

	def configure_interface(self, name):
		""" Export a specific overlay which is identified by name, such as "I2C2" or "UART4" """

		if name == "I2C2":
			pass
		elif name == "UART1":
			pass
		elif name == "UART2":
			pass
		elif name == "UART3":
			pass
		elif name == "UART4":
			pass
		# ... more devices here
	else:
		logging.error("BBB-Support:\tInterface %s unknown.", name)
		return

		# It's basically just executing a shell command, that exports the device.
		# Each if/elif specifies a string that gets put into the exec command that is issued at the end.