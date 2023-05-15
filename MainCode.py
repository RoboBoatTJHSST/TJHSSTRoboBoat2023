#this is the main piece of code that will call on the other software files
import TaskManager as tm
import cv2
from cv2 import *
import requests
from bs4 import BeautifulSoup
import xyz_to_gps
import pixhawkMessager
import detect
import PyLidarMapper.pymapper as limap

def getTask(url):
    r = requests.get(url)
    return r.text
html = getTask('https://roboboat-groundstation.sites.tjhsst.edu/tasknum/1')
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)
"""initialize the necessary things first, probably a boat object"""
while True: 
    task = getTask('enter url')
    if task: #if there is a task to do
        opt = detect.parse_opt()
        rawoutput = detect.main(opt)
        while rawoutput: #while there are still buoys/relevant objects:
            buoys = {}
            for x in rawoutput:
                if "green" in rawoutput[x]: buoys[x] = "Green"
                elif "red" in rawoutput[x]: buoys[x] = "Red"
                elif "yellow" in rawoutput[x]: buoys[x] = "Yellow"
                elif "black" in rawoutput[x]: buoys[x] = "Black"
                elif "blue" in rawoutput[x]: buoys[x] = "Blue"
            limap.start()
            convertedbuoydata = {}
            for data in buoys:
                print()
                pt =limap.find_sphere(data[0], data[1], data[2], data[3])
                convertedbuoydata[pt] = buoys[(data[0], data[1], data[2], data[3])]
            limap.end()
            #using the buoy location and color data collected from CV and lidar, call task manager to output 3d points that the boat needs to go to
            convertedbuoydata = {(3,1,2): "Green", (5,6,1): "Red", (1,5,2): "Red", (2,6,4): "Black", (2,5,3): "Green", (5,2,6): "Yellow"}
            waypt = tm.task1(convertedbuoydata)
            print(waypt)
            #convert pt to gps coordinates
            pixhawkMessager.init()
            location = pixhawkMessager.getlocation()
            boat_lat, boat_long = location['lat'], location['long']
            direction = location["hdg"]
            NS, EW = xyz_to_gps.xyz_to_NSEW(waypt[0], waypt[1], direction)
            new_lat, new_long = xyz_to_gps.path_coords(boat_lat, boat_long, NS, EW)
            pixhawkMessager.create_waypoint(new_lat, new_long)
            """followPoint(boat, lat, long)
            boat is the boat object, need to set up before hand"""
            print('') 
    else:
        if task == 0: #assign a special value to terminate the program if we're done
            break
