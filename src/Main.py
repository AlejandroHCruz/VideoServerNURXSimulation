__author__ = 'Alejandro Hdz. Cruz, Federico Vorrath'

# Imports
import csv
import random

# ====== Declare global variables ======

# Static constants
Lambda = 0.5                        # rate of requests entering the system every second (1/tp)
waitTimeMax = 1                     # U. 1 second in seconds
simulationTime = 600                # Time the simulation will run
fps = 24                            # Each video runs at 24 frames per second (frame request per user)
packagesTobeServedPerUser = 2000    # number of packages that every user receives
frameLeavesApplicationLayer = .01   # r
throughputFrames = 1/frameLeavesApplicationLayer  # number of frames going out of the application layer (1/r= 100)
throughputPackages = 4500           # rate of packages leaving the buffer every second (Miu)
requestArrivalTime = 1/Lambda       # Average time between any user request (tp = 2)
packageLeavesBufferTime = 1/throughputPackages    # Average time in which a package leaves the buffer = .000222 seconds
wifiUserLimit = 256                 #
randomFrameRangeMin = 10            # Used to choose the start of the frames to be sent to any user (randrange)
randomFrameRangeMax = 87997         # Used to choose the end of the frames to be sent to any user (randrange)
bufferSizeInPackages = 50           # n { 50, 100, 250 & 500 }
eDividedByK = .001                  # factor that gets multiplied by the users to calculate the error probability

# Variables
time = 0                            # current simulation time in seconds

requestsTotal = 0                   # number of requests made to the server
usersServed = 0                     # number of users that were well served by the system
framesServed = 0                    # frames that were served through the system
packagesServed = 0                  # packages that were served through the system
framesAcceptedInBuffer = 0
framesRejectedFromBuffer = 0

packagesInBuffer = 0                # number of packages currently in the system
framesInSystem = 0                  # number of frames currently in the system
usersInSystem = 0                   # number of users currently in the system
userBeingServed = -1                # position that the current user has in the users/petitions array
usersBeingServed = 0                # users being served in any moment (max 52)
amazonCurrentDelay = 0              #
amazonCurrentDelayCounter = 0       # used to read the delay from the delays array
currentFrameSize = 0                #
currentFrameCounter = 0             #
numPackagesOfCurrentFrame = 0       #
servedPackagesOfCurrentFrame = 0    #
packagesArrivedWithError = 0
framesArrivedWithError = 0
usersServedWithError = 0

# Not needed since I have packagesInBuffer, framesInSystem and usersInSystem
# sp = 0                              # Integral of the number of packages in the system
# sf = 0                              # Integral of the number of frames in the system
# su = 0                              # Integral of the number of users in the system

lp = 0                              # total packages in system
lf = 0                              # total frames in system
lu = 0                              # total users in system

serviceTime = 0                     # total service time in seconds (occupation time)
utilization = 0                     # percentage of utilization of the system
delay = 0                           #
waitInBufferTime = 0                #

probabilityServerSaturation = 0     # G
probabilityPackageSendFail = eDividedByK*usersInSystem  # e
randomE = 0                         # to compare e with and determine if a package arrives successfully to client

# Arrays
arrivalTimeUsersArray = []       # time in which every request that reaches the system arrived
departureTimeUsersRequestsArray = []     # time in which every request that left the system
arrivalTimeFramesArray = []              # time in which every frame entered the system
departureTimeFramesArray = []            # time in which every frame left the system
arrivalTimePackagesArray = []            # time in which every package entered the system
departureTimePackagesArray = []          # time in which every package left the system

probabilityServerSaturationArr = []      # G
probabilityPackageSendFailArr = []       # e

framesArray = []                    # the video frames to be served (from the .csv file)
framesServed = []                   # frames that came out of the system
amazonDelaysArray = []              # Amazon delays from the .csv file
bandwidthArray = []                 # bits transferred every second

# packagesInBufferArray = []          # array of the number of packages in the system
# framesInSystemArray = []            # array of the number of frames in the system
# usersInSystemArray = []             # array of the number of users in the system
startStreamingPositionPerUser = []    # in which position of the framesArray every user starts
currentFrameCounterPerUser = []       # to know which frame is being served to every user
frameAcceptedInBufferStatus = []      # to save which frames were taken or rejected of the buffer

# Historical & Control Arrays
packagesPerFrameArray = []            # history of how many packages has every frame processed
frameOwnersArray = []                 # list of users by frame in the system (owner)
waitInBufferTimePerPackageArr = []    # history of how many seconds ech petition waited in buffer
framesReceivedPerUserArray = []       # count of how many frames each user has received, up to 2000

packagesInBufferArr = []               # history of the number of packages in the system
framesInSystemArr = []                 # history of the number of frames in the system
usersInSystemArr = []                  # history of the number of users in the system
usersBeingServedArr = []               # history of the users being served in the moment

packagesFinalStatusArr = []            # accepted or rejected
framesFinalStatusArr = []              # accepted or rejected
usersFinalStatusArr = []               # accepted or rejected

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
        # one request arrives every 2 seconds, add one user to the system
        requestsTotal += 1
        usersInSystem += 1
        arrivalTimeUsersArray.append(time)
        # userBeingServed = len(arrivalTimeUsersRequestsArray) - 1
        framesReceivedPerUserArray.append(0)
        startStreamingPositionPerUser.append(random.randrange(randomFrameRangeMin, randomFrameRangeMax))
        currentFrameCounterPerUser.append(0)

        # TODO: or time == 2
    elif time > 2 & time-2 % 1/fps == 0:
        # starting on second 2, every 1/24 seconds a user asks for a frame
        framesInSystem += 1
        arrivalTimeFramesArray.append(time)

        # serve only 256 users - wifiLimit - (framesServedPerUser[] < 2000), the other ones wait
        if usersBeingServed < wifiUserLimit:
            # find next user in the array that still needs to receive one of the 2000 frames
            for index, item in enumerate(framesReceivedPerUserArray):
                if item <= packagesTobeServedPerUser & index > userBeingServed:
                    userBeingServed = index  # get the user :)

                    # get next currentFrameSize from framesArray for this user
                    currentFrameCounter = currentFrameCounterPerUser[userBeingServed]
                    currentFrameSize = framesArray[currentFrameCounter]

                    frameOwnersArray.append(userBeingServed)
                    usersBeingServed += 1
        else:
            userBeingServed = 0

            # if packagesOfCurrentFrame <= throughputFrames:
            #     packagesInBuffer += packagesOfCurrentFrame
            # else:
            #     packagesInBuffer += throughputFrames
            #     packagesOfCurrentFrame -= throughputFrames
            #     # TOD O: logic to send the remaining packages the next millisecond

        # for user in arrivalTimeUsersArray:

    elif time % frameLeavesApplicationLayer == 0 & usersInSystem > 0:
        # one frame leaves the application layer every .01 seconds and enters the buffer

        # TODO: Check G
        # TODO: Compute G = packagesFailed/PackagesServed

        if waitInBufferTime <= 1 & packagesInBuffer+numPackagesOfCurrentFrame <= bufferSizeInPackages:
            # send packages of one user to the network layer

            # divide frame in packages
            while currentFrameSize >= 1500:
                # subdivide frames into packages
                currentFrameSize - 1500
                numPackagesOfCurrentFrame += 1
            if currentFrameSize > 0:
                numPackagesOfCurrentFrame += 1

            packagesPerFrameArray.append(numPackagesOfCurrentFrame)

            packagesInBuffer += numPackagesOfCurrentFrame
            frameAcceptedInBufferStatus.append("accepted")
            framesAcceptedInBuffer += 1
            packagesInBuffer += numPackagesOfCurrentFrame
        else:
            frameAcceptedInBufferStatus.append("rejected")
            framesRejectedFromBuffer += 1
            # TODO: marcar todos los paquetes como rechazados (no añadir paquetes al sistema)

        currentFrameCounter += 1
        currentFrameCounterPerUser[userBeingServed] = currentFrameCounter

    elif time % packageLeavesBufferTime == 0 & packagesInBuffer > 0:
        # one package leaves the buffer every .000222 seconds

        departureTimePackagesArray.append(time)
        packagesInBuffer -= 1
        packagesServed += 1
        servedPackagesOfCurrentFrame += 1

        # compute W
        waitInBufferTime = 1/(4500 - numPackagesOfCurrentFrame) + amazonCurrentDelay
        # compute and save e
        probabilityPackageSendFail = eDividedByK*usersInSystem
        probabilityPackageSendFailArr.append(probabilityPackageSendFail)

        # check e
        randomE = round(random.uniform(0, 1), 4)  # probability with 4 decimals
        if randomE > probabilityPackageSendFail:
            packagesFinalStatusArr.append("success")
        else:
            packagesFinalStatusArr.append("error")
            packagesArrivedWithError += 1

        # === Follow-up of the packages->frames->users final status and departure times ===

        # When all the packages of one frame are served
        if servedPackagesOfCurrentFrame == numPackagesOfCurrentFrame:
            framesServed.append(currentFrameCounter)  # this array might be unnecessary
            departureTimeFramesArray.append(time)
            servedPackagesOfCurrentFrame = 0

            # TODO: Search for one "error" in the packagesFinalStatusArr from ___ to numPackagesOfCurrentFrame later

        # what is this?
        packs = 0
        for numOfPackages in packagesPerFrameArray:
            if packagesServed < packs:
                packs += numOfPackages  # wtf!

        # framesInSystem -= 1, departureTimeFramesArray.append(time)

        # TODO: when 2000 frames of one user are served:
        # usersServed += 1, usersInSystem -= 1, departureTimeUsersArray.append(time)

amazonCurrentDelayCounter += 1

# ====== Compute LU ======

lp = (packagesServed+packagesInBuffer)/time  # also compute this in excel
lf = (framesServed+framesInSystem)/time      # also compute this in excel
lu = (usersServed+usersInSystem)/time        # also compute this in excel


printableResults = [usersInSystem]

# TODO: Print 2 csv files

with open("results.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(printableResults)