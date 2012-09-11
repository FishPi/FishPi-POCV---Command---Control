
#
# FishPi - An autonomous drop in the ocean
#
# NavigationUnit, PathPlanner, NavigationController
#  - Provides navigation capabilities
#  - Responsible for:
#       - planning route to goal (via waypoints)
#       - controlling drive and steering to maintain course
#

class NavigationUnit:
    """ Coordinator between internal perception model, outer high level command software (UI or AI), path planning through to drive control and course maintainence."""
    
    def __init__(self, driveController, perceptionUnit):
        self.driveController = driveController
        self.perceptionUnit = perceptionUnit
    
    def NavigateTo(self, route):
        """ Navigate a given route. """
        pass

    def Halt(self):
        """ All HALT the engines...! """
        pass



class PathPlanner:
    """ Responsible for providing navigation unit with waypoints to final goal"""

    def PlanRoute(self, currentLocation, waypoints):
        """ Plans route based on predicted current location and waypoints (to include final goal). """
        pass

    def GetNextWaypoint(self, currentLocation):
        """ Gets next waypoint on route. """
        pass

    def CheckAtGoal(self, currentLocation):
        """ Checks if reached final goal location. """
        pass


class NavigationController:
    """ Responsible for providing navigation unit with direction, heading, speeds etc to maintain course towards waypoints or goal. 
        Initially simple point to point, likely to extend to PID with smooth curves around buoys etc"""

    def Update(self, currentLocation):
        """ Update step for current location (measure) and gets control adjustment. """
        pass