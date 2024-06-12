###############################################################
# Title: AutoCalib
# Description: Determine gain settings to inter-calibrate four
#    EMCal channels, using the cosmic muon telescope (mini-
#    hodoscope coincidence trigger). Run this script during a
#    Janus job, and when the first run stops, it will determine
#    the appropriate gain settings for the next.
# Arguments: 1. First run number of calibration
# Author: Catherine Miller, cmiller6@bu.edu
################################################################

import sys
from gaincalibration import calibrate
from set_gain import configread, configset
from os.path import exists
import time
from calibsettings import *

def recalibrate(run_i): #argument: initial run number
    print('hi')
    if exists(homedir+"DataFiles/Janus_Config_Run"+str(run_i)+".txt"):
        infile = homedir + "DataFiles/Janus_Config_Run"+str(run_i)+".txt" #if the config file for previous run has job format
    else: infile = homedir+"Janus_Config.txt" #otherwise assume it has non-job config file name
    gs_i = configread(infile, len(ecalchannels)) #initial gain settings
    gs_f = calibrate(run_i,gs_i,homedir)
    run_f = run_i + 1
    configset(infile,run_f,ecalchannels,gs_f)

run = int(sys.argv[1])
print('test')
bool = True
while(bool):
    try:
        if exists(homedir+"DataFiles/Run"+str(run)+"_list.txt"):
            recalibrate(run)
            run += 1
        time.sleep(60*int(sys.argv[2]))
    except KeyboardInterrupt:
        bool = False
