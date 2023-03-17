# inputs: gps coordinates of boat, x-y coordinates of projected path, direction of boat
# outputs: gps coordinates of projected path to send to pixhawk

import math

def get_long_shift(lat):
    earth_circumference = 24901.461 # earth circumference in miles 
    miles_per_long = math.cos( lat*math.pi/180.0 )*earth_circumference/360.0 # fomula for amount of miles per degree of longitude
    ft_per_long = 5280*miles_per_long
    long_per_ft = 1/ft_per_long
    return long_per_ft # return change in longitude per ft

# returns north-south and east-west vector components of destination
def xyz_to_NSEW(x, y, deg_dir):
    dir = deg_dir*(math.pi/180.0) # convert to radians
    cos = math.cos(dir)
    sin = math.sin(dir)
    NS = (x*cos) - (y*sin) # NS component of vector
    EW = (x*sin) + (y*cos) # EW component of vector
    return (EW, NS)


# returns gps coordinates of destination
def path_coords(lat, long, NS_change, EW_change):
    
    perFootLat = 0.00000274483 # constant change in latitude per foot movement all around Earth
    lat_shift = (perFootLat * NS_change) # total change in latitude
        
    perFootLong = get_long_shift(lat)
    long_shift = (perFootLong * EW_change)

    new_lat, new_long = (lat + lat_shift), (long + long_shift) # create new gps coordinates
    return (new_lat, new_long)


# test data
x, y = -2,2 # assuming scale of 1 foot (can easily convert later, once I figure out the scale)
boat_lat, boat_long = 38, -77 # lat, long
direction = 315 # deg CCW of Due North

NS, EW = xyz_to_NSEW(x, y, direction)
print(f'North-South component: {NS}, East-West component: {EW}')
print(f'Current coordinates {boat_lat}, {boat_long}')
new_lat, new_long = path_coords(boat_lat, boat_long, NS, EW)
print(f'New coordinates {new_lat}, {new_long}')