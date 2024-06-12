#######################################################################################################
# Title: Hodoscope Selection
# Description: Read a Janus output file and filter events based on hodoscope hits (select valid
#    combinations of hodo hits in the muon telescope configuration). For each channel, make a list of
#    events where the reconstructed muon track passes through that channel. Also make a list of events
#    where the muon track did not pass through that channel. Compare the two energy distributions
#    (we expect them to be different). Also compare to data from a second run, which used the periodic
#    trigger as a control.
# Arguments: 1. Run number of muon telescope run; Options: -ptrg [periodic trigger run number] to set run
#     number of ptrg run, -p to make debugging/control plots, -t to add a string to title (must be the last
#     argument), -n [nboards] to set number of boards (default to 2)
#     N.B. there are also many important parameters in calibsettings.py
# Run with (e.g.):
#    python3 hodoselection.py 4004 -ptrg 4080 -p -t HG = 20
#    python3 hodoselection.py 2928 -n 1 -ptrg 4081 -p -t HG = 50, Horizontal Orientation
# Author: Catherine Miller, cmiller6@bu.edu
# Date: 29 May 2024
#######################################################################################################

import pandas
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as fit
from calibsettings import *
from ROOT import *

fitrange = (0,800)
fitrangelg = (0,500)

class calibrate:
    def __init__(self, run_i, run_ptrg, title, homedir, fitrange):
        self.run_i = run_i
        self.run_ptrg = run_ptrg
        self.title = title #label for plots
        self.homedir = homedir #arguments: initial run number, initial gain settings
        self.fitrange = fitrange
    ch_lg = {}
    ch_hg = {}
    ch_hg_control = {}
    ch_hg_ptrg = {}
    ch12 = [[0],[0]] #for each trigger combo
    colors = ['red','blue','green','purple']
    #event count
    neventstotal = 0

    for ch in range(4):
        ch_hg[ch] = [0]
        ch_lg[ch] = [0]
        ch_hg_control[ch] = [0]
        ch_hg_ptrg[ch] = [0]

    rawlist_hg = [[[] for _ in range(4)] for _ in range(2)] #brd, ch, evt
    rawlist_lg = [[[] for _ in range(4)] for _ in range(2)]
    evtlist = [[] for _ in range(2)] #brd, evt

    def readevent2board(self,infile):
        time = 0
        #this simply constructs an event list sorted by trgid and board
        #we will later pare down lists based on trigger logic
        for ch in range(4):
            line = infile.readline()
            if not line: return False, time
            while ("//" in line) or ("Tstamp" in line): line = infile.readline()
            if ch == 0:
                evt = int(line.split()[1])
                brd = int(line.split()[2])
                '''
                if evt != 0:
                    if (self.evtlist[brd][-1] != evt-1):
                        for i in range(evt-1 -self.evtlist[brd][-1]):
                            for j in range(4):
                                self.rawlist_lg[brd][j].append(0)
                                self.rawlist_hg[brd][j].append(0)
                            print("filling in skipped event")
                if evt > 3000: return False, time'''
                self.evtlist[brd].append(evt)
                #print(self.evtlist[brd][-1])
                self.rawlist_lg[brd][ch].append(float(line.split()[4]))
                self.rawlist_hg[brd][ch].append(float(line.split()[5]))
                time = float(line.split()[0])
            else:
                self.rawlist_lg[brd][ch].append(float(line.split()[2]))
                self.rawlist_hg[brd][ch].append(float(line.split()[3]))
        return True, time
    def readeventsingleboard(self,infile): #read one event and add appropriate channels to histogram
        time = 0
        lg = []
        hg = []
        for brd in range(2): #there are not really 2 boards but we will pretend: hodos on board 0
            for ch in range(4): #for now rely on the fact that EMCal hits (brd 1) appear before hodo hits (brd 0) in event list
                line = infile.readline()
                if not line: return False, time
                while ("//" in line) or ("Tstamp" in line): line = infile.readline()
                if (ch==0 and brd == 0):
                    time = float(line.split()[0])
                    lg.append(float(line.split()[4]))
                    hg.append(float(line.split()[5]))
                else:
                    lg.append(float(line.split()[2]))
                    hg.append(float(line.split()[3]))
            self.rawlist_lg[brd-1].append(lg)
            self.rawlist_hg[brd-1].append(hg)
        return True, time

    def hodotrigger(self): #hodoscope trigger logic--construct list of events
        npath = 2*[0]
        #print(self.evtlist[::][-1])
        for evt in range(np.min([len(self.evtlist[0]), len(self.evtlist[1])])):
            hodohits = []
            for hodoch in range(4):
                if self.rawlist_lg[0][hodoch][evt] > 350:
                    hodohits.append(chlist[hodoch + 4])
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
                    self.ch_lg[ch1].append(self.rawlist_lg[1][ch1][evt])
                    self.ch_lg[ch2].append(self.rawlist_lg[1][ch2][evt])
                    self.ch_hg[ch1].append(self.rawlist_hg[1][ch1][evt])
                    self.ch_hg[ch2].append(self.rawlist_hg[1][ch2][evt])
                    self.ch_hg_control[ch1cont].append(self.rawlist_hg[1][ch1cont][evt])
                    self.ch_hg_control[ch2cont].append(self.rawlist_hg[1][ch2cont][evt])
                #ch12[i].append(ch12adc) #just never use this array if there is no control channel 12
        #print out some run information:
        #calculate run length
        print("Analyzed run "+str(self.run_i))
        time_str = ""
        hours = int(np.round(self.lasttime/3600))
        if hours != 0: time_str += str(hours) + " h, "
        min = int(np.round(np.mod(self.lasttime,3600)/60))
        if min != 0: time_str += str(min) + " m, "
        s = int(np.round(np.mod(self.lasttime,60)))
        time_str += str(s) + " s"
        print("\nNumber of events passing trigger path 1: "+str(npath[0]))
        print("Number of events passing trigger path 2: "+str(npath[1]))
        print("Total events passing selection: "+str(npath[0]+npath[1]))
        print("Run length: "+time_str)
        print("Event rate (passing selection): "+str(np.round((npath[0]+npath[1])/self.lasttime,5))+" Hz \n")




    def readfile_singleboard(self):
        linegood = True
        with open(self.homedir+"DataFiles/Run"+str(self.run_i)+"_list.txt") as infile:
            while linegood:
                linegood, time = self.readeventsingleboard(infile)
                if (linegood): time_s = time*10**(-6)
        self.lasttime = time_s

    def readfile_multiboard(self): #for two board setup
        linegood = True
        with open(self.homedir+"DataFiles/Run"+str(self.run_i)+"_list.txt") as infile:
            while linegood:
                linegood, time = self.readevent2board(infile)
                if (linegood): time_s = time*10**(-6)
        self.lasttime = time_s

    def readfile_ptrg(self):
        #now read from periodic trigger file
        with open(self.homedir+"DataFiles/Run"+str(self.run_ptrg)+"_list.txt") as infile:
            for line in infile:
              if ("//" in line): continue
              if ("Tstamp" in line): continue
              for ch in range(4):
                if ("01  "+chlist[ch] in line):
                  if (ch==0):
                    #ch_lg[ch].append(float(line.split()[4]))
                    self.ch_hg_ptrg[ch].append(float(line.split()[5]))
                  else:
                    #ch_lg[ch].append(float(line.split()[2]))
                    self.ch_hg_ptrg[ch].append(float(line.split()[3]))


    def analyze_control_hits(self):
        mpv_control = []
        mpverr_control = []
        names = ['Track through channel','Track outside channel', 'Periodic trigger']
        for i in range(4):
            plt.figure()
            k = 0
            for arr in [self.ch_hg[i],self.ch_hg_control[i],self.ch_hg_ptrg[i]]:
                hist,bins = np.histogram(arr, range = fitrange,bins=25)
                #find bin centers
                bin_center = []
                for j in range(len(bins)-1):
                    bin_center.append((bins[j]+bins[j+1])/2)
                #find average of histogram
                clipped = []
                for j in range(len(arr)):
                    if (arr[j] < self.fitrange[1]) and (arr[j] > self.fitrange[0]):
                        clipped.append(arr[j])
                if len(clipped) == 0:
                    clipped.append(1) #this doesn't mean anything, should just help keep your code from breaking
                mpv_control.append(np.average(np.array(clipped)))
                mpverr_control.append(np.std(np.array(clipped))/np.sqrt(len(clipped)))
                plt.hist(arr,bins=50,label=names[k],color=self.colors[k],fill=False,histtype='step',edgecolor=self.colors[k],range=fitrange, density = True)
                x = np.arange(*fitrange,1)
                #plt.plot(x,gauss(x,*popt),color=colors[i])
                ylim = plt.gca().get_ylim()
                plt.ylim(0,.01)
                plt.plot(np.repeat(np.average(np.array(clipped)),1000),np.arange(0,1000,1),color=self.colors[k],linestyle = "dotted", label = "Mean, "+names[k])
                plt.xlim(*self.fitrange)
                plt.xlabel("ADC (High Gain)")
                plt.ylabel("Counts")
                plt.title("Cosmic Muon Telescope Studies, "+self.title+", Channel "+str(i),wrap=True)
                plt.legend()
                k+=1
            plt.savefig(homedir+"Figures/Telescope_Comparison_ptrg_Run"+self.run_i+"_Channel_"+str(i)+".pdf")
            plt.savefig(homedir+"Figures/Telescope_Comparison_ptrg_Run"+self.run_i+"_Channel_"+str(i)+".png")
            print("Saving figure "+homedir+"Figures/Telescope_Comparison_ptrg_Run"+self.run_i+"_Channel_"+str(i)+".pdf")
            print("Saving figure "+homedir+"Figures/Telescope_Comparison_ptrg_Run"+self.run_i+"_Channel_"+str(i)+".png")
        print(mpv_control)
        print(mpverr_control)
    '''
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
                plt.title("Cosmic Muon Telescope Studies, "+self.title+", Channel "+str(i))
                plt.legend()
                k+=1
            plt.savefig(homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".pdf")
            plt.savefig(homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".png")
            print("Saving figure "+homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".pdf")
            print("Saving figure "+homedir+"Figures/Ch12_Comparison_ptrg_Run"+str(sys.argv[1])+"_Channel_"+str(i)+".png")
        print(mpv_control)
        print(mpverr_control)
    '''
    def twoside_correlation(self,channel1, channel2):
        plt.figure()
        plt.hist2d(self.ch_hg[channel1],self.ch_hg_control[channel2],bins = [20,20],range = [self.fitrange,[0,200]]) #ch_hg_control[1]
        plt.title("Cosmic Muon Telescope Lateral Correlation, Run "+self.run_i+", "+self.title, wrap=True)
        plt.xlabel("Channel "+str(channel1)+" ADC (Within Track)")
        plt.ylabel("Channel "+str(channel2)+" ADC (No Track)")
        figtitle = self.homedir +"Figures/bilateral_correlation_Run_"+self.run_i+"ch"+str(channel1)+"ch"+str(channel2)
        plt.savefig(figtitle+".pdf")
        plt.savefig(figtitle+".png")
        print("Saving figure "+figtitle+".pdf")
        print("Saving figure "+figtitle+".png")
    def ptrg_correlation(self,channel1,channel2):
        plt.figure()
        plt.hist2d(self.ch_hg[channel1],self.ch_hg_control[channel2],bins = [20,20],range = [[10,100],[10,100]]) #ch_hg_control[1]
        plt.title("EMCal Periodic Trigger Correlation, Run "+self.run_ptrg, wrap=True)
        plt.xlabel("Channel "+str(channel1)+" ADC")
        plt.ylabel("Channel "+str(channel2)+" ADC")
        figtitle = self.homedir +"Figures/ptrg_correlation_Run_"+self.run_ptrg+"ch"+str(channel1)+"ch"+str(channel2)
        plt.savefig(figtitle+".pdf")
        plt.savefig(figtitle+".png")
        print("Saving figure "+figtitle+".pdf")
        print("Saving figure "+figtitle+".png")
    '''
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
    '''
    def plot4channel(self):
        #for each trigger combo, plot all four channels together
        mpv_control = []
        mpverr_control = []
        titles = ['Trigger combination 1 -- Channel 1', 'Trigger combination 2 -- Channel 0']
        for i in range(2): #iterate over trigger combinations
            plt.figure()
            for j in range(2): #iterate over "right" and "wrong" trigger combinations
                elist = [self.ch_hg[channelcombos[i][j]], self.ch_hg_control[channelcombos[i-1][j]]]
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
                        if (elist[k][l] < self.fitrange[1]) and (elist[k][l] > self.fitrange[0]):
                            clipped.append(elist[k][l])
                    if len(clipped) == 0:
                        clipped.append(1) #this doesn't mean anything, should just help keep your code from breaking
                    #mpv_control.append(np.average(np.array(clipped)))
                    #mpverr_control.append(np.std(np.array(clipped))/np.sqrt(len(clipped)))
                    plt.hist(elist[k],bins=50,label="Channel "+names[k],color=self.colors[2*j+k],fill=False,histtype='step',edgecolor=self.colors[2*j+k],range=self.fitrange, density = True)
                    x = np.arange(*self.fitrange,1)
                    #plt.plot(x,gauss(x,*popt),color=colors[i])
                    ylim = plt.gca().get_ylim()
                    plt.ylim(0,.01)
                    #plt.plot(np.repeat(np.average(np.array(clipped)),1000),np.arange(0,1000,1),color=colors[k],linestyle = "dotted", label = "Mean, "+names[k])
                    plt.xlim(*self.fitrange)
                    plt.xlabel("ADC (High Gain)")
                    plt.ylabel("Probability Density")
                    plt.title("Cosmic Muon Telescope Studies, "+self.title+", "+titles[i],wrap=True)
                    plt.legend()
            plt.savefig(self.homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+self.run_i+".pdf")
            plt.savefig(self.homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+self.run_i+".png")
            print("Saving figure "+self.homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+self.run_i+".pdf")
            print("Saving figure "+self.homedir+"Figures/Telescope_4channel_combo"+str(i)+"Run_"+self.run_i+".png")

    def savehistos(self):
        h_lg = {}
        h_hg = {}
        for ch in range(4):
            h_lg[ch] = TH1F("h_lgch"+chlist[ch],"h_lgch"+chlist[ch], 25, fitrangelg[0], fitrangelg[1])
            h_hg[ch] = TH1F("h_hgch"+chlist[ch],"h_hgch"+chlist[ch], 25, fitrange[0], fitrange[1])
            for i in range(len(self.ch_lg[ch])):
                h_lg[ch].Fill(self.ch_lg[ch][i])
                h_hg[ch].Fill(self.ch_hg[ch][i])
            h_lg[ch].SaveAs(self.homedir+"DataFiles/h_lgch"+chlist[ch]+"_Run"+str(self.run_i)+".root")
            h_hg[ch].SaveAs(self.homedir+"DataFiles/h_hgch"+chlist[ch]+"_Run"+str(self.run_i)+".root")

    def offlineselection(self,nboards):
        if nboards > 1:
            self.readfile_multiboard()
        else:
            self.readfile_singleboard()
        self.hodotrigger()
        self.savehistos()
        
    def telescope_control(self):
        #basically several checks
        self.readfile_ptrg()
        self.analyze_control_hits()
        self.twoside_correlation(1,0)
        self.twoside_correlation(0,1)
        self.twoside_correlation(2,3)
        self.twoside_correlation(3,2)
        self.plot4channel()
    #compare_channel_12()
    #ch12_correlation(run_i,gain)


if __name__ == "__main__":
    #read optional arguments
    i = 2
    cplots = False
    ptrgrun = 4080
    title = ''
    nboards = 2
    while i < len(sys.argv):
        option = sys.argv[i]
        if option == "-ptrg":
            i += 1
            ptrgrun = sys.argv[i]
        if option == "-t":
            for j in range(len(sys.argv)-i-1):
                i += 1
                title += sys.argv[i] + ' '
        if option == "-p": #make control plots
            cplots = True
        if option == "-n":
            i += 1
            nboards = int(sys.argv[i])
        i += 1
    if cplots == True:
        c = calibrate(sys.argv[1],ptrgrun,title,homedir,fitrange)
        c.offlineselection(nboards)
        c.telescope_control()
        c.ptrg_correlation(0,1)
    else:
        c = calibrate(sys.argv[1],ptrgrun,title,homedir,fitrange)
        c.offlineselection(nboards)



