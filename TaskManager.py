#maybe it's a good idea to pass in what task the boat is doing
manatees = 0 #black buoys
jellyfish = 0 #yellow buoys

# def countbuoys(BuoyData: dict): #counting black and yellow buoys
#     manatee = 0
#     jelly = 0
#     for coord in BuoyData:
#         if BuoyData[coord] == 'Black': manatee +=1
#         if BuoyData[coord] == 'Yellow' : jelly +=1
#     return manatee, jelly
# m, j = countbuoys({(1,2,3): "Black", (3,2,3): "Yellow"})
# manatees += m
# jellyfish +=j

def calcmidpoint(BuoyPair: dict) -> tuple: #takes a pair of buoys returing the midpoint
    keys = list(BuoyPair.keys())
    buoy1 = keys[0]
    buoy2 = keys[1]
    return ((buoy1[0]+buoy2[0])/2,(buoy1[1]+buoy2[1])/2, (buoy1[2]+buoy2[2])/2)

def nearestbuoy(BuoyPair: dict): #finds nearest buoy and returns its coordinates and color
    coord = ''
    color = ''
    for coor in BuoyPair:
        if not coord: #first coordinate in BuoyPair
            coord = coor
            color = BuoyPair[coor]
        else:
            zDist = coor[2] #z distance is the distance from boat
            if zDist < coord[2]:
                coord = coor
                color = BuoyPair[coor]
    return coord, color

def task1(BuoyPair: dict): #returns point that boat needs to go to
    red = {}
    green = {}
    for coord in BuoyPair: #organize red and green buoys into two dictionaries
        if BuoyPair[coord] == "Red": red[coord] = BuoyPair[coord]
        if BuoyPair[coord] == "Green": green[coord] = BuoyPair[coord]
    
    points = [] #for path of points
    greenCoord, gcolor = nearestbuoy(green)
    redCoord, rcolor = nearestbuoy(red)
    midpt = calcmidpoint({greenCoord: gcolor, redCoord: rcolor})
    return midpt
    
def task2(BuoyPair: dict): #returns point that boat needs to go to
    red = {}
    green = {}
    MandJ = {}
    for coord in BuoyPair: #return buoys into three dictionaries, red, green, and yellow and black as one 
        if BuoyPair[coord] == "Red": red[coord] = BuoyPair[coord]
        if BuoyPair[coord] == "Green": green[coord] = BuoyPair[coord]
        if BuoyPair[coord] == "Yellow" or BuoyPair[coord] == "Black": MandJ[coord] = BuoyPair[coord]
    greenCoord, gcolor = nearestbuoy(green)
    redCoord, rcolor = nearestbuoy(red)
    MandJCoord, mjcolor = nearestbuoy(MandJ)
    midpt = calcmidpoint({greenCoord: gcolor, redCoord: rcolor})
    #pairs the red and green buoy with the yellow or black buoy
    if MandJCoord:
        for mjcoord, mjcolor in MandJ:
            if mjcolor == "Yellow":
                jellyfish+=1
            elif mjcolor == "Black":
                manatees +=1
        greenAndMJ = calcmidpoint({greenCoord: gcolor, MandJCoord: mjcolor})
        redAndMJ = calcmidpoint({redCoord: rcolor, MandJCoord: mjcolor})
        if abs(midpt[0] - greenAndMJ[0]) < abs(midpt[0] - redAndMJ[0]):
            return greenAndMJ
        elif abs(midpt[0] - greenAndMJ[0]) > abs(midpt[0] - redAndMJ[0]):
            return redAndMJ
    else:
        return midpt
    #need to do counting

buoyData = {(3,1,2): "Green", (5,6,1): "Red", (1,5,2): "Red", (2,6,4): "Black", (2,5,3): "Green", (5,2,6): "Yellow"}
print(f"Task1 - Midpoint: {task1(buoyData)}")
print(f"Task2 - Midpoint: {task2(buoyData)}")

def task3(Walls): #takes in coordinates for side of the dock and the front of the dock. Should be 3 points
    coord = list(Walls.keys())
    #checks which two pairs are the side of the dock and which point is the front of the deck
    if coord[0][2] == coord[1][2]:
        pair = {coord[0]: Walls[coord[0]], coord[1]: Walls[coord[1]]}
        diff = coord[2]
    elif coord[0][2] == coord[2][2]:
        pair = {coord[0]: Walls[coord[0]], coord[2]: Walls[coord][2]}
        diff = coord[1]
    elif coord[2][2] == coord[1][2]:
        pair = {coord[2]: Walls[coord[2]], coord[1]: Walls[coord[1]]}
        diff = coord[0]
    midpt = calcmidpoint(pair)
    #z coordinate is changed to account for the depth of the dock
    newmidpt  = (midpt[0], midpt[1], (midpt[2] + diff[2])/2)
    return newmidpt
test = {(1,2,3):'', (5,2,3):'', (3, 2, 8):''}
print(f"Task3 - Midpoint: {task3(test)}")
    
def task4(BuoyPair):
    if len(BuoyPair) > 1:
        for coord in BuoyPair:
            x = BuoyPair.get(coord)
            if x == "Blue":
                BuoyPair.pop(coord)
        return calcmidpoint(BuoyPair)
    else:
        BuoyCoord = list(BuoyPair.keys())[0]
        p1 = (BuoyCoord[0]+1, BuoyCoord[1], BuoyCoord[2]) #left vertex
        p3 = (BuoyCoord[0]+3, BuoyCoord[1], BuoyCoord[2]) #right vertex
        p2 = (BuoyCoord[0], BuoyCoord[1], (p3[0]-p1[0]/2)+3) #top vertex
        cnpt = ((p3[0]-p1[0]/2), p1[1], p1[2])
        medDis = (p2[1]-cnpt[1])*(2/3)
        centroid = (cnpt[0], p1[1], p1[2]+medDis)
        turnPt = ((p2[0]-p1[0]/2), (p2[1]-p1[1]/2), (p2[2]-p1[2]/2)) #return point at midpoint of p1 and p2 at an angle
    return turnPt

# print(calcmidpoint({(1,2,3): "Green", (3,2,3): "Red"}))
# print(f'Manatees: {manatees}')
# print(f'Jellyfish: {jellyfish}')
