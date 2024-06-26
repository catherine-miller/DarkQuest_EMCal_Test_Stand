#Title: set_gain
#Description: Reads a Janus config file. Updates it with new gain settings
#Arguments: 1. file name of previous configuration file, 2. run number of next run in calibration, 3. new gain settings to use

import sys
import re
from calibsettings import *

def configread(infilename,nchannels): #reads a file and returns the gain settings of channels 0,1,2,3
    ret = nchannels*[0] #list to store previous gain settings
    with open(infilename) as infile:
        for line in infile:
            if ("HG_Gain " in line): #pass over line where previous individual gain setting is set
                g = int(line.split()[1])
                for i in range(len(ret)):
                    ret[i] = g
            if ("HG_Gain[" in line): #always precedes the individual gain setting for the same channel
                #ch = int(re.split('[|]',line)[2])
                ch = int(line.replace(']','[').split('[')[3])
                if (ch in ecalchannels):
                    ret[ch] = int(line.split()[1])
    infile.close()
    return ret

def configset(infilename,newrunno,channels,gain):
    with open(infilename) as infile, open(homedir+"DataFiles/Janus_Config_Run"+str(newrunno)+".txt", 'w') as outfile:
        for line in infile:
            if not ("HG_Gain[" in line): #pass over line where previous individual gain setting is set
                outfile.write(line)
                if ("HV_IndivAdj[" in line): #always precedes the individual gain setting for the same channel
                    #print(line.replace(']','[').split('['))
                    ch = int(line.replace(']','[').split('[')[3])
                    if (ch in channels):
                        outfile.write("HG_Gain[0]["+str(ch)+"]                      "+str(int(gain[ch]))+"                      #\n")
            else:
                 ch = int(line.replace(']','[').split('[')[3])
                 if not (ch in ecalchannels): outfile.write(line) #for any channels (e.g. hodoscopes) not included in calibration keep previous gain setting
    infile.close()
    outfile.close()

if __name__ == "__main__":
    infilename = sys.argv[1]
    newrunno = sys.argv[2]
    gain_str = sys.argv[3].split(",")
    gain = []
    for g in gain_str:
        gain.append(int(g))
    print(configread(infilename))
    configset(infilename, newrunno, channels, gain)
