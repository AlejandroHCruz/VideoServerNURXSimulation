from __future__ import division
__author__ = 'Alejandro Hdz. Cruz'

# Imports
import csv
import random
import numpy as np  # install in your computer: http://stackoverflow.com/questions/1273203/cant-import-numpy-in-python

# ====== Declare global variables ======

# === Static constants ===

# change to test different simulation results
eDividedByK = .001                  # to answer question 1 {.001, .01, .1}
frameMinSuccessRate = .9            # to answer question 1 {.9, .95, .99}
bufferSizeInPackages = 50           # to answer question 2 {50, 100, 250 & 500 } (n)
probServerSaturationLimit = .05     # to answer question 2 {.05, .01, .001}
fixedUsers = 5                      # to answer question 2 {5, 10, 15, 20}

# fixed
simulationTime = 600                # Time the simulation will run
Lambda = 0.5                        # rate of requests entering the system every second (1/tp)
requestArrivalTime = 1/Lambda       # Average time between any user request (tp = 2)
waitTimeMax = 1                     # U. 1 second in seconds
packagesTobeServedPerUser = 2000    # number of packages that every user receives
throughputPackages = 4500           # rate of packages leaving the buffer every second (Miu)
packageLeavesBufferTime = round(1/throughputPackages, 6)  # Average time in which a package leaves the buffer(.000222)
randomFrameRangeMin = 10            # Used to choose the start of the frames to be sent to any user (randrange)
randomFrameRangeMax = 87997         # Used to choose the end of the frames to be sent to any user (randrange)
wifiUserLimit = 256                 #
fps = 24.0                          # Each video runs at 24 frames per second (frame request per user)
videoRatePerUser = round(1/fps, 6)  # Each user needs one frame 24 times per second
bandwidthMaxInPackages = 4500

# UPDATE: the limitation of 100 fps was removed of the simulation
# frameLeavesApplicationLayer = .01   # r
# throughputFrames = 1/frameLeavesApplicationLayer  # number of frames going out of the application layer (1/r= 100)

# === Variables ===

# time
time = 1.9                          # current simulation time in seconds
serviceTimePackage = 0                 # total service time in seconds (occupation time)
serviceTimeFrame = 0                 # total service time in seconds (occupation time)
serviceTimeUser = 0                 # total service time in seconds (occupation time)

# users
usersInSystem = 0                   # number of users currently in the system
usersServed = 0                     # users whose 2000 frames came through the system
usersSuccess = 0                    # number of users that were well served by the system
usersFailed = 0                     # users that received a corrupt video
usersAcceptedInBuffer = 0           #
usersRejectedFromBuffer = 0         #
usersDelivered = 0                  #
usersNotDelivered = 0               # these users received a corrupt video (without 1 or more packages)
usersBeingServed = 0                # users being served in any moment (max 256)
currentUserIndex = 0                # position that the current user has in the users/petitions array
servedFramesOfCurrentUser = 0       #
lastUserServed = -1                 #

lu = 0                              # average of users in system

# frames
framesInSystem = 0                  # number of frames currently in the system
framesServed = 0                    # frames that went out of the system
framesSuccess = 0                   # frames that were successfully served through the system
framesFailed = 0                    # frames that failed due to waiting or e
framesAcceptedInBuffer = 0          # frames that waited less than 1 second
framesRejectedFromBuffer = 0        # frames that waited more than 1 second
framesDelivered = 0                 #
framesNotDelivered = 0              #
currentFrameSize = 0                #
currentFrameIndex = 0               # id of the frame being sent to the user
currentFrameStreamingIndex = 0      # position of the original frame sequence being streamed to the current user
numPackagesOfCurrentFrame = 0       #
servedPackagesOfCurrentFrame = 0    #
lastFrameServed = -1                #

lf = 0                              # average of frames in system

# packages
packagesInSystem = 0                # number of packages currently in the system
packagesServed = 0                  # packages that went out of the system
packagesSuccess = 0                 # packages that were successfully served through the system
packagesFailed = 0                  # packages that failed to be delivered or accedpted in the system
packagesAcceptedInBuffer = 0
packagesRejectedFromBuffer = 0
packagesDelivered = 0               # made it to their destiny
packagesNotDelivered = 0            # failed because of e
# packagesInBuffer = 0              # number of packages waiting to go out of the system
packagesPendingForCurrentFrame = 0  #
currentPackageIndex = 0             #
currentPackageSize = 0              #
lastPackageServed = -1              #

lp = 0                              # average of packages in system

# probabilities
G = 0                               # probability of buffer saturation
e = eDividedByK*usersInSystem       # probability of package not arriving its destination
randomE = 0                         # to compare e with and determine if a package arrives successfully to client

# delays
delay = 0                           # total waiting time: timeInBuffer + amazonCurrentDelay
timeInBuffer = 0                    # time between arrival and departure of the current package
amazonCurrentDelay = 0              #
amazonDelayIndexLimit = 52686       # determined from the csv file provided
amazonCurrentDelayIndex = 0         # used to read the delay from the delays array

# utilization
utilizationUser = 0                 # percentage of utilization of the system
utilizationFrame = 0                # percentage of utilization of the system
utilizationPackage = 0                 # percentage of utilization of the system


# bandwidth
currentBandwidth = 0                # bits coming out of the system

# === Arrays ===

# probabilities
probabilityServerSaturationArr = []  # G
probabilityPackageSendFailArr = []   # e

# users
arrivalTimeUsersArr = []            # time in which every request that reaches the system arrived
departureTimeUsersArr = []          # time in which every request that left the system
usersInSystemArr = []               # history of the number of users in the system
usersBeingServedArr = []            # history of the users going out of the system (not waiting in buffer)
startStreamingPositionPerUser = []  # in which position of the framesArray every user starts
framesDeliveredPerUserArr = []      # count of how many frames have been sent to every user, up to 2000
currentFramePerUserIndex = []       # to know which frame is being served to every user
usersAcceptedInBufferArr = []       # accepted or rejected
usersFullyDeliveredArr = []         # yes or no, depending on it's packages e check

# frames
arrivalTimeFramesArr = []           # time in which every frame entered the system
departureTimeFramesArr = []         # time in which every frame left the system
framesArray = []                    # sequence of the frames to be served
framesOriginalArray = []            # all the video frames that can be served (from the .csv file)
framesInSystemArr = []              # history of the number of frames in the system
# framesServed = []                 # frames that came out of the system
frameSizeArr = []
frameOwnersArr = []                 # list of users by frame in the system (owner)
packagesPerFrameArr = []            # history of how many packages has every frame produced
packagesServedPerFrameArr = []      # to know hoy many packages of each frame have left the system
framesAcceptedInBufferArr = []      # to save which frames were taken or rejected of the buffer
framesFullyDeliveredArr = []        # yes or no, depending on the error e of its packages

# packages
arrivalTimePackagesArr = []         # time in which every package entered the system
departureTimePackagesArray = []     # time in which every package left the system
packagesArray = []                  # Sequence of the packages
packagesInSystemArr = []            # history of the number of packages in the system
packagesAcceptedInBufferArr = []    # accepted or rejected, depending on the error e
packagesDeliveryStatusArr = []      # delivered or failed
packageSizeArr = []                 #
packageOwnersArr = []               # user that will needs every package
frameOfEveryPackage = []            # to know of which frame every package is part of

# delay
delayArr = []                       # history of the # total waiting time: timeInBuffer + amazonCurrentDelay
timeInBufferPerPackageArr = []      # history of how many seconds ech petition waited in buffer
amazonDelaysArr = []                # Amazon delays from the .csv file

# bandwidth
bandwidthArr = []                   # bits transferred every second

# Read Amazon delay data from csv file
delaysReader = csv.reader(open('/mnt/5512B8C217C7CAC1/Dropbox/Desarrollo/Python/VideoServerNURXSimulation/rsc/AmazonS3_delays-Ag-15.csv', 'rb'), delimiter= ',', quotechar='"')
for i in delaysReader:
    amazonDelaysArr.append(i)

framesReader = csv.reader(open('/mnt/5512B8C217C7CAC1/Dropbox/Desarrollo/Python/VideoServerNURXSimulation/rsc/Terse_DieHardIII.csv', 'rb'), delimiter= ',', quotechar='"')
for i in framesReader:
    framesOriginalArray.append(i)

# ====== Main ======

while time < simulationTime:  # Run simulation for "10 minutes"

    # save system's status (saving this might be too much data and we should save it every .01 seconds)
    usersInSystemArr.append(usersInSystem)
    usersBeingServedArr.append(usersBeingServed)
    framesInSystemArr.append(framesInSystem)
    packagesInSystemArr.append(packagesInSystem)
    bandwidthArr.append(currentBandwidth)
    probabilityServerSaturationArr.append(G)
    probabilityPackageSendFailArr.append(e)
    delayArr.append(delay)

    time += 0.000001
    time = round(time, 6)

    # define amazonCurrentDelay
    amazonCurrentDelay = amazonDelaysArr[amazonCurrentDelayIndex]

    # === new user arrives ===
    if (time*1000000) % (requestArrivalTime*1000000) == 0:
        # one user enters the system every 2 seconds

        usersInSystem += 1
        print time, ": user added. Total: ", usersInSystem
        arrivalTimeUsersArr.append(time)
        usersFullyDeliveredArr.append("no")
        framesDeliveredPerUserArr.append(0)
        startStreamingPositionPerUser.append(random.randrange(randomFrameRangeMin, randomFrameRangeMax))
        currentFramePerUserIndex.append(0)

    # === new frames needed ===
    elif ((time*1000000) % (videoRatePerUser*100000) < 0.000001) and (usersInSystem > 0):
        # every 1/24 seconds, every user asks for a frame

        currentUserIndex = 0

        if usersBeingServed < wifiUserLimit:  # serve only 256 users
            # find next user that needs one of her 2000 frames
            for index, item in enumerate(framesDeliveredPerUserArr):
                if item <= packagesTobeServedPerUser and index > currentUserIndex:
                    currentUserIndex = index

        # get index of next currentFrame for current user
        # nextFrameForThisUser = framesOriginalArray[currentFramePerUserIndex[currentUserIndex] + startStreamingPositionPerUser[currentUserIndex]]
        # this shouldn't fail because the randomFrameRangeMax is the frame sequence - 2000
        currentFrameStreamingIndex = currentFramePerUserIndex[currentUserIndex]

        if currentFrameStreamingIndex == 0:
            currentFrameStreamingIndex += startStreamingPositionPerUser[currentUserIndex]
        else:
            currentFrameStreamingIndex += 1

        # save new currentFrameIndex for this user
        currentFramePerUserIndex[currentUserIndex] = currentFrameStreamingIndex

        # add frame to the system
        currentFrameSize = framesOriginalArray[currentFrameStreamingIndex]
        currentFrameSize = np.int32(currentFrameSize)
        arrivalTimeFramesArr.append(time)
        packagesServedPerFrameArr.append(0)
        framesFullyDeliveredArr.append("no")
        frameOwnersArr.append(currentUserIndex)
        frameSizeArr.append(currentFrameSize)
        print time, ": CurrentFrameSize: ", currentFrameSize

        usersBeingServed += 1

        # divide frame in packages
        while currentFrameSize >= 1500:
            # subdivide frames into packages
            currentFrameSize -= 1500
            numPackagesOfCurrentFrame += 1
        if currentFrameSize > 0:
            numPackagesOfCurrentFrame += 1

        packagesPerFrameArr.append(numPackagesOfCurrentFrame)

        packs = 0
        # save data for n-1 packages of the frame
        while packs < (numPackagesOfCurrentFrame-1):
            packageSizeArr.append(1500)
            frameOfEveryPackage.append(currentFrameIndex)
            packageOwnersArr.append(currentUserIndex)
            arrivalTimePackagesArr.append(time)
            packs += 1

        # save data for last package of the frame
        packageSizeArr.append(currentPackageSize)
        frameOfEveryPackage.append(currentFrameIndex)
        packageOwnersArr.append(currentUserIndex)
        arrivalTimePackagesArr.append(time)

        if delay > 1 and packagesInSystem+numPackagesOfCurrentFrame < bufferSizeInPackages:
            # reject the frame
            print time, ": Frame rejected. Total: ", framesInSystem, "..."
            framesFailed += 1
            framesRejectedFromBuffer += 1
            framesAcceptedInBufferArr.append("rejected")

            rej = 0
            # mark all the packages of this frame as rejected and failed
            while rej < numPackagesOfCurrentFrame:
                print time, ":", numPackagesOfCurrentFrame, " Packages rejected. Total: ", packagesInSystem
                packagesRejectedFromBuffer += 1
                packagesAcceptedInBufferArr.append("rejected")
                packagesDeliveryStatusArr.append("-")
                rej += 1

        else:
            # accept the frame in the system
            framesInSystem += 1
            print time, ": Frame added. - Total: ", framesInSystem, "..."
            framesAcceptedInBuffer += 1
            framesAcceptedInBufferArr.append("accepted")

            acc = 0
            # mark all the packages of this frame as accepted and in the system
            packagesInSystem += numPackagesOfCurrentFrame
            print time, ":", numPackagesOfCurrentFrame, " packages added. Total: ", packagesInSystem
            while acc < numPackagesOfCurrentFrame:
                packagesAcceptedInBuffer += 1
                packagesAcceptedInBufferArr.append("accepted")
                packagesArray.append(currentPackageIndex)
                acc += 1


# === package leaves ===
    elif (time*1000000) % (packageLeavesBufferTime*1000000) < .000001 and packagesInSystem > 0:
        # one package leaves the buffer every .000222 seconds

        currentBandwidth = 0

        isInSys = False
        inx = 0
        # find next package in system
        while isInSys is False:
            packageInSystemStatus = packagesAcceptedInBufferArr[inx]
            if packageInSystemStatus is "accepted":
                currentPackageIndex = inx
                isInSys = True
                # Compute bandwidth
                currentBandwidth = 1/bandwidthMaxInPackages  # since only one package is being served
            inx += 1

        # remove package from system
        departureTimePackagesArray.append(time)
        packagesInSystem -= 1
        print time, ": Package served. Total: ", packagesInSystem
        packagesServed += 1
        packagesAcceptedInBufferArr[currentPackageIndex] = "served"  # package was served

        # we need cpi to get arrivalTime of package that entered the system
        cpi = 0
        for index, package in enumerate(packagesArray):
            if package == currentPackageIndex:
                currentUserIndex = index
                cpi = index

        # calculate service time
        serviceTimePackage += time - arrivalTimePackagesArr[cpi]

        servedPackagesOfCurrentFrame = packagesServedPerFrameArr[currentFrameIndex]
        servedPackagesOfCurrentFrame += 1
        packagesServedPerFrameArr[currentFrameIndex] = servedPackagesOfCurrentFrame

        # get this package's user and frame
        currentFrameIndex = frameOfEveryPackage[currentPackageIndex]
        currentUserIndex = packageOwnersArr[currentPackageIndex]
        numPackagesOfCurrentFrame = np.int32(packagesPerFrameArr[currentFrameIndex])

        # compute waiting time in Buffer/System
        delay = 1/(4500 - numPackagesOfCurrentFrame) + np.float64(amazonCurrentDelay)
        # delay = departureTimePackagesArray[currentPackageIndex] - arrivalTimePackagesArr[currentPackageIndex]
        # delay += amazonCurrentDelay

        # compute and check e
        e = eDividedByK*usersInSystem
        randomE = round(random.uniform(0, 1), 4)  # probability with 4 decimals
        if randomE > e:
            packagesDeliveryStatusArr.append("delivered")
            packagesDelivered += 1
            packagesSuccess += 1

            # tag package's frame
            if framesFullyDeliveredArr[currentFrameIndex] is not "no":
                framesFullyDeliveredArr[currentFrameIndex] = "yes"
            # tag package's user
            if usersFullyDeliveredArr[currentUserIndex] is not "no":
                usersFullyDeliveredArr[currentUserIndex] = "yes"
        else:
            packagesDeliveryStatusArr.append("failed")
            packagesFailed += 1
            packagesNotDelivered += 1
            # tag package's frame
            framesFullyDeliveredArr[currentFrameIndex] = "no"
            # tag package's user
            usersFullyDeliveredArr[currentUserIndex] = "no"

        # === Follow-up of the packages->frames->users final departure times ===

        # When all the packages of one frame are served
        if servedPackagesOfCurrentFrame == packagesPerFrameArr[currentFrameIndex]:
            # remove frames from the system
            framesInSystem -= 1
            print time, ": Frame served. Total: ", framesInSystem
            departureTimeFramesArr.append(time)
            serviceTimeFrame += time - arrivalTimeFramesArr[currentFrameIndex]

            # up-count the good frames
            framesServed += 1
            if framesFullyDeliveredArr[currentFrameIndex] is "yes":
                framesDelivered += 1
                framesSuccess += 1
            else:
                framesFailed += 1
                framesNotDelivered += 1
                # tag user's delivery status
                usersFullyDeliveredArr[currentUserIndex] = "no"

            fdpu = framesDeliveredPerUserArr[currentUserIndex]
            fdpu += 1
            framesDeliveredPerUserArr[currentUserIndex] = fdpu

            # When the system has already sent 2000 frames to the current user
            if fdpu == packagesTobeServedPerUser:

                print time, ": User served. Total: ", usersInSystem
                # remove user from system
                usersServed += 1
                usersInSystem -= 1
                departureTimeUsersArr.append(time)
                # compute service time
                serviceTimeUser += time - arrivalTimeUsersArr[currentUserIndex]
                # tag user's delivery status
                if usersFullyDeliveredArr[currentUserIndex] != "no":
                    usersFullyDeliveredArr[currentUserIndex] = "yes"
                    usersSuccess += 1
                else:
                    usersFailed += 1

    # Compute G
    if packagesServed > 0:
        G = packagesFailed/packagesServed

    if amazonCurrentDelay < amazonDelayIndexLimit:
        amazonCurrentDelayIndex += 1
    else:
        amazonCurrentDelayIndex = 0


# ====== Compute L & U ======

# average of objects in the system
lp = (packagesServed+packagesInSystem)/time
lf = (framesServed+framesInSystem)/time
lu = (usersServed+usersInSystem)/time

utilizationPackage = serviceTimePackage/time
utilizationFrame = serviceTimeFrame/time
utilizationUser = serviceTimeUser/time

# TODO: Print all csv files

with open("results.csv", "w") as f:
    writer = csv.writer(f)
    # writer.writerows(printableResults)
