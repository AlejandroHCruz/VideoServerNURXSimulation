__author__ = 'Alejandro Hdz. Cruz, Federico Vorrath'

# Imports
import csv

# ====== Declare global variables ======

# Static constants
Lambda = 0.5                        # rate of requests entering the system every second (1/tp)
waitTimeMax = 1000000               # U. 1 second in microseconds = 1,000,000
simulation_limit = 2000             # number of packages sent in the entire simulation
frameLeavesApplicationLayer = .01   # r
throughputFrames = 1/frameLeavesApplicationLayer  # number of frames going out of the application layer (1/r)
throughputPackages = 4500           # rate of packages leaving the buffer every second
requestArrivalTime = 1/Lambda       # Average time between any user request (tp)
packageLeavesBufferTime = 1/throughputFrames    # Average time in which a package leaves the buffer

bufferSizeInPackages = 50           # n { 50, 100, 250 & 500 }

# Variables
time = 0                            # current simulation time in seconds
processedFrames = 0                 # frames that were served through the system
requestsTotal = 0                   # number of requests made to the server
users = 0                           # number of users currently in the system.
usersServed = 0                     # number of users that were well served by the system

packagesInSystem = 0                # number of packages currently in the system
framesInSystem = 0                  # number of frames currently in the system
usersInSystem = 0                   # number of users currently in the system

sp = 0                              # Integral of the number of packages in the system
sf = 0                              # Integral of the number of frames in the system
su = 0                              # Integral of the number of users in the system

lp = 0                              # total packages in system
lf = 0                              # total frames in system
lu = 0                              # total users in system

serviceTime = 0                     # total service time in seconds (occupation time)
utilization = 0                     # percentage of utilization of the system
delay = 0                           #

probabilityServerSaturation = 0     # G
probabilityPackageSendFail = .001*usersInSystem  # e

# Arrays
requestsArrivalTimeArray = []            # time in which every request entered the system
requestsDepartureTimeArray = []          # time in which every request left the system
framesTimeArrivalArray = []              # time in which every frame entered the system
framesTimeDepartureArray = []            # time in which every frame left the system
packagesTimeArrivalArray = []            # time in which every package entered the system
packagesTimeDepartureArray = []          # time in which every package left the system
frameSequenceByUserServed = []           # list of users by frame processed

framesArray = []                    # the 2000 frames to be served (from the .csv file)
delaysArray = []                    # Amazon delays from the .csv file
bandwidth = []                      # bits transferred every second

npArray = []                        # array of the number of packages in the system
nfArray = []                        # array of the number of frames in the system
nuArray = []                        # array of the number of users in the system

pFinalStatus = []                   # history of which packages were successfully delivered and which not
fFinalStatus = []                   # history of which frames were successfully delivered and which not
uFinalStatus = []                   # history of which users were successfully delivered and which not

printableResults = []               # array of arrays with everything that's relevant for further statistical analysis

# Read delay data from csv file
with open('/rsc/AmazonS3_delays-Ag-15.csv', 'rb') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvReader:
        print ', '.join(row)

# Read 2000 frames from csv file

# Main

while processedFrames < 2000:

    time += 0.000001

    if time % packageLeavesBufferTime == 0 & packagesInSystem > 0:
        # execute this every .000222 seconds
        packagesInSystem -= 1

    elif time % frameLeavesApplicationLayer == 0:
        # execute this every .01 seconds

        packagesOfCurrentFrame = 0

        while currentFrameSize >= 1500:

            currentFrameSize - 1500
            packagesOfCurrentFrame += 1

        if currentFrameSize != 0:
            packagesOfCurrentFrame += 1
        packagesInSystem +=  packagesOfCurrentFrame

    elif time % requestArrivalTime == 0:
        # execute this every 2 seconds
        requestsTotal += 1

        # check G probability of request being rejected, if request is not rejected:
        usersInSystem += 1
        #get next currentFrameSize from frameArray

with open("results.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(printableResults)