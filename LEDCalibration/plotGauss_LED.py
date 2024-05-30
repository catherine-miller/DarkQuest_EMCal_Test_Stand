########################################################
# Title: plotGauss_LED
# Function: read a ROOT file and fit a histogram to a
# Gaussian distribution. Return the mean and standard
# deviation. Write these values, along with the gain
# setting, to a csv file which can be used to make an
# LED voltage scan plot.
# Arguments: channel (in 2-digit format eg 00,01,...),
# run number, LED driving voltage
# Author: Catherine Miller, cmiller6@bu.edu
# Date: 15 May 2024
########################################################

import sys
from ROOT import *
from array import array
import pandas
import os
from IPython.display import display

gStyle.SetOptStat(0)
#gStyle.SetOptTitle(0)
homedir = "/home/cmiller6/"
filename = homedir+'DataFiles/SiPMscan_1stop.csv'

drivingvoltage = [1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3,1.7,1.8,1.9,1.85,1.95,2,2.1,2.2,2.3,2.4,2.5]
#for led calibration drivingvoltage = [1.4,1.45,1.5,1.5,1.55,1.6,1.6,1.65,1.7,1.7,1.75,1.8,1.85,1.9,1.95,1.95,2,2.1,2.2,2.3,2.4,2.5,2.5,2.6,2.7,2.8,2.9,3,3.1,3.2,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.4,4.5,4.6,4.7,4.8,4.9,5]

#Arguments
channels = str(sys.argv[1]).split(",")
runs = str(sys.argv[2]).split(",")
gain = str(sys.argv[3]).split(",")

cols=[1,2,4,6,8,10,12,14,16]
f={}
h={}
fit={}
maximums = []
mpv = []
mpverr = []
stddev = []
stddeverr = []
title = ["Low Gain","High Gain"]
filenm = ["LG","HG"]
adcmax=[8000,8000]
fitmin = [10,30]
fitmax = [8000,8000]
hist = ["h_lgch","h_hgch"]
maxx= 1000

for i in range(2):
  for ch in range(len(channels)):
    #f[ch]=TFile.Open("h_lgch"+channels[ch]+"_max_Run"+runs[ch]+".root","READ")
    #h[ch]=f[ch].Get("h_lgch"+channels[ch]+"_max")
    f[ch]=TFile.Open(homedir+"DataFiles/"+hist[i]+channels[ch]+"_Run"+runs[ch]+".root","READ")
    h[ch]=f[ch].Get(hist[i]+channels[ch])
    h[ch].SetLineColor(cols[ch])
    h[ch].SetMarkerColor(cols[ch])
    h[ch].SetMarkerSize(0.5)
    h[ch].SetMaximum(maxx)
    h[ch].SetMarkerStyle(20)
    h[ch].GetXaxis().SetRangeUser(fitmin[i],fitmax[i])#fitmax[i][3])
    fit[ch]=TF1("fit"+channels[ch],"gaus",fitmin[i],fitmax[i])
    fit[ch].SetLineColor(cols[ch])
    h[ch].Fit("fit"+channels[ch],"R")
    maximums.append(h[ch].GetMaximum())


  #draw superimposed
  c2 = TCanvas("c2","c2",800,600)
  c2.cd()
  leg2 = TLegend(0.6,0.55,0.85,0.85)
  #legs = ["Channel 0","Channel 1","No resistor"]
  for ch in range(len(channels)):
    leg2.AddEntry(fit[ch],"Channel "+channels[ch],"l")
    if (ch==0):
      h[ch].SetTitle("DarkQuest EMCal Cosmic Ray Test Stand; ADC ("+title[i]+"); Counts")
      #h[ch].SetTitle("Inter-Channel Calibration Test; ADC; Counts")
      h[ch].Draw("ep")
      fit[ch].Draw("lsame")
    else:
      h[ch].Draw("epsame")
      fit[ch].Draw("lsame")
      leg2.Draw()
    c2.SaveAs(homedir+"Figures/gaussian_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".pdf")
    c2.SaveAs(homedir+"Figures/gaussian_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".png")

  for ch in range(len(channels)):
    mpv.append(fit[ch].GetParameter(1))
    mpverr.append(fit[ch].GetParError(1))
    stddev.append(fit[ch].GetParameter(2))
    stddeverr.append(fit[ch].GetParError(2))
  print(mpv,mpverr)
names = ["run","LED voltage","lgmpv","lgmpverr","lgstddev","lgstddeverr","hgmpv","hgmpverr","hgstddev","hgstddeverr"]
#for gain studies!
#write to file which will be used to make plot
if not os.path.isfile(filename): 
  with open(filename, 'w') as creating_new_csv_file: 
    pass
  creating_new_csv_file.close()
df = pandas.read_csv(filename, names=names,index_col=False)
#read a csv whose format is:
#run, channel, voltage, mpv, mpverr
dfsz = range(df.shape[0])

df1 = pandas.DataFrame(data=[[int(runs[0]),float(drivingvoltage[int(sys.argv[3])]),mpv[0],mpverr[0],stddev[0],stddeverr[0],mpv[1],mpverr[1],stddev[1],stddeverr[1]]],columns=names)
df = pandas.concat([df,df1])

#write to file
df.to_csv(path_or_buf=filename,header=False,index=False)
print("saved file "+filename+"\n")

