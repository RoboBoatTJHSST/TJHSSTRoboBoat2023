import time
from pymavlink import mavutil, mavwp
import sys; args = sys.argv[1:]

MANUAL = 0
AUTO = 10
GUIDED = 15


pixhawkConnection = None
returnPoints = dict()

if args: port = args[0]
else: port = 5


def init() -> None:
	global pixhawkConnection

	# Create the connection
	pixhawkConnection = mavutil.mavlink_connection('COM6')

	# Wait for a heartbeat before sending commands
	print(pixhawkConnection.wait_heartbeat())

	# Make sure the pixhawk is armed
	pixhawkConnection.armed = True


	# set_mode_autopilot(GUIDED)

	# message = pixhawkConnection.mav.command_long_encode(
    #     pixhawkConnection.target_system, pixhawkConnection.target_component,
    #     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
	# 	0, 0, 0, 0, 0, 0, 0)
	# pixhawkConnection.mav.send(message)

def get_system_status():
	systemStatusMessage = pixhawkConnection.mav.command_long_encode(1, 0,
		1, 0,
		1,
		0, 0, 0, 0, 0, 0)
	pixhawkConnection.mav.send(systemStatusMessage)
	return pixhawkConnection.recv_match(type = "SYS_STATUS")

def get_current_mode():
	return pixhawkConnection.wait_heartbeat()


# def set_mode_autopilot(mode):
# 	message = pixhawkConnection.mav.command_long_encode(
#         pixhawkConnection.target_system, pixhawkConnection.target_component, # stuff that you should always put at the start
#         mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,		# name of the command
#         mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode, 0, 0, 0, 0, 0)  # arguments
	
# 	pixhawkConnection.mav.send(message)
# 	print(get_current_mode())


def get_location() -> tuple:
	gpsMessage = pixhawkConnection.mav.command_long_encode(1, 0,
		mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
		33, # this cooresponds to the enum GLOBAL_POSITION_INT
		0, 0, 0, 0, 0, 0)
	pixhawkConnection.mav.send(gpsMessage)
	try:
		return pixhawkConnection.recv_match(type = "GLOBAL_POSITION_INT")
	except:
		print("failed to get location")

def set_servo_pwm(microseconds: int, pwmPort: int = 5) -> None:
	# this is a shorthand for the whole sending a command thing
	pixhawkConnection.set_servo(pwmPort, microseconds)

	# pixhawkConnection.mav.command_long_send(
    # 	pixhawkConnection.target_system, pixhawkConnection.target_component,
    #     mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
    #     0,            # first transmission of this command
    #     pwmPort + 8, # servo instance, offset by 8 MAIN outputs if you are connected to the pwm port on the right hand side
    #     microseconds, # PWM pulse-width
    #     0,0,0,0,0     # unused parameters
    # )

	

# for auto mode?
def create_waypoint(latitude: float, longitude: float):
	latitude = int(latitude * 10**7); longitude = int(longitude * 10**7)

	message = pixhawkConnection.mav.command_long_encode(
        pixhawkConnection.target_system, pixhawkConnection.target_component, # random stuff to include
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, # name of the mavlink command
        0, 0.2, 0, 0, latitude, longitude, 0)	# arguments to the command
	pixhawkConnection.mav.send(message)

# for guided mode?
def set_target_position(latitude: float, longitude: float):
	latitude = int(latitude * 10**7); longitude = int(longitude * 10**7)

	message = mavutil.mavlink.MAVLink_set_position_target_global_int_message(
		10, 
		pixhawkConnection.target_system, pixhawkConnection.target_component, 
		mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 	# reference frame
		int(0b110111111000),
		latitude, longitude,
		0,0,0,0,0,0,0,1.57,0.5
	)
	pixhawkConnection.mav.send(message)


def create_waypoints_through_waypoint_manager(latitude: float, longitude: float):
	latitude = int(latitude * 10**7); longitude = int(longitude * 10**7)

	wp = mavwp.MAVWPLoader()
	waypointMessage = mavutil.mavlink.MAVLink_mission_item_message(pixhawkConnection.target_system,
        pixhawkConnection.target_component,
        1,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        0, 0, 0, 10, 0, 0,
        latitude,longitude, 0)
	wp.add(waypointMessage)

	# its either one of these
	# pixhawkConnection.mav.send(waypointMessage)
	pixhawkConnection.mav.send(wp.wp(0)) 

	msg = pixhawkConnection.recv_match('MISSION_REQUEST',blocking=True) # could be MISSION_REQUESTION instead of WAYPOINT_REQUEST            
	pixhawkConnection.mav.send(wp.wp(1)) 
	print('Sending waypoint {0}'.format(1))


def get_guided_mode_waypoints():
	gpsConfirmationMessage = pixhawkConnection.mav.command_long_encode(1, 0,
		mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
		87,		# requests the current position POSITION_TARGET_GLOBAL
		0, 0, 0, 0, 0, 0)
	pixhawkConnection.mav.send(gpsConfirmationMessage)
	return pixhawkConnection.recv_match(type = "POSITION_TARGET_GLOBAL_INT")

def main():
	init()

	# pixhawkConnection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, pixhawkConnection.target_system,
	# 	pixhawkConnection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
	# 	int(0b110111111000), int(-35.3629849 * 10 ** 7), int(149.1649185 * 10 ** 7), 10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))

	# THIS IS THE IMPORTANT ONE
	# pixhawkConnection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, pixhawkConnection.target_system,
    #     pixhawkConnection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
	# 	int(0b010111111000), 40, 0, -10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))

	# while True:
	# 	set_servo_pwm(1600)

	set_servo_pwm(1600)


	# while True:
	# 	for i in range(1000, 2000):
	# 		set_servo_pwm(i)

if __name__== "__main__": main()
