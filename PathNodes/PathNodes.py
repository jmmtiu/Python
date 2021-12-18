#Nodes of path
longList = ["121.0009013", "120.5284330", "120.3032997"]
latList = ["14.6785949", "15.1576557", "14.8279319"]

#Generate and print URL to query and view path
queryString = "http://router.project-osrm.org/route/v1/driving/"
mapString = "https://map.project-osrm.org/?z=11&center={}\%2C{}".format(latList[0], longList[0])

for long, lat in zip(longList[:-1], latList[:-1]):
    queryString +=  "{},{};".format(long, lat)
    mapString += "&loc={}\%2C{}".format(lat, long)

queryString += "{},{}?alternatives=false&annotations=nodes".format(longList[-1], latList[-1])
mapString += "&loc={}\%2C{}&hl=en&alt=0&srv=0".format(latList[-1], longList[-1])

print("\nQuery: {}\n".format(queryString))
print("Map Visualization: {}\n".format(mapString))


#Create request and convert to json
import requests

responseReq = requests.get(queryString)

response = responseReq.json()

#Create node list from start to end of path
nodeList = []

for leg in response['routes'][0]['legs']:
    nodeList += (leg['annotation']['nodes'])

#Create text file to load lon,lat data with Overpass API
outputFile = open("nodelist.txt", "w")
outputFile.write("[out:json];\n(\n")

for node in nodeList:
    outputFile.write("node({});\n".format(node))

outputFile.write(");\n(._;>;);\nout;")
outputFile.close()


#Use Overpass API to generate an output from the nodelist query
import overpy

api = overpy.Overpass()

with open('nodelist.txt') as overpyQuery:
    queryLines = overpyQuery.read()
    result = api.query(queryLines)


#Sort output from Overpass API to match output from initial query
nodeCount = len(nodeList)
unsortedNodeList = result.nodes
sortedNodeList = []

for i in range(nodeCount):
    sortedNodeList.append(next(node for node in unsortedNodeList if node.id == nodeList[i]))


#Create new long and lat list
longList = []
latList = []

for i in range(nodeCount):
    longList.append(float(sortedNodeList[i].lon))
    latList.append(float(sortedNodeList[i].lat))


#Populating sparse sections
import numpy as np
#Save old lat and long list
oldLon = longList
oldLat = latList

#1 degree = 111,139m
maxDist = (50/2)/111139 #degrees

i = 0
while i < len(longList) - 1:
    dist = ((longList[i+1]-longList[i])**2 + (latList[i+1]-latList[i])**2)**(0.5)

    #Populate section between nodes if distance is larger than max distance
    if dist >= maxDist:
        newNodeCount = int(round(dist/maxDist)) + 2

        newNodeLon = np.linspace(longList[i], longList[i+1], newNodeCount)
        newNodeLat = np.linspace(latList[i], latList[i+1], newNodeCount)
        
        longList[i+1:i+1] = newNodeLon[1:-1]
        latList[i+1:i+1] = newNodeLat[1:-1]

    i += 1


#Generate output file
outputFile = open("coordList.csv", "w")
outputFile.write("lon,lat\n")

for i in range(len(longList)):
    outputFile.write("{},{}\n".format(longList[i],latList[i]))


#Plot output
import matplotlib.pyplot as plt
plt.plot(longList, latList, marker='.', markersize=2)
plt.plot(oldLon, oldLat, linestyle='--')
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.axis('equal')
plt.show()