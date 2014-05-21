
#
# FishPi - An autonomous drop in the ocean
#
# Commands for RPC interface
#


from twisted.protocols.amp import Boolean, Integer, String, Float, Command


class Sum(Command):
    arguments = [('a', Integer()),
                 ('b', Integer())]
    response = [('status', Integer())]


class HeartbeatCmd(Command):
    arguments = [('enabled', Boolean())]
    response = [('status', Boolean())]
    requiresAnswer = False


class HaltCmd(Command):
    arguments = []
    response = [('status', Boolean())]
    requiresAnswer = False


class ModeCmd(Command):
    arguments = [('mode', String())]
    response = [('status', String())]
    requiresAnswer = False


class QueryStatus(Command):
    arguments = []
    response = [('fix', Boolean()),
                ('lat', Float()),
                ('lon', Float()),
                ('gps_heading', Float()),
                ('gps_speed', Float()),
                ('altitude', Float()),
                ('num_sat', Integer()),
                ('timestamp', String()),
                ('datestamp', String()),
                ('compass_heading', Float()),
                ('temperature', Float())]


class NavigationCmd(Command):
    arguments = [('speed', Float()), ('heading', Float())]
    response = [('status', Boolean())]
    requiresAnswer = False


class ManualDriveCmd(Command):
    arguments = [('throttle', Float()), ('steering', Float())]
    response = [('status', Boolean())]
    requiresAnswer = False


class CameraCmd(Command):
    arguments = [('camera_cmd', String())]
    response = [('status', Boolean())]
    requiresAnswer = False


class ExitCmd(Command):
    arguments = []
    response = []
    requiresAnswer = False
