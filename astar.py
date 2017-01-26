import cv2
import numpy as np
import conquest_main 
from conquest_main import getThresoldValue,locateObstacle,resources,locateMap,tcCenter,pid,run,locateBot,findError,Ki,Kd,Kp,last_time,integrat,prev_err

#tast
#get frame size
#60*60 divisions
#
#plot the groups in a image to verify
#make algo a* on 60*60 squares
#find path 
#find centroid of the position got and connect them
#####error minimization function to make the curve smooth##########my not be needed


#capture = cv2.VideoCapture(0)
'''a=np.array([[[  1,   1]],
       [[  1, 478]],
       [[638, 478]],
       [[638,   1]]])'''

''''def computerHCF(x, y):
   """This function takes two
   integers and returns the H.C.F"""
   # choose the smaller number
   if x > y:
       smaller = y
   else:
       smaller = x
   for i in range(1,smaller + 1):
       if((x % i == 0) and (y % i == 0)):
           hcf = i
       return hcf'''


#x = a[2][0][0]-a[1][0][0]
#xprint np.shape(a)

'''while 1:
    img = capture.read()
    frame_size = img[1].shape
    print frame_size
    cv2.waitKey(1)'''

#############################################################################################3
#                         A star algo
#############################################################################################
class Node:
    def __init__(self,value,point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0
    def move_cost(self,other):
        return 0 if self.value == '0' else 1
        
def children(point,grid):
    x,y = point.point
    links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]]
    return [link for link in links if link.value != 0]
def manhattan(point,point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])
def aStar(start, goal, grid):
    #The open and closed sets
    openset = set()
    closedset = set()
    #Current point is the starting point
    current = start
    #Add the starting point to the open set
    openset.add(current)
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        #If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #Loop through the node's children/siblings
        for node in children(current,grid):
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score 
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
                openset.add(node)
    #Throw an exception if there is no path
    raise ValueError('No Path Found')
def next_move(town_center,food,grid):
    #Convert all the points to instances of Node
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid[x][y] = Node(grid[x][y],(x,y))
    #Get the path
    path = aStar(grid[town_center[0]][town_center[1]],grid[food[0]][food[1]],grid)
    #Output the path
    print len(path) - 1
    for node in path:
        x, y = node.point
        grid[x][y].value=2
        print x,y
    grid2 = [[grid[x][y].value for x in range(120)] for y in range(120)]
    return grid2
    
def convert(grid,pixel_no,start):
    pixel = []
    for i in range(120):
        for j in range(120):
            if grid[i][j] == 2:
                x = i*pixel_no[0] + start[0]
                y = j*pixel_no[1] + start[1]
                pixel.append([x,y])
    return pixel

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):
    # Make a deep copy of path into newpath
    newpath = [[0 for row in range(len(path[0]))] for col in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] =path[i][j]

    change = tolerance
    while change >= tolerance:
        change = 0.0
        for i in range(1,len(path)-1):
            for j in range(len(path[0])):
                aux = newpath[i][j]
                newpath[i][j] = newpath[i][j] + weight_data*(path[i][j] - newpath[i][j])
                newpath[i][j] = newpath[i][j] + weight_smooth*(newpath[i-1][j] + newpath[i+1][j] - 2*newpath[i][j])
                change = change + abs(aux - newpath[i][j])
    return newpath
############################################################################
############################################################################################3
#print resources[0][1]

oMin , oMax,mask = getThresoldValue('obstacle')
obstacles = mask
mMin , mMax, _ = getThresoldValue('map')
map1 = locateMap(mMin , mMax)
start = [map1[1][0][0],map1[1][0][1]]
#print map1,"map"
#grid created with default value one
grid = [[1 for _ in range(120)] for _ in range(120)]
for i in range(120):
    grid[i][0]=0
    grid[0][i]=0
    grid[119][i]=0
    grid[i][119]=0
#pixel cordinaten of map(3m*3m)
#print map1
########!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!not yet threshonded and founf contour of the arena 
#pixel lenght of map
print map1[1][0][1],map1[0][0][1]
print map1[2][0][0],map1[0][0][0]
map_y=map1[2][0][1]-map1[0][0][1]
map_x=map1[2][0][0]-map1[1][0][0]

#dimension of each block of grid in terms of pixels... its in float
pixels_per_block=[map_x/120.0,map_y/120.0]
print pixels_per_block,"pixels"
cordinates_obstacle=[[]]
#coordinates of obstacles....marking there boxes in grid with '%'
for x in range(len(obstacles)):
    for y in range(len(obstacles[x])):
        #print obstacles[x][y]
        if obstacles[x][y]==255:
            print "fuck2"
            a1=int(round(abs((x-map1[1][0][0])/pixels_per_block[0])))
            b=int(round(abs((y-map1[1][0][1])/pixels_per_block[1])))            print a1,b,"a,b"
            cordinates_obstacle.append([a1,b])
            grid[a1][b]=0
cordinates_res=[]
#finding the box for food and wood in the grid through there centroid..... cordinate will be automatically sorted
print resources,"res"
for x in resources:
        f_x=int(round(abs((x[0][0]-map1[1][0][0])/pixels_per_block[0])))
        f_y=int(round(abs((x[0][1]-map1[1][0][1])/pixels_per_block[1])))
        print f_x,f_y
        cordinates_res.append([f_x,f_y])    #town_center coordinates
town_center=[0,0]
town_center[0]=int(round(abs((tcCenter[0]-map1[1][0][0])/pixels_per_block[0])))
town_center[1]=int(round(abs((tcCenter[1]-map1[1][0][1])/pixels_per_block[1])))
print cordinates_res,"Resources"
print town_center,"tc",tcCenter
#now we have to send each and every food and wood coordinates as goal one by one in the next move function
#for case one as we reach a goal two time ... we'll remove it from the list ...as a safe gourd while searching for a particular goal we must also keep a check 
#that by_mistake if bot steps on a unchecked food or wood ... led must blink and other measurements must change too

    
#for i in xrange(0, x):
v    #grid.append(list(raw_input().strip()))
 

#how to make contours line show, how to make grid show
def listPathPoints1(start,end):
    stx=start[0]
    sty=start[1]
    enx=end[0]
    eny=end[1]
    l=[]
    vx=(enx-stx)
    vy=(eny-sty)
    if (vx==0 and vy==0):
        return start
    d=int(math.sqrt((stx-enx)**2+(sty-eny)**2))
    cos=vx/math.sqrt(vx**2+vy**2)
    sin=vy/math.sqrt(vx**2+vy**2)
    i=1
    while(i<d):
        l.append([int(stx+cos*i),int(sty+sin*i)])
        i=i+1
    return l


for x in cordinates_res:
    full_path_points=[]
    reverse_path=[]
    grid2=next_move(town_center,x, grid)
    path=convert(grid2,pixels_per_block,start)
    for x in range(len(path)-1):
        full_path_points=full_path_points+(listPathPoints1(path[x],path[x+1]))
    path=smooth(full_path_points)
    for i in path:
        cv2.circle(obstacles,(i[0],i[1]),3,(127,127,127),1)_
	ki=1
	kd=1
	kp=1
	prev_err=0
	integrat=0
	last_time=0
        run(i)
        
    path.reverse() 
    for i in path:
	    cv2.circle(obstacles,(i[0],i[1]),3,(127,127,127),1)
	    run(i)   
    cv2.imshow("newewrsdaf",obstacles)

    



