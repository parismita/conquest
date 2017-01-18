import cv2
import numpy as np
import conquest_main


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


class Node:
    def __init__(self,value,point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0
    def move_cost(self,other):
        return 0 if self.value == '.' else 1
        
def children(point,grid):
    x,y = point.point
    links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]]
    return [link for link in links if link.value != '%']
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
def next_move(pacman,food,grid):
    #Convert all the points to instances of Node
    for x in xrange(len(grid)):
        for y in xrange(len(grid[x])):
            grid[x][y] = Node(grid[x][y],(x,y))
    #Get the path
    path = aStar(grid[town_center[0]][town_center[1]],grid[food[0]][food[1]],grid)
    #Output the path
    print len(path) - 1
    for node in path:
        x, y = node.point
        print x, y
#pacman_x, pacman_y = [ int(i) for i in raw_input().strip().split() ]
#food_x, food_y = [ int(i) for i in raw_input().strip().split() ]
#x,y = [ int(i) for i in raw_input().strip().split() ]
 
grid = ones((120,120),dtype=int)
map1=conquest_main.cntSet[0]
map_y=map1[0][0][1]-map1[1][0][1]
map_x=map1[3][0][0]-map1[0][0][0]
pixels_per_block=[map_x/120.0,map_y/120.0]
cordinates_obstacle=[[]]
for x in conquest_main.square:
	for i in range(4):
		a=int((x[i][0][0]-map1[0][0][0])/pixels_per_block[0])
		b=int((x[i][0][1]-map1[0][0][1])/pixels_per_block[1])
		cordinates_obstacle.append([a,b])
		grid[a][b]='%'
cordinates_food=[]
cordinates_wood=[]
for x,x_type in conquest_main.reslist:
	if x_type=='f':
		f_x=int((x[0]-map1[0][0][0])/pixels_per_block[0])
		f_y=int((x[1]-map1[0][0][1])/pixels_per_block[1])
		cordinates_food.append([f_x,f_y])
	else:
		w_x=int((x[0]-map1[0][0][0])/pixels_per_block[0])
		w_y=int((x[1]-map1[0][0][1])/pixels_per_block[1])
		cordinates_wood.append([w_x,w_y])
town_center[0]=int((tcCenter[0]-map1[0][0][0])/pixels_per_block[0])
town_center[1]=int((tcCenter[1]-map1[0][0][1])/pixels_per_block[1])


    
for i in xrange(0, x):
    grid.append(list(raw_input().strip()))
 
next_move((pacman_x, pacman_y),(food_x, food_y), grid)
