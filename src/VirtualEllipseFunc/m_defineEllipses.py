import numpy as np 
import math
from scipy.spatial import distance
from shapely.geometry.polygon import LinearRing
from math import atan2, pi, sin, cos

def generatePosiblePositions(grid_dimention_x = 101, grid_dimention_y = 75, linelength = 10):

    start_x = -0.5*linelength*grid_dimention_x + 0.5*linelength
    start_y = -0.5*linelength*grid_dimention_y + 0.5*linelength

    positions =[]
    for x_count in range(0, grid_dimention_x):
        new_x = start_x + x_count*linelength
        for y_count in range(0, grid_dimention_y):
            new_y = start_y + y_count*linelength
            positions.append((new_x, new_y))

    '''(0, 0) should not be in the positions list'''
    try:
        positions.remove((0,0))
    except ValueError:
        pass
    
    return positions

def removefovelPositions(r = 100):
    ''' Define and remove a fovea area (a circle) of r == ??'''
    del_p = []
    positions = generatePosiblePositions()
    tempList = positions.copy()
    for tempP in positions:
        if math.sqrt((tempP[0]**2) + (tempP[1]**2)) < r:
            del_p.append(tempP)
            try:
                tempList.remove(tempP)
            except ValueError:
                pass
    positions = tempList
    return positions

def defineVirtualEllipses(coordinate,ka,kb):
# parameter for a and b; When adjust them, DO NOT forget to change in the drawEllipse
    '''
    This function defines the virtual ellipse. coordinate: the center of the ellipse
    ka and kb are parameters of semi-major axis and semi-minor axis of the ellipse, respectivly.
    ka and kb should be defined according to crowding zone areas. This function reutrns coordiante of ellipse(the center),
    ellipse_axis(a and b for ellipse) and 2 angles (radial and tangential direction)
    '''
    e = distance.euclidean(coordinate, (0,0)) #np.sqrt((coordinate[0])**2 + (coordinate[1])**2)    
    a = ka * e
    b = kb * e
    ellipse_axis = [a, b]
    #radial angle
    angle_rad = atan2(coordinate[1],coordinate[0])
    angle_radial = angle_rad*180/pi
    angle_tangential = angle_radial + 90
    V_ellipse = (coordinate[0],coordinate[1], ellipse_axis[0],ellipse_axis[1], angle_radial, angle_tangential)

    return V_ellipse
def defineCircleRegion(coordinate, r):
    angle_rad = atan2(coordinate[1],coordinate[0])
    angle_radial = angle_rad*180/pi
    angle_tangential = angle_radial + 90
    V_circle = (coordinate[0],coordinate[1], r,r, angle_radial, angle_tangential)
    
    return V_circle
def rotateposi(centralPosi, toRotatePosi, theta = pi/2):
    '''
    This fucntion caculates the coordinate that rotate
    given position (x1, y1) anticlockwise theta degree 
    around (x0, y0)
    '''
    x2 = (toRotatePosi[0]-centralPosi[0])*cos(theta) - (toRotatePosi[1]-centralPosi[1])*sin(theta) + centralPosi[0]
    y2 = (toRotatePosi[0]-centralPosi[0])*sin(theta) + (toRotatePosi[1]-centralPosi[1])*cos(theta) + centralPosi[1]
    return (round((x2),1), round((y2),1))

def caclulateNewList (random_disk_coordinate, taken_list, positions,ka,kb): 
    # global positions
    # (新生成的随机点，已经保存的点坐标list) # new random disk corrdinate, previous disk corrdinates list
    '''
    This function generate the final list that contains a group of disks coordinate. 
    The newly selected disk position (with a virtual ellipse) will be inspected with all the exited virtual ellipses
    Only the one without intersection could be reutrned.
    '''
    virtual_e_2 = defineVirtualEllipses(random_disk_coordinate,ka,kb)
    
    for_number = 0
    for exist_n in taken_list: 
        exist_e = defineVirtualEllipses(exist_n,ka,kb) #perivous ellipses  
        for_number = for_number + 1
        ellipses = [exist_e, virtual_e_2]
        intersectionXList, intersectionYList = ellipse_polyline_intersection(ellipses)
        if len(intersectionXList) > 0:
            positions.pop(-1)
            return [0] #breakout the function and  go into the while loop to delete this position
        else:
            continue

    taken_list.append(random_disk_coordinate)
    #delete the the current position from the list positions and the corrosponding ellipses points.
    positions.pop(-1)
    return taken_list  #final list of position I want

def caclulateNewList_2direction (random_disk_coordinate, taken_list, positions,ka,kb): 
    # global positions
    # (新生成的随机点，已经保存的点坐标list) # new random disk corrdinate, previous disk corrdinates list
    '''
    This function generate the final list that contains a group of disks coordinate. 
    The newly selected disk position (with a virtual ellipse) will be inspected with all the exited virtual ellipses
    Only the one without intersection could be reutrned.
    '''
    virtual_e_2 = defineVirtualEllipses(random_disk_coordinate,ka,kb)
    
    for_number = 0
    for exist_n in taken_list: 
        exist_e = defineVirtualEllipses(exist_n,ka,kb) #perivous ellipses  
        for_number = for_number + 1
        ellipses = [exist_e, virtual_e_2]
        intersectionXList, intersectionYList = ellipse_polyline_intersection_full(ellipses)
        if len(intersectionXList) > 0:
            positions.pop(-1)
            return [0] #breakout the function and  go into the while loop to delete this position
        else:
            continue

    taken_list.append(random_disk_coordinate)
    #delete the the current position from the list positions and the corrosponding ellipses points.
    positions.pop(-1)
    return taken_list  #final list of position I want

'''
if new点和takenlist里的一个点相交
  删去该positions点，得到新点

else 不相交
 取下一个takenlist的点，直到和所有已知的takenlist都不相交，
  则把该点加入到takenlist,并删除positions里的该点，并删除该点周围的椭圆格点
'''
def ellipse_polyline_intersection(ellipses, n=500):
    '''
    This function transfer an ellipse to ellipse_poluline and then check the intersections of two ellipses. It
    returns the intercetion coordinate 
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle, angle2 in ellipses: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        pointE = np.empty((n, 2))
        pointE[:, 0] = x0 + a * ca * ct - b * sa * st
        pointE[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(pointE)
    #ellipseA, ellipseB are the dots of two ellipse
    ellipseA = result[0]
    ellipseB = result[1]
    ea = LinearRing(ellipseA)
    eb = LinearRing(ellipseB)
    mp = ea.intersection(eb)
    #intersectionX, intersectionY are the intersections
    #if type(mp) == types.GeneratorType:
    # print(mp.geom_type)
    # print(mp)
    if mp.geom_type == 'Point':
        #print(mp.geom_type)
        #print(mp.x)
        return [mp.x], [mp.y]
    elif mp.geom_type == 'LineString':
        newmp = list(mp.coords)
        #print("newmp", newmp)
        intersectionX = [pE[0] for pE in newmp] 
        intersectionY = [pE[1] for pE in newmp]
        return intersectionX, intersectionY
    else:
        intersectionX = [pE.x for pE in mp] 
        intersectionY = [pE.y for pE in mp]
        return intersectionX, intersectionY
#    try:
#        #TypeError: 'Point' object is not iterable
#        intersectionX = [p.x for p in mp]
#        intersectionY = [p.y for p in mp]
#    except Exception as er:
#        print('Error:', er)
#        print("mp: ", mp)
#if you want to draw the two ellipse:
#   plt.plot(intersectionX, intersectionY, "o")
#   plt.plot(ellipseA[:, 0], ellipseA[:, 1])
#   plt.plot(ellipseB[:, 0], ellipseB[:, 1])

#ellipses = [(1, 1, 1.5, 1.8, 90), (2, 0.5, 5, 1.5, -180)]
#intersectionX, intersectionY = ellipse_polyline_intersection(ellipses)
def ellipse_polyline_intersection_full(ellipses, n=500):
    '''
    This function transfer an ellipse to ellipse_polyline and then check the intersections of two ellipses. It
    returns the intercetion coordinate 
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result_radial = []
    result_tangential = []
    for x0, y0, a, b, angle, angle2 in ellipses: #angle2: tangential direction of the ellilpse
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        pointE = np.empty((n, 2))
        pointE[:, 0] = x0 + a * ca * ct - b * sa * st
        pointE[:, 1] = y0 + a * sa * ct + b * ca * st
        result_radial.append(pointE)
        
        angle2 = np.deg2rad(angle2)
        sa2 = np.sin(angle2)
        ca2 = np.cos(angle2)
        pointE_t = np.empty((n, 2))
        pointE_t[:, 0] = x0 + a * ca2 * ct - b * sa2 * st
        pointE_t[:, 1] = y0 + a * sa2 * ct + b * ca2 * st
        result_tangential.append(pointE_t)
        
    #ellipseA, ellipseB are the dots of two ellipse
    ellipseA = result_radial[0]
    ellipseB = result_radial[1]
    ea = LinearRing(ellipseA)
    eb = LinearRing(ellipseB)
    mp = ea.intersection(eb) #2 radial ellipses
    
    #same for ellipseC and ellipseD, the dots of two ellipses
    ellipseC = result_tangential[0]
    ellipseD = result_tangential[1]
    ec = LinearRing(ellipseC)
    ed = LinearRing(ellipseD)
    mp2 = ec.intersection(ed) #2 tangential ellipses
    
    mp3 = ea.intersection(ed) # 1 tangental and 1 radial
    mp4 = eb.intersection(ec)
    
    #intersectionX, intersectionY are the intersections
    #if type(mp) == types.GeneratorType:
    # print(mp.geom_type)
    # print(mp)
    mp_list = []
    mp_list = [mp,mp2,mp3,mp4]
    #loop to judge all 4 situations
    for i_mp in mp_list:
        #point: 相切,only one point overloop
        if i_mp.geom_type == 'Point':
            #print(mp.geom_type)
            #print(mp.x)
            return [i_mp.x], [i_mp.y]
        #lingstring: two ellipses overlap
        elif i_mp.geom_type == 'LineString':
            newmp = list(mp.coords)
            #print("newmp", newmp)
            intersectionX = [pE[0] for pE in newmp] 
            intersectionY = [pE[1] for pE in newmp]
            return intersectionX, intersectionY
        #normal situation:if len()==0 means there is no overlap return empty list[][]
                            #if len()>0 return the two points
        else:
            intersectionX = [pE.x for pE in i_mp]
            intersectionY = [pE.y for pE in i_mp]
            if len(intersectionX) == 0:#if len()==0: no overlap, next situation
                continue
            else:#if len()>0 return the two points
                return intersectionX, intersectionY
    #all four situations no overlap
    return [], []
    #    try:
    #        #TypeError: 'Point' object is not iterable
    #        intersectionX = [p.x for p in mp]
    #        intersectionY = [p.y for p in mp]
    #    except Exception as er:
    #        print('Error:', er)
    #        print("mp: ", mp)
    #if you want to draw the two ellipse:
    #   plt.plot(intersectionX, intersectionY, "o")
    #   plt.plot(ellipseA[:, 0], ellipseA[:, 1])
    #   plt.plot(ellipseB[:, 0], ellipseB[:, 1])

    #try
    # e1 = defineVirtualEllipses((200, 0))
    # e2 = defineVirtualEllipses((220, 20))
    # intersectionX, intersectionY = ellipse_polyline_intersection_full((e1,e2))

    # e=drawEllipse(((200,0),(220,20)))
    # ellipses = [(1, 1, 1.5, 1.8, 90), (2, 0.5, 5, 1.5, -180)]
    # intersectionX, intersectionY = ellipse_polyline_intersection(ellipses)
def ellipseToPolygon(ellipse, n=200):
    '''
    This function transfer an ellipse to ellipseToPolygon in radial and tangential directions
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle, angle2 in ellipse: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        pointE = np.empty((n, 2))
        pointE[:, 0] = x0 + a * ca * ct - b * sa * st
        pointE[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(pointE)
    result2 = []
    for x0, y0, a, b, angle, angle2 in ellipse: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle2 = np.deg2rad(angle2)
        sa2 = np.sin(angle2)
        ca2 = np.cos(angle2)
        pointE2 = np.empty((n, 2))
        pointE2[:, 0] = x0 + a * ca2 * ct - b * sa2 * st
        pointE2[:, 1] = y0 + a * sa2 * ct + b * ca2 * st
        result2.append(pointE2)
    #ellipseA, ellipseB are the dots of two ellipse
    ellipse1 = result[0]
    ellipse2 = result2[0]
#    ellipseB = result[1]
#    ellipse1 = Polygon(ellipse1)
#    ellipse2 = Polygon(ellipse2)
    return ellipse1, ellipse2
def checkPosiOnEllipse( h, k, x, y, a, b):
    '''
    Check a given point (x, y) is inside, outside or on the ellipse
    centered (h, k), semi-major axis = a, semi-minor axix = b
    '''
    p = ((math.pow((x-h), 2) // math.pow(a, 2)) + (math.pow((y-k), 2) // math.pow(b, 2)))
    return p #if p<1, inside