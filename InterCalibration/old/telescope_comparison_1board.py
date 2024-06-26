#######################################################################################################
# Title: Telescope Comparison
# Description: Read a Janus output file and filter events based on hodoscope hits (select valid
#    combinations of hodo hits in the muon telescope configuration). For each channel, make a list of
#    events where the reconstructed muon track passes through that channel. Also make a list of events
#    where the muon track did not pass through that channel. Compare the two energy distributions
#    (we expect them to be different). Also compare to data from a second run, which used the periodic
#    trigger--this is an even more controlled control.
# Arguments: 1. Run number of muon telescope run, 2. Run number of ptrg run, 3. Gain setting (for the
#     purpose of legend)
#     N.B. there are also many important parameters in calibsettings.py
# Run with (e.g.):
#    python3 telescope_comparison.py 4004 4080 20
#    python3 telescope_comparison.py 2928 4081 50
# Author: Catherine Miller, cmiller6@bu.edu
# Date: 3 May 2024
#######################################################################################################

import pandas
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as fit
from calibsettings import *

fitrange = (0,500)

def calibrate(run_i, run_ptrg, gain, homedir): #arguments: initial run number, initial gain settings
    ch_lg = {}
    ch_hg = {}
    ch_hg_control = {}
    ch_hg_ptrg = {}
    ch12 = [[0],[0]] #for each trigger combo
    colors = ['red','blue','green','purple']
    #event count
    npath = 2*[0]
    neventstotal = 0

    for ch in range(4):
        ch_hg[ch] = [0]
        ch_lg[ch] = [0]
        ch_hg_control[ch] = [0]
        ch_hg_ptrg[ch] = [0]
    def readevent(infile): #read one event and add appropriate channels to histogram
        time = 0
        hodohits = []
        lg = []
        hg = []
        for ch in range(4): #for now rely on the fact that EMCal hits (brd 1) appear before hodo hits (brd 0) in event list
            line = infile.readline()
            if not line: return False, time
            while ("//" in line) or ("Tstamp" in line): line = infile.readline()
            if (ch==0):
                time = float(line.split()[0])
                lg.append(float(line.split()[4]))
                hg.append(float(line.split()[5]))
            else:
                lg.append(float(line.split()[2]))
                hg.append(float(line.split()[3]))
        for hodo in range(len(chlist)-4):
            line = infile.readline()
            if not line: return False, time
            if (hodo == 0 and len(line.split()) > 4):
                if float(line.split()[4]) > 280:
                    hodohits.append(chlist[hodo + 4])
            else:
                if float(line.split()[2])> 280:
                    hodohits.append(chlist[hodo + 4])
            #ch12adc = float(line.split()[3])
        for i in range(2):
            combo = triggercombos[i]
            if (combo[0] in hodohits) and (combo[1] in hodohits):
                npath[i] += 1
                #the channels the particle did go through:
                ch1 = channelcombos[i][0]
                ch2 = channelcombos[i][1]
                #the channels the particle did not go through:
                ch1cont = channelcombos[i-1][0]
                ch2cont = channelcombos[i-1][1]
                ch_lg[ch1].append(lg[ch1])
                ch_lg[ch2].append(lg[ch2])
                ch_hg[ch1].append(hg[ch1])
                ch_hg[ch2].append(hg[ch2])
                ch_hg_control[ch1cont].append(hg[ch1cont])
                ch_hg_control[ch2cont].append(hg[ch2cont])
                #ch12[i].append(ch12adc) #just never use this array if there is no control channel 12
        return True, time





    linegood = True
    with open(homedir+"DataFiles/Run"+str(run_i)+"_list.txt") as infile:
        while linegood:
            linegood, time = readevent(infile)
            if (linegood): time_s = time*10**(-6)

    #now read from periodic trigger file
    with open(homedir+"DataFiles/Run"+str(run_ptrg)+"_list.txt") as infile:
        for line in infile:
          if ("//" in line): continue
          if ("Tstamp" in line): continue
          for ch in range(4):
            if ("00  "+chlist[ch] in line):
              if (ch==0):
                #ch_lg[ch].append(float(line.split()[4]))
                ch_hg_ptrg[ch].append(float(line.split()[5]))
              else:
                #ch_lg[ch].append(float(line.split()[2]))
                ch_hg_ptrg[ch].append(float(line.split()[3]))


    #ch_hg[2] = np.sqrt(8.5**2+20**2)/np.sqrt(12.5**2+20**2)*np.array(ch_hg[2])
    #ch_hg[0] = np.sqrt(8.5**2+20**2)/np.sqrt(12.5**2+20**2)*np.array(ch_hg[0])

    def analyze_control_hits():
    #anal
        mpv_control = []
        mpverr_control = []
        names = ['Track through channel','Track outside channel', 'Periodic trigger']
        for i in range(4):
            plt.figure()
            k = 0
            for arr in [ch_hg[i],ch_hg_control[i],ch_hg_ptrg[i]]:
                hist,bins = np.histogram(ch_hg[i], range = fitrange,bins=25)
                #find bin centers
                bin_center = []
                for j in range(len(bins)-1):
                    bin_center.append((bins[j]+bins[j+1])/2)
                #find average of histogram
                clipped = []
                for j in range(len(arr)):
                    if (arr[j] < fitrange[1]) and (arr[j] > fitrange[0]):
                        clipped.append(arr[j])
                if len(clipped) == 0:
                    clipped.append(1) #this doesn't mean anything, should just help keep your code from breaking
                mpv_control.append(np.average(np.array(clipped)))
                mpverr_control.append(np.std(np.array(clipped))/np.sqrt(len(clipped)))
                plt.hist(arr,bins=50,label=names[k],color=colors[k],fill=False,histtype='step',edgecolor=colors[k],range=fitrange, density = True)
                x = np.arange(*fitrange,1)
                #plt.plot(x,gauss(x,*popt),color=colors[i])
                ylim = plt.gca().get_ylim()
                plt.ylim(0,.01)
                plt.plot(np.repeat(np.average(np.array(clipped)),1000),np.arange(0,1000,1),color=colors[k],linestyle = "dotted", label = "Mean, "+names[k])
                plt.xlim(*fitrange)
                plt.xlabel("ADC (High Gain)")
                plt.ylabel("Counts")
                plt.title("Cosmic Muon Telescope Studies, HG "+gain+", Channel "+str(i))
                plt.legend()
                k+=1
            plt.savefig(homedir+"Figures/Telescope_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".pdf")
            plt.savefig(homedir+"Figures/Telescope_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".png")
            print("Saving figure "+homedir+"Figures/Telescope_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".pdf")
            print("Saving figure "+homedir+"Figures/Telescope_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".png")
        print(mpv_control)
        print(mpverr_control)
    def compare_channel_12():
    #anal
        mpv_control = []
        mpverr_control = []
        names = ['Track through channel','Track outside channel', 'Periodic trigger','Control channel--No SiPM']
        for i in range(2):
            plt.figure()
            k = 0
            for arr in [ch_hg[i],ch_hg_control[i],ch_hg_ptrg[i],ch_hg[1]]: #this ch12 index depends on hodo combo info
                hist,bins = np.histogram(ch_hg[i], range = fitrange,bins=25)
                #find bin centers
                bin_center = []
                for j in range(len(bins)-1):
                    bin_center.append((bins[j]+bins[j+1])/2)
                #find average of histogram
                clipped = []
                for j in range(len(arr)):
                    if (arr[j] < fitrange[1]) and (arr[j] > fitrange[0]):
                        clipped.append(arr[j])
                if len(clipped) == 0:
                    clipped.append(1) #this doesn't mean anything, should just help keep your code from breaking
                mpv_control.append(np.average(np.array(clipped)))
                mpverr_control.append(np.std(np.array(clipped))/np.sqrt(len(clipped)))
                plt.hist(arr,bins=50,label=names[k],color=colors[k],fill=False,histtype='step',edgecolor=colors[k],range=fitrange, density = True)
                x = np.arange(*fitrange,1)
                #plt.plot(x,gauss(x,*popt),color=colors[i])
                ylim = plt.gca().get_ylim()
                plt.ylim(0,.01)
                plt.plot(np.repeat(np.average(np.array(clipped)),1000),np.arange(0,1000,1),color=colors[k],linestyle = "dotted", label = "Mean, "+names[k])
                plt.xlim(*fitrange)
                plt.xlabel("ADC (High Gain)")
                plt.ylabel("Counts")
                plt.title("Cosmic Muon Telescope Studies, HG "+gain+", Channel "+str(i))
                plt.legend()
                k+=1
            plt.savefig(homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".pdf")
            plt.savefig(homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".png")
            print("Saving figure "+homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".pdf")
            print("Saving figure "+homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".png")
        print(mpv_control)
        print(mpverr_control)
    def twoside_correlation(run,gain):
        plt.figure()
        plt.hist2d(ch_hg[3],ch_hg_control[0],bins = [20,20],range = [fitrange,fitrange]) #ch_hg_control[1]
        plt.title("Cosmic Muon Telescope Lateral Correlation, Run "+run+", HG "+gain)
        plt.xlabel("Channel 3 ADC (Within Track)")
        plt.ylabel("Channel 0 ADC (No Track)")
        plt.savefig(homedir +"Figures/bilateral_correlation_Run_"+run_i+".pdf")
        plt.savefig(homedir +"Figures/bilateral_correlation_Run_"+run_i+".png")
        print("Saving figure "+homedir +"Figures/bilateral_correlation_Run_"+run_i+".pdf")
        print("Saving figure "+homedir +"Figures/bilateral_correlation_Run_"+run_i+".png")
    def ch12_correlation(run,gain):
        plt.figure()
        plt.hist2d(ch_hg[0],ch12[0],bins = [20,20],range = [[0,1500],[0,1500]])
        plt.title("Cosmic Muon Telescope Lateral Correlation, Run "+run+", HG "+gain)
        plt.xlabel("Channel 0 ADC (Within Track)")
        plt.ylabel("Channel 12 ADC (No SiPM plugged in)")
        plt.savefig(homedir +"Figures/ch12_correlation_Run_"+run_i+".pdf")
        plt.savefig(homedir +"Figures/ch12_correlation_Run_"+run_i+".png")
        print("Saving figure "+homedir +"Figures/ch12_correlation_Run_"+run_i+".pdf")
        print("Saving figure "+homedir +"Figures/ch12_correlation_Run_"+run_i+".png")
    def plot4channel(run_i):
        #for each trigger combo, plot all four channels together
        mpv_control = []
        mpverr_control = []
        titles = ['Trigger combination 1 -- Channel 1', 'Trigger combination 2 -- Channel 0']
        for i in range(2): #iterate over trigger combinations
            plt.figure()
            for j in range(2): #iterate over "right" and "wrong" trigger combinations
                elist = [ch_hg[channelcombos[i][j]], ch_hg_control[channelcombos[i-1][j]]]
                names = [chlist[channelcombos[i][j]], chlist[channelcombos[i-1][j]]]
                for k in range(2): #iterate over both channels in the combo
                    #this doesn't exactly apply to vertical config. where only 1 channel is correct
                    #but keeping this way for generality
                    hist,bins = np.histogram(elist[k], range = fitrange,bins=25)
                    #find bin centers
                    bin_center = []
                    for l in range(len(bins)-1):
                        bin_center.append((bins[l]+bins[l+1])/2)
                    #find average of histogram
                    clipped = []
                    for l in range(len(elist[k])):
                        if (elist[k][l] < fitrange[1]) and (elist[k][l] > fitrange[0]):
                            clipped.append(elist[k][l])
                    if len(clipped) == 0:
                        clipped.append(1) #this doesn't mean anything, should just help keep your code from breaking
                    #mpv_control.append(np.average(np.array(clipped)))
                    #mpverr_control.append(np.std(np.array(clipped))/np.sqrt(len(clipped)))
                    plt.hist(elist[k],bins=50,label="Channel "+names[k],color=colors[2*j+k],fill=False,histtype='step',edgecolor=colors[2*j+k],range=fitrange, density = True)
                    x = np.arange(*fitrange,1)
                    #plt.plot(x,gauss(x,*popt),color=colors[i])
                    ylim = plt.gca().get_ylim()
                    plt.ylim(0,.01)
                    #plt.plot(np.repeat(np.average(np.array(clipped)),1000),np.arange(0,1000,1),color=colors[k],linestyle = "dotted", label = "Mean, "+names[k])
                    plt.xlim(*fitrange)
                    plt.xlabel("ADC (High Gain)")
                    plt.ylabel("Probability Density")
                    plt.title("Cosmic Muon Telescope Studies, HG "+gain+", "+titles[i])
                    plt.legend()
            plt.savefig(homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+run_i+".pdf")
            plt.savefig(homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+run_i+".png")
            print("Saving figure "+homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+run_i+".pdf")
            print("Saving figure "+homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+run_i+".png")
        

    analyze_control_hits()
    twoside_correlation(run_i,gain)
    plot4channel(run_i)
    #compare_channel_12()
    #ch12_correlation(run_i,gain)
    

if __name__ == "__main__":
    calibrate(sys.argv[1],sys.argv[2],sys.argv[3],homedir)



