#this is the main piece of code that will call on the other software files
import TaskManager as tm
import cv2
from cv2 import *
import requests
from bs4 import BeautifulSoup
import xyz_to_gps
import pixhawkMessager
import detect
#import lidarmapping
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
print(remove_tags(html))
"""initialize the necessary things first, probably a boat object"""
while True: #do everything in the while loop. Whenever groundstation sends us information, such as which task we're doing, perform the task in the while loop
    # the loop will end when groundstation sends a certain type of data.
    """
    groundstation will be a webserver on the jetson, so there will be a python function that will access the webserver and return
    the task number that we need to do. that means there will be another python file that this code needs to import, and the python function
    is something that lauren needs to do.
    """
    task = getTask('enter url')
    if task: #if there is a task to do
        #get data from camera
        cam = VideoCapture()
        result, image = cam.read()
        #Run Yolo once to detect relevant objects
        # CV: send image data from camera: output pixels of buoys and their respective colors (dict{pixel: color})
        # ideally, cv should take the border of the buoys and average them to a single pixel value that represents the 
        # center of the buoy and assigns it to that color
        opt = detect.parse_opt()
        detect.main(opt)
        buoys = {("centerCoord","radius" ): 'color'} #return format of YOLO
        while buoys:
            convertedbuoydata = {}
            for centerCoord, radius in buoys:
                print()
                pt =lidarmapping.convertCircleTo3D(centerCoord, radius)
                convertedbuoydata[pt] = buoys[(centerCoord, radius)]
            #using the buoy location and color data collected from CV and lidar, call task manager to output 3d points that
            #the boat needs to go to
            buoys = {(3,1,2): "Green", (5,6,1): "Red", (1,5,2): "Red", (2,6,4): "Black", (2,5,3): "Green", (5,2,6): "Yellow"}
            waypt = tm.task1(buoys)
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
            #while there are still buoys/relevant objects:
            # CV: send image data from camera: output pixels of buoys and their respective colors (dict{pixel: color})
            # ideally, cv should take the border of the buoys and average them to a single pixel value that represents the 
            # center of the buoy and assigns it to that color
            buoys = {"pixel": 'color'}
    else:
        if task == 0: #assign a special value to terminate the program if we're done
            break