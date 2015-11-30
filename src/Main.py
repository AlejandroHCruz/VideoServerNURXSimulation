__author__ = 'Alejandro Hdz. Cruz, Federico Vorrath'

# Imports
import csv

# ====== Declare global variables ======

# Static constants
Lambda = 0.5                        # rate of requests entering the system every second (1/tp)
waitTimeMax = 1                     # U. 1 second in seconds
simulationTime = 600                # Time the simulation will run
packagesTobeServedPerUser = 2000    # number of packages that every user receives
frameLeavesApplicationLayer = .01   # r
throughputFrames = 1/frameLeavesApplicationLayer  # number of frames going out of the application layer (1/r= 100)
throughputPackages = 4500           # rate of packages leaving the buffer every second (Miu)
requestArrivalTime = 1/Lambda       # Average time between any user request (tp = 2)
packageLeavesBufferTime = 1/throughputPackages    # Average time in which a package leaves the buffer = .000222 seconds
wifiUserLimit = 52                  #

bufferSizeInPackages = 50           # n { 50, 100, 250 & 500 }

# Variables
users = 0                           # number of users currently in the system.
time = 0                            # current simulation time in seconds

requestsTotal = 0                   # number of requests made to the server
usersServed = 0                     # number of users that were well served by the system
framesServed = 0                    # frames that were served through the system
packagesServed = 0                  # packages that were served through the system

packagesInBuffer = 0                # number of packages currently in the system
framesInSystem = 0                  # number of frames currently in the system
usersInSystem = 0                   # number of users currently in the system
amazonCurrentDelay = 0              #
amazonCurrentDelayCounter = 0       # used to read the delay from the delays array
currentFrameSize = 0                #
currentFrameCounter = 0             #
packagesOfCurrentFrame = 0          #

sp = 0                              # Integral of the number of packages in the system
sf = 0                              # Integral of the number of frames in the system
su = 0                              # Integral of the number of users in the system

lp = 0                              # total packages in system
lf = 0                              # total frames in system
lu = 0                              # total users in system

serviceTime = 0                     # total service time in seconds (occupation time)
utilization = 0                     # percentage of utilization of the system
delay = 0                           #
waitInBufferTime = 0                #

probabilityServerSaturation = 0     # G
probabilityPackageSendFail = .001*usersInSystem  # e

# Arrays
arrivalTimeRequestsArray = []            # time in which every request entered the system
departureTimeRequestsArray = []          # time in which every request left the system
arrivalTimeFramesArray = []              # time in which every frame entered the system
departureTimeFramesArray = []            # time in which every frame left the system
arrivalTimePackagesArray = []            # time in which every package entered the system
departureTimePackagesArray = []          # time in which every package left the system

framesArray = []                    # the video frames to be served (from the .csv file)
amazonDelaysArray = []              # Amazon delays from the .csv file
bandwidthArray = []                 # bits transferred every second

packagesInBufferArray = []          # array of the number of packages in the system
framesInSystemArray = []            # array of the number of frames in the system
usersInSystemArray = []             # array of the number of users in the system
startStreamingPositionPerUser = []  # in which position of the framesArray every user starts

# Historical & Control Arrays
packagesPerFrameArray = []          # history of how many packages has every frame processed
frameSequenceByUserServed = []      # list of users by frame processed
framesServedPerUser = []            # history of how many frames have been served for each user
waitInBufferTimePerPackage = []     # history of how many seconds ech petition waited in buffer
framesPendingToBeServedPerUser = []  # count of how many frames each user needs to receive to achieve 2000

printableResults = []               # array of arrays with everything that's relevant for further statistical analysis

# Read Amazon delay data from csv file
delaysReader = csv.reader(open('/mnt/5512B8C217C7CAC1/Dropbox/Desarrollo/Python/VideoServerNURXSimulation/rsc/AmazonS3_delays-Ag-15.csv', 'rb'), delimiter= ',', quotechar='"')
for i in delaysReader:
    amazonDelaysArray.append(i)

framesReader = csv.reader(open('/mnt/5512B8C217C7CAC1/Dropbox/Desarrollo/Python/VideoServerNURXSimulation/rsc/Terse_DieHardIII.csv', 'rb'), delimiter= ',', quotechar='"')
for i in framesReader:
    framesArray.append(i)

    # with open('/rsc/AmazonS3_delays-Ag-15.csv', 'rb') as csvfile:
    #     csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #     for row in csvReader:
    #         print ', '.join(row)

# ====== Main ======

while time < simulationTime:  # Run simulation for "10 minutes"

    time += 0.000001

    # define amazonCurrentDelay
    amazonCurrentDelay = amazonDelaysArray[amazonCurrentDelayCounter]

    if time % requestArrivalTime == 0:
        # one request arrives every 2 seconds
        requestsTotal += 1
        arrivalTimeRequestsArray.append(time)

        # check W, if W <= 1 second
        if waitInBufferTime <= 1:
            usersInSystem += 1
            # get next currentFrameSize from framesArray
            currentFrameSize = framesArray[currentFrameCounter]
            currentFrameCounter += 1
            framesInSystem += 1

        elif time % frameLeavesApplicationLayer == 0 & usersInSystem > 0:
            # one frame leaves the application layer every .01 seconds

            while currentFrameSize >= 1500:
                # subdivide frames into packages
                currentFrameSize - 1500
                packagesOfCurrentFrame += 1

            if currentFrameSize > 0:
                packagesOfCurrentFrame += 1

            packagesPerFrameArray.append(packagesOfCurrentFrame)

            # TODO: serve only 52 users - wifiLimit - (framesServedPerUser[] < 2000), the other ones wait

            if packagesInBuffer+packagesOfCurrentFrame <= bufferSizeInPackages:
                # send packages of one user to the network layer
                packagesInBuffer += packagesOfCurrentFrame

                # if packagesOfCurrentFrame <= throughputFrames:
                #     packagesInBuffer += packagesOfCurrentFrame
                # else:
                #     packagesInBuffer += throughputFrames
                #     packagesOfCurrentFrame -= throughputFrames
                #     # TOD O: logic to send the remaining packages the next millisecond

    elif time % packageLeavesBufferTime == 0 & packagesInBuffer > 0:
        # one package leaves the buffer every .000222 seconds
        departureTimePackagesArray.append(time)
        packagesInBuffer -= 1
        # calculate W
        waitInBufferTime = 1/(4500 - packagesOfCurrentFrame) + amazonCurrentDelay
        probabilityPackageSendFail = probabilityPackageSendFail = .001*usersInSystem

        # TODO: when all the packages of one frame are served:
        # framesInSystem -= 1, departureTimeFramesArray.append(time)

        # TODO: when 2000 frames of one user are served:
        # usersServed += 1, usersInSystem -= 1, departureTimeUsersArray.append(time)

amazonCurrentDelayCounter += 1

# ====== Compute LUWX ======



printableResults = [usersInSystem]

with open("results.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(printableResults)