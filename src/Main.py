__author__ = 'Alejandro Hdz. Cruz, Federico Vorrath'

# Imports
import csv

# ====== Declare global variables ======

# Static constants
Lambda = 0.5                        # rate of requests entering the system every second
simulation_limit = 2000             # number of packages sent in the entire simulation
throughputFrames = 100              # number of frames going out of the application layer (1/r)
throughputPackages = 4500           # rate of packages leaving the buffer every second
requestArrivalTime = 1/Lambda       # Average time between any user request
packageLeavesBufferTime = 1/throughputFrames    # Average time in which a package leaves the buffer

# Variables
time = 0.000000                     # current simulation time in microseconds
processedFrames = 0                 # frames that were served through the system
requests = 0                        # number of requests made to the server
users = 0                           # number of users currently in the system
usersServed = 0                     # number of users that were well served by the system

np = 0                              # number of packages currently in the system
nf = 0                              # number of frames currently in the system
nu = 0                              # number of users currently in the system

sp = 0                              # Integral of the number of packages in the system
sf = 0                              # Integral of the number of frames in the system
su = 0                              # Integral of the number of users in the system

lp = 0                              # total packages in system
lf = 0                              # total frames in system
lu = 0                              # total users in system

serviceTime = 0                     # total service time (occupation time)
utilization = 0                     # percentage of utilization of the system
delay = 0

# Arrays
requestsArrivalTime = []            # time in which every request entered the system
requestsDepartureTime = []          # time in which every request left the system
framesTimeArrival = []              # time in which every frame entered the system
framesTimeDeparture = []            # time in which every frame left the system
packagesTimeArrival = []            # time in which every package entered the system
packagesTimeDeparture = []          # time in which every package left the system

framesArray = []                    # the 2000 frames to be served (from the .csv file)
delaysArray = []                    # Amazon delays from the .csv file
bandwidth = []                      # bits transferred every second

npArray = []                        # array of the number of packages in the system
nfArray = []                        # array of the number of frames in the system
nuArray = []                        # array of the number of users in the system


# Read delay data from csv file
with open('/rsc/AmazonS3_delays-Ag-15.csv', 'rb') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvReader:
        print ', '.join(row)

# Read frames from csv file
