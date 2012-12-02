
#
# FishPi - An autonomous drop in the ocean
#
# NavigationUnit, PathPlanner, NavigationController
#  - Provides navigation capabilities
#  - Responsible for:
#       - planning route to goal (via waypoints)
#       - controlling drive and steering to maintain course
#

import logging

class NavigationUnit:
    """ Coordinator between internal perception model, outer high level command software (UI or AI), path planning through to drive control and course maintainence."""
    
    def __init__(self, perception_unit, drive_controller, vehicle_constants):
        self._perception_unit = perception_unit
        self._drive_controller = drive_controller
        self._vehicle_constants = vehicle_constants
        
        # local behaviour components
        self._drive_ctrl = BasicPIDControl(vehicle_constants.pid_drive_gain_p, vehicle_constants.pid_drive_gain_i, vehicle_constants.pid_drive_gain_d)
        self._heading_ctrl = BasicPIDControl(vehicle_constants.pid_heading_gain_p, vehicle_constants.pid_heading_gain_i, vehicle_constants.pid_heading_gain_d)
        
    
        self._enabled = False
        self._desired_speed = 0.0
        self._desired_heading = 0.0
    
    @property
    def auto_mode_enabled(self):
        return self._enabled
    
    # update loop
    
    def update(self):
        """ Update drive output for new observations. """
        if self._enabled:
            # current observed state
            observed_speed = self._perception_unit.observed_speed
            observed_heading = self._perception_unit.observed_heading
            
            # TODO: update desired speed and heading from path / waypoint checks
            desired_speed, desired_heading = self._desired_speed, self._desired_heading
        
            logging.debug("NAV:\tobserved vs desired (speed, heading):\t(%f, %f) vs (%f, %f)", observed_speed, observed_heading, desired_speed, desired_heading)
            
            # current drive settings
            current_throttle = self._drive_controller.throttle_level
            current_steering = self._drive_controller.steering_angle
            
            # TODO: determine new drive settings based on desired vs observed speed and heading values
            dt = 0.2
            new_throttle = self._drive_ctrl.update(desired_speed, observed_speed, dt)
            new_steering = self._heading_ctrl.update(desired_heading, observed_heading, dt)
            
            logging.debug("NAV:\tcurrent vs new (throttle, steering):\t(%f, %f) vs (%f, %f)", current_throttle, current_steering, new_throttle, new_steering)
            
            # set new drive settings (could return these)
            self._drive_controller.set_throttle(new_throttle)
            self._drive_controller.set_steering(new_steering)
        else:
            pass
    
    # control commands
    
    def navigate_to(self, route):
        """ Navigate a given route. """
        pass
    
    def set_speed(self, speed):
        """ Set speed to maintain. """
        self._desired_speed = speed
        self.start()
    
    def set_heading(self, heading):
        """ Set heading to maintain. """
        self._desired_heading = heading
        self.start()
    
    def start(self):
        """ Enable navigation control. """
        self._enabled = True
    
    def stop(self):
        """ All HALT the engines...! Disable self-navigation control. """
        # stop navigation control
        self._enabled = False

        # stop engines
        self._drive_controller.halt()
        
        # reset desired speed, heading
        self._desired_speed = 0.0
        self._desired_heading = 0.0

class BasicPIDControl:
    """ Basic discrete PID controller for supplied gain. """

    def __init__(self, gain_p, gain_i = 0.0, gain_d = 0.0):
        # setup constants
        self.gain_p = gain_p
        self.gain_i = gain_i
        self.gain_d = gain_d
        # initialise loop variables
        self.integrated_error = 0.0
        self.last_error = 0.0
        self.last_var_desired = 0.0

    def update(self, v_d, v_m, dt):
        """ Calculate the plant signal based on variables (desired vs measured) for given update time (dt). """

        # check if need reset
        if v_d != self.last_var_desired:
            self.reset()
            self.last_var_desired = v_d
        
        # calculate error
        error = v_d - v_m
        
        # calculate response
        p = self.gain_p * error
            
        self.integrated_error += error * dt
        i = self.gain_i * self.integrated_error

        d_error = (error - self.last_error) / dt
        d = self.gain_d * d_error
        self.last_error = error
        
        response = p + i + d
                
        # TODO: apply eg deadband, saturation
        
        # return response
        return response

    def reset(self):
        """ Resets the integral and derivative parts of loop, eg after a change to the desired variable. """
        self.integrated_error = 0.0
        self.last_error = 0.0
        self.last_var_desired = 0.0


class PathPlanner:
    """ Responsible for providing navigation unit with waypoints to final goal"""

    def plan_route(self, currentLocation, waypoints):
        """ Plans route based on predicted current location and waypoints (to include final goal). """
        pass

    def get_next_waypoint(self, currentLocation):
        """ Gets next waypoint on route. """
        pass

    def check_at_goal(self, currentLocation):
        """ Checks if reached final goal location. """
        pass


class NavigationController:
    """ Responsible for providing navigation unit with direction, heading, speeds etc to maintain course towards waypoints or goal. 
        Initially simple point to point, likely to extend to PID with smooth curves around buoys etc"""

    def update(self, currentLocation):
        """ Update step for current location (measure) and gets control adjustment. """
        pass
