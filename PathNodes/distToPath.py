import numpy as np

#Loading path data
lonData, latData = np.loadtxt('coordList.csv', unpack=True, delimiter=',', skiprows = 1)

#Function that returns distance and index of closest node to given coordinates
def distToPath(lon, lat, lonData, latData):    
    dists = np.sqrt((lonData - lon)**2 + (latData - lat)**2)

    minDist = dists.min()
    minIndex = np.argmin(dists)

    return minDist, minIndex

#Function that finds the smallest distance of P3 from the line formed by P1 and P2
def distPointToLine(P1, P2, P3):
    return np.abs(np.cross(P2-P1,P3-P1))/np.linalg.norm(P2-P1)

#Function that determines if the coordinates are within the path including an error
def withinPath(lon, lat, lonData, latData, errorDist):
    minDist, minIndex = distToPath(lon, lat, lonData, latData)

    #If node is within error distance to another node
    if minDist <= errorDist:
        return True
    
    #If node is close to another node, but not within error
    if minDist <= errorDist*2:

        P1 = np.array([lonData[minIndex], latData[minIndex]])
        P3 = np.array([lon, lat])

        #If node has 2 adjacent nodes
        if minIndex >= 1 & minIndex <= len(lonData):
            P2 = np.array([lonData[minIndex+1], latData[minIndex+1]])
            lineDist = distPointToLine(P1, P2, P3)
            P2 = np.array([lonData[minIndex-1], latData[minIndex-1]])
            lineDist_2 = distPointToLine(P1, P2, P3)
            lineDist = min([lineDist, lineDist_2])
        #If node has only 1 adjacent nodes (2 possibilities)
        if minIndex == 1:
            P2 = np.array([lonData[minIndex+1], latData[minIndex+1]])
            lineDist = distPointToLine(P1, P2, P3)
        if minIndex == len(lonData):
            P2 = np.array([lonData[minIndex-1], latData[minIndex-1]])
            lineDist = distPointToLine(P1, P2, P3)

        #If distance to line is within error distance
        if lineDist <= errorDist:
            return True

    #Else, false
    return False


#Given coordinates and error distance in degrees
lon = 120.514031
lat = 15.060852
errorDist = 50/111139 #degrees

#Run functions
minDist, minIndex = distToPath(lon, lat, lonData, latData)
bool = withinPath(lon, lat, lonData, latData, errorDist)

#Print output
print("Min Distance to Node: {} m".format(minDist*111139))
print("Within Path: {}".format(bool))

#Plot adjacent path, point and closest node
import matplotlib.pyplot as plt
plt.plot(lonData[minIndex - 500: minIndex + 500], latData[minIndex - 500: minIndex + 500])
plt.scatter(lonData[minIndex], latData[minIndex])
plt.scatter(lon, lat)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.axis('equal')
plt.show()